# Cursor / Windsurf 安装

本页对应 v2.7.1。手动升级时先用新的空目录收集四个运行文件，核对本地定制后再替换旧安装；仅覆盖入口会留下旧参考文件。

## mini / lite / full 怎么选

- `mini`：把 [`dist/shuorenhua-mini.md`](../dist/shuorenhua-mini.md) 粘贴进单次聊天或临时 Rule（不含修订稿）。
- `lite`：只加载 [`SKILL.md`](../skills/shuorenhua/SKILL.md)，适合日常去套话和轻量审稿（不含修订稿）。
- `full`：加载 `SKILL.md`、`references/editing-guide.md`、`references/examples.md`、`references/revision.md` 四个文件。修订稿依赖 `revision.md`，目前尚未在 Cursor / Windsurf 内实测验证，使用时请核对改动清单与原文。

## 方式 0：一行安装（推荐）

```bash
npx skills add MrGeDiao/shuorenhua
```

先试这条；需要把文件手动放进 `.cursor/rules` 或 `.windsurf/rules` 目录时，用下方命令。

## 方式 1：项目 Rules

只装入口（`lite` 用法）：

```bash
# Cursor
mkdir -p .cursor/rules
cp skills/shuorenhua/SKILL.md .cursor/rules/shuorenhua.md

# Windsurf
mkdir -p .windsurf/rules
cp skills/shuorenhua/SKILL.md .windsurf/rules/shuorenhua.md
```

需要使用编辑边界、改写对照或修订稿时，再把参考文件复制进去，升级为 `full` 用法：

```bash
# Cursor
mkdir -p .cursor/rules/references
cp skills/shuorenhua/references/editing-guide.md skills/shuorenhua/references/examples.md skills/shuorenhua/references/revision.md .cursor/rules/references/

# Windsurf
mkdir -p .windsurf/rules/references
cp skills/shuorenhua/references/editing-guide.md skills/shuorenhua/references/examples.md skills/shuorenhua/references/revision.md .windsurf/rules/references/
```

## 方式 2：全局 Rules

在 Cursor Settings > Rules 中粘贴 `SKILL.md`（或上下文紧张时粘贴 `dist/shuorenhua-mini.md`）的内容。

## 常用说法与范围控制

Rules 放进目录不等于会自动改写所有输出，使用时请明确下达指令：

```text
用说人话规则把这段去掉套话，保留信息和我的口气：……
用说人话规则改写，别吹，写平实点：……
用说人话彻底清理，黑话都换成大白话：……
用说人话给我一份修订稿，逐条列出改动，我来决定留哪些：……
先不要改写，只按 annotation mode 标出下面这段文字的问题：……
```

- **修订稿撤销**：拿到修订稿后，同一对话可回复 `撤销 2、5`、`撤销所有猜的`、`全部撤销`、`全收` 或 `再过一遍`。
- **范围控制**：程序代码块（含注释和文档字符串）默认逐字保留；约 1000 字以上的中文长文默认保留句段结构。可指定 `structural`（可删并重排）、`bounded`（句内清理，整句删除只列文后建议）、`in-place`（只在原位改，保句数时不拆句），以及无源论断处理方式（`audit-only` / `rewrite-safe`）。

## 手动检查

用来确认规则已加载（应去掉「值得注意的是」，保留超时从 30 秒改为 60 秒的关系）：

```text
用说人话规则改写这段文本：值得注意的是，接口超时从 30 秒改为 60 秒。
```
