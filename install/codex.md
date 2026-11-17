# Codex 安装 / 使用

本页对应 v2.7.1。手动升级时先用新的空目录收集四个运行文件，核对本地定制后再替换旧安装；仅覆盖入口会留下旧参考文件。

## mini / lite / full 怎么选

- `mini`：只把 [`dist/shuorenhua-mini.md`](../dist/shuorenhua-mini.md) 作为一次性 prompt，适合上下文很紧时粘贴使用（不含修订稿）。
- `lite`：只加载 [`SKILL.md`](../skills/shuorenhua/SKILL.md)，适合单次快速去套话（不含修订稿）。
- `full`：加载 `SKILL.md`、`references/editing-guide.md`、`references/examples.md`、`references/revision.md` 四个文件。修订稿已在 Codex CLI（GPT-6.1-sol）实测可用；lite 和 mini 没有这个模式。

## 方式 0：一行安装（推荐）

```bash
npx skills add MrGeDiao/shuorenhua
```

只安装四个运行文件；加 `--global` 对所有项目生效。需要放进自定义目录或核对本地定制时，用下面的手动复制。

## 方式 1：项目内长期使用

```bash
mkdir -p shuorenhua/references
cp skills/shuorenhua/SKILL.md shuorenhua/
cp skills/shuorenhua/references/editing-guide.md skills/shuorenhua/references/examples.md skills/shuorenhua/references/revision.md shuorenhua/references/
```

在项目 `AGENTS.md` 里补清楚触发入口：

```markdown
## 写作风格
当任务涉及"去 AI 味""说人话""自然一点""别像模板"这类改写时，遵循 `shuorenhua/SKILL.md`。
对外文本优先按它处理；代码、日志、配置和命令输出不套这个 skill。
```

## 方式 2：全局安装

```bash
mkdir -p ~/.codex/skills/shuorenhua/references
cp skills/shuorenhua/SKILL.md ~/.codex/skills/shuorenhua/
cp skills/shuorenhua/references/editing-guide.md skills/shuorenhua/references/examples.md skills/shuorenhua/references/revision.md ~/.codex/skills/shuorenhua/references/
```

如需在全局 `~/.codex/AGENTS.md` 写触发提示，只写触发条件即可，不要把整份 `SKILL.md` 拼进全局规则，按需读取更稳。

## 方式 3：命令行单次改写

在源码目录直接调用（不改任何项目配置）：

```bash
# 日常去套话
codex exec -C . "读取 ./skills/shuorenhua/SKILL.md，把下面这段文字去掉套话并保留原意：..."

# 只标问题，不改写
codex exec -C . "读取 ./skills/shuorenhua/SKILL.md，按 annotation mode 标出下面这段文字的问题：..."
```

## 常用说法与范围控制

装了 skill 后建议给明确要求触发：

- **日常直改**：`用说人话把这段去掉套话，保留信息和我的口气：……`
- **去掉吹捧腔**：`用说人话改写，别吹，写平实点：……`
- **黑话长文修订稿**：`用说人话彻底清理，黑话都换成大白话：……` 或 `用说人话给我一份修订稿，逐条列出改动，我来决定留哪些：……`（只说后者时改动较少；拿到结果后同一会话可回复 `撤销 2、5`、`撤销所有猜的`、`全部撤销`、`全收`、`再过一遍`，定稿前请重点看标「猜的」的条目）
- **控制范围**：代码块（含注释）默认逐字保留；约 1000 字以上的中文长文默认保留句段结构。可指定 `structural`（可删并重排）、`bounded`（句内清理，整句删除列在文后待确认）、`in-place`（只在原位改，要求保句数时不拆句），或无源论断处理方式（`audit-only` / `rewrite-safe`）。

## 手动检查

用来确认规则已加载（应去掉「值得注意的是」，保留超时从 30 秒改为 60 秒的关系）：

```text
用说人话规则改写：值得注意的是，接口超时从 30 秒改为 60 秒。
```
