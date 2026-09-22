# Pre-Review Notes · 来源可溯的学习与复习笔记

**中文** | [English](./README.en.md)

`pre-review-notes` 是一个 Agent Skill：它把学习者自己的讲义、习题、作业、往年题和
官方答案整理成可溯源、可增量维护的学习章节。知识巩固版重视知识覆盖与适度拓展；
考试复习版根据真实课程证据组织优先级、例题和答题深度。

当前版本为 **v0.2.10**，同一仓库提供两个可独立安装的入口：

| Skill | 定位 | 专属能力 |
|---|---|---|
| `pre-review-notes` | 可打印笔记 | PDF / LaTeX / Markdown、纸张与分页、逐图最终页面检查 |
| `pre-review-notes-html` | 屏幕阅读 | 离线 HTML、章节导航、可选折叠问答、阅读宽度/密度/主题 |

两者共享知识覆盖、来源证据、论文拓展及图片提取规则，但分别使用配置、模板、状态和布局验收。
HTML 版不默认把讲解变成题目；知识巩固版默认无新题，显式启用自测后才增加折叠问答。
浏览器打印不是经过验证的 PDF 产品，也不会在 PDF 中模拟折叠。

安装包及各自 SHA-256 校验文件见 [v0.2.10 Release](https://github.com/liquidtoy001/PRN/releases/tag/v0.2.10)。
原版安装目录名不变；HTML 版可单独安装，也可与原版并存。
本轮已验证 CLI、配置隔离与独立 ZIP 构建；浏览器本地页面访问被运行环境策略阻止，
因此宽窄屏、真实键盘交互和公式视觉验收仍待完成，不宣称 HTML 教学效果已验证。

## 它解决什么问题

- 首次集中确认笔记用途、模式、材料范围、讲解深度、语言、交付格式、页面规格、排版密度、论文拓展、练习配套及时间约束，保存后续用。
- 知识巩固版默认不生成新题，保留课程原有例题讲解；考试复习版依据考核证据组织复习。练习配套以用户选择为准。
- 逐页登记知识点，保留小条件与图示信息；lightweight 缩小批次，不默认压缩讲解深度。
- 支持原始图表复用及可选论文推荐/整合；核验来源与图表保真度。

- 先确认 `lightweight`、`full` 或 `exam-cram` 模式，以及中文、English 或中英双语。
- 没有考核证据时明确产出“讲义驱动笔记”，不冒充“考试重点预测”。
- 中文笔记首次出现专业术语时保留英文标准名和缩写。
- 用稳定 source ID、页码/题号和材料哈希维护证据链。
- 输出 Markdown，或可编辑 LaTeX + 经过结构和视觉检查的 PDF。
- 用 `study_state.json` 保存机器状态，并生成面向学习者的 `progress.md`。
- 选择练习配套后生成可验证的 flashcards/quiz，记录错题、信心、掌握度并安排阶段性重测。
- 开始生成前检查材料容量和质量上限；每次生成后记录 token 用量及可选费用估算。

## 适用领域与验证范围

流程按课程材料组织，设计上不限定 AI；但目前实际生成经验集中在 AI/机器学习课程，
仓库课程 fixture 为 STAT3007，不能据此宣称跨学科效果已验证。脚本测试验证的是工具行为，
不是笔记事实正确性、教学效果或长期记忆效果。这里的课程样本属于评测/迭代材料，
修改 Skill 并没有训练或微调底层模型。

| 领域 | 适配判断（尚非跨领域实测结论） | 重点验证 |
|---|---|---|
| AI、机器学习、数据科学 | 已有有限课程生成经验，仍发现过内容与排版缺陷 | 覆盖、推导、公式、图表、引用 |
| 数学、统计、算法及其他计算机课程 | 与现有公式/步骤型流程较接近 | 证明条件、符号、代码与复杂度、执行证据 |
| 物理及工程课程 | 可复用公式与图示流程，需试点 | 单位、近似条件、工程图与推导 |
| 生物及其他图示密集课程 | 可尝试，图像细节风险较高 | 结构标注、过程顺序、图表完整性 |
| 人文、社会科学及论述型课程 | 有 Markdown 模板，尚需验证论证表达 | 观点归属、争议、文本语境及论述评分标准 |

医学、法律等领域的课程整理仍需相应领域审阅，不能把生成笔记视为专业决策依据。
建议先对不同材料类型做小规模人工对照评测，再扩大适用声明：公式推导、代码/算法、
多层图示、长篇论证各选一章，逐项检查遗漏、错误、拓展来源和阅读体验。

## 仓库结构

```text
pre-review-notes/
├── pre-review-notes/                  可安装的 skill
│   ├── SKILL.md                       精简入口与路由
│   ├── VERSION
│   ├── assets/                        输出、学习题库、状态和定价配置模板
│   ├── references/                    写作、证据、学习闭环、容量与测量规则
│   └── scripts/                       材料、容量、token、学习、状态和 PDF 工具
├── pre-review-notes-html/             独立 HTML skill，不依赖原版目录
├── shared/                            格式无关资源的唯一开发源
├── tools/sync_shared.py               同步共享副本，--check 检查漂移
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

HTML 请求示例：

> 用 pre-review-notes-html 处理我的课程 slides，中文、知识巩固版、lightweight，先做第 1 章。
> 需要完整讲解和可选折叠自测，其他配置先一次给我确认；输出离线 HTML 文件夹。

维护共享规则时只编辑 `shared/`，然后执行 `python tools/sync_shared.py`。安装目录中的
对应文件是随包携带的副本，打包会拒绝漂移。分别构建：

```powershell
python tools/sync_shared.py --check
python tools/package_skill.py
python tools/package_skill.py --skill-dir pre-review-notes-html
```

下面的命令示例属于原版打印工作流；不要把它的状态配置用于 HTML 版。

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
| v0.2.10 | 2026-09-22 | 独立 HTML 入口、可选折叠问答与离线构建；共享资源防漂移、双包发布，保留原版打印定位。 |
| v0.2.9 | 2026-09-19 | 图片提取完整性与最终布局双重检查，裁剪和逐图渲染记录。 |
| v0.2.8 | 2026-09-16 | 论文拓展配置、文献核验和论文内容/图表整合规则。 |
| v0.2.7 | 2026-09-15 | 知识巩固版/考试复习版、完整配置询问和保存；包含 0.2.5 知识覆盖、0.2.6 图表复用改进。 |
| v0.2.0 | 2026-08-25 | 第二阶段：flashcards/quiz、错题/信心/掌握度、动态重测、Anki/CSV、材料容量与质量上限、逐次 token/费用账本。 |
| v0.1.0 | 2026-08-24 | 第一阶段工程化：渐进式 skill、三种模式、local-only manifest、材料/引用/状态/PDF 工具、增量构建和可复现打包。 |
| v0.0.2 | 2026-08-13 | 增加语言确认、中文术语英文保留、LaTeX 到 PDF 和 STAT3007 测试；迁移标签保留功能快照并排除第三方 slides。 |
| v0.0.1 | 2026-07 | 初始方法论、模板和人工评测方案。 |

本项目代码和原创模板采用 [MIT License](./LICENSE)。课程材料不包含在该授权范围内。
