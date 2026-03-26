# OpenClaw 安装

## 1. 把 skill 放进 workspace

```bash
mkdir -p workspace/skills/shuorenhua
cp SKILL.md workspace/skills/shuorenhua/
cp -r references workspace/skills/shuorenhua/
```

token 紧张时只放 `SKILL.md` 也能完成基础改写；`references/` 能让场景判断和误杀防护更稳。

## 2. 触发方式选一个

**方式 A：按需触发（默认）**

把文件放进 `workspace/skills/` 后，OpenClaw 会按 skill 的 `name` 和 `description` 判断何时启用。对话里说"用说人话规则改写"就能触发，不需要额外配置。

**方式 B：设为默认写作风格**

如果希望所有对外文本都自动套用，在 `workspace/SOUL.md` 中加：

```markdown
## 说人话
所有对外文本（消息、文档、摘要、公开写作）遵循 `skills/shuorenhua/SKILL.md` 的规则。
内部技术输出（代码、日志、配置）不受约束。
```

## 3. 同步到 VM

```bash
git add workspace/skills/shuorenhua
git commit -m "feat: add shuorenhua skill"
git push
```

VM 上 `git pull` 后即生效。如果 VM 配了自动拉取，push 之后直接就能用。

## 验证

```text
用说人话规则改写这段文本：在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。
```

输出里不再保留 `打造 / 赋能 / 不容忽视 / 关键议题`，且信息没有改散，说明 skill 生效了。
