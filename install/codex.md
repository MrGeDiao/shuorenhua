# Codex CLI 安装

## 方式 1：AGENTS.md（推荐）

在项目根目录创建或编辑 `AGENTS.md`，添加以下内容：

```markdown
## 写作风格
对外文本遵循 `stop-slop-zh/SKILL.md` 的反模式规则。
```

然后将 skill 文件放到项目中：

```bash
mkdir -p stop-slop-zh
cp SKILL.md stop-slop-zh/
cp -r references/ stop-slop-zh/
```

Codex 会自动读取 `AGENTS.md` 并在需要时引用规则文件。

## 方式 2：System Prompt

直接通过 `--system-prompt` 传入规则：

```bash
codex --system-prompt "$(cat SKILL.md)" "改写以下文本：..."
```

适合一次性使用，不需要修改项目文件。

## 方式 3：全局 Instructions

在 `~/.codex/instructions.md` 中添加规则：

```bash
mkdir -p ~/.codex
cat SKILL.md >> ~/.codex/instructions.md
```

这样所有 Codex 会话都会自动加载去 AI 味规则。

## 注意

- 推荐方式 1，让规则跟随项目版本控制
- 如果 token 预算紧张，只放 `SKILL.md` 即可（核心规则自包含）
- 需要深度改写时再手动引用 `references/` 下的禁用短语表
