# 评测集 | Benchmark

> 用于验证 说人话 规则的稳定性：该改的要改，不该改的不能误杀。

## 使用方法

将本文件中的测试文本交给 AI 工具，要求"按 说人话 规则改写"，然后对比输出是否符合预期。

## 覆盖矩阵

说明：

- `short`：单段、单轮、短文本
- `long`：长段落或多句连续文本
- `mixed`：带引用、对话、上下文依赖，或同段混合多类病灶
- `code-context`：代码注释、docstring、commit message 等代码编辑器场景

| 场景 | short | long | mixed | code-context |
|------|-------|------|-------|-------------|
| chat | SF-01, SF-06, SF-11, SF-17, SF-29, SNF-07, SNF-11 | - | SF-19, SNF-16 | - |
| status | SF-02, SF-09, SF-15, SF-21, SF-25, SF-30, SNF-03, SNF-06, SNF-10, SNF-13, SNF-19, SNF-21 | - | - | SF-23, SNF-18 |
| docs | SF-04, SF-07, SF-26, SNF-01, SNF-02, SNF-04, SNF-05, SNF-08, SNF-09, SNF-14, SNF-20 | SF-18, SNF-15 | - | SF-22, SF-24, SF-27, SNF-17 |
| public-writing | SF-03, SF-05, SF-08, SF-10, SF-12, SF-13, SF-16, SF-20, SF-28, SNF-12 | - | SF-14 | - |

---

## 第一部分：该改的（Should Fix）

### A. Short

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

### SF-11 | chat | 工程师腔 / 调试腔
> 我已经把差异收窄了，根因基本坐实，和我刚抓到的现象对上了。接下来做一个更硬的排除法，稳稳把问题兜住，落盘之后就能收口了。

**预期**：删掉全部调试腔黑话。"收窄"→"缩小了"，"根因"→"原因"，"坐实"→"确认了"，"对上了"→"一致"，"更硬的排除法"→"再排查一遍"，"兜住"→"解决"，"落盘"→"记下来"，"收口"→"结束"。用正常人说话的方式复述同一件事。

### SF-12 | public-writing | 小红书 AI 腔
> 姐妹们！今天给大家拆解一个保姆级干货！真的绝绝子！谁懂啊，这个工具狠狠提升了我的效率！强烈建议收藏！划重点：避坑指南在最后！

**预期**：删掉"姐妹们""拆解""保姆级""干货""绝绝子""谁懂啊""狠狠""强烈建议收藏""划重点""避坑"。用正常语气说清楚工具是什么、好在哪。

### SF-13 | public-writing | 正能量收尾 + 鸡汤
> 诚然，AI 技术仍面临诸多挑战。但与其抗拒变化，不如积极拥抱这个充满无限可能的时代。只有不断学习、勇于创新，才能在未来的浪潮中乘风破浪。让我们拭目以待！

**预期**：删掉整段或改成具体观点。"诚然"删掉。"与其…不如…"鸡汤结构删掉。"只有…才能…"删掉。"乘风破浪""拭目以待"删掉。如果要保留，说清楚具体挑战是什么、具体该学什么。

### SF-14 | chat | 语域混搭
> 诚然，这个 feature 的实现确实存在一定的技术复杂度。不过说白了就是绝绝子！我们需要进一步深入探讨其底层逻辑，稳稳把核心链路兜住。综上所述，建议收藏。

**预期**：这段话混搭了学术腔（"诚然""进一步深入探讨"）、网络语（"绝绝子"）、商业黑话（"底层逻辑""链路"）、工程师腔（"兜住"）、自媒体腔（"建议收藏"），应全部统一为一种语域。用正常口语重写。

### SF-15 | status | 句长均匀（节奏单调）
> 本次更新优化了系统的整体性能。我们改进了数据库的查询效率。前端页面的加载速度得到了提升。用户反馈的体验问题已经得到解决。后续将持续关注系统的稳定性。

**预期**：五句话长度几乎一样（14-16字），节奏单调。改写时应长短句交替，合并或拆分句子，制造呼吸感。例如："数据库查询快了 3 倍。前端加载也从 2 秒降到 0.4 秒，用户之前反馈的卡顿问题顺带解了。"

### SF-16 | public-writing | 基础中文套话骨架
> 真正的竞争力不是功能堆砌，而是体验细节。最后比拼的是执行效率。归根结底，关键在于团队协同。

**预期**：至少命中四类基础套路并重写："真正的 X 不是……而是……"、"最后比拼的是……"、"归根结底"、"关键在于……"。改写后应直接陈述判断，不保留原骨架。

### SF-17 | chat | 模式变体归并
> 我先把问题扒开，现象也拽出来了。再补一刀，把这轮链路锁住，基本就闭环了。

**预期**：即使 `扒开 / 拽出来` 不在主词表的代表项里，也应按现有“庸医问诊腔 / 暴力动作腔 / 调试腔”处理，删掉姿态层，直接说清楚发现了什么、接下来要怎么改。

### B. Long

### SF-18 | docs | 长段落混合病灶
> 这次改造不是一次简单的配置调整，而是一套面向未来的系统性升级。研究表明，采用这一策略的团队在稳定性和交付效率上都能取得显著提升。我们通过对网关、缓存层和任务队列进行全链路治理，最终把整体质量稳稳兜住。综上所述，这次升级为后续扩展奠定了坚实基础。

**预期**：去掉 `不是……而是……` 骨架，处理无源引用，删掉 `系统性升级 / 全链路治理 / 稳稳兜住 / 奠定坚实基础` 这类姿态层，改回具体动作和结果。不能编造不存在的数据或研究来源。

### C. Mixed

### SF-19 | chat | 带上下文的引用式改写
> 用户：这段发布说明太像 AI 写的，帮我只改引号里的正文，不要改我的话。<br>
> 原文："结论先说，这次升级不是一次常规修复，而是对核心链路的系统性重塑。我们先把历史包袱扒开，再补一刀，把关键体验稳稳兜住。最终，产品体验完成了质的跃迁。"

**预期**：只处理引号里的正文，不改用户指令本身；删掉 `结论先说`、二元对比骨架、`扒开 / 补一刀 / 稳稳兜住` 等姿态词和 `质的跃迁` 这类拔高表达，改成正常发布说明语气。

### D. Code Context

### SF-22 | docs | docstring 里的 AI 腔
> ```python
> def refresh_cache(self):
>     """通过全面优化缓存刷新策略，显著提升系统整体性能，为用户提供更加流畅、高效的使用体验。"""
>     self.cache.clear()
>     self.cache.load()
> ```

**预期**：只改 docstring 正文，不动代码。删掉"全面优化""显著提升""整体性能""更加流畅、高效的使用体验"，改成描述函数实际行为的说明，例如"清空并重新加载缓存"。

### SF-23 | status | commit message 里的 AI 腔
> ```
> feat: 打造全新缓存方案，赋能高并发场景，实现降本增效闭环，显著提升系统整体性能与用户体验
> ```

**预期**：删掉"打造""赋能""降本增效""闭环""显著提升"，改成说清楚做了什么，例如 `feat: 缓存从本地 LRU 换成 Redis，支撑 10k QPS`。

### SF-24 | docs (English) | Code comment with AI slop
> ```javascript
> // This groundbreaking utility serves as a testament to modern engineering,
> // leveraging cutting-edge algorithms to deliver unprecedented performance.
> function sort(arr) { return arr.sort((a, b) => a - b); }
> ```

**Expected**: Only fix the comment, not the code. Remove "groundbreaking", "serves as a testament", "leveraging", "cutting-edge", "unprecedented". Replace with what the function actually does, e.g. `// Sort array ascending`.

### E. Unsourced Citation Focus

### SF-20 | public-writing (English) | Unsourced authority claim
> Studies show that teams using AI pair programming ship features 40% faster. Experts say this shift will redefine software delivery over the next decade.

**Expected**: For `public-writing`, prefer `rewrite-safe`: remove `Studies show` / `Experts say` unless a real source is available, and do not invent a study, expert group, or statistic. If the model only flags the missing source without rewriting away the authority scaffold, count it as partial.

### SF-21 | status | 无源引用在保守场景里的处理
> 数据显示，这次改版显著提升了留存率。业内人士认为，这个方向已经验证可行，后续只要继续投入就能稳定放大收益。

**预期**：对 `status` 场景应优先走 `audit-only`：明确指出缺少数据来源和归属，而不是把这两句改写成像是已经证实的事实。不能编造图表、报表、分析师或外部来源。

### F. Fact Preservation Focus

### SF-25 | status | 指标、归属和时间点不能漂
> 截至 4 月 12 日，iOS 次日留存从 31.4% 涨到 34.1%，但这次修复不是一次简单 patch，而是对 onboarding 链路的系统性重塑。王宁今天会把漏掉的 `source=campaign` 维度补回去，明天下午 3 点前再同步一次结果。

**预期**：可以去掉 `不是一次简单 patch`、`系统性重塑` 这类姿态层，但必须保留 `4 月 12 日`、`iOS 次日留存`、`31.4%`、`34.1%`、`王宁`、`source=campaign`、`明天下午 3 点前`。不能把“今天会补回去”改成“已经补回去了”。

### SF-26 | docs | 命令、报错、版本号和配置值保留
> 在 `v2.3.1` 中，运行 `bin/migrate --tenant=prod --dry-run` 后，如果日志出现 `schema mismatch on orders_v2`，说明迁移前置检查没有通过。不要试图通过“系统性治理”把问题稳稳兜住；先确认 `DB_SCHEMA_VERSION=20260412` 和线上一致，再继续。

**预期**：可以清掉 `系统性治理`、`稳稳兜住` 这类 AI 腔，但必须保留 `v2.3.1`、`bin/migrate --tenant=prod --dry-run`、`schema mismatch on orders_v2`、`DB_SCHEMA_VERSION=20260412` 原样。不能改命令、报错、配置值，也不能把“前置检查没有通过”写成别的错误类型。

### SF-27 | docs | code comment 里的 fact-bearing spans
> ```go
> // 截至 2026-04-12，这个 fallback 逻辑已经把 504 从 3.8% 压到 0.6%，
> // 通过系统性治理稳稳兜住高峰期流量。
> // If `ENABLE_EDGE_CACHE=false`, keep header `x-cache-bypass: 1`.
> func handleRequest(req *Request) {}
> ```

**预期**：只改注释，不动代码；可以清掉 `系统性治理`、`稳稳兜住`，但必须保留 `2026-04-12`、`504`、`3.8%`、`0.6%`、`ENABLE_EDGE_CACHE=false`、`x-cache-bypass: 1`。不能把 header 名、配置值或比较关系写错。

### G. Residual Audit / Two-pass

### SF-28 | public-writing | narrator 残留需要第二遍收一下
> 这次把 onboarding 流程改了一遍，新用户从注册到完成首次导入少走了两步。更重要的是，这也说明我们开始真正理解用户在第一天最容易卡住的地方。

**预期**：第二遍应去掉 `更重要的是` 和 `这也说明我们开始真正理解` 这层 narrator 话术，只保留“少走两步”和“首次导入最容易卡住”这类原文已有信息。不要补新事实，不要把整段重写成另一套口气。

### SF-29 | chat | 开场残留 + 总结残留
> 直接说结论：问题不在鉴权，而在缓存键拼错了。改完这个以后，请求就能正常命中。总的来说，这次排查方向是对的。

**预期**：第二遍应删掉 `直接说结论` 和 `总的来说` 这类提示层，只保留直接结论和结果。不要把“缓存键拼错了”改成别的问题，也不要再补新的排查细节。

### SF-30 | status | 空泛判断残留，第二遍只轻改
> 4 月 13 日把重试次数从 2 次调到 5 次。支付超时从 1.9% 降到 0.7%。这次调整也进一步验证了我们的优化方向是正确的。明天继续看晚高峰数据。

**预期**：第二遍应删掉 `进一步验证了我们的优化方向是正确的` 这种空判断，但必须保留 `4 月 13 日`、`2 次`、`5 次`、`1.9%`、`0.7%` 和“明天继续看晚高峰数据”。这是 `status` 场景，只做轻量收束，不要改成聊天腔。

---

## 第二部分：不该误杀的（Should NOT Fix）

### A. Short

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

### SNF-11 | chat | 真人工程师 debug 对话中合理使用技术术语
> 刚查了下，root cause 是连接池打满了，max_connections 才 20，高峰期不够用。我把它调到 100，观察了半小时，没再报错。

**理由**：真人工程师在 debug 讨论中使用"root cause""打满"等术语是自然的技术沟通，不是 AI 腔。关键区别：这段话有具体参数（20→100）、具体操作（观察半小时）和具体结果（没再报错），不是空泛的调试腔叙事。

### SNF-12 | public-writing | 真人博主正常使用网络用语
> 昨天踩了个大坑，Next.js 的 app router 在 production build 里 cache 行为和 dev 完全不一样，调了三小时。谁懂那种崩溃感啊。

**理由**：真人在具体经历后自然使用"踩坑""谁懂"，有具体技术细节（Next.js app router、cache 行为、三小时）作支撑，不是 AI 批量生成的空洞感叹。

### SNF-13 | status | 合理的语域一致（纯技术语域）
> 根因分析：OOM 触发了 pod 重启。内存泄漏点在 WebSocket 连接未释放。修复方案：idle 超过 30 分钟的连接自动断开。已上线验证，内存稳定在 512MB 以下。

**理由**：纯技术场景中"根因分析"是标准术语，语域全程一致（技术报告），有具体数据支撑，不需要改。

### SNF-14 | docs | 收词说明中的被讨论词
> 这一轮先不要把"扒开""拽出来""补一刀"逐个加进词表。它们更像现有模式的变体，先补 benchmark 和归并规则，再看要不要单独收录。

**理由**：这里是在讨论词条维护策略，不是在使用这些词制造 AI 腔。被讨论的词应保留原样。

### SNF-17 | docs | 正常的技术注释
> ```python
> # 缓存过期后回源查询，TTL 默认 300 秒
> # 如果 Redis 挂了，fallback 到本地 LRU cache
> def get_user(user_id: str) -> User:
>     ...
> ```

**理由**：正常的代码注释，有具体参数（TTL 300 秒）和具体降级策略（Redis → 本地 LRU），不是 AI 腔。

### SNF-18 | status | 正常的 commit message
> ```
> fix: 连接池上限从 20 调到 100，解决高峰期 504
> ```

**理由**：具体、事实性的 commit message，有数据（20→100）和问题（504），不需要改写。

### SNF-19 | status | 已经直接的事实同步
> 4 月 12 日把连接池上限从 20 调到 100 后，504 错误率从 3.8% 降到 0.6%。今天继续观察 24 小时，再决定是否全量。

**理由**：这段已经是直接的状态同步，重点全在时间、动作、数值和下一步上。即使 protected spans 很密，也不应该为了“更像人”再抛光一遍。

### SNF-20 | docs | 第二遍不该为了节奏改技术说明
> 在 `v2.4.0` 里，`retry_budget=0.2` 时默认开启指数退避；如果看到 `429 too many requests`，先把 `MAX_INFLIGHT=64` 调低再重试。

**理由**：这已经是直接的技术说明，版本号、参数和报错都承载事实。第二遍不该为了“节奏更自然”去改写这种命令式说明，也不能动这些受保护片段。

### SNF-21 | status | 已经够直接时，第二遍应该停手
> 4 月 14 日补回 `source=campaign` 维度后，Android 次日留存从 28.7% 修正到 30.1%。王宁今晚再核一次报表，明早 10 点同步最终数。

**理由**：这段已经把时间、动作、归属、数值和下一步说清楚了。第二遍不该再加口语化停顿、补解释句，或为了“更像人”改掉这种直接同步风格。

### B. Long

### SNF-15 | docs | 长段技术复盘中的工程术语
> 在 2026-03-20 的事故复盘里，我们确认 root cause 是连接池配置过小：`max_connections=20` 在峰值流量下被打满。修复动作包括把上限调到 100、给 `users` 表补复合索引、把慢查询指标接进告警。上线后观察 6 小时，错误率从 3.2% 降到 0.4%，没有再出现连接超时。

**理由**：这是证据充分的技术复盘，虽然包含 `root cause / 打满 / 指标 / 告警` 等工程语汇，但都承载了具体参数、动作和结果，不应为了“去 AI 味”而改平。

### C. Mixed

### SNF-16 | chat | 多轮讨论中引用待收录词
> A：这轮先别把“稳稳兜住”“补一刀”加进词表。<br>
> B：同意，这两个更像现有模式的变体。先补 benchmark，再看要不要进 `phrases-zh.md`。

**理由**：这是在讨论收词策略，不是在正文里表演姿态。即使出现了已标记词，也应因为“被讨论 / 被引用”而放行。

---

## 评测标准

| 类别 | 通过标准 |
|------|----------|
| Should Fix (SF) | 改写后命中项被消除，原意保留，不过度改写 |
| Should NOT Fix (SNF) | 文本保持原样或仅做最小调整，不误杀合理表达 |

- `code-context` 样本额外要求：只处理注释 / docstring / commit message 中的文字，不改动代码本身
- `fact-preservation` 样本额外要求：数字、日期、责任主体、引用、命令、代码、参数、路径、报错、指标和比较关系都必须保真；为了“更自然”补进原文没有的事实，一律记 `❌`
- `Residual Audit` 样本额外要求：第二遍只允许轻量修正；如果为了抛光而重写全文、补新事实，或把 `docs / status / code-context` 写得更口语，记 `❌`
- `必须改写`：能直接消除问题且不损失事实时，应输出改写结果
- `允许只标注风险`：遇到无源引用、缺上下文或不能安全补全事实的样本，允许明确指出风险并不给虚构改写；这种情况记为 `⚠️`，不直接算规则失效
- `mixed` 样本额外要求：只处理真正有问题的正文，不误改引用、用户指令、命令、字段名和被讨论词
- `无源引用类 SF` 额外口径：`public-writing / chat` 默认以删掉无证据权威铺垫为 `✅`；`docs / status` 默认以明确标注缺来源且不伪装成已证实为 `✅`；识别到问题但没有按场景默认动作处理，记 `⚠️`
- 无论场景，给无源引用补出不存在的研究名、机构、年份、专家或数据，一律记 `❌`

**整体通过率目标**：SF 通过率 > 90%，SNF 误杀率 < 10%。
