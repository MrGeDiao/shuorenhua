# Codex CLI 安装

## 方式 1：项目内长期使用（推荐）

把 skill 文件放进项目：

```bash
mkdir -p shuorenhua
cp SKILL.md shuorenhua/
cp -r references shuorenhua/
```

在 `AGENTS.md` 里写清楚触发条件和适用边界：

```markdown
## 写作风格
当任务涉及"去 AI 味""说人话""自然一点""别像模板"这类改写时，遵循 `shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

这样规则跟项目一起版本管理，团队成员也能复用。

## 方式 2：单次改写

直接把 `SKILL.md` 当 system prompt 传入：

```bash
codex --system-prompt "$(cat SKILL.md)" "改写以下文本：..."
```

不需要修改项目文件，适合临时使用。

如果你想先判断“哪里像 AI”，不要直接改稿，可以这样用：

```bash
codex --system-prompt "$(cat SKILL.md)" "先不要改写，只按 annotation mode 标出下面这段文字里的问题：..."
```

适合这几类场景：

- 你想先看这段话该不该改
- 你要做审稿或 review，不想直接替作者重写
- 你怀疑有无源引用、语域混搭或工程师腔，但还不想动正文

## 方式 3：全局 Instructions

```bash
mkdir -p ~/.codex
cat SKILL.md >> ~/.codex/instructions.md
```

所有 Codex 会话都会带上这套风格。建议只放 `SKILL.md`，不要把整个 `references/` 全量拼入——按需在具体任务里引用更稳。

## 注意

"装了 skill"不等于 Codex 会无条件自动套用全部规则。你需要给它一个清楚的触发入口（`AGENTS.md`、system prompt 或 instructions），它才会按规则处理。

## 验证

```text
用说人话规则改写：在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。
```

输出去掉了 `打造 / 赋能 / 不容忽视 / 关键议题`，但没把信息改空，说明接上了。
