# STAT3007/STAT7007 复习笔记进度

- 模式：`lightweight`
- 主语言：`zh`
- 格式：`latex-pdf`
- 考试日期：未提供
- 机器状态：`study_state.json`
- 状态 schema：`2`（本章为 v0.1.0 历史生成，`legacy_generation=true`）
- 测试 manifest：`tests/fixtures/stat3007/materials.csv`
- 容量检查：`not-checked`（清理后的公开仓库不包含原始 slides）
- Token 账本：无；不追溯编造历史生成用量
- 主动学习产物：未生成

## 证据边界

当前测试输入只有 33 个唯一 lecture slide PDF。没有评分结构、考试形式、往年卷、评分标准
或官方答案，因此本示例是讲义驱动笔记，不是考试权重排序。

## 章节

| 章节 | 状态 | 优先级依据 | 产物 |
|---|---|---|---|
| Regression | `delivered` | 代表性 smoke-test 章节；考试权重未知 | `chapter-01-regression-zh.tex`, `pdf/stat3007-regression-notes-zh.pdf` |

## 验证

- 10 个 source references 均解析为 manifest 中的 `S002`。
- OLS、Ridge Regression 和 1-NN 推导已独立复算。
- XeLaTeX 连续编译两次，PDF 可重新打开并遍历全部 3 页。
- 3 个代表页已渲染并目视检查；未发现裁切、重叠、缺字或空白页。
- 本章早于 v0.2.0 的容量/token 门禁，因此对应 QA 为 `not-applicable`，不代表已测得精确用量。

## 下一步

在获得当前课程 assessment specification、往年题和官方答案之前，不继续生成“考试重点”
排序。继续生成前先对本地材料运行容量检查；生成后立即写入 token ledger。可以继续以
lightweight 模式制作其他讲义驱动章节。
