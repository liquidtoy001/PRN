#!/usr/bin/env python3
"""Build an offline teaching chapter from a restricted HTML fragment; no network or overwrite."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import shutil
from string import Template
import sys
from urllib.parse import quote, unquote, urlsplit
from xml.etree import ElementTree

from validate_citations import find_citations, load_inventory, locator_is_placeholder

SKILL = Path(__file__).resolve().parents[1]
VOID = {"img", "br", "hr"}
TAGS = set("section article aside div p h2 h3 h4 ul ol li strong em b i small span a figure figcaption img br hr pre code blockquote table caption thead tbody tr th td details summary sub sup dl dt dd math mrow mi mn mo mfrac msup msub msubsup msqrt mroot mtable mtr mtd mtext munder mover munderover mspace semantics annotation".split())
ATTRS = set("id class title lang href src alt width height colspan rowspan scope display xmlns mathvariant stretchy fence separator accent accentunder encoding columnalign rowalign tabindex role aria-label data-k-ids".split())
IMAGE_SUFFIXES = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_configuration(value: object) -> dict:
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value.get("schema_version") != 1 or value.get("format") != "html":
        raise ValueError("expected HTML configuration schema 1 (not print study state)")
    if set(value) != {"schema_version", "format", "preferences"}:
        raise ValueError("unexpected top-level configuration fields")
    prefs = value.get("preferences")
    if not isinstance(prefs, dict) or set(prefs) != {"mode", "language", "assessment_date", "study_hours_available", "note_configuration"}:
        raise ValueError("incomplete or unknown preferences")
    config = prefs.get("note_configuration")
    choices = {
        "purpose": {"knowledge", "exam"}, "depth": {"standard-detailed", "extended"},
        "paper_enrichment": {"off", "reading-list", "integrated"},
        "reading_width": {"standard", "wide"}, "layout_density": {"comfortable", "compact"},
        "theme": {"light", "dark", "auto"}, "self_test": {"none", "folded-qa"},
    }
    expected = set(choices) | {"scope", "deliverables", "answers_initial", "confirmed"}
    if not isinstance(config, dict) or set(config) != expected:
        raise ValueError("incomplete or unknown HTML note_configuration; print options are not accepted")
    for key, allowed in choices.items():
        if not isinstance(config[key], str) or config[key] not in allowed:
            raise ValueError(f"invalid {key}")
    if prefs["mode"] not in ("lightweight", "full", "exam-cram") or prefs["language"] not in ("zh", "en", "bilingual"):
        raise ValueError("invalid mode or language")
    if config["confirmed"] is not True or config["deliverables"] != ["html"]:
        raise ValueError("configuration must be confirmed and HTML-only")
    if not isinstance(config["scope"], str) or not config["scope"].strip():
        raise ValueError("scope must be a nonempty string")
    initial = config["answers_initial"]
    if (config["self_test"] == "none" and initial is not None) or (config["self_test"] == "folded-qa" and initial not in ("open", "closed")):
        raise ValueError("answers_initial must match self_test")
    deadline, hours = prefs["assessment_date"], prefs["study_hours_available"]
    if deadline is not None:
        if not isinstance(deadline, str):
            raise ValueError("assessment_date must be an ISO date or null")
        date.fromisoformat(deadline)
    if hours is not None and (type(hours) not in (int, float) or not math.isfinite(hours) or hours <= 0):
        raise ValueError("study_hours_available must be positive finite hours or null")
    if prefs["mode"] == "exam-cram" and (deadline is None or hours is None):
        raise ValueError("exam-cram requires a deadline and study hours")
    return config


class Fragment(HTMLParser):
    """Validate the deliberately small authoring subset and collect build dependencies."""
    def __init__(self, root: Path, config: dict):
        super().__init__(convert_charrefs=True)
        self.root, self.config = root.resolve(), config
        self.stack: list[dict] = []
        self.ids = {"main"}
        self.links: list[str] = []
        self.assets: dict[str, Path] = {}
        self.headings: list[tuple[str, str]] = []
        self.parts: list[str] = []
        self.questions = 0

    def local_asset(self, url: str) -> None:
        parsed = urlsplit(url)
        decoded = unquote(parsed.path)
        if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or "\\" in decoded:
            raise ValueError(f"asset must be a plain relative local path: {url}")
        parts = decoded.split("/")
        if len(parts) < 2 or parts[0] != "assets" or any(p in ("", ".", "..") for p in parts):
            raise ValueError(f"asset must stay inside assets/: {url}")
        target = (self.root / decoded).resolve()
        asset_root = (self.root / "assets").resolve()
        if not asset_root.is_relative_to(self.root) or not target.is_relative_to(asset_root):
            raise ValueError(f"asset escapes source directory: {url}")
        if not target.is_file() or target.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError(f"missing or unsupported local image: {url}")
        if target.suffix.lower() == ".svg":
            try:
                svg = ElementTree.fromstring(target.read_bytes())
            except ElementTree.ParseError as exc:
                raise ValueError(f"invalid SVG: {url}") from exc
            for element in svg.iter():
                if element.tag.split("}")[-1] in {"script", "foreignObject", "style"}:
                    raise ValueError(f"active/style SVG content is unsupported: {url}")
                for key, value in element.attrib.items():
                    local = key.split("}")[-1].lower()
                    if local.startswith("on") or local == "style" or "url(" in value.lower() or (local in {"href", "src"} and not value.startswith("#")):
                        raise ValueError(f"external or active SVG attribute: {url}")
        self.assets[decoded] = target

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        if tag not in TAGS:
            raise ValueError(f"unsupported or executable element: {tag}")
        attrs = dict(attributes)
        if len(attrs) != len(attributes) or any(k not in ATTRS or v is None for k, v in attributes):
            raise ValueError(f"duplicate, boolean or unsupported attribute on {tag}")
        if "src" in attrs and tag != "img" or "href" in attrs and tag != "a":
            raise ValueError("src/href must belong to img/a")
        identifier = attrs.get("id")
        if identifier:
            if identifier in self.ids or identifier == "qa-controls" or any(c.isspace() for c in identifier):
                raise ValueError(f"duplicate or invalid id: {identifier}")
            self.ids.add(identifier)
        if tag == "h2" and not identifier:
            raise ValueError("h2 requires a stable id for navigation")
        if tag == "img":
            if not attrs.get("alt", "").strip() or not attrs.get("src"):
                raise ValueError("image needs a nonempty alt and local src")
            self.local_asset(attrs["src"])
        if tag == "a":
            href = attrs.get("href", "")
            parsed = urlsplit(href)
            if href.startswith("#"):
                self.links.append(unquote(href[1:]))
            elif parsed.scheme == "https" and parsed.netloc:
                pass
            else:
                self.local_asset(href)
        if tag == "details":
            if self.config["self_test"] != "folded-qa" or "qa" not in attrs.get("class", "").split():
                raise ValueError("details.qa requires explicitly selected folded-qa")
            if not identifier or not attrs.get("data-k-ids", "").strip():
                raise ValueError("question needs id and linked data-k-ids")
            if any(frame["tag"] == "details" for frame in self.stack):
                raise ValueError("nested questions are not supported")
            self.questions += 1
        if tag == "summary":
            if not self.stack or self.stack[-1]["tag"] != "details" or self.stack[-1]["children"]:
                raise ValueError("summary must be the first child of details")
        if self.stack:
            self.stack[-1]["children"].append(tag)
        serial = "".join(f' {k}="{escape(v, quote=True)}"' for k, v in attrs.items())
        if tag == "details" and self.config["answers_initial"] == "open":
            serial += " open"
        self.parts.append(f"<{tag}{serial}>")
        if tag not in VOID:
            self.stack.append({"tag": tag, "id": identifier, "children": [], "text": [], "summary": ""})

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack or self.stack[-1]["tag"] != tag:
            raise ValueError(f"unbalanced closing tag: {tag}")
        frame = self.stack.pop()
        text = "".join(frame["text"]).strip()
        if tag == "h2":
            if not text:
                raise ValueError("empty navigation heading")
            self.headings.append((frame["id"], text))
        if tag == "summary":
            if not text:
                raise ValueError("empty question")
            self.stack[-1]["summary"] = text
        if tag == "details" and (frame["children"].count("summary") != 1 or not text.removeprefix(frame["summary"]).strip()):
            raise ValueError("question needs one summary and a nonempty answer")
        if tag == "details" and not find_citations(text.removeprefix(frame["summary"]), ".md"):
            raise ValueError("each answer requires a source citation")
        if tag == "figure" and "figcaption" not in frame["children"]:
            raise ValueError("figure needs an adjacent figcaption")
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        self.parts.append(escape(data, quote=False))
        for frame in self.stack:
            frame["text"].append(data)

    def finish(self) -> str:
        self.close()
        if self.stack:
            raise ValueError("unclosed fragment elements")
        if not self.headings:
            raise ValueError("chapter needs at least one h2 section")
        missing = set(self.links) - self.ids
        if missing:
            raise ValueError(f"broken internal anchors: {sorted(missing)}")
        if self.config["self_test"] == "folded-qa" and not self.questions:
            raise ValueError("folded-qa selected but no questions were authored")
        return "".join(self.parts)


def build(args: argparse.Namespace) -> Path:
    content_bytes = args.content.read_bytes()
    configuration_bytes = args.configuration.read_bytes()
    settings = json.loads(configuration_bytes)
    config = validate_configuration(settings)
    inventory, errors = load_inventory(args.inventory)
    fragment = Fragment(args.content.parent, config)
    fragment.feed(content_bytes.decode("utf-8"))
    body = fragment.finish()
    citations = find_citations(body, ".html")
    if not citations:
        errors.append("chapter has no source citations")
    for ref in citations:
        if ref["id"] not in inventory:
            errors.append(f"unknown source id: {ref['id']}")
        if locator_is_placeholder(ref["locator"]):
            errors.append(f"unresolved locator: {ref['id']}")
    if errors:
        raise ValueError("; ".join(errors))
    zh = settings["preferences"]["language"] != "en"
    labels = ("跳到正文", "本章导航", "全部展开", "全部折叠", "离线学习笔记 · 资料边界见正文") if zh else ("Skip to content", "In this chapter", "Expand all", "Collapse all", "Offline study notes · See the source boundary above")
    controls = ""
    enhancement = ""
    if fragment.questions:
        controls = f'<div class="toolbar" id="qa-controls" hidden><button type="button" data-open="true">{labels[2]}</button><button type="button" data-open="false">{labels[3]}</button></div>'
        enhancement = '<script>const bar=document.getElementById("qa-controls");bar.hidden=false;bar.addEventListener("click",(event)=>{const button=event.target.closest("button[data-open]");if(button){document.querySelectorAll("details.qa").forEach((item)=>{item.open=button.dataset.open==="true";});}});</script>'
    template_bytes = (SKILL / "assets/template.html").read_bytes()
    rendered = Template(template_bytes.decode("utf-8")).substitute(
        language="zh-CN" if zh else "en", theme=config["theme"], density=config["layout_density"],
        width=config["reading_width"], title=escape(args.title), skip_label=labels[0], toc_label=labels[1],
        toc="".join(f'<li><a href="#{quote(key, safe="")}">{escape(label)}</a></li>' for key, label in fragment.headings),
        subtitle=escape(config["scope"]), controls=controls, body=body, footer=labels[4], enhancement=enhancement,
    ).encode("utf-8")
    output = args.output_dir.resolve()
    # No artifact writes happen before configuration, markup, citations and dependencies pass.
    output.mkdir(parents=True, exist_ok=False)
    for relative, source in fragment.assets.items():
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    (output / "index.html").write_bytes(rendered)
    (output / "configuration.json").write_bytes(configuration_bytes)
    report = {
        "schema_version": 1, "format": "html", "skill_version": (SKILL / "VERSION").read_text().strip(),
        "static_checks": "pass", "browser_review": "pending", "semantic_review": "pending",
        "question_count": fragment.questions, "citation_count": len(citations),
        "inputs": {"content": digest(content_bytes), "configuration": digest(configuration_bytes),
                   "inventory": digest(args.inventory.read_bytes()), "template": digest(template_bytes)},
        "artifacts": {"index.html": digest(rendered), **{name: digest(path.read_bytes()) for name, path in fragment.assets.items()}},
        "scope_note": "Restricted markup, local dependencies and citation syntax only; not semantic or browser QA.",
    }
    (output / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output / "index.html"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("content", "configuration", "inventory", "output-dir"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    try:
        output = build(args)
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"HTML build failed: {exc}", file=sys.stderr)
        return 2
    print(f"HTML built: {output}; static checks passed, browser/semantic review pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
