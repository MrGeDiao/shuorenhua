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
