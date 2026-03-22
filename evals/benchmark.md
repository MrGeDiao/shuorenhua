# 评测集 | Benchmark

> 用于验证 stop-slop-zh 规则的稳定性：该改的要改，不该改的不能误杀。

## 使用方法

将本文件中的测试文本交给 AI 工具，要求"按 stop-slop-zh 规则改写"，然后对比输出是否符合预期。

---

## 第一部分：该改的（Should Fix）

### SF-01 | chat | 开场套话 + 谄媚
> 好问题！值得注意的是，这个问题的本质在于数据库索引策略。让我来为你详细解释一下。首先，我们需要了解的是……

**预期**：删掉"好问题""值得注意的是""让我来为你详细解释""首先我们需要了解的是"，直接给索引策略的答案。

### SF-02 | status | 渲染词堆砌
> 本次迭代在性能方面取得了显著提升，有效解决了长期困扰团队的延迟问题，充分体现了团队在技术创新领域的持续探索与不懈追求。

**预期**：给具体数据（延迟从 X 降到 Y），删掉"显著提升""有效解决""充分体现""持续探索""不懈追求"。

### SF-03 | public-writing | 互联网黑话
> 为了解决这一痛点，我们打造了一套全新的解决方案，旨在赋能开发者社区，助力企业实现降本增效的闭环。

**预期**："痛点"→"问题"，"打造"→"做了"，"赋能"→"帮"，"助力"→"帮"，"降本增效"→"省钱提速"，"闭环"→删掉或改成具体流程。

### SF-04 | docs | 二元对比 + 否定式列举
> 它不是一个框架，不是一个库，也不是一个工具——它是一种全新的开发范式。这不是简单的效率提升，而是对人机协作底层逻辑的根本性重构。

**预期**：去掉否定式列举和二元对比结构，直接说它是什么。"底层逻辑"→"原理"或删掉。

### SF-05 | public-writing | 无源引用
> 研究表明，采用微服务架构的团队生产力显著高于单体架构团队。业内人士认为，这一趋势将在未来五年内持续加速。

**预期**：给出具体研究名称/来源，或删掉"研究表明"直接给数据。"业内人士"说清楚是谁。

### SF-06 | chat | 总结式收尾 + 过渡废话
> 综上所述，总的来说，该方案在性能、安全性和可维护性方面都表现优异。简而言之，这是一个值得推荐的解决方案。希望这对你有帮助！

**预期**：整段删掉（前面已经说清楚了就不用再总结）。至少删掉"综上所述""总的来说""简而言之""希望这对你有帮助"。

### SF-07 | docs (English) | Copula avoidance + significance inflation
> The platform serves as a testament to the transformative potential of cloud-native architecture. It showcases how cutting-edge technology can foster seamless collaboration, underscoring its pivotal role in the evolving landscape of modern development.

**Expected**: "serves as a testament" → "shows", "showcases" → "shows", "cutting-edge" → "latest/modern", "foster" → "enable/help", "pivotal" → "important", "evolving landscape" → delete.

### SF-08 | public-writing | 戏剧化碎句 + 金句感
> 三年。两个团队。一个目标。当我们回头看这段旅程，每一步都充满了不可磨灭的意义。这不仅仅是一个产品，更是一种信念的传承。

**预期**：去掉碎句格式，改成正常叙述。删掉"不可磨灭""信念的传承"。去掉"不仅仅是…更是…"结构。

### SF-09 | status | 被动语态堆砌
> 系统被全面优化后，性能被显著提升，用户体验被大幅改善，安全性被进一步加强。

**预期**：改成主动语态，说清楚谁做了什么。给具体数据。

### SF-10 | public-writing (English) | Sycophantic + meta-commentary
> Great question! You're absolutely right that this is a fascinating topic. In this essay, we will explore the implications of AI-assisted coding. As we'll see, the landscape is evolving rapidly. Let's dive in!

**Expected**: Delete all of it. Start directly with the content about AI-assisted coding.

---

## 第二部分：不该误杀的（Should NOT Fix）

### SNF-01 | docs | 系统主语描述技术行为
> 网关在请求超时后返回 504。缓存服务每 5 分钟刷新一次热点 key。负载均衡器将流量按权重分配到三个后端节点。

**理由**：技术文档中系统/组件作为主语是合理的，不是虚假主语。

### SNF-02 | docs | 引用原文
> 根据 RFC 7231 的定义："The 200 (OK) status code indicates that the request has succeeded." 这意味着服务端已成功处理了请求。

**理由**：引用原文应保留原样，即使包含被标记的词汇。

### SNF-03 | status | 单独出现的 Tier 2 词
> 然而，这次升级引入了一个已知的兼容性问题，影响 iOS 14 以下的设备。

**理由**："然而"单独出现是合理的转折。只在同段聚集 2+ 个 Tier 2 词时才标记。

### SNF-04 | docs | 行业标准术语
> 该交易使用了 10 倍杠杆（leverage），通过做空期货合约对冲现货风险。

**理由**：金融领域的"杠杆"是标准术语，不应替换。

### SNF-05 | docs (English) | Technical use of flagged words
> The system navigates the network topology using Dijkstra's algorithm, traversing each node to find the shortest path.

**Reason**: "navigates" and "traversing" are literal technical descriptions of graph algorithms, not business jargon.

### SNF-06 | status | 变更日志中的简洁描述
> Fixed: API response time regression. Root cause: unindexed query on users table. Added composite index on (tenant_id, created_at).

**理由**：变更日志的简洁风格不需要改写，句式本身就是直接的。

### SNF-07 | chat | 正常的 Tier 3 低频使用
> 这个功能很重要，上线前一定要确保测试覆盖到位。

**理由**："重要""确保"是 Tier 3 词，低频使用完全正常。

### SNF-08 | docs | 讨论术语本身
> 什么是"赋能"？在互联网行业中，这个词通常被用来指代"提供工具或能力让他人能做之前做不到的事"。但由于过度使用，它已经失去了具体含义。

**理由**：当 Tier 1 词本身是讨论对象时，不应替换。

### SNF-09 | docs (English) | Appropriate passive voice
> The experiment was conducted by researchers at MIT. Results were published in Nature in 2024.

**Reason**: Academic passive voice is conventional and appropriate in research contexts.

### SNF-10 | status | 合理的非第二人称叙述
> 该团队在 Q1 完成了 3 个核心模块的重构，代码行数从 12000 行降到 4500 行。预计 Q2 完成剩余模块的迁移。

**理由**：status 报告用第三人称叙述团队工作是合理的，不应强制改成"你"。

---

## 评测标准

| 类别 | 通过标准 |
|------|----------|
| Should Fix (SF) | 改写后命中项被消除，原意保留，不过度改写 |
| Should NOT Fix (SNF) | 文本保持原样或仅做最小调整，不误杀合理表达 |

**整体通过率目标**：SF 命中率 > 90%，SNF 误杀率 < 10%。
