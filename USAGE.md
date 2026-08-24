# 使用方法 · USAGE

完整功能需要一个能够读取 skill 目录、访问课程材料、运行本地脚本并写出文件的 Agent。
只有对话框或知识库的平台仍可使用核心方法，但无法自动获得材料哈希、增量状态和 PDF QA。

## 1. 安装完整 skill

### 从源码目录安装

把整个 `pre-review-notes/` 目录复制到目标 Agent 的 skills 目录。不要只复制
`SKILL.md`，因为 v0.1.0 会按需读取 `references/`、复用 `assets/` 并运行 `scripts/`。

如果目标环境支持 `skills` CLI，可以从仓库安装：

```bash
npx skills add https://github.com/liquidtoy001/PRN
```

### 从 Release ZIP 安装

运行下面的命令会在本地 `dist/` 生成扁平 ZIP；`SKILL.md` 位于 ZIP 根目录：

```powershell
python tools/package_skill.py
```

将 `dist/pre-review-notes-v0.1.0.zip` 上传到支持 skill ZIP 导入的平台。`dist/` 被 Git
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
还会抽样检查 PDF 文本并标记可能需要 OCR 的扫描件。角色分类和 OCR 标记都是路由提示，
不是课程事实。

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
材料目录是 ./materials，输出放在 ./output。
```

如果没有提供模式、语言、格式或影响排序的考试时间，skill 会只确认缺失项，不会重复询问
已经明确的偏好。

### 三种模式

| 模式 | 适合场景 | 主要结果 |
|---|---|---|
| `lightweight` | 第一次试用、只做一章、只有 slides | 材料边界、临时 topic map、一篇代表章节 |
| `full` | 多种资料齐全、准备长期维护 | 完整 assessment map、状态文件、逐章交付和增量更新 |
| `exam-cram` | 考试临近且时间预算明确 | 证据驱动的取舍、最高收益章节、练习动作和未覆盖风险 |

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

## 6. LaTeX 和 PDF

```powershell
python path/to/pre-review-notes/scripts/build_note.py `
  output/chapter.tex `
  --output-dir output/pdf
```

脚本会编译、重新打开 PDF、遍历页面并用 Poppler 渲染代表页。它会把视觉状态保留为
`pending`；Agent 或用户必须真正查看最新 PNG，确认没有裁切、重叠、乱码或空白页后，才能
把章节标记为 delivered。缺少编译器、`pypdf` 或 Poppler 时必须明确报告，不能把 `.tex`
冒充已完成的 PDF。

## 7. 仅支持文本指令的平台

无法加载目录的网页版可以粘贴 `SKILL.md`，再按任务附上相应 reference 和模板。例如做中文
LaTeX/PDF 时至少附上：

- `references/modes.md`；
- `references/evidence-workflow.md`；
- `references/authoring.md`；
- `references/pdf-workflow.md`；
- `assets/template.tex`。

这种方式没有自动脚本、稳定状态和渐进式资源加载，是兼容性降级方案，不等同于完整安装。
