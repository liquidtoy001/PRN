# 使用方法 · USAGE

完整功能需要一个能够读取 skill 目录、访问课程材料、运行本地脚本并写出文件的 Agent。
只有对话框或知识库的平台仍可使用核心方法，但无法自动获得材料哈希、增量状态和 PDF QA。
精确 token 也只有在平台返回 usage 时可得；否则 v0.2.0 会记录明确标注的部分估算或
`unavailable`，不会把字符数估算冒充账单。

## 1. 安装完整 skill

### 从源码目录安装

把整个 `pre-review-notes/` 目录复制到目标 Agent 的 skills 目录。不要只复制
`SKILL.md`，因为 v0.2.0 会按需读取 `references/`、复用 `assets/` 并运行 `scripts/`。

如果目标环境支持 `skills` CLI，可以从仓库安装：

```bash
npx skills add https://github.com/liquidtoy001/PRN
```

### 从 Release ZIP 安装

运行下面的命令会在本地 `dist/` 生成扁平 ZIP；`SKILL.md` 位于 ZIP 根目录：

```powershell
python tools/package_skill.py
```

将 `dist/pre-review-notes-v0.2.8.zip` 上传到支持 skill ZIP 导入的平台。`dist/` 被 Git
忽略，正式包应作为 GitHub Release asset 发布，而不是提交进仓库。

## 2. 准备课程资料

课程材料默认属于本地输入，不属于 skill、Git 仓库或 Release。推荐结构：

```text
my-course-project/
├── materials/             自己的 slides、作业、往年题、答案
├── output/                inventory、state、笔记和 PDF
└── .gitignore             忽略 materials/ 中不可公开的文件
```

生成材料清单：

```powershell
python path/to/pre-review-notes/scripts/inventory_materials.py `
  materials `
  --output output/materials.json
```

脚本会生成稳定 source ID、相对路径、角色提示、大小和 SHA-256。安装了 `pypdf` 时，
还会抽样检查 PDF 文本、标记可能需要 OCR 的扫描件，并生成保守 token 区间。角色分类、
OCR 标记和 token 区间都是路由/容量提示，不是课程事实或模型精确计数。

生成正文前必须运行容量检查：

```powershell
python path/to/pre-review-notes/scripts/assess_capacity.py `
  output/materials.json `
  --context-window 128000 `
  --reserved-output-tokens 16000 `
  --output output/capacity-report.json `
  --markdown output/capacity-report.md `
  --language zh
```

上下文上限未知时省略 `--context-window`。报告会标记 `unknown`，工作流应改为逐章选取
source IDs，并在成品中列出尚未处理的材料。`fits-estimate` 也不等于模型一定完整理解材料。

如果资料由 URL manifest 管理：

```powershell
python path/to/pre-review-notes/scripts/download_materials.py `
  materials.csv `
  --output-dir local-materials
```

## 3. 发起任务

一个足够完整的请求示例：

```text
使用 pre-review-notes 处理 STAT3007。
模式使用 lightweight，主语言中文，专业术语首次出现保留英文。
先完成 Regression 一章，交付可编辑 LaTeX 和经过检查的 PDF。
同时生成带来源的 flashcards 和 quiz，并安排阶段性重测。
材料目录是 ./materials，输出放在 ./output。
```

如果没有提供模式、语言、格式或影响排序的考试时间，skill 会只确认缺失项，不会重复询问
已经明确的偏好。

### 三种模式

| 模式 | 适合场景 | 主要结果 |
|---|---|---|
| `lightweight` | 第一次试用、只做一章、只有 slides | 容量/证据边界、临时 topic map、代表章节；卡片/quiz 按需 |
| `full` | 多种资料齐全、准备长期维护 | 完整 assessment map、状态、逐章交付、题库、掌握度和增量更新 |
| `exam-cram` | 考试临近且时间预算明确 | 证据驱动取舍、计时 quiz、动态重测和明确未覆盖风险 |

## 4. 输出语言与专业术语

主语言可以是中文、English 或中英双语。中文笔记首次出现专业或易混淆术语时使用：

```text
普通最小二乘法（Ordinary Least Squares, OLS）
岭回归（Ridge Regression）
1-最近邻（1-Nearest Neighbour, 1-NN）
```

代码标识符、公式、论文标题和原文引用保留规范形式。双语正文与中文正文加少量英文术语不是
同一种输出，skill 会保持已确认的主语言一致。

## 5. 引用、状态和增量更新

LaTeX 使用：

```tex
\sourceref{S002}{PDF p. 18}
\assessref{S014}{2023 final Q2(b)}
```

Markdown 使用：

```text
[source:S002|PDF p. 18]
[assessment:S014|2023 final Q2(b)]
```

验证引用：

```powershell
python path/to/pre-review-notes/scripts/validate_citations.py `
  output/chapter.tex `
  --inventory output/materials.json
```

多章节任务使用 `study_state.json` 记录真实状态，`progress.md` 只是可读摘要。输入 digest
没有变化且章节已经 verified/delivered 时，可以跳过重建。

旧的 schema 1 状态可迁移；历史章节会标为 `legacy_generation`，不会伪造旧 token 数据：

```powershell
python path/to/pre-review-notes/scripts/manage_state.py migrate output/study_state.json
```

## 6. Flashcards、Quiz、掌握度与重测

模型按 `assets/learning-bank-template.json` 生成题库后，先校验来源：

```powershell
python path/to/pre-review-notes/scripts/manage_learning.py validate-bank `
  output/learning-bank.json `
  --inventory output/materials.json
python path/to/pre-review-notes/scripts/manage_learning.py init `
  --bank output/learning-bank.json `
  --output output/learning_state.json `
  --assessment-date 2026-11-10
```

每次作答记录正确/错误、1–5 信心和错题类型；再按考试日期和可用时间生成重测计划：

```powershell
python path/to/pre-review-notes/scripts/manage_learning.py record-attempt `
  --bank output/learning-bank.json `
  --state output/learning_state.json `
  --item-id regression-Q001 --correct no --confidence 5 `
  --mistake-tag objective-confusion
python path/to/pre-review-notes/scripts/manage_learning.py plan `
  --bank output/learning-bank.json `
  --state output/learning_state.json `
  --available-minutes 45 `
  --output output/retest-plan.json
```

用 `manage_learning.py export --format csv` 生成普通表格，或 `--format anki` 生成 UTF-8
三列 TSV（front、back、tags）。掌握度是近几次作答的调度信号，不是考试通过保证。

## 7. 每次生成后的 Token 与可选费用记录

OpenAI Responses API 的 `usage` 可包含 input、output、total 以及缓存/推理 token 明细，
但其他平台或普通聊天界面未必暴露这些字段。能取得 response JSON 时：

```powershell
python path/to/pre-review-notes/scripts/usage_ledger.py record `
  --ledger output/usage-ledger.jsonl `
  --operation chapter-generation `
  --provider openai --model exact-model-id `
  --usage-file output/response.json `
  --artifact output/chapter.tex
```

只有文件可见时，使用 `--input-file` 和 `--output-file` 得到 `partial-estimate`；两者都拿不到
时使用 `--unavailable-reason` 留下审计记录。费用计算必须显式传入基于
`assets/pricing-template.json` 的定价文件。API 价格、订阅套餐、积分、工具调用和长上下文加价
不能互相替代；结果不是发票。官方 usage 字段见
[OpenAI Responses API](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)。

## 8. LaTeX 和 PDF

```powershell
python path/to/pre-review-notes/scripts/build_note.py `
  output/chapter.tex `
  --output-dir output/pdf
```

脚本会编译、重新打开 PDF、遍历页面并用 Poppler 渲染代表页。它会把视觉状态保留为
`pending`；Agent 或用户必须真正查看最新 PNG，确认没有裁切、重叠、乱码或空白页后，才能
把章节标记为 delivered。缺少编译器、`pypdf` 或 Poppler 时必须明确报告，不能把 `.tex`
冒充已完成的 PDF。

## 9. 仅支持文本指令的平台

无法加载目录的网页版可以粘贴 `SKILL.md`，再按任务附上相应 reference 和模板。例如做中文
LaTeX/PDF 时至少附上：

- `references/modes.md`；
- `references/evidence-workflow.md`；
- `references/authoring.md`；
- `references/pdf-workflow.md`；
- `references/measurement-and-capacity.md`；
- `references/active-learning.md`（若需要题库）；
- `assets/template.tex`。

这种方式没有自动脚本、稳定状态和渐进式资源加载，也通常拿不到完整 input token；是兼容性
降级方案，不等同于完整安装。
