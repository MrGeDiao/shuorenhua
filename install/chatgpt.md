# ChatGPT / 通用 LLM 安装

## 先说结论

这类通用宿主最容易犯的错，是把这份 skill 当成“大词表”，一股脑全塞进 Custom Instructions 或 system prompt。

更稳的用法是：
- 默认只放 `SKILL.md`
- 真遇到复杂改写、误杀边界或重写争议，再补具体 `references/`

原因很简单：
- `SKILL.md` 已经负责主判断：场景、Tier、档位、禁改边界、输出合同
- `references/` 主要负责补细节，而不是每次都必须常驻上下文

---

## ChatGPT

1. 打开 ChatGPT Settings > Personalization > Custom Instructions
2. 将 `SKILL.md` 的内容粘贴到响应风格相关指令中
3. 保存

如果你只是偶尔使用，不一定要长期写进 Custom Instructions。直接在单次对话里贴一段说明，通常更省。

推荐指令写法：

```text
按“说人话”规则改写下面这段文本。先判断它是 chat、status、docs 还是 public-writing，再决定轻改、标准改还是重写。保留术语、系统主语和关键信息，不要为了自然把内容改空。
```

---

## Claude（Web / Project）

1. 创建一个 Project
2. 将 `SKILL.md` 内容添加到 Project Instructions
3. 如果需要更稳的误杀防护，再把相关 `references/` 文件加入 Project Knowledge

不建议默认把整个 `references/` 全量加入。更合理的是：
- 常驻：`SKILL.md`
- 按需补充：`phrases / structures / severity / operation-manual / boundary-cases`

---

## API / System Prompt

将 `SKILL.md` 作为 system prompt 的一部分传入：

```python
messages = [
    {"role": "system", "content": open("SKILL.md").read()},
    {"role": "user", "content": "改写以下文本：..."}
]
```

如果你已经有自己的主 system prompt，不要粗暴整段覆盖。更稳的是把“说人话”当成一个风格模块拼进去。

---

## 怎么判断该不该补 `references/`

### 只用 `SKILL.md` 就够

适合：
- 一般聊天改写
- 普通状态同步
- 轻度去模板感
- token 比较紧

### 需要补 `references/`

适合：
- AI 腔很重
- 中英文混合
- 技术文案里怕误杀术语
- 需要处理结构问题，不只是删词
- 需要判断某句到底该不该改

优先补这几类：
- `references/structures.md`
- `references/severity.md`
- `references/operation-manual.md`
- `references/boundary-cases.md`

---

## 一个更准确的理解方式

这份 skill 的核心不是“替换 200 个词”，而是：

1. 先判断场景
2. 再判断问题类型和严重度
3. 最后决定怎么改，以及哪些地方不能乱动

所以在通用 LLM 里，给清楚任务边界，往往比堆更多词表更重要。
