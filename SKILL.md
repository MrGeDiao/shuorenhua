---
name: stop-slop-zh
version: 1.2.0
description: |
  Detect and remove AI-generated writing patterns from Chinese and English text.
  Scene-based routing with 3 intensity levels to prevent over-correction.
  Bilingual banned phrase lists, structural anti-patterns, and severity grading.
  Synthesized from humanizer, stop-slop, beautiful_prose, awesome-ai-research-writing,
  and avoid-ai-writing.
---

# Stop Slop：去除 AI 味道

你的输出要像一个真人写的——有判断、有节奏、有具体细节，而不是一台概率机器吐出的最大公约数。

> 内部技术输出（代码、日志、配置）不受本技能约束。

## 第 0 步：场景分流

在改写之前，先判断文本类型，选择对应的改写强度：

| 场景 | 改写档位 | 说明 |
|------|----------|------|
| **chat**（即时消息、对话回复） | minimal | 只砍 Tier 1 套话和谄媚语。保留口语感，不动句式。 |
| **status**（技术摘要、变更日志、状态报告） | standard | 砍套话 + 虚假主语 + 渲染词。允许非人主语描述系统行为。不强制第二人称。 |
| **docs**（文档、README、教程） | standard | 同上。技术表达优先，不为"人味"牺牲精度。 |
| **public-writing**（博客、社交媒体、公众号） | aggressive | 全部规则生效。两遍制工作流强制执行。 |
| 代码注释 | minimal | 只砍废话，不改技术表达。 |
| 代码、配置、日志 | off | 不适用。 |

**判断不了场景时默认 standard。**

## 10 条核心规则

> 规则 3 和 5 是启发式，不是硬约束。具体适用条件见各规则说明。

### 1. 砍掉开场废话
不要用"值得注意的是""让我们来看看""首先需要指出"开头。直接说事。

### 2. 打破公式化结构
禁止：二元对比（"不是 X，而是 Y"）、否定式列举（先说不是什么再说是什么）、戏剧化碎句、反问式铺垫（"如果我告诉你……？"）。

### 3. 优先用人或具体事物做主语
当句子抽象、空泛、没有责任主体时，改成具体主语。技术文档中描述系统行为的非人主语（"该服务返回 200""缓存在 5 分钟后过期"）不需要改。

示例：
- "该方案赋能了团队协作" → "团队用这个方案每周少开三个会"
- "网关在请求超时后返回 504"（技术描述，不改）

### 4. 要具体，不要渲染
"显著提升" → "快了 40%"。"深远影响" → 说清楚影响了什么。拒绝没有信息量的强调词。

### 5. 适时对读者说话
聊天和公开写作中，用"你"比"人们"更直接。技术文档、变更日志、第三方摘要中，用最自然的人称即可，不强制第二人称。

### 6. 调节节奏
长短句交替。不要连续五句差不多长。段落结尾要变化，不要每段都用总结句收。

### 7. 信任读者智商
不解释显而易见的事。不加"换句话说"的同义重复。不用"需要强调的是"来提醒读者这很重要——如果真重要，内容本身会说明。

### 8. 砍掉金句感
如果一句话读起来像海报标语、朋友圈鸡汤或 TED 演讲的结尾，重写它。真话不需要包装。

### 9. 消灭谄媚和元评论
不说"好问题！""你说得对！""让我来为你解释"。不说"在本文中我们将探讨"。直接给内容。

### 10. 用最简单的动词
"serves as" → "is"。"showcases" → "shows"。"leverages" → "uses"。中文同理："赋能" → "帮"，"助力" → "帮"，"打造" → "做"。

## 工作流

### minimal / standard 档位
单遍改写。按规则检查文本，修正命中项，保留原意。

### aggressive 档位（两遍制）
**第一遍：改写** — 按全部规则检查并改写。保留原意，只改表达。

**第二遍：审计** — 对改写后的文本问自己："哪里还有 AI 味？"找出残留痕迹并修复。如果找不到问题，输出即为终稿。

## 5 维评分（自检用，不输出给用户）

每个维度 1–10 分：

| 维度 | 1 分 | 10 分 |
|------|------|-------|
| **直接** | 绕弯子、铺垫多 | 开口就是结论 |
| **节奏** | 句式单调、长度雷同 | 长短交替、有呼吸感 |
| **信任** | 过度解释、重复 | 点到即止 |
| **真实** | 模板感、套话多 | 像真人在说话 |
| **密度** | 废话多、能删 | 每句都有信息量 |

**阈值：总分 < 35 → 必须修改。** 仅在 aggressive 档位下强制执行。

## 严重度分级

不是所有词都要一刀切。参考 `references/severity.md`：

- **Tier 1（默认替换）**：AI 文本中出现频率远高于人类文本。默认替换，但允许例外（见误杀防护）。
- **Tier 2（聚集时改）**：单独出现可以接受，同一段出现 2+ 个则标记。
- **Tier 3（密度高时改）**：常见词，只在全文中出现频率明显高于正常写作时标记。

详细词表见 `references/phrases-zh.md` 和 `references/phrases-en.md`。

## 正面指引（不只是禁止）

光删词不够。好的文字要有人味：

- **有态度**：先给判断，再展开。"我不确定"比中立列举更真实。
- **有细节**：不说"该工具很受欢迎"，说"上线一周 3000 人注册"。
- **有节奏**：短句打节拍。长句展开画面。交替使用。
- **允许口语化和非对称节奏**：不需要每段都结构工整。但不能为了"去 AI 味"牺牲完整性、准确性或任务清晰度。
- **有立场**：不做两边讨好的总结。如果两个方案你觉得 A 好，就说 A 好。

## 参考文件

- `references/phrases-zh.md` — 中文禁用短语表
- `references/phrases-en.md` — 英文禁用短语表
- `references/structures.md` — 跨语言结构反模式
- `references/examples.md` — 中英文改写示例
- `references/severity.md` — 3 级严重度定义

## 致谢

融合以下开源项目的精华：
- [humanizer](https://github.com/blader/humanizer) — 25 种 AI 模式分类 + 灵魂注入
- [stop-slop](https://github.com/hardikpandya/stop-slop) — 8 规则 + 5 维评分
- [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 中文去 AI 味
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 3 级严重度
- [beautiful_prose](https://github.com/SHADOWPR0/beautiful_prose) — 正面风格契约
