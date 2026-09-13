# Codex 安装 / 使用

手动升级时先用新的空目录收集运行文件，核对本地定制后再切换旧安装；仅覆盖入口会留下旧参考文件。下方复制命令面向首次安装或空目录。

本页对应 v2.5.0。升级时请核对本地定制，并用新的运行文件替换旧安装。

## mini / lite / full 怎么选

- `mini`：只把 `dist/shuorenhua-mini.md` 作为一次性 prompt。适合上下文很紧或临时粘贴使用；它不是完整 skill。
- `lite`：只加载 `SKILL.md`。适合单次临时改写、上下文紧张、只想先压掉明显模板感的场景。
- `full`：加载 `SKILL.md`、`references/editing-guide.md`、`references/examples.md` 三个文件。适合长期项目、README / release note / issue 回复、技术文档和需要查看编辑边界与改写对照的任务。

## 方式 1：项目内长期使用（推荐）

把 skill 文件放进项目：

```bash
mkdir -p shuorenhua/references
cp SKILL.md shuorenhua/
cp references/editing-guide.md references/examples.md shuorenhua/references/
```

这是 full 用法，也是项目内长期使用的默认建议。

在 `AGENTS.md` 里写清楚触发条件和适用边界：

```markdown
## 写作风格
当任务涉及"去 AI 味""说人话""自然一点""别像模板"这类改写时，遵循 `shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

这样规则跟项目一起版本管理，团队成员也能复用。

## 方式 2：单次改写

在仓库根目录运行，让 Codex 先读取 `SKILL.md` 再改写：

```bash
codex exec -C . "读取 ./SKILL.md，按其中规则改写以下文本：..."
```

不需要修改项目文件，适合临时使用。这是 lite 用法；如果要处理复杂的语义边界或需要对照改写例子，建议同时让 Codex 读取 `references/` 下的相关文件。

如果当前上下文放不下完整规则，可以改读 mini：

```bash
codex exec -C . "读取 ./dist/shuorenhua-mini.md，按其中规则改写以下文本：..."
```

如果你想先判断“哪里像 AI”，不要直接改稿，可以这样用：

```bash
codex exec -C . "读取 ./SKILL.md，只按 annotation mode 标出下面这段文字里的问题：..."
```

适合这几类场景：

- 你想先看这段话该不该改
- 你要做审稿或 review，不想直接替作者重写
- 你怀疑有无源引用、语域混搭或工程师腔，但还不想动正文

## 方式 3：全局 AGENTS

先把完整规则放到本地 skill 目录：

```bash
mkdir -p ~/.codex/skills/shuorenhua/references
cp SKILL.md ~/.codex/skills/shuorenhua/
cp references/editing-guide.md references/examples.md ~/.codex/skills/shuorenhua/references/
```

这是 full 用法。只复制 `SKILL.md` 是 lite；两份参考文件只在需要时读取。

再在全局 `AGENTS.md` 里写触发入口：

```bash
mkdir -p ~/.codex
cat >> ~/.codex/AGENTS.md <<'EOF'
当任务涉及"去 AI 味""说人话""自然一点""别像模板"这类改写时，使用本地 skill `shuorenhua`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
EOF
```

全局入口只建议写触发条件，不建议把整份 `SKILL.md` 直接拼进全局规则。完整规则仍应放在项目内或本地 skill 目录里，按需读取更稳。

## 注意

"装了 skill"不等于 Codex 会无条件自动套用全部规则。你需要给它一个清楚的触发入口（`AGENTS.md`、项目提示，或在单次任务里明确要求读取 `SKILL.md`），它才会按规则处理。

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
用说人话规则改写：值得注意的是，接口超时从 30 秒改为 60 秒。
```

可以去掉“值得注意的是”，但必须保留接口超时及 30 秒改为 60 秒的关系。
