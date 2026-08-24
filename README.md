# Pre-Review Notes · 考试校准型课程复习笔记

**中文** | [English](./README.en.md)

一个跨平台的 **Agent Skill（智能体技能包）**：把你自己的零散课程材料（讲义、习题、作业、往年卷、官方答案）转化成一套按**考试权重**排序、每个论断都**可溯源**的复习笔记。适用于任意学科（数理/CS/法学/医学/文科等）。

> 核心原则：笔记按考试校准，而不是按教材校准。重考的主题给完整章节和真题推导；只顺带提过的主题合并或跳过。所有"这个常考"的判断必须能追溯到课程材料里的真实依据。

👉 **各平台安装与使用方法见 [USAGE.md](./USAGE.md)**

## 仓库结构

```
pre-review-notes/                      技能源目录（可直接作为 skill 使用）
├── SKILL.md                           技能主文件：方法论 + 反模式清单
├── template.tex                       章节笔记 LaTeX 模板（数理/CS）
├── markdown-template.md               章节笔记 Markdown 模板（文科）
├── course-overview-template.svg       一页式课程全景图模板
├── calendar-template.ics              复习日历模板（可导入任意日历 App）
└── progress-template.md               跨会话进度追踪模板
pre-review-notes-v0.0.1.zip            发布包（SKILL.md 在包根部，可直接上传 claude.ai / Qoder 等平台）
USAGE.md                               各平台安装与使用方法
TESTING.md                             人工测试实验方案（验证技能有效性）
README.en.md                           英文版 README
LICENSE                                MIT 许可
```

## 包内文件

| 文件 | 用途 | 对应工作流步骤 |
|---|---|---|
| `SKILL.md` | 技能主文件：9 步方法论 + 反模式清单 | 全流程 |
| `template.tex` | 章节笔记 LaTeX 模板（数理/CS 类课程） | Step 5 |
| `markdown-template.md` | 章节笔记 Markdown 模板（法律/历史/语言等文科） | Step 5 |
| `course-overview-template.svg` | 一页式课程全景图模板（彩色主题分区 + 考核结构区） | Step 3 |
| `calendar-template.ics` | 复习日历模板：按权重分配学习时段，可导入任意日历 App | Step 3 |
| `progress-template.md` | 跨会话进度追踪模板，新会话零成本接续 | Step 9 |

## 工作流一览（9 步）

1. **Step 0** 确认输出偏好（LaTeX / Markdown、是否双语注释、一章一文件）
2. **Step 1** 摸清考核结构：评分权重、考试形式、老师明示的重点
3. **Step 2** 盘点手头全部材料
4. **Step 3** 按考核权重 + 先修依赖排章节顺序，可渲染 SVG 全景图与你确认计划，并可导出 .ics 复习日历（倒推考试日期、按权重分配时段）
5. **Step 4** 每章定向检索课程自己的例题、习题、真题
6. **Step 5** 按统一模板起草：概念区 → 真题完整推导 → 陷阱框 → 速查卡 → 考核映射表
7. **Step 6** 对照官方答案校准答题深度（不多写、不少写）
8. **Step 7** 独立复算所有推导，不盲信任何来源
9. **Step 8–9** 一次交付一章，按优先级迭代；进度写入 `progress.md`，换会话/换平台可无缝接续

## 按学科选模型（参考）

| 学科 | 建议 | 理由 |
|---|---|---|
| 数理 / CS | DeepSeek-R1、GLM + Claude Code | Step 7 推导复算最可靠，可本地编译 LaTeX |
| 法学 / 历史 / 语言 | Kimi | 长上下文，适合大量 prose 材料盘点 |
| 医学 | Qwen 系、腾讯元宝 | 中英混杂指南处理好，双语注释可用 |

## 常见问题

- **没有真实课程材料怎么办？** 本技能会明确拒绝编造"某年考过"之类的引用，只会提供通用笔记并声明缺少校准来源。
- **中文支持？** 模板原生支持：SVG 内置中文字体栈，`template.tex` 预留 CJK 宏，Markdown 模板自带双语注释块。
- **一次能生成整本笔记吗？** 不建议（见反模式"one-shot mega-files"）：默认一轮一章，先确认优先级计划再动笔。
- **会出题考我吗？** 不会。本技能不做测验/刷题功能；真题以原文形式直接写进笔记的"完整推导"区，配满分答案风格的逐步解答。

## 有效性验证

本技能配有一套可复现的人工测试实验方案（A/B 对照 + 盲评，5 条可证伪假设、5 个测试案例、6 维度量表，硬性指标"编造率 = 0"一票否决）。

👉 **完整方案见 [TESTING.md](./TESTING.md)**

## 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.0.1 | 2026-07 | 首个公开版本：SKILL.md 9 步方法论 + 5 个模板（LaTeX / Markdown / SVG 全景图 / .ics 日历 / 进度追踪），中英双版 README，独立 USAGE / TESTING 文档，GitHub Release 附可安装技能 zip |

## 许可

[MIT](./LICENSE)
