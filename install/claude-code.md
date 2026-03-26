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

## 验证

```text
在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。
```

输出不再保留 `打造 / 赋能 / 不容忽视 / 关键议题`，且信息没有改散，说明接好了。
