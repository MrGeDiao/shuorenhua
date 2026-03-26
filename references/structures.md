# 结构反模式（跨语言）

> 这些模式不是某个词的问题，而是句子和段落层面的 AI 痕迹。中英文通用。

## 1. 二元对比假戏剧

**模式**：先否定 X，再肯定 Y，制造虚假的顿悟感。

```
❌ 这不是技术问题，而是管理问题。
❌ It's not about the code. It's about the culture.
```

```
✅ 管理流程比代码本身更容易出问题。
✅ The culture around code review matters more than the code itself.
```

## 2. 否定式列举

**模式**：先说不是什么，再说是什么。绕了一圈。

```
❌ 它不是框架，不是库，也不是工具——它是一种思维方式。
❌ It's not a framework. It's not a library. It's a way of thinking.
```

```
✅ 把它当作一种思维方式，不是一个具体工具。
✅ Think of it as a mental model, not a tool.
```

## 3. 戏剧化碎句

**模式**：用句子碎片制造假的力量感。

```
❌ 三年。两个人。一个想法。
❌ Three years. Two people. One idea.
```

```
✅ 两个人花了三年把这个想法做成了产品。
✅ Two people spent three years turning the idea into a product.
```

## 4. 反问式铺垫

**模式**：用反问或"如果"开头吊胃口。

```
❌ 如果我告诉你，90% 的创业公司都在犯同一个错误呢？
❌ What if I told you 90% of startups make the same mistake?
```

```
✅ 90% 的创业公司在定价上犯同一个错误：按成本定价而不是按价值定价。
✅ 90% of startups misprice their product, using cost-based pricing instead of value-based.
```

## 5. 虚假主语（False Agency）

**模式**：给无生命的事物安上人类动作（"赋能""助力""驱动"）。当句子抽象空泛、没有具体信息时优先改写。技术文档中描述系统行为的非人主语（"网关返回 504""缓存过期"）是合理的，不需要改。

```
❌ 该框架赋能了开发者社区。
❌ The framework empowers the developer community.
```

```
✅ 开发者用这个框架能少写 30% 的样板代码。
✅ Developers write 30% less boilerplate with this framework.
✅ 网关在超时后返回 504。（技术描述，不改）
```

## 6. 被动语态堆砌

**模式**：连续使用被动语态，隐藏动作执行者。研究论文、实验报告或正式学术摘要里的常规被动不一定要改。

```
❌ 系统被优化后，性能被显著提升，用户体验被大幅改善。
❌ The system was optimized, performance was improved, and user experience was enhanced.
```

```
✅ 我们优化了数据库查询，页面加载从 3 秒降到 0.8 秒。
✅ We optimized database queries and cut page load time from 3s to 0.8s.
```

```
✅ The experiment was conducted by researchers at MIT.（学术语体，可保留）
```

## 7. 三件套列举

**模式**：AI 偏爱三个一组。两个或一个往往更自然。

```
❌ 创新、协作、卓越。
❌ Innovation, collaboration, and excellence.
```

```
✅ 把东西做出来，做好。
✅ Build things. Build them well.
```

## 8. "首先…其次…最后…" 机械排列

**模式**：中文特有的机械递进，制造假的逻辑感。

```
❌ 首先，我们需要明确目标；其次，制定计划；最后，执行落地。
```

```
✅ 先把目标定清楚，然后排优先级，边做边调。
```

## 9. Wh- 开头句（英文特有）

**模式**：用 What/When/Where/Which/Who/Why/How 开头的句子在 AI 文本中过度集中。

```
❌ What makes this approach unique is its simplicity.
```

```
✅ This approach works because it's simple.
```

## 10. 总结式收尾

**模式**：每段或全文末尾用"总之""综上"做总结，重复已说过的内容。

```
❌ 综上所述，该方案在性能、安全性和可维护性方面都表现优异。
❌ In conclusion, this approach excels in performance, security, and maintainability.
```

```
✅ 删掉。前面说清楚了就不用再说一遍。
✅ Delete it. If you said it clearly above, don't repeat it.
```

## 11. 对称填充（Symmetry Padding）

**模式**：为了"平衡"而硬凑对仗，没有信息增量。

```
❌ 既要保证速度，又要保证质量；既要创新突破，又要稳定可靠。
```

```
✅ 速度和质量之间我们优先质量。
```

## 12. 无源引用

**模式**：用"研究表明""数据显示""专家指出"但不给具体来源，制造假的权威感。

```
❌ 研究表明，远程办公能提高 30% 的生产力。
❌ Studies show that remote work increases productivity by 30%.
```

```
✅ Stanford 2023 年的一项实验发现，全远程员工的代码提交量比混合办公多 13%。
✅ A 2023 Stanford experiment found fully remote employees committed 13% more code than hybrid workers.
```

## 13. 加粗滥用

**模式**：机械地给每个要点加粗，制造假的层次感。

```
❌ **用户体验：** 界面全面升级。**性能优化：** 算法显著提升。**安全加固：** 新增端到端加密。
```

```
✅ 界面重新设计了，算法快了 2 倍，加了端到端加密。
```

## 14. 分条列点强迫症

**模式**：任何内容都要 1. 2. 3. 分条，连简单回复也列点，制造假的条理感。

```
❌ 关于这个问题，我的建议如下：
   1. 先检查配置文件
   2. 确认环境变量
   3. 重启服务
```

```
✅ 配置文件里的 DB_HOST 可能写错了，先看一眼。不是的话重启一下服务试试。
```

## 15. 正能量收尾强迫症

**模式**：不管前面说了什么，最后一段必须上价值、给鸡汤、展望未来。

```
❌ ……总之，让我们拥抱变化，积极迎接 AI 时代的无限可能！未来可期！
```

```
✅ 删掉。前面说完了就结束。
```

## 16. 假口语化 / 硬凹网感

**模式**：AI 试图"接地气"时硬塞网络流行语（绝绝子、谁懂啊、真的会谢），反而更假。真人用这些词是随机的，AI 是批量的。

```
❌ 姐妹们！这个工具真的绝绝子！谁懂啊，效率直接拉满！狠狠心动了！
```

```
✅ 这个工具确实好用，主要是批量处理的速度快，省了不少时间。
```

## 17. 调试腔叙事

**模式**：AI 在编程场景中用 postmortem / SRE 口吻讲日常事务——"兜住""落盘""根因""收口"。把 debug 术语泛化到一切对话中。

```
❌ 我已经把差异收窄了，根因基本坐实，接下来做一个更硬的排除法把问题打掉。
```

```
✅ 原因找到了：是缓存过期导致的。我把可能性排查了一遍，现在就剩这一个。
```

## 18. 句长均匀（统计信号）

**模式**：AI 文本每句话长度几乎一样（句长标准差约 1.2，人类约 4.7+）。表现为"读起来很平，没有呼吸感"。

**检测**：不是看单个词，而是看整段的节奏是否单调。长短句应该交替出现。

## 19. 价值拔高骨架

**模式**：先给一个事实，再用 `不仅仅是……更是……`、`真正的 X 不是……而是……`、`最后比拼的是……` 把句子抬高成“洞见”。

```
❌ 这不仅仅是一个产品，更是一种信念的传承。
❌ 真正的竞争力不是功能堆砌，而是体验细节。最后比拼的是执行效率。
```

```
✅ 这就是一个产品判断：体验细节决定它能不能长期被用下去。
✅ 产品做得再多，最后还是看体验细节和执行效率。
```
