# Pre-Review Notes · 考试证据驱动的复习笔记

**中文** | [English](./README.en.md)

`pre-review-notes` 是一个 Agent Skill：它把学习者自己的讲义、习题、作业、往年题和
官方答案整理成可溯源、可增量维护的复习章节。它的重点不是“总结得像一本教材”，而是
只根据真实课程证据决定优先级、例题和答题深度。

当前源代码版本为 **v0.2.0**。本版本完成第二阶段学习闭环与资源测量，可从
[GitHub Releases](https://github.com/liquidtoy001/PRN/releases/tag/v0.2.0) 获取安装包。

## 它解决什么问题

- 先确认 `lightweight`、`full` 或 `exam-cram` 模式，以及中文、English 或中英双语。
- 没有考核证据时明确产出“讲义驱动笔记”，不冒充“考试重点预测”。
- 中文笔记首次出现专业术语时保留英文标准名和缩写。
- 用稳定 source ID、页码/题号和材料哈希维护证据链。
- 输出 Markdown，或可编辑 LaTeX + 经过结构和视觉检查的 PDF。
- 用 `study_state.json` 保存机器状态，并生成面向学习者的 `progress.md`。
- 生成可验证的 flashcards/quiz，记录错题、信心、掌握度并安排阶段性重测。
- 开始生成前检查材料容量和质量上限；每次生成后记录 token 用量及可选费用估算。

## 仓库结构

```text
pre-review-notes/
├── pre-review-notes/                  可安装的 skill
│   ├── SKILL.md                       精简入口与路由
│   ├── VERSION
│   ├── assets/                        输出、学习题库、状态和定价配置模板
│   ├── references/                    写作、证据、学习闭环、容量与测量规则
│   └── scripts/                       材料、容量、token、学习、状态和 PDF 工具
├── examples/stat3007/notes/           本项目生成的示例输出，不含原始 slides
├── tests/
│   ├── fixtures/stat3007/materials.csv  本地测试资料 manifest
│   └── unit/                          标准库单元测试
├── test-data/                         本地第三方测试资料，Git 忽略
├── tools/package_skill.py             可复现的 Release ZIP 构建器
├── dist/                              本地打包输出，Git 忽略
├── USAGE.md
├── TESTING.md
└── LICENSE
```

## 快速开始

将自己的课程资料放在一个本地目录，然后生成可引用的材料清单：

```powershell
python pre-review-notes/scripts/inventory_materials.py `
  E:\path\to\course-materials `
  --output output/materials.json
```

在生成正文前检查材料是否能安全装入当前模型上下文，并输出具体质量上限：

```powershell
python pre-review-notes/scripts/assess_capacity.py `
  output/materials.json `
  --context-window 128000 `
  --output output/capacity-report.json `
  --markdown output/capacity-report.md `
  --language zh
```

`128000` 只是命令示例，必须替换为当前平台/模型已确认的限制；未知时应省略该参数并采用
分章检索，不能猜一个容量后声称全量覆盖。

初始化跨会话状态：

```powershell
python pre-review-notes/scripts/manage_state.py init `
  --output output/study_state.json `
  --course-id STAT3007 `
  --course-title "Deep Learning" `
  --mode lightweight `
  --language zh `
  --format latex-pdf `
  --learning-output flashcards `
  --learning-output quiz
```

然后在支持 Agent Skills 的工具里调用 `pre-review-notes`，并提供课程资料目录。完整安装和
平台差异见 [USAGE.md](./USAGE.md)。

## 本地测试资料与 manifest

第三方课程 PDF 不属于本项目的示例资产，也不会进入新的 Git 提交、skill ZIP 或 Release。
仓库只保存测试清单 [materials.csv](./tests/fixtures/stat3007/materials.csv)。需要复现本地测试时：

```powershell
python pre-review-notes/scripts/download_materials.py `
  tests/fixtures/stat3007/materials.csv `
  --output-dir test-data/stat3007/slides
```

下载器会检查文件大小和 SHA-256，但不会替用户判断下载许可。请遵守原始课程页面的使用
条件。

> 迁移说明：新仓库从干净的 v0.0.1、v0.0.2、v0.1.0 提交链继续发布 v0.2.0。v0.0.2 保留
> 功能快照和 Release 安装包，但没有迁移第三方 slides 或包含它们的旧 Git 对象。

## 第一阶段改造内容

- 将 322 行的单体说明拆成精简 `SKILL.md` 和按需读取的 `references/`。
- 新增三种工作模式及其明确边界。
- 新增材料 inventory、扫描件/OCR 风险检测和稳定 source ID。
- 新增 CSV/JSON manifest 下载器，第三方文件只进入本地忽略目录。
- 新增机器可检查的 LaTeX/Markdown 引用格式和引用验证器。
- 新增 `study_state.json`、章节状态、输入 digest 和增量重建判断。
- 新增 LaTeX 编译、PDF 结构遍历、代表页渲染和 QA 报告工具。
- 新增可复现的扁平 ZIP 打包器；生成包放在 `dist/`，由 GitHub Release 承载。

## 第二阶段功能

- `manage_learning.py` 校验带来源的 flashcards/quiz 题库，记录正确率、1–5 信心、错题标签、
  掌握度与重测日期。
- 根据考试日期、显式 assessment evidence、掌握度、到期状态和答题时间生成阶段性重测计划；
  没有考试证据的项目不会伪装成“高频预测”。
- 支持 UTF-8 CSV 和 Anki 三列 TSV 导出。
- inventory 为可提取材料给出保守 token 区间；`assess_capacity.py` 报告上下文适配、OCR/
  加密/未读取风险，以及内容覆盖、考试校准和答题深度三类质量上限。
- `usage_ledger.py` 为每次生成记录 provider-reported、manually-reported、partial-estimate 或
  unavailable 四种精度；只有提供明确、带日期的定价配置时才计算可选费用。
- `study_state.json` 升级为 schema 2；新章节未通过容量披露和 token 记账门禁时不能标记为
  verified/delivered，旧状态可无损迁移并标为历史生成。

## 证据边界

示例 STAT3007 Regression 笔记只以 lecture slides 为证据，因此没有声称评分权重、题型、
往年高频或官方答案深度。它展示的是 source-grounded note generation，而不是真实考试预测。

## 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.2.0 | 2026-08-25 | 第二阶段：flashcards/quiz、错题/信心/掌握度、动态重测、Anki/CSV、材料容量与质量上限、逐次 token/费用账本。 |
| v0.1.0 | 2026-08-24 | 第一阶段工程化：渐进式 skill、三种模式、local-only manifest、材料/引用/状态/PDF 工具、增量构建和可复现打包。 |
| v0.0.2 | 2026-08-13 | 增加语言确认、中文术语英文保留、LaTeX 到 PDF 和 STAT3007 测试；迁移标签保留功能快照并排除第三方 slides。 |
| v0.0.1 | 2026-07 | 初始方法论、模板和人工评测方案。 |

本项目代码和原创模板采用 [MIT License](./LICENSE)。课程材料不包含在该授权范围内。
