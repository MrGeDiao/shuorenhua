# ChatGPT / 通用 LLM 安装

默认只放 `SKILL.md`，不要一上来就把整个 `references/` 全塞进去。`SKILL.md` 已经负责主判断（场景、Tier、档位、禁改边界），`references/` 是按需补细节用的，不需要每次常驻。

## ChatGPT

1. 打开 ChatGPT Settings > Personalization > Custom Instructions
2. 将 `SKILL.md` 的内容粘贴到 "How would you like ChatGPT to respond?" 中
3. 保存

如果只是偶尔使用，不必写进 Custom Instructions，直接在对话里贴 `SKILL.md` 内容更灵活。

## Claude（Web / Project）

1. 创建一个 Project
2. 将 `SKILL.md` 内容添加到 Project Instructions
3. 需要更稳的误杀防护时，再把相关 `references/` 文件加入 Project Knowledge

## API / System Prompt

```python
messages = [
    {"role": "system", "content": open("SKILL.md").read()},
    {"role": "user", "content": "改写以下文本：..."}
]
```

如果已有主 system prompt，把 `SKILL.md` 当成一个风格模块拼进去，不要整段覆盖。

## 使用提示

如果你想先判断"哪里像 AI"，不要直接改稿，在对话里说：

```text
先不要改写，只按 annotation mode 标出下面这段文字里的问题：...
```

适合这几类场景：

- 你想先看这段话该不该改
- 你要做审稿或 review，不想直接替作者重写
- 你怀疑有无源引用、语域混搭或工程师腔，但还不想动正文

处理无源引用时，可以指定模式：

```text
用说人话规则改写这段文本，无源引用按 audit-only 处理。
```

三种模式：`rewrite-safe`（默认用于 chat/public-writing，直接删无证据权威铺垫）、`audit-only`（默认用于 docs/status，只标缺来源）、`rewrite-with-placeholder`（保留结构但暴露缺来源）。不指定时按场景默认值走。

## 什么时候需要补 `references/`

- AI 腔很重，普通去词表改写效果不够
- 中英文混合，需要精细场景判断
- 技术文案，担心误杀术语
- 需要处理结构问题，不只是删词

优先补：`structures.md` / `severity.md` / `operation-manual.md` / `boundary-cases.md`
