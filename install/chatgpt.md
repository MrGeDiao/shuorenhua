# ChatGPT / 通用 LLM 安装

## ChatGPT

1. 打开 ChatGPT Settings > Personalization > Custom Instructions
2. 将 `SKILL.md` 的内容粘贴到 "How would you like ChatGPT to respond?" 中
3. 保存

## Claude (Web / API)

1. 创建一个 Project
2. 将 `SKILL.md` 内容添加到 Project Instructions
3. 如果需要完整词表，将 `references/` 下的文件也加到 Project Knowledge

## API / System Prompt

将 `SKILL.md` 内容作为 system prompt 的一部分传入：

```python
messages = [
    {"role": "system", "content": open("SKILL.md").read()},
    {"role": "user", "content": "改写以下文本：..."}
]
```

## 注意

受 token 限制，通用 LLM 可能无法一次加载全部参考文件。建议只加载 `SKILL.md`（核心规则自包含），需要深度改写时再手动引用具体的 `references/` 文件。
