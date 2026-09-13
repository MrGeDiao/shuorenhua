# 改写示例

> 本文件是解释、示例与操作细则；行为合同的单源是 `SKILL.md`，两处表述不一致时以 `SKILL.md` 为准。

> 每个示例展示同一段内容的 AI 版和人话版。人话版里的每个事实都能在 AI 版里找到；示例示范的是拎出被包装埋掉的信息，不示范补材料。

## 中文示例

### 示例 1：项目介绍

**AI 版：**
> 该项目是一个创新性的解决方案，旨在通过深度整合语音识别与自动翻译等前沿技术，为用户提供全方位、一站式的智能化字幕体验，用户说中文即可直接生成英文字幕。上线两周以来，日活已达 1200，翻译准确率高达 94%，不仅能够显著提升工作效率，还能有效降低运营成本，实现真正的降本增效。

**人话版：**
> 这个项目把语音识别和自动翻译接到一起，用户说中文就能直接出英文字幕。上线两周日活 1200，翻译准确率 94%。

**改了什么：**
- 删掉"创新性""前沿技术""全方位""一站式""智能化"——全是空词
- 删掉"不仅…还能…"的二元结构；"提升效率 / 降低成本 / 降本增效"是没有任何依据的效果宣称，剥掉包装后没有剩余命题，所以整个删
- 功能描述和两个数字都是原文本来就有的，只是被包装埋住了，把它们拎出来直接说

---

### 示例 2：技术总结

**AI 版：**
> 综上所述，通过对系统架构的全面优化和持续迭代，我们在性能（API 响应时间由 800ms 优化至 120ms）、安全性（修复 3 个 SQL 注入漏洞）和可维护性（6000 行的 God Class 已拆分为 12 个模块）等方面均取得了显著提升。这一成果充分体现了团队在技术创新方面的不懈追求和卓越实力。

**人话版：**
> 这轮改完之后：API 响应时间从 800ms 降到 120ms，修了 3 个 SQL 注入漏洞，把 6000 行的 God Class 拆成了 12 个模块。

**改了什么：**
- 删掉"综上所述"和整个总结式开头
- 三项改动原文都写在括号里，把它们从"显著提升"的壳里拎出来当正文，壳本身删掉
- 删掉"充分体现""不懈追求""卓越实力"——自吹自擂

---

### 示例 3：消息回复

**AI 版：**
> 好问题！这确实是一个值得深入探讨的话题。让我来为你详细解释一下。首先，我们需要了解的是，这个问题的本质在于缓存失效策略：用户更新头像后 CDN 仍返回旧文件，TTL 设置为 7 天过长，建议调整为 1 小时。

**人话版：**
> 核心原因是缓存没失效。用户改了头像但 CDN 还在用旧的，TTL 设了 7 天太长了。改成 1 小时就行。

**改了什么：**
- 删掉全部谄媚和铺垫
- 直接给原因和解决方案

---

### 示例 4：新闻摘要

**AI 版：**
> 在当今快速发展的人工智能领域，某实验室近日发布了其最新的大语言模型 X-2，引发了业界的广泛关注和热烈讨论。该模型 MMLU 跑分达到 92.3%，较上一代高出 7 个点，上下文窗口翻倍至 256K，API 价格维持不变，在多个关键指标上实现了显著突破，标志着人工智能技术迈入了一个全新的发展阶段。

**人话版：**
> 某实验室发了新模型 X-2。MMLU 跑分 92.3%，比上一代高 7 个点。上下文窗口翻倍到 256K。API 价格没涨。

**改了什么：**
- 删掉"在当今""快速发展""广泛关注""热烈讨论"——全是废话
- 四项指标原文都写了，只是被"在多个关键指标上实现了显著突破"这句概括压住，删掉概括让指标自己说话
- "全新的发展阶段"删掉——读者自己会判断

---

### 示例 5：工程师腔 / 调试腔

**AI 版：**
> 我先拆开看了一下，发现根因偏硬，不太好直接打掉。目前已经把差异收窄了，和刚抓到的现象也对上了。接下来稳稳兜住，落盘之后就能收口。

**人话版：**
> 查了一下，原因是配置写死了，不能直接改。我把排查范围缩小到两个可能的地方，和之前的报错信息对得上。先把结论记下来，回头改一版就行。

**改了什么：**
- "拆开看"→"查了一下"，"根因偏硬"→"原因是配置写死了"
- "打掉"→"改"，"收窄"→"缩小"，"抓到的现象"→"报错信息"
- "兜住"→删掉，"落盘"→"记下来"，"收口"→"就行"
- 整段从 postmortem 腔调改成正常同事对话

---

### 示例 6：小红书 AI 腔

**AI 版：**
> 姐妹们！今天给大家拆解一个保姆级避坑攻略！Raycast 真的绝绝子，免费版就够用，启动快插件多，从 Alfred 切过来之后，每天切窗口查文档狠狠省下十几分钟！建议收藏！划重点：免费！

**人话版：**
> 推荐一个工具：Raycast。免费版就够用，主要是启动快、插件多。我之前用 Alfred，切过来之后每天大概能省十几分钟，主要省在切窗口和查文档上。

**改了什么：**
- 删掉全部硬凹人设的网络语
- "拆解""保姆级""避坑""绝绝子""狠狠""建议收藏""划重点"全删
- 工具名、用法和省下的时间原文都有，去掉网感包装后按正常语序说一遍

---

### 示例 7：语域混搭

**AI 版：**
> 诚然，这个 bug 的修复确实存在一定的技术复杂度，牵涉到三个服务之间的调用顺序。不过说白了就是绝绝子的体验！我们需要进一步深入探讨其底层逻辑，先把支付服务的超时时间从 3 秒调到 10 秒，稳稳把核心链路兜住，观察一周。综上所述，未来可期。

**人话版：**
> 这个 bug 不好修，涉及到三个服务之间的调用顺序。我先把支付服务的超时时间从 3 秒调到 10 秒，观察一周再说。

**改了什么：**
- 原文混搭了 5 种语域（学术/网络/商业/工程/鸡汤），统一成技术口语
- 调用顺序、超时改动和观察周期原文都有，剥掉五种语域的包装后按事情本来的顺序排一遍

---

## English Examples

### Example 1: Product description

**AI version:**
> Our groundbreaking platform serves as a testament to the transformative potential of AI, empowering teams to navigate complex challenges by auto-assigning each ticket to whoever fixed similar bugs before, and unlocking unprecedented levels of productivity — teams using it close issues 2 days faster on average. Nestled at the intersection of innovation and practicality, it showcases how cutting-edge technology can foster meaningful collaboration.

**Human version:**
> The platform auto-assigns tickets based on who fixed similar bugs before. Teams using it close issues 2 days faster on average.

**What changed:**
- Removed "groundbreaking", "testament", "empowering", "navigate", "unprecedented", "nestled", "showcases", "cutting-edge", "foster"
- The routing rule and the 2-day figure were already in the original, buried inside those claims; the human version just states them on their own

---

### Example 2: Technical update

**AI version:**
> We're excited to announce a comprehensive update that significantly enhances performance by cutting cold start time by 60%, bolsters security by patching an injection vulnerability, and streamlines the developer experience by dropping the config from 200 lines to 40. This pivotal release underscores our commitment to delivering robust, scalable solutions. The upgrade guide is in the changelog.

**Human version:**
> This release cuts cold start time by 60%, patches an injection vulnerability, and drops the config from 200 lines to 40. Upgrade guide is in the changelog.

**What changed:**
- Dropped the "comprehensive update / significantly enhances / bolsters / streamlines" wrappers; the three changes they wrapped were already spelled out in the original
- Deleted "pivotal", "underscores", "commitment", "robust", "scalable"
- The original names no CVE id, so the rewrite doesn't add one

---

### Example 3: Analysis (two-pass demo)

**AI version:**
> The landscape of remote work has undergone a profound transformation. It's not just about working from home — it's about reimagining the very fabric of how we collaborate. Companies that fail to navigate this paradigm shift risk being left behind in an increasingly competitive ecosystem.

**First pass:**
> Remote work changed how teams collaborate. The teams that leaned into async communication and cut meetings adapted faster.

**Audit — what still feels AI?**
- "changed how teams collaborate" is still broad
- "adapted faster" is vague and a bit polished

**Final:**
> Remote work changed how teams collaborated, but not every company adjusted in the same way. Some changed how they communicated and worked together. Others just kept the same habits in a different setting.

**What changed in second pass:**
- Replaced the broad opener with a clearer contrast that stays inside the original claim
- Removed the vague "adapted faster"
- Broke the rhythm a bit without inventing new facts

---

## Two-pass examples | Residual Audit

### 示例 A：公开写作里的一遍 vs 两遍

**原文：**
> 这次把 onboarding 流程改了一遍，新用户从注册到完成首次导入少走了两步。更重要的是，这也说明我们开始真正理解用户在第一天最容易卡住的地方。

**第一遍：**
> 这次把 onboarding 流程改了一遍，新用户从注册到完成首次导入少走了两步。我们也更清楚用户第一天最容易卡在哪里。

**第二遍：**
> 这次把 onboarding 流程改了一遍，新用户从注册到完成首次导入少走了两步。用户第一天最容易卡的地方，就是首次导入。

**第二遍改了什么：**
- 去掉了 `更重要的是 / 这也说明我们开始真正理解` 这层 narrator 话术
- 保留原文已有判断，只把它压回更直接的句子
- 没有补新事实，也没有重写整段

### 示例 B：status 场景里的克制 second pass

**原文：**
> 4 月 13 日把重试次数从 2 次调到 5 次。支付超时从 1.9% 降到 0.7%。这次调整也进一步验证了我们的优化方向是正确的。明天继续看晚高峰数据。

**第一遍：**
> 4 月 13 日把重试次数从 2 次调到 5 次后，支付超时从 1.9% 降到 0.7%。这次调整说明方向是对的。明天继续看晚高峰数据。

**第二遍：**
> 4 月 13 日把重试次数从 2 次调到 5 次后，支付超时从 1.9% 降到 0.7%。明天继续看晚高峰数据。

**第二遍改了什么：**
- 只删掉 `方向是对的` 这种空判断
- 保留日期、数字和下一步，不往更口语的方向抛光
- `status` 场景如果第一遍已经够直接，第二遍就到这里停

---

## Bounded 双合同示例 | Bounded Scope Example

> bounded 的输出分两部分：句内洗过的正文，和一份交用户确认的删除清单。示例（合成文本）：

**原文**

> 在数字化浪潮席卷各行各业的今天，提效工具层出不穷。我们团队过去三个月把周报流程从手填 Excel 改成了机器人自动汇总，每周大约省出两小时。研究表明，重复性事务的自动化能显著提升组织效能。具体做法是：机器人每周五拉取任务系统的状态变更，生成草稿，负责人只补一句风险说明。这不仅仅是一次流程优化，更是一种工作方式的革新。下个月我们准备把例会纪要也接进来。

**正文（句内洗后）**

> 提效工具很多。我们团队过去三个月把周报流程从手填 Excel 改成了机器人自动汇总，每周大约省出两小时。具体做法是：机器人每周五拉取任务系统的状态变更，生成草稿，负责人只补一句风险说明。下个月我们准备把例会纪要也接进来。

**建议删除（待确认）**

1. 「研究表明，重复性事务的自动化能显著提升组织效能。」——无源权威铺垫；删掉后该段信息点不变（前后句已经给出做法和收益），也不承担过渡。不建议改写成「听说 / 据说」，那只是把无源说法换个壳。
2. 「这不仅仅是一次流程优化，更是一种工作方式的革新。」——价值拔高收尾；剥掉句式后没有剩余信息，前句（具体做法）和后句（下月计划）直接相接不断裂。

第一句「在数字化浪潮……层出不穷」没有进清单：剥掉铺垫后还剩「提效工具很多」这个实质判断，所以走句内洗，不删整句。

---

## 标注模式示例 | Annotation Mode Examples

> 下面这几组展示同一段文本在 `annotation mode` 和默认改写模式下的区别。

### 示例 A：公开文案里的无源引用

**原文：**
> 我们组今年用 AI 协作开发后，需求交付周期从两周缩到一周。研究表明，采用 AI 协作开发的团队交付效率显著提升。业内人士认为，这一趋势将在未来十年持续加速。

**Annotation mode：**
- `问题族`：无源引用
- `触发点`：`研究表明`、`业内人士认为`
- `建议动作`：补具体来源；如果没有来源，删掉权威铺垫
- `是否建议改写`：是

**默认改写：**
> 我们组今年用 AI 协作开发后，需求交付周期从两周缩到一周。

### 示例 B：status 场景里的保守处理

**原文：**
> 数据显示，这次改版显著提升了留存率。业内人士认为，这个方向已经验证可行。

**Annotation mode：**
- `问题族`：无源引用
- `触发点`：`数据显示`、`业内人士认为`
- `建议动作`：在 `status` 场景优先补数据来源和归属，不要改写成像已证实的事实
- `是否建议改写`：是

**默认改写：**
> 这段缺数据来源和观点归属。作为 status，同步时应补具体报表、时间范围或负责人；在补齐之前，不建议把它写成已经证实的结论。

### 示例 C：抽象观点撑成长段（材料不足）

**原文：**
> 语音输入正在成为越来越重要的交互方式。它的价值不仅在于输入效率的提升，更在于它重新定义了人与设备之间的关系。随着技术不断成熟，这一趋势将在更多场景中得到验证，并最终重塑我们的表达习惯。

**Annotation mode：**
- `问题族`：材料不足 + 价值拔高骨架
- `触发点`：`不仅在于……更在于`、`重新定义`、`重塑我们的表达习惯`；删掉拔高与预测后，全段只剩「语音输入用的人变多了」一句
- `建议动作`：清掉拔高和预测。同时说明这段缺的是材料不是措辞——没有产品、数字、使用过程或具体场景，改完长度会掉到原文两成左右；要恢复原来的篇幅得补材料，不是换说法
- `是否建议改写`：是

**默认改写：**
> 语音输入用的人越来越多。

（默认模式只交改写结果。原文其余部分是拔高和预测，没有可依托的事实，清理后长度明显下降是正常的，不靠换说法填回去。）

### 示例 D：技术文档里的不改案例

**原文：**
> 网关在请求超时后返回 504。缓存服务每 5 分钟刷新一次热点 key。负载均衡器将流量按权重分配到三个后端节点。

**Annotation mode：**
- `问题族`：无明显问题
- `触发点`：系统主语和技术术语都属于正常文档写法
- `建议动作`：保持不动
- `是否建议改写`：否

**默认改写：**
> 网关在请求超时后返回 504。缓存服务每 5 分钟刷新一次热点 key。负载均衡器将流量按权重分配到三个后端节点。
