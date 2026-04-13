# v1.7 Todo

> 目标：让改写结果更像真人表达，不只是删套话。

## 已完成（v1.7.0 已发布）

- [x] Positive Style Contract — `references/positive-style.md`
- [x] Protected Spans — `references/protected-spans.md`
- [x] 4 条 fact-preservation benchmark（SF-25、SF-26、SF-27、SNF-19）
- [x] `SKILL.md` 执行顺序改为先划 protected spans 再改写
- [x] `scene-guardrails.md` 接入 Protected Spans
- [x] README 同步、CHANGELOG 记录
- [x] 打 tag v1.7.0

## 待开发（v1.7.1 — 二次审稿）

- [ ] 把回读拆成两步：保真回读 + 残留味回读
- [ ] 残留味回读只查：开场残留、总结残留、narrator 残留、空泛判断残留、句长过匀
- [ ] 第二遍只做轻量修正，不重写全文
- [ ] `docs / status` 第二遍默认更保守
- [ ] 新增 3 条 benchmark（第二遍应该帮忙）
- [ ] 新增 2 条 benchmark（第二遍应该克制）
- [ ] 补 2 组 before/after 示例
- [ ] 同步 SKILL.md、operation-manual.md、examples.md、CHANGELOG.md

## 待开发（v1.7.2 — 真实样本评测）

- [ ] 创建 `evals/real-samples.md`
- [ ] 首批 8-12 条真实样本
- [ ] 评分维度：自然 / 保真 / 可直接发（5 分制）
- [ ] 挑 5+ 条可复用为展示素材

## 待开发（v1.7.3 — 入口打通）

- [ ] install 文档统一 lite vs full 说明
- [ ] `.github/ISSUE_TEMPLATE/bad-case.md`
- [ ] pinned issue 征集 bad cases
- [ ] 真实样本扩到 20+ 条

## 延后到 v1.8+

- Voice Calibration Lite
- Scene Packs（README / release-note / forum-post / issue-reply）
- 结构化输出 schema
