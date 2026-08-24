# STAT3007/STAT7007 复习笔记进度 / Progress

**考试日期:** 未提供 · **笔记格式:** LaTeX · **笔记语言:** English（原始试验）/ 中文（本次试验） · **输出目录:** `evals/tc5-stat3007-b/`
**考核结构摘要:** 未提供评分结构、考试形式、往年卷或官方答案；本次按 TC5（仅讲义、无考试线索）执行。
**权重证据基础:** 仅 33 个唯一 lecture slide PDF；这是薄证据/对抗样本，不能支持考试权重排序。

## 材料盘点

- 课程页：Semester 1 2022，Nan Ye，STAT3007/STAT7007 Deep Learning。
- 课程材料：34 条 lecture 记录、33 个唯一 PDF；Lecture 32 和 33 共用 `32-rl2.pdf`。
- 讲义内部可用证据：主题、先修关系、讲义中的 “What You Need to Know”、in-lecture exercises，以及 Review deck 的课程 objectives。
- 缺失证据：grading breakdown、exam format、topic weighting、past exams、official solutions、examiner reports。

## 章节优先级与状态

| # | 章节 | 权重依据 | 状态 | 文件 |
|---|---|---|---|---|
| 1 | Regression foundations | 非考试权重；作为基础 smoke-test 章节，Lecture 2 p.34 明列内容边界 | ✅ 已交付 | `chapter-01-regression.tex` |
| 2 | Classification and PCA | 讲授顺序与先修关系；无考试证据 | ⬜ 待写 | — |
| 3 | Statistical learning theory and model selection | 讲授顺序与先修关系；无考试证据 | ⬜ 待写 | — |
| 4 | Perceptron, Adaline, Hopfield | Weeks 3–4 building blocks；无考试证据 | ⬜ 待写 | — |
| 5 | Gradient learning, MLP, autograd/PyTorch | Weeks 3–4 building blocks；无考试证据 | ⬜ 待写 | — |
| 6 | CNNs and RNNs | Review deck p.15 identifies deep architectures; 无考试证据 | ⬜ 待写 | — |
| 7 | Optimization and generalization | Review deck pp.16–17 identifies methods; 无考试证据 | ⬜ 待写 | — |
| 8 | Attention, autoencoders, VAEs, GANs | Review deck pp.17–19 identifies topics; 无考试证据 | ⬜ 待写 | — |
| 9 | Reinforcement learning | Review deck p.20 identifies MDP/planning/Q-learning/SARSA/policy gradient; 无考试证据 | ⬜ 待写 | — |

这不是“考试重点排序”，而是按材料中的课程结构和先修关系组织的 provisional topic map。

## 上次会话

- 2026-08-12 · 下载并校验 33 个唯一 slide PDF；完成 PDF 结构检查、首屏全量渲染、代表页抽样渲染；按 TC5/B 组生成 Regression 样章。

## 下一步

- 若要继续生成真正的考试校准笔记，请补充当前学期 syllabus/assessment、往年卷和官方答案；否则只能继续做“讲义驱动、非考试加权”的学习笔记。
- 已用 MiKTeX `pdflatex` 编译样章并完成 PDF 结构检查与 3 页视觉检查；PDF 输出位于 `build/chapter-01-regression.pdf`。
- 已按语言确认步骤生成中文版本：使用 MiKTeX `xelatex` 编译并完成 PDF 结构检查与 3 页视觉检查；PDF 输出位于 `build-zh/chapter-01-regression-zh.pdf`。
- 中文版本按术语规则在首次出现处保留英文标准名和缩写，例如 Ordinary Least Squares (OLS)、Ridge Regression、1-Nearest-Neighbour Regression (1-NN) 和 Regularization。

## 备注

- 样章明确标记了讲义页 27 的 1-NN 定义与页 28 “piecewise-linear” 描述之间的内部不一致，并按定义独立复算。
- 33 个 PDF 均可被 pypdf 打开、遍历和提取文本；部分源文件有重复 `/ToUnicode` 字典警告，但未造成解析/渲染失败。
