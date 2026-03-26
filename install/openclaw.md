# OpenClaw 安装

## 1. 把 skill 放进 workspace

```bash
mkdir -p ~/.openclaw/workspace/skills/shuorenhua
cp SKILL.md ~/.openclaw/workspace/skills/shuorenhua/
cp -r references ~/.openclaw/workspace/skills/shuorenhua/
```

如果你只是想先试效果，放 `SKILL.md` 也能工作；`references/` 会让场景判断、误杀防护和重写更稳。

## 2. 让 OpenClaw 更容易触发这个 skill

OpenClaw 会先读取 skill 的 `name` 和 `description` 来决定什么时候启用它，所以这两点最重要：

- skill 目录名尽量和项目名一致：`shuorenhua`
- `SKILL.md` 的 frontmatter 里要写清楚触发语，比如：`去 AI 味 / 说人话 / 自然一点 / 别像模板`

只把文件放进 `workspace/skills/`，通常就足够让它进入技能扫描范围。

## 3. 如果你想把它设成默认写作风格

可以在 `SOUL.md` 或其他长期风格文件里加一句偏好约束，例如：

```markdown
## 说人话
所有对外文本（消息、文档、摘要、公开写作）优先遵循 `skills/shuorenhua/SKILL.md` 的规则；
内部技术输出（代码、日志、配置）默认不套这个技能。
```

这一步不是必须的。

- **只想在用户明确要求时触发**：不加这一段
- **想让它变成默认外发文风**：加这一段

## 4. 怎么验证有没有生效

在 OpenClaw 对话里输入：

```text
用说人话规则改写这段文本：在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。
```

如果输出里：
- 没有继续保留 `打造 / 赋能 / 不容忽视 / 关键议题` 这类套话
- 但也没有把技术信息改散

说明 skill 已经基本生效。

## 5. token 预算紧张时怎么放

### 最省

只放：
- `SKILL.md`

适合：
- 只是想做基础去味
- 触发频率不高
- 希望尽量少占上下文

### 推荐

放：
- `SKILL.md`
- `references/phrases-zh.md`
- `references/phrases-en.md`
- `references/structures.md`
- `references/severity.md`
- `references/operation-manual.md`
- `references/scene-guardrails.md`
- `references/boundary-cases.md`

适合：
- 想要更稳的场景判断
- 想减少误杀
- 想让重写不只靠词表，而是能按问题类型处理

## 6. 一个更贴近 OpenClaw 的理解方式

这份 skill 现在的结构是：

1. `SKILL.md` 负责入口判断：场景、Tier、档位、输出合同
2. `references/` 负责补细节：短语、结构、边界、微操作

也就是说，它不是“把一大坨规则一次性塞进上下文”，而是“先给主判断，再按需补读”。这更适合 OpenClaw 这种会先做 skill 选择、再按需读取文件的运行方式。
