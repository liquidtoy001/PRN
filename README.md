# Pre-Review Notes · 考试校准型课程复习笔记

**中文** | [English](./README.en.md)

一个跨平台的 **Agent Skill（智能体技能包）**：把你自己的课程材料（讲义、习题、作业、往年卷、官方答案）整理成按真实考核证据排序、每个重要判断都可溯源的复习笔记。适用于数学、CS、自然科学、医学、法学、语言和商科等课程。

> 核心原则：笔记按考试校准，而不是按教材顺序校准。没有课程材料支持，就不编造“某年考过”或“这里很重要”的结论。

👉 安装与使用方法见 [USAGE.md](./USAGE.md)；人工评测方案见 [TESTING.md](./TESTING.md)。

## 仓库结构

```text
pre-review-notes/
├── pre-review-notes/                 可安装的 skill 源目录（只含运行所需文件）
│   ├── SKILL.md
│   ├── template.tex                  数理/CS 章节 LaTeX 模板
│   ├── markdown-template.md          文科章节 Markdown 模板
│   ├── course-overview-template.svg  一页式课程全景图模板
│   ├── calendar-template.ics         复习日历模板
│   └── progress-template.md          跨会话进度模板
├── examples/stat3007/                可复现的 STAT3007 示例与来源材料
│   ├── slides/                       仅含来源说明和 manifest.csv；原始 PDF 不再分发
│   └── notes/                        英文/中文 LaTeX、编译后的 PDF 和 progress.md
├── GitHub Release                    提供可直接上传的 v0.0.2 skill ZIP
├── README.md / README.en.md          双语项目说明
├── USAGE.md                          安装与使用
├── TESTING.md                        人工评测方案
└── LICENSE                           MIT 许可
```

`pre-review-notes/` 是安装边界；课程 PDF、示例笔记和 LaTeX 构建中间文件不混入安装包。历史安装包由 GitHub Release 保存，不提交到 Git 历史。

## v0.0.2 的主要更新

- 在 Step 0 明确确认笔记主语言：中文、English 或中英双语，并让 `.tex`、PDF、课程全景图和 `progress.md` 保持一致。
- 中文笔记对特殊/易混淆术语保留英文：首次出现使用“中文（English, acronym）”，例如普通最小二乘法（Ordinary Least Squares, OLS）、岭回归（Ridge Regression）、1 近邻回归（1-Nearest-Neighbour Regression, 1-NN）。
- 新增 Step 8：编译 LaTeX、检查 PDF 可读性，并用 Poppler 渲染代表页检查裁切、重叠、缺字和空白页；Windows MiKTeX 的 `latexmk` 不可用时回退到 `pdflatex`/`xelatex`。
- 新增 `examples/stat3007/`：manifest 记录 34 个 lecture 行对应的 33 个唯一 slide 来源（Lecture 32/33 共用 `32-rl2.pdf`），并提供中英文 Regression 示例笔记和可直接观看的生成 PDF。原始 slides 仅用于本地测试。

## 工作流一览（Step 0–10）

1. **Step 0**：确认输出格式、编译 PDF 需求、笔记主语言、注释语言和章节粒度。
2. **Step 1**：从真实材料摸清评分权重、考试形式和教师明示重点。
3. **Step 2**：盘点讲义、习题、作业、真题和官方答案。
4. **Step 3**：按考核权重与先修依赖确定章节顺序，可生成 SVG 全景图和 `.ics` 日历。
5. **Step 4**：为每章检索课程自己的例题、习题、作业和真题。
6. **Step 5**：按统一模板起草概念、完整推导、陷阱框、速查卡和考核映射。
7. **Step 6**：对照官方答案校准答题深度。
8. **Step 7**：独立复算所有数值、代数和逻辑推导。
9. **Step 8**：编译 LaTeX 并完成 PDF 结构、文本和视觉检查。
10. **Step 9**：交付一章，说明证据边界、语言和输出文件。
11. **Step 10**：按优先级迭代后续章节，并更新 `progress.md`。

## 示例：STAT3007

示例材料来自课程公开页面：[STAT3007/STAT7007 Deep Learning](https://yenan.github.io/teach/stat3007/index.html)。`examples/stat3007/slides/README.md` 和 manifest 记录下载来源、页数、字节数和 SHA-256，但仓库不包含原始 slide PDF。用户在本地取得材料时仍须遵守原始页面的许可和教学用途限制。

可以直接打开：

- [中文 Regression PDF](./examples/stat3007/notes/pdf/stat3007-regression-notes-zh.pdf)
- [English Regression PDF](./examples/stat3007/notes/pdf/stat3007-regression-notes-en.pdf)
- [中文 LaTeX 源文件](./examples/stat3007/notes/chapter-01-regression-zh.tex)
- [English LaTeX 源文件](./examples/stat3007/notes/chapter-01-regression.tex)

该示例只有 lecture slides 作为证据，因此没有虚构考试权重、题型或官方答案；`progress.md` 明确记录了这一边界。

## 许可证

本 skill 代码和模板采用 [MIT](./LICENSE) 许可。第三方课程材料不属于本项目授权范围，也不随仓库或 Release 分发。

## 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.0.2 | 2026-08-13 | 重组 skill 与 examples；增加笔记语言确认、中文术语英文保留规则、LaTeX→PDF 编译与视觉 QA；加入 STAT3007 可复现实例和 33 个 slide 的 manifest；发布新的 skill zip。 |
| v0.0.1 | 2026-07 | 首个公开版本：基础方法论、LaTeX/Markdown/SVG/ICS/进度模板和人工评测方案。 |
