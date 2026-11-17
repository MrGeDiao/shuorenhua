# OpenClaw 安装

本页对应 v2.7.1。手动升级时先用新的空目录收集四个运行文件，核对本地定制后再替换旧安装；仅覆盖入口会留下旧参考文件。

## mini / lite / full 怎么选

- `mini`：把 [`dist/shuorenhua-mini.md`](../dist/shuorenhua-mini.md) 放进一次性 prompt 或 `SOUL.md` 的风格段；它不含 skill 元数据，不参与自动发现，也不含修订稿。
- `lite`：只放 [`SKILL.md`](../skills/shuorenhua/SKILL.md)，适合 token 紧张或只做基础改写。
- `full`：放 `SKILL.md`、`references/editing-guide.md`、`references/examples.md`、`references/revision.md` 四个文件。修订稿依赖 `revision.md`，目前尚未在 OpenClaw 实测验证，使用时请核对改动清单与原文。

## 1. 把 skill 放进 workspace

```bash
mkdir -p workspace/skills/shuorenhua/references
cp skills/shuorenhua/SKILL.md workspace/skills/shuorenhua/
cp skills/shuorenhua/references/editing-guide.md skills/shuorenhua/references/examples.md skills/shuorenhua/references/revision.md workspace/skills/shuorenhua/references/
```

## 2. 触发方式选一个

**方式 A：按需触发（默认）**

放进 `workspace/skills/` 后，OpenClaw 会按 `name` 和 `description` 自动识别。对话里说「用说人话规则改写」即可触发。

**方式 B：设为对外文本默认规则**

在 `workspace/SOUL.md` 中添加：

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

VM 上 `git pull`（或自动拉取）后即生效。

## 常用说法与范围控制

- **日常直改**：`用说人话把这段去掉套话，保留信息和我的口气：……`
- **去掉吹捧腔**：`用说人话改写，别吹，写平实点：……`
- **黑话长文修订稿**：`用说人话彻底清理，黑话都换成大白话：……` 或 `用说人话给我一份修订稿，逐条列出改动，我来决定留哪些：……`（可回复 `撤销 2、5`、`撤销所有猜的`、`全部撤销`、`全收`、`再过一遍`）
- **只标问题不改写**：`先不要改写，只按 annotation mode 标出下面这段文字的问题：……`
- **范围控制**：程序代码块（含注释）默认逐字保护；约 1000 字以上的中文长文默认保留句段结构。可指定 `structural`、`bounded`、`in-place` 或无源论断模式（`audit-only` / `rewrite-safe`）。

## 手动检查

用来确认规则已生效（应去掉「值得注意的是」，保留超时从 30 秒改为 60 秒的关系）：

```text
用说人话规则改写这段文本：值得注意的是，接口超时从 30 秒改为 60 秒。
```
