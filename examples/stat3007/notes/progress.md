# STAT3007/STAT7007 复习笔记进度

- 模式：`lightweight`
- 主语言：`zh`
- 格式：`latex-pdf`
- 考试日期：未提供
- 机器状态：`study_state.json`
- 测试 manifest：`tests/fixtures/stat3007/materials.csv`

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

## 下一步

在获得当前课程 assessment specification、往年题和官方答案之前，不继续生成“考试重点”
排序。可以继续以 lightweight 模式制作其他讲义驱动章节。
