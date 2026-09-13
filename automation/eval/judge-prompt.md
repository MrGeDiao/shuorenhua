# 判分输出协议

v2.5 依据 [编辑质量判据](../../evals/v2.5/criteria.md)，对照冻结的原文、用户请求和完整实际输出分别判断；不要求模型复述 skill 流程，不从旧风格预期推导硬失败。

使用 `shuorenhua-judge-v1`：

```json
{"cases":[{"id":"B-01","fidelity":"pass","task":"pass","quality":"same","evidence":"引用原文与输出，说明对应关系"}]}
```

- `fidelity`、`task`：`pass / fail / review`。
- `quality`：`better / same / worse / review`，相对原文判断阅读收益。
- `evidence`：逐题给依据。失败要指出具体丢失、改变或越界；存在合理不同解释时用 `review`。

不重新改写，不输出自己算的总分。解析器按期望 ID 校验，汇总由逐题结果计算。判官须先做参考案例校准；它的结论保留为原判，负责整合者另存复核，不能覆盖原判或把模型多数票当成人类共识。

实际提示由 [runner.py](runner.py) 的 `build_prompt` 生成。发布门槛在判据中，CLI 的 `complete` 只表示本次运行覆盖与身份校验完整。
