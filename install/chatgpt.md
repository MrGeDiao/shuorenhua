# ChatGPT / 通用 LLM 安装

本页对应 v2.7.1。

OpenAI 计划在 2026-12-11 停用 Custom GPT，原来的说人话 GPT 届时不能再用，请改用下面的方式。

## mini / lite / full 怎么选

- `mini`：粘贴 [`dist/shuorenhua-mini.md`](../dist/shuorenhua-mini.md)，适合一次性使用或字数限制严的输入框（1,500 字符以内，不含修订稿）。
- `lite`：只加载 [`SKILL.md`](../skills/shuorenhua/SKILL.md)，包含核心保真边界、写平实和交付要求（不含修订稿）。
- `full`：加载 [`SKILL.md`](../skills/shuorenhua/SKILL.md)、[`editing-guide.md`](../skills/shuorenhua/references/editing-guide.md)、[`examples.md`](../skills/shuorenhua/references/examples.md)、[`revision.md`](../skills/shuorenhua/references/revision.md) 四个文件。修订稿依赖 `revision.md`，目前尚未在 ChatGPT 上实测验证，使用时请核对改动清单与原文。

## ChatGPT

### 方案一：Projects（推荐长期使用）

1. 新建 Project。
2. 下载上面 `full` 的四个文件，上传到 Project Files；临时使用也可只放 `SKILL.md`。
3. 在 Project Instructions 中填入：

```text
按照项目文件中 SKILL.md 的规则编辑用户提供的文本。遇到语义边界或需要例子时，查阅 editing-guide.md 和 examples.md。用户要修订稿或要求彻底清理黑话时，先读 revision.md 并按其中格式交付。
```

### 方案二：直接贴进单次对话

在对话开头贴 [`dist/shuorenhua-mini.md`](../dist/shuorenhua-mini.md) 或 [`SKILL.md`](../skills/shuorenhua/SKILL.md) 的内容，再附上原文和编辑要求。

### 方案三：Custom Instructions

将 `mini` 粘贴到 Settings > Personalization > Custom Instructions（以界面实际字数上限为准）。

## Claude（Web / Project）

1. 创建 Project，将 `SKILL.md` 内容放入 Project Instructions。
2. 将 `editing-guide.md`、`examples.md`、`revision.md` 放入 Project Knowledge，按需查阅。

## API / System Prompt

```python
messages = [
    {"role": "system", "content": open("skills/shuorenhua/SKILL.md").read()},
    {"role": "user", "content": "把这段去掉套话，保留信息和我的口气：..."}
]
```

没有文件读取工具的 API 调用不会自动加载路径指向的文件；若要用修订稿或参考边界，需将对应文件内容一并拼入上下文。

## 常用说法与范围控制

- **日常直改（默认）**：`把这段去掉套话，保留信息和我的口气：……`（默认只交正文；正常原文完整返回；程序代码块含注释默认逐字保护）
- **去掉吹捧腔**：`别吹，写平实点：……`（降掉只表示程度的夸饰、删空口号，保留承诺、首次和数字）
- **长文修订稿（需 full）**：`彻底清理，黑话都换成大白话：……` 或 `给我一份修订稿，逐条列出改动，我来决定留哪些：……`（只说后者时改动较少；交付后可回复 `撤销 2、5`、`撤销所有猜的`、`全部撤销`、`全收`、`再过一遍`）
- **只审稿不改写**：`只标问题，不改写：……`（`annotation mode`，只指出问题片段和修改方向，不交替换全文）
- **控制改动范围**：约 1000 字以上的中文长文默认保留句段结构；也可点名 `structural`（可删并重排）、`bounded`（句内改，整句删除只列文后建议）、`in-place`（不删并重排，要求保句数时也不拆句）。
- **无源论断**：「研究表明」等缺出处的说法默认连归属一起保留并在文后提示；明确指定 `rewrite-safe` 才允许按范围删减，或用 `audit-only` 只标缺口。
