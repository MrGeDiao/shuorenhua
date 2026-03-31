# Claude Code 安装

## 方式 1：项目级（推荐）

```bash
mkdir -p .claude/skills/shuorenhua
cp SKILL.md .claude/skills/shuorenhua/
cp -r references .claude/skills/shuorenhua/
```

在项目的 `CLAUDE.md` 中写清楚触发条件：

```markdown
## 写作风格
当任务涉及"去 AI 味""说人话""自然一点""别像模板"这类改写时，遵循 `.claude/skills/shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

Claude Code 不会自动发现并应用 skill 文件——CLAUDE.md 里的说明是触发入口，不能省略。

## 方式 2：全局

```bash
mkdir -p ~/.claude/skills/shuorenhua
cp SKILL.md ~/.claude/skills/shuorenhua/
cp -r references ~/.claude/skills/shuorenhua/
```

即使放到全局目录，也建议在各项目的 `CLAUDE.md` 里补一条触发说明，否则 Claude Code 不会主动读取。

## 使用

对话里直接说：

```text
用说人话规则改写这段文本。
```

或者更具体：

```text
把这段 status 更新按说人话规则轻改，保留术语和系统主语，不要改成口语闲聊体。
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

三种模式：`rewrite-safe`（默认用于 chat/public-writing，直接删无证据权威铺垫）、`audit-only`（默认用于 docs/status，只标缺来源）、`rewrite-with-placeholder`（保留结构但暴露缺来源）。不指定时按场景默认值走。

## 验证

```text
在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。
```

输出不再保留 `打造 / 赋能 / 不容忽视 / 关键议题`，且信息没有改散，说明接好了。
