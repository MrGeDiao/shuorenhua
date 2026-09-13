# ChatGPT / 通用 LLM 安装

本页对应 2.5.0 开发候选，尚未发布。现有公开 GPT 未随本地文件自动更新；测试候选时，请自行加载本地文件。

## mini / lite / full 怎么选

- `mini`：粘贴 [`dist/shuorenhua-mini.md`](../dist/shuorenhua-mini.md)，适合一次性使用或输入空间有限的地方。
- `lite`：只加载 `SKILL.md`，包含主要编辑边界和交付要求。
- `full`：加载 `SKILL.md`、`references/editing-guide.md`、`references/examples.md` 三个文件；两份参考文件按需查阅。

## ChatGPT

### 方案一：Custom GPT

可以使用现有的[说人话 GPT](https://chatgpt.com/g/g-6a5829b1163481919e1e45851f6bc709-shuo-ren-hua)。它的线上版本与本地候选分开维护。

自建时沿用以下方式：

1. 打开 [GPT Editor](https://chatgpt.com/gpts/editor)，新建 GPT。
2. 名称填“说人话”，描述填“去 AI 味的中英文改写助手”。
3. 把 [Custom GPT Instructions](chatgpt-gpt-instructions.md) 分隔线以下的内容放进 Instructions。
4. 在 Knowledge Files 中上传 `SKILL.md`、`references/editing-guide.md`、`references/examples.md`。
5. 保存，并按自己的使用范围选择可见性。

上传文件不等于每次都会读取全部内容；入口要求以 `SKILL.md` 为准，遇到边界问题再查两份参考文件。

### 方案二：Projects

1. 新建 Project。
2. 将上述三个文件上传到 Project Files；临时使用也可以只放 `SKILL.md`。
3. 在 Project Instructions 中写：`按照项目文件中 SKILL.md 的规则编辑用户提供的文本。遇到语义边界或需要例子时，再查 editing-guide.md 和 examples.md。`

### 方案三：直接贴对话

在对话开头贴 mini 的内容，再提供原文和编辑要求。也可以直接贴 `SKILL.md` 使用 lite。

### 方案四：Custom Instructions

将 mini 粘贴到 Settings > Personalization > Custom Instructions。mini 控制在 1,500 字符以内；实际输入限制以界面提示为准。完整入口和参考文件可用上面的 GPT 或 Project 文件方式加载。

## Claude（Web / Project）

1. 创建 Project。
2. 将 `SKILL.md` 内容放入 Project Instructions。
3. 将 `references/editing-guide.md` 和 `references/examples.md` 放入 Project Knowledge，按需查阅。

## API / System Prompt

```python
messages = [
    {"role": "system", "content": open("SKILL.md").read()},
    {"role": "user", "content": "改写以下文本：..."}
]
```

已有主 system prompt 时，把入口作为编辑规则补入，不覆盖其他任务要求。两份参考文件可在需要时一起提供；没有文件访问能力的模型不会因为文本里写了路径就自动读取文件。

## 使用要求

直接说“轻改，保留作者口气”，或“只标问题，不改写”。后一种是 `annotation mode`：只引用问题片段并给修改方向，不交替换全文。默认保持原文语言；无须修改时，完整返回原文。

默认保留来源不明的论断及其归属，必要时在正文外提示缺来源。只有用户明确指定 `rewrite-safe` 或要求删除无源论断，才允许整条删除；`bounded` 只列删除建议，`in-place` 保留原句并提示缺来源。`audit-only` 标出来源缺口，其他内容照常编辑；`rewrite-with-placeholder` 按用户要求保留论证结构、标待补来源，不编出处。

## 编辑范围

默认做最小必要修改；中文公开长文约 1000 字以上默认保留句段结构。可指定：

程序代码块（包括注释和文档字符串）默认逐字保留；只有用户明确点名修改注释或说明文字时才编辑相应部分，且不改程序行为。代码围栏里的普通文案仍可按用户要求编辑。

- `structural`：允许删、并、重排，保留有效信息与作者意图。
- `bounded`：不直接删整句、不并句、不重排；纯空句列“建议删除（待确认）”，正文暂保留。
- `in-place`：不删句、不并句、不重排，只在句内替换或删修饰；要求保句数时也不拆句。

这些范围不会因编辑力度或来源处理方式而放宽。需要进一步判断时，查 `editing-guide.md`；需要看改写对照时，查 `examples.md`。
