# OpenClaw 安装

## 把 skill 放进 workspace

```bash
mkdir -p workspace/skills/shuorenhua
cp SKILL.md workspace/skills/shuorenhua/
cp -r references/ workspace/skills/shuorenhua/
```

## 在 SOUL.md 里引用

在 `workspace/SOUL.md` 中加一段：

```markdown
## 说人话
所有对外文本（消息、文档、摘要、公开写作）遵循 `skills/shuorenhua/SKILL.md` 的规则。
内部技术输出（代码、日志、配置）不受约束。
```

## 同步到 VM

```bash
git add workspace/skills/shuorenhua workspace/SOUL.md
git commit -m "feat: add shuorenhua skill"
git push
```

VM 上 `git pull` 后即生效。如果 VM 配了自动拉取，push 之后直接就能用。

## 怎么工作的

OpenClaw 启动时会读 `SOUL.md`，发现里面引用了 `skills/shuorenhua/SKILL.md`，就会把整个 skill 目录加载到上下文里。之后每次生成对外文本，都会按 12 条规则自动检查。

## token 预算紧张时

只放 `SKILL.md` 就够，核心规则是自包含的。`references/` 下的词表（phrases-zh.md 210+ 条、phrases-en.md 96 条）会占额外 token，但能让深度改写更准。按需取舍：

- **只要基本去味**：只放 `SKILL.md`
- **要精细改写**：放 `SKILL.md` + `references/`

## 验证

在 OpenClaw 对话里输入：

```
用说人话规则改写这段文本：在当今快速发展的人工智能时代，如何打造一个真正赋能开发者的工具，已经成为业界不容忽视的关键议题。
```

如果输出里没有"打造""赋能""不容忽视""关键议题"，说明 skill 生效了。
