# 评测入口

v2.5 按 [编辑质量判据](v2.5/criteria.md)评估保真、任务和编辑收益。运行方法见 [automation/eval/README.md](../automation/eval/README.md)，中性请求见 [suite.json](v2.5/suite.json)。

改写模型只收到冻结规则、请求和原文；判分模型另收实际输出与判据。不要把 benchmark 的预期一并发给改写模型，也不要要求判定链、自评分或固定词语替换。

`benchmark.md`、`benchmark-tiers.md` 和旧结果保留历史含义；其中强制删某个句式的风格预期不自动算新版错误。静态阅读不等于盲测实跑，旧版通过不等于新候选通过。
