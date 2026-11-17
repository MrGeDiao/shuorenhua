# Claude Code 安装

本页对应 v2.7.1。升级时请核对本地定制，并用新的运行文件替换旧安装。

## 方式 1：plugin 一键安装（推荐）

```text
/plugin marketplace add MrGeDiao/shuorenhua
/plugin install shuorenhua@shuorenhua
```

在 Claude Code 对话里执行这两条命令即可自动发现并按需触发。升级可在 `/plugin` 面板操作或运行 `claude plugin update shuorenhua`。

Git 插件会拉取源仓库，但只加载 `skills/shuorenhua/` 下的四个运行文件，评测和历史材料不会被加载。只需要独立运行目录时，用下面的手动复制方式。

## mini / lite / full 怎么选（手动使用时）

- `mini`：把 [`dist/shuorenhua-mini.md`](../dist/shuorenhua-mini.md) 贴进单次会话，适合上下文很紧时临时用（不参与自动发现，不含修订稿）。
- `lite`：只放 [`SKILL.md`](../skills/shuorenhua/SKILL.md)，适合轻量改写和审稿（不含修订稿）。
- `full`：放 `SKILL.md`、`references/editing-guide.md`、`references/examples.md`、`references/revision.md` 四个文件。修订稿已在 Claude Code（Opus 5.5）实测通过；lite 和 mini 没有这个模式。

手动升级时先用空目录收集四个运行文件，核对本地定制后再替换旧目录，避免残留旧版词表文件。

## 方式 2：项目级或全局手动复制

先克隆本仓库，在源码目录执行。项目级（随项目进版本管理，团队共享）：

```bash
mkdir -p .claude/skills/shuorenhua/references
cp skills/shuorenhua/SKILL.md .claude/skills/shuorenhua/
cp skills/shuorenhua/references/editing-guide.md skills/shuorenhua/references/examples.md skills/shuorenhua/references/revision.md .claude/skills/shuorenhua/references/
```

全局（当前机器所有项目可用）：

```bash
mkdir -p ~/.claude/skills/shuorenhua/references
cp skills/shuorenhua/SKILL.md ~/.claude/skills/shuorenhua/
cp skills/shuorenhua/references/editing-guide.md skills/shuorenhua/references/examples.md skills/shuorenhua/references/revision.md ~/.claude/skills/shuorenhua/references/
```

若用软链接跟随本地源码更新，请链接到单独抽取的运行目录（仅含这四个文件），**不要把整个开发仓库软链接进 skills 扫描目录**。

可选：若想在项目里限定只对外部文案触发，可在项目 `CLAUDE.md` 补一段说明：

```markdown
## 写作风格
当任务涉及“去 AI 味”“说人话”“自然一点”“别像模板”这类改写时，遵循 `.claude/skills/shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

## 常用说法与范围控制

对话里直接贴原文并说要求（想确保触发可点名「用说人话」）：

```text
把这段去掉套话，保留术语和我的口气：……
别吹，写平实点：……
彻底清理，黑话都换成大白话：……
给我一份修订稿，逐条列出改动，我来决定留哪些：……
只标问题，不改写：……
```

- **修订稿与撤销**：说「彻底清理，黑话都换成大白话」或「给我一份修订稿……」都会进入修订稿（只说后者时改动较少，想多改请带上「彻底清理」）。拿到修订稿后，同一会话内可回复 `撤销 2、5`、`撤销所有猜的`、`全部撤销`、`全收` 或 `再过一遍`。
- **范围控制**：程序代码块（含注释和文档字符串）默认逐字保留；约 1000 字以上的中文公开长文默认保留句段结构。也可指定 `structural`（可删并重排）、`bounded`（句内清理，整句删除只列文后建议）、`in-place`（只在原位改，要求保句数时不拆句）。
- **无源论断**：缺出处的「研究表明」默认保留归属并在文后提示；指定 `rewrite-safe` 才按编辑范围删减，或用 `audit-only` 只标缺口。

## 手动检查

用来确认规则已生效（应去掉「值得注意的是」，完整保留超时从 30 秒改为 60 秒的关系）：

```text
用说人话规则改写：值得注意的是，接口超时从 30 秒改为 60 秒。
```
