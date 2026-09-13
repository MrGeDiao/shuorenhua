# Claude Code 安装

本页对应 2.5.0 开发候选，尚未发布。远程安装入口仍提供已发布版本；测试候选时，请从本地候选源码目录复制文件。

## 方式 1：plugin 一键安装（推荐）

```text
/plugin marketplace add MrGeDiao/shuorenhua
/plugin install shuorenhua@shuorenhua
```

在 Claude Code 对话里执行这两条命令即可，skill 自动发现和触发。升级用 `/plugin` 面板或 `claude plugin update shuorenhua`。

Git 插件会下载源仓库，其中实际运行规则是 `SKILL.md`、`references/editing-guide.md`、`references/examples.md` 三个文件；它不是只含三个文件的归档。评测和历史材料不由入口加载。只需要独立运行目录时，使用下方手动复制方式。

这种根目录单 SKILL 插件布局要求 Claude Code v2.1.142 或以上，见[官方插件说明](https://code.claude.com/docs/en/plugins-reference)。本地候选已在 Claude Code 2.1.268 上用隔离的 `CLAUDE_CONFIG_DIR` 完成 `marketplace add` → `plugin install` → `plugin details` → `plugin uninstall` 验收：能发现 1 个 `shuorenhua` skill，卸载后恢复为空。GitHub 远程安装路径仍需发布后另行复测。已有手动安装时，先备份并核对本地定制，再切换到一种安装方式，避免重复发现。

## mini / lite / full 怎么选（手动使用时）

- `mini`：只把 `dist/shuorenhua-mini.md` 贴进单次会话。适合上下文很紧；它不参与 skill 自动发现。
- `lite`：只加载 `SKILL.md`。适合临时改写和轻量审稿。
- `full`：加载 `SKILL.md`、`references/editing-guide.md`、`references/examples.md` 三个文件。适合项目级安装、公开文本、技术文档和需要查看编辑边界与改写对照的任务。

Claude Code 会基于 `SKILL.md` 开头的 description 自动发现并触发 skills 目录里的 skill，装好即用。

手动升级时先在新的空目录中放入三个文件，核对本地定制后再切换旧安装；不要直接覆盖一个仍含旧词表的目录。以下复制命令面向首次安装或空目录，在本地 2.5 候选源码目录执行。

## 方式 2：项目级

```bash
mkdir -p .claude/skills/shuorenhua/references
cp SKILL.md .claude/skills/shuorenhua/
cp references/editing-guide.md references/examples.md .claude/skills/shuorenhua/references/
```

这是 full 用法，也是项目级安装的默认建议。规则跟项目一起进版本管理，团队成员 clone 即用。

## 方式 3：全局

```bash
mkdir -p ~/.claude/skills/shuorenhua/references
cp SKILL.md ~/.claude/skills/shuorenhua/
cp references/editing-guide.md references/examples.md ~/.claude/skills/shuorenhua/references/
```

只复制这三个运行文件。不要把含评测与历史快照的整个开发仓库放进 skills 扫描目录；lite 只复制 `SKILL.md`。

## 方式 4：跟随更新

```bash
mkdir -p ../shuorenhua-runtime/references
cp SKILL.md ../shuorenhua-runtime/
cp references/editing-guide.md references/examples.md ../shuorenhua-runtime/references/
mkdir -p ~/.claude/skills
ln -s "$PWD/../shuorenhua-runtime" ~/.claude/skills/shuorenhua
```

软链接指向源码目录旁单独的运行目录。源码更新并核对差异后，再重复两条 `cp` 命令同步三个文件；不要把软链接改为整个开发仓库。

## 触发说明（可选）

Claude Code 会基于 SKILL.md 开头的 description 自动触发这个 skill。如果你想在长期项目里提高命中稳定性、或限定它只处理对外文本，可以在项目的 `CLAUDE.md` 里补一段触发说明（可选，不是必需）：

```markdown
## 写作风格
当任务涉及“去 AI 味”“说人话”“自然一点”“别像模板”这类改写时，遵循 `.claude/skills/shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

## 使用

对话里直接说：

```text
用说人话规则改写这段文本。
```

或者更具体：

```text
把这段进展说明按说人话规则轻改，保留术语和系统主语，不要改成口语闲聊体。
```

如果你想先判断"哪里像 AI"，不要直接改稿：

```text
先不要改写，只按 annotation mode 标出下面这段文字里的问题：...
```

适合这几类场景：

- 你想先看这段话该不该改
- 你要做审稿或 review，不想直接替作者重写
- 你怀疑有无源引用、语域混搭或工程师腔，但还不想动正文

处理无源引用时，可以指定模式：

```text
用说人话规则改写这段文本，无源引用按 audit-only 处理。
```

默认保留无源论断及其归属，必要时在正文外提示缺来源。只有明确指定 `rewrite-safe` 或要求删除无源论断，才允许整条删除；`bounded` 只列删除建议，`in-place` 保留原句并提示。`audit-only` 标出来源缺口，其他内容照常编辑；`rewrite-with-placeholder` 按用户要求保留论证结构、标待补来源，不编出处。

## 编辑范围

默认做最小必要修改；中文公开长文约 1000 字以上默认保留句段结构。可以直接指定：

程序代码块（包括注释和文档字符串）默认逐字保留；只有用户明确点名修改注释或说明文字时才编辑相应部分，且不改程序行为。代码围栏里的普通文案仍可按用户要求编辑。

- `structural`：允许删、并、重排，仍须保留有效信息与作者意图。
- `bounded`：不直接删整句、不并句、不重排。纯空句可列“建议删除（待确认）”，正文暂时保留。
- `in-place`：不删句、不并句、不重排，只在句内替换或删修饰；要求保句数时也不拆句。

例如：“按 bounded 改，删除建议放在正文后。”这些范围不因编辑力度或来源处理方式而放宽。

## 手动检查

提交正文后，确认保留原文语言、事实、条件与作者立场。正常原文应完整返回，不只回复“保留原文”；只标问题时不应附替换全文。以下提示可用来检查是否加载，但不能代替效果评测。

```text
值得注意的是，接口超时从 30 秒改为 60 秒。
```

可以去掉“值得注意的是”，但必须保留接口超时及 30 秒改为 60 秒的关系。
