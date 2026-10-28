# Pre-Review Notes

**中文** | [English](./README.en.md)

把课程 slides、讲义和习题整理成带来源说明的学习笔记。适合想补全知识、理解推导，
或者根据课程资料复习的学生。中文笔记会保留重要术语的英文名称。

这是给 AI Agent 使用的 Skill（任务说明和配套工具），需要配合支持 Skill、能读取文件的
Agent 使用。它本身不是双击就能运行的软件。

## 第一次用，从这里开始

1. **选一个版本。** 想打印、手写批注，选 PDF 版；想在屏幕上阅读、展开自测答案，选 HTML 版。
2. **下载并安装。** 打开 [最新 Release](https://github.com/liquidtoy001/PRN/releases/latest)，
   在 Assets 中选择下表里的 ZIP。安装方法见 [小白使用指南](./USAGE.md)。
3. **准备资料。** 把需要处理的 slides 或讲义交给 Agent，先选一章试用。
4. **复制下面的开场白。** Agent 会集中询问缺少的选项，再逐章生成。

| 你想要什么 | 下载哪个文件 | 调用名称 |
|---|---|---|
| 打印笔记、PDF，也可选 Markdown / LaTeX | [pre-review-notes-v0.2.10.zip](https://github.com/liquidtoy001/PRN/releases/download/v0.2.10/pre-review-notes-v0.2.10.zip) | pre-review-notes |
| 离线网页笔记、可选折叠问答 | [pre-review-notes-html-v0.2.10.zip](https://github.com/liquidtoy001/PRN/releases/download/v0.2.10/pre-review-notes-html-v0.2.10.zip) | pre-review-notes-html |

不确定时先选 PDF 版。两个包可以分别安装，也可以同时安装。下载 Assets 里的安装 ZIP，
不需要下载 GitHub 自动提供的 Source code。旁边的 `.sha256` 是校验文件，不能用来安装。

**PDF 版开场白：**

```text
使用 pre-review-notes，帮我把这些课程资料整理成中文学习笔记。
选择知识巩固版、lightweight，先做第 1 章，最后给我 PDF。
请保留细小知识点，解释公式和有用的图表。
其他配置请一次列出来让我选。
```

**HTML 版开场白：**

```text
使用 pre-review-notes-html，帮我把这些课程资料整理成中文网页笔记。
选择知识巩固版、lightweight，先做第 1 章。
正文保留完整讲解，另外加可折叠答案的自测题。
请交付能离线打开的整个文件夹，其他配置请一次列出来让我选。
```

把“第 1 章”换成你要处理的文件名或页码。`lightweight` 的意思是先做一小批，
同一范围内仍应充分讲解。知识巩固版默认不出新题；上面的 HTML 示例明确选择了自测。

## 它会怎样处理资料

- 登记选定页面和知识点，保留条件、推导、原有例题和有教学价值的图表。
- 标明来源页码，区分课程内容、补充说明和可选的论文拓展。
- 提供知识巩固版和考试复习版；考试优先级需要课程考核证据支持。
- PDF 版要求检查分页和图表布局；HTML 版要求检查阅读、公式、图表和折叠交互。
- 分章保存进度，后续可以继续。PDF 版还提供可选的题库、Anki 导出和重测工具；
  HTML 版的折叠问答目前不记录掌握度。

生成 PDF 需要 Agent 所在环境有可用的排版工具；如果缺少工具，Agent 应说明缺哪一步，
不能把源文件当作已完成的 PDF。你可以先让 Agent 检查环境，详见使用指南。

## 示例与当前限制

[自编 HTML 样本](./tests/fixtures/html/) 用于检查公式、图片和问答结构；
[早期课程笔记示例](./examples/stat3007/README.md) 是历史试验，不代表当前版本的效果保证。

实际课程试用主要集中在 AI / 机器学习。跨学科准确性和学习效果尚未经过系统评测。
当前有 28 项自动化测试；测试通过不等于笔记内容和页面已经人工核对。
v0.2.10 的真实浏览器视觉与交互验收仍有未完成项，见
[验证记录](./TESTING-0.2.10.md)。使用时仍需对照原始资料检查。

课程 slides 和个人资料应保存在本地，不要提交到本仓库。
原始第三方课件不随安装包分发；代码和原创模板使用 [MIT License](./LICENSE)，
该授权不覆盖第三方课程材料。

## 版本与开发

当前安装版本：**v0.2.10**。Releases 保留最新双入口版本，以及 **v0.2.9**
这个最近的纯打印版本，供已有用户回退。更早版本的 Git 标签保留供历史查看，不再推荐安装。

开发者可阅读 [开发与测试说明](./DEVELOPMENT.md)、[测试方案](./TESTING.md)
和 [更新记录](./CHANGELOG.md)。两个 Skill 的共享规则只在 `shared/` 中维护，
安装包各自携带完整副本。
