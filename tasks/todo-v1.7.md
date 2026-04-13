# v1.7 Todo — rewrite quality foundation

> Goal: improve "feels human" quality without sacrificing facts, terminology, or conservative technical scenes.

## Scope

This version does:

- define a stronger positive rewrite target
- strengthen protection for fact-bearing spans
- add a lightweight residual second pass
- introduce a real-sample eval pilot

This version does not need to do:

- full `Voice Calibration Lite`
- full sub-scene packs
- public launch work
- directory submissions
- automation that edits the repo

## Success criteria

- `SKILL.md` and `references/` can describe a clearer target than "remove slop"
- docs / status / code-context rewrites remain conservative
- at least one second-pass flow improves real samples without causing drift
- repo gains a reusable real-sample pack instead of relying only on synthetic benchmark

## Release train

Recommended split:

- `v1.7.0` — target definition + Positive Style Contract + Protected Spans
- `v1.7.1` — Residual Audit / Two-pass
- `v1.7.2` — Real Sample Eval pilot + release calibration
- `v1.7.3` — hardening pass for docs, intake, and sample expansion

Reason:

- `Positive Style Contract` and `Protected Spans` belong together because one raises style ambition and the other limits drift
- `Residual Audit` should land only after those two are stable
- `Real Sample Eval` is most useful after there is something new to judge
- the public-facing polish and intake loop should not block the first three releases

## Version breakdown

### v1.7.0 — rewrite target and safety rails

Goal:

- define what "more human" means and raise the safety floor before adding a second pass

Includes:

- `Phase 0 — framing and scoring`
- `Phase 1 — Positive Style Contract`
- `Phase 2 — Protected Spans`

Must ship:

- `references/positive-style.md`
- `references/protected-spans.md`
- benchmark additions for fact preservation
- synced `SKILL.md`, `README.md`, `CHANGELOG.md`

Does not ship:

- residual second pass
- real-sample pilot pack
- intake templates

Release gate:

- no new claim in README depends on unshipped second-pass or voice features
- at least 3 mixed or technical benchmark cases confirm fact preservation

### v1.7.1 — residual polish pass

Goal:

- reduce the "still feels a bit AI" residue after first-pass cleanup

Includes:

- `Phase 3 — Residual Audit`

Must ship:

- split reread into `fidelity` and `residual-slop`
- examples for pass-one vs pass-two
- 3 positive benchmark cases where pass two helps
- 2 conservative cases where pass two should mostly abstain

Does not ship:

- voice calibration
- scene packs
- public intake loop

Release gate:

- pass two improves at least 3 real or benchmark samples
- no obvious new drift in `docs / status / code-context`

### v1.7.2 — real-sample reality check

Goal:

- verify that the new rewrite behavior actually improves publishable output, not just rule-facing metrics

Includes:

- `Phase 4 — Real Sample Eval pilot`
- `Phase 5 — release review`

Must ship:

- `evals/real-samples.md` or `evals/real-samples/`
- first `8-12` samples
- scoring fields: `natural / fidelity / publishable`
- README wording calibrated to the new evidence

Does not ship:

- full bad-case intake workflow
- expanded scene matrix

Release gate:

- at least 5 pilot samples are strong enough to reuse as standing regression assets
- roadmap and README still separate shipped features from planned features

### v1.7.3 — hardening and intake

Goal:

- make the new `v1.7` foundation easier to use and easier to improve with outside feedback

Includes:

- `lite` vs `full` wording pass across install docs
- public bad-case intake template
- real-sample pack expansion beyond pilot

Must ship:

- install doc wording pass
- `.github/ISSUE_TEMPLATE/bad-case.md`
- at least one pinned issue or discussion draft
- expanded sample pack beyond the first pilot set

Release gate:

- users can tell when to use `lite` vs `full`
- outside contributors have a stable way to submit bad cases
- the sample pack starts becoming a reusable regression asset, not a one-off pilot

## Execution order

### Phase 0 — framing and scoring

- [ ] Define `v1.7` score dimensions for real samples: `natural / fidelity / publishable`
- [ ] Decide pilot sample count target: recommended `8-12`
- [ ] Decide release gate for new quality features
- [ ] Add `tasks/todo-v1.7.md` updates if scope changes

### Phase 1 — Positive Style Contract

- [ ] Add `references/positive-style.md`
- [ ] Pull current positive guidance out of `SKILL.md` and make it more explicit
- [ ] Add examples that compare:
  - cleaned but still AI-ish
  - cleaned and more human
- [ ] Sync `SKILL.md`
- [ ] Sync `README.md`
- [ ] Add changelog entry when shipped

### Phase 2 — Protected Spans

- [ ] Add `references/protected-spans.md`
- [ ] Define protected categories:
  - numbers and dates
  - names and quoted text
  - commands, code, params, fields, paths
  - errors and metric claims
- [ ] Add at least 3 benchmark cases that stress fact preservation
- [ ] Sync `scene-guardrails`, `SKILL.md`, `README.md`, `CHANGELOG.md`

### Phase 3 — Residual Audit

- [ ] Split reread into `fidelity` and `residual-slop` checks
- [ ] Document what the second pass may and may not do
- [ ] Add examples for pass-one vs pass-two behavior
- [ ] Add at least 3 benchmark cases where second pass should help
- [ ] Add at least 2 conservative cases where second pass should mostly abstain
- [ ] Sync docs and changelog

### Phase 4 — Real Sample Eval pilot

- [ ] Add `evals/real-samples.md` or `evals/real-samples/`
- [ ] Collect first `8-12` samples
- [ ] Cover at least these sample types:
  - README intro
  - release note
  - issue reply
  - dev update
  - X-style short post
  - forum-style long post
  - docstring or code comment
- [ ] Define per-sample fields:
  - original
  - scene
  - AI-ish symptoms
  - must-keep items
  - recommended rewrite
  - score
- [ ] Decide whether part of the pack should stay maintainer-only

### Phase 5 — release review

- [ ] Check README claims against what is actually shipped
- [ ] Check benchmark and real-sample pack together
- [ ] Review diff for scope creep
- [ ] Decide whether `Voice Calibration Lite` stays deferred to `v1.8`

## Deferred to v1.7.x

- [ ] `lite` vs `full` wording pass across install docs
- [ ] public bad-case intake template
- [ ] expand real-sample pack beyond pilot

## Deferred to v1.8+

- [ ] `Voice Calibration Lite`
- [ ] scene packs such as `README`, `release-note`, `forum-post`, `issue-reply`
- [ ] optional structured output for workflow integration
