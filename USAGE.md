# 使用方法 · USAGE

前提只有两个：你使用的 AI 工具能 **(a) 检索/读取你的课程材料**，且 **(b) 能输出文件或长文本**。技能本身与具体平台无关。

## 方式一：国产模型 + Agent 工具（推荐，技能零修改原生可用）

- **一键安装**（需 Node.js，适用于 Claude Code 及兼容 skills 目录的 agent）：

  ```bash
  npx skills add https://github.com/liquidtoy001/pre-review-notes
  ```

- **Claude Code + 国产模型兼容 API**（智谱 GLM Coding Plan / Kimi K2 / DeepSeek 均提供 Anthropic 兼容端点）：
  1. 把 `pre-review-notes/` 目录整个复制到 `~/.claude/skills/pre-review-notes/`
  2. 课程材料放进项目目录
  3. 直接说"帮我做 XX 课的期末复习笔记"，技能自动触发
- **Qoder / Trae / CodeBuddy 等国产 Agentic IDE**：把 `pre-review-notes/` 目录放入工作区或注册为本地 skill / rules，材料放同一工作区即可。

## 方式二：智能体平台（非技术背景用户，一次配置长期用）

在 **扣子 Coze / 腾讯元器 / 智谱清言智能体** 上新建智能体：

1. 将 `SKILL.md` 全文粘贴为智能体的系统提示词（人设与回复逻辑）
2. 课程材料上传到平台的知识库
3. 文科课程可将 `markdown-template.md` 的正文一并贴入提示词末尾
4. 配置完成后可分享给同学复用

## 方式三：网页版直接对话（降级用法）

Kimi（长上下文，适合一次传几十个课件）、腾讯元宝、豆包、DeepSeek 网页版等：每次会话先粘贴 `SKILL.md` 全文，再上传材料。可用，但没有自动触发机制，建议手动提醒模型遵守"反模式清单"（不许按教材顺序写、不许编造考试相关性）。

## 方式四：海外平台

- **claude.ai / Claude Desktop**：设置 → Capabilities 中直接上传 `pre-review-notes-v0.0.1.zip`
- **ChatGPT / Gemini**：同方式三，将 `SKILL.md` 贴入 Project Instructions 或 Gem 指令

## 检索端补强（可选）

材料量大时，可用 **腾讯 ima 知识库 / 飞书知识问答 / NotebookLM** 做带引用溯源的材料库，负责检索端；生成端接上述任一方式。
