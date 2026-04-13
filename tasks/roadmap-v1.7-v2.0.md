# v1.7-v2.0 Roadmap

> Updated: 2026-04-13
> Purpose: turn the external planning package into an implementation-facing roadmap that fits the current repo state.

## 1. Current repo snapshot

Current shipped baseline:

- Latest release: `1.6.1`
- Stable strengths already in repo:
  - Chinese-first rewrite skill with scene routing
  - tiered severity and no-touch rules
  - `annotation mode`
  - unsourced citation policy
  - code-context benchmark coverage
  - pattern-first intake guidance
- Current weakness:
  - strong at cleaning obvious AI patterns
  - weaker at making output feel like a real person wrote it
  - weaker at post-rewrite polish
  - benchmark is still mostly rule-facing, not publishability-facing

## 2. Gap map

The external deliverables are directionally correct, but they mix three layers:

1. already-shipped capability
2. near-term product work
3. longer-term branding and distribution work

We should separate them.

| Theme | External expectation | Current repo state | Gap level | First landing |
| --- | --- | --- | --- | --- |
| Positive Style Contract | dedicated positive style spec | only lightweight guidance in `SKILL.md` | medium | `references/positive-style.md` |
| Protected Spans / Facts Ledger | explicit pre-rewrite protection pass | partial `no-touch` rules, but no dedicated contract | medium | `references/protected-spans.md` |
| Residual Audit / Two-pass | distinct second pass for residual AI smell | only generic final reread; no dedicated pass | medium | `SKILL.md` + `references/operation-manual.md` |
| Voice Calibration Lite | optional user-voice fitting from 2-3 samples | not implemented | high | `references/voice-calibration.md` |
| Real Sample Eval Pack | real publishable samples and human scoring | synthetic benchmark is strong; real sample pack absent | high | `evals/real-samples.md` |
| Lite vs Full productization | users understand fallback vs full mode clearly | partially documented in README, not yet a full cross-doc contract | low-medium | README + install docs |
| Scene Packs | sub-scenes like `README`, `release-note`, `forum-post` | only 4 top-level scenes | medium | `references/scene-packs.md` or staged additions |
| Bad-case intake loop | templates + public collection point | internal intake docs exist; public intake is missing | medium | `.github/ISSUE_TEMPLATE/` |
| Structured workflow output | reusable schema for agent use | only `annotation mode` has a minimal contract | low-medium | defer to v1.8 |
| Growth / launch assets | cold-start and directory submission flow | README exists, but no maintained launch kit | low-medium | after core quality work |

## 3. Recommended sequencing

Do not implement the external package in listed order. The safer order is:

1. safety and rewrite-floor upgrades
2. second-pass quality upgrades
3. evaluation upgrades
4. productization and intake
5. distribution and growth

Reason:

- `voice calibration` without stronger guardrails increases drift risk
- `residual audit` without positive style guidance can over-flatten text
- `real sample eval` should start early, but it becomes much more useful after we define what "better" means

## 4. Horizon plan

## Horizon A — v1.7 foundation

Goal:

- make the rewrite output more human without increasing hallucination or misfire risk

Required deliverables:

- `Positive Style Contract`
- `Protected Spans`
- `Residual Audit / Two-pass`
- first batch of `Real Sample Eval Pack`

Explicitly not required for `v1.7.0`:

- full `Voice Calibration Lite`
- full sub-scene matrix
- public intake automation
- directory / launch work

## Horizon B — v1.7.x hardening

Goal:

- stabilize new quality features with real samples and boundary cases

Required deliverables:

- expand real sample pack from pilot to reusable regression asset
- harden docs for `lite` vs `full`
- add bad-case intake templates
- patch misfires discovered during `v1.7.0`

## Horizon C — v1.8 workflow

Goal:

- make the repo easier to embed in agents and editor workflows

Likely deliverables:

- `Voice Calibration Lite`
- sub-scenes such as `README`, `release-note`, `forum-post`, `issue-reply`
- optional output schema for structured workflows

## Horizon D — v2.0 productization

Goal:

- turn the repo into a more complete project, not just a rule pack

Likely deliverables:

- public bad-case collection loop
- stronger examples and release assets
- repeatable launch/distribution process

## 5. v1.7 work breakdown

## Phase 0 — Definition and scoring

Success condition:

- the team agrees on what "better" means before adding more rules

Tasks:

- [ ] Write `v1.7` scope into a dedicated todo file
- [ ] Define 3 new human-facing eval dimensions: `natural`, `specific`, `publishable`
- [ ] Decide minimum real-sample pack size for first release: recommended `8-12`
- [ ] Decide what counts as a pass for second-pass changes: recommended "improves at least 3 pilot samples without harming any protected case"

Files:

- `tasks/todo-v1.7.md`
- `evals/real-samples.md` or `evals/real-samples/README.md`

Risk:

- if we skip this phase, later tasks will optimize against fuzzy taste instead of stable criteria

## Phase 1 — Positive Style Contract

Why first:

- this defines the target shape of "more human" before we add more rewrite behavior

Tasks:

- [ ] Add `references/positive-style.md`
- [ ] Turn current positive guidance into explicit rewrite targets:
  - concrete actions over abstract uplift
  - mild sentence-length variation
  - fewer empty judgment wrappers
  - no "I am now explaining" narration
  - allow mild asymmetry; do not polish every sentence to uniform smoothness
- [ ] Add 4-6 examples to `references/examples.md` showing the difference between:
  - cleaner but still AI-ish
  - cleaner and actually more human
- [ ] Sync summary wording into `SKILL.md`
- [ ] Sync user-facing promise into `README.md`
- [ ] Log scope and non-goals in `CHANGELOG.md` when shipped

Acceptance:

- outputs become more specific, not just less slop-heavy
- no new universal "house style" emerges across all scenes

Main files:

- `references/positive-style.md`
- `references/examples.md`
- `SKILL.md`
- `README.md`
- `CHANGELOG.md`

## Phase 2 — Protected Spans / Facts Ledger

Why second:

- stronger style guidance is only safe if fact-bearing spans are protected more explicitly

Tasks:

- [ ] Add `references/protected-spans.md`
- [ ] Promote current no-touch rules into a pre-rewrite checklist:
  - numbers
  - dates
  - names
  - code blocks
  - commands
  - params / fields / paths
  - quoted text
  - error messages
  - metric claims
- [ ] Decide whether this stays prompt-only or becomes a visible "facts ledger" mini-format
- [ ] Add benchmark cases for mixed technical text where style changes should not drift facts
- [ ] Update `references/scene-guardrails.md` to point at the new protection layer
- [ ] Update `README.md` so users know this is a safety feature, not a style feature

Acceptance:

- protected spans survive rewrites in docs, status, code-context, and mixed scenes
- no fake precision is added during cleanup

Main files:

- `references/protected-spans.md`
- `references/scene-guardrails.md`
- `evals/benchmark.md`
- `SKILL.md`
- `README.md`
- `CHANGELOG.md`

## Phase 3 — Residual Audit / Two-pass

Why third:

- once target style and safety rails exist, second-pass cleanup becomes much less risky

Tasks:

- [ ] Split final reread into two named checks:
  - fidelity check
  - residual-slop check
- [ ] Define what residual-slop check is allowed to touch:
  - opener residue
  - summary residue
  - narrator residue
  - empty judgment residue
  - overly even sentence rhythm
- [ ] Keep second pass lightweight; forbid full rewrite in pass two
- [ ] Make `docs` and `status` more conservative by default
- [ ] Add before/after examples that show:
  - pass one is cleaner
  - pass two is cleaner and less template-like
- [ ] Add at least 3 eval cases where pass two should help and 2 where pass two should leave text mostly alone

Acceptance:

- pass two improves real-sample quality without adding drift
- riskier scenes do not become more casual than intended

Main files:

- `SKILL.md`
- `references/operation-manual.md`
- `references/examples.md`
- `evals/benchmark.md`
- `CHANGELOG.md`

## Phase 4 — Real Sample Eval Pack (pilot)

Why now:

- we need a reality check before calling `v1.7.0` done

Tasks:

- [ ] Create `evals/real-samples.md` or a folder-based pack
- [ ] Start with 8-12 samples across:
  - README intro
  - release note
  - issue reply
  - commit message
  - dev update
  - X-style short post
  - Linux.do style longer post
  - docstring / code comment
- [ ] Define per-sample fields:
  - source text
  - scene
  - why it feels AI-ish
  - what must not be damaged
  - recommended rewrite
  - score for `natural / fidelity / publishable`
- [ ] Add a short evaluation rubric
- [ ] Decide whether this pack is repo-public or partly kept as maintainer-only working material

Acceptance:

- at least 5 samples are strong enough to reuse in README, release notes, or future launch posts
- the pack can catch regressions that the current synthetic benchmark would miss

Main files:

- `evals/real-samples.md`
- `README.md` or future docs links

## Phase 5 — v1.7 release cleanup

Tasks:

- [ ] Update README claims to match only shipped features
- [ ] Update changelog with new files, new guarantees, and new known limits
- [ ] Run static review across benchmark plus real-sample pilot
- [ ] Review diff for scope creep
- [ ] Decide whether `Voice Calibration Lite` stays out of `v1.7.0` and moves to `v1.8`

Release gate:

- do not ship `v1.7.0` if `voice calibration` is only half-described and undocumentedly absent

## 6. v1.7.x follow-up breakdown

These are important, but should not block `v1.7.0`.

### Track A — Lite vs Full productization

- [ ] check all install docs for consistent `lite` vs `full` wording
- [ ] add a simple "which mode should I use?" matrix
- [ ] make sure README, install docs, and `SKILL.md` do not imply that single-file mode equals full capability

### Track B — Bad-case intake

- [ ] add `.github/ISSUE_TEMPLATE/bad-case.md`
- [ ] add `DISCUSSION_TEMPLATE` or a pinned issue draft
- [ ] define minimum fields so reports are useful: original text, scene, expected tone, what felt AI-ish, what must not be touched

### Track C — Real Sample expansion

- [ ] grow pilot pack from `8-12` to `20+`
- [ ] tag samples by risk type so future changes can target them
- [ ] pull 5+ cases from real user feedback instead of self-authored samples only

## 7. v1.8 breakdown

Only start this after `v1.7.x` is stable.

### Voice Calibration Lite

Dependencies:

- positive style contract exists
- protected spans are stable
- real sample scoring is in place

Tasks:

- [ ] define allowed inputs: `2-3` user-provided samples
- [ ] extract only style signals, not reusable wording
- [ ] define forbidden use: celebrity / brand / third-party imitation
- [ ] add examples showing delta with and without voice samples
- [ ] add eval cases for "closer to user voice without copying"

### Scene Packs

Tasks:

- [ ] split `public-writing` into sub-scenes with actual rewrite constraints
- [ ] start with the most common ones: `README`, `release-note`, `forum-post`, `issue-reply`
- [ ] add worked examples before adding more categories

### Workflow / structured output

Tasks:

- [ ] decide whether agent-facing structured output is worth the extra maintenance
- [ ] if yes, keep it opt-in and do not disrupt the default one-shot rewrite path

## 8. Repo management for external planning inputs

Principle:

- raw external deliverables should be archived, not mixed with live product docs

Recommended structure:

- `tasks/external-inputs/`
  - read-only snapshots from ChatGPT, Claude, humans, or other external collaborators
- `tasks/roadmap-*.md`
  - our distilled, repo-specific execution plans
- `tasks/todo-*.md`
  - versioned implementation checklists

Rules:

- do not edit external originals after archiving them
- if we disagree with an external suggestion, record that in our roadmap, not by rewriting the source file
- each external bundle should have a dated folder name and a short source note
- once a plan is adopted, the source bundle becomes reference material, not the active todo list

## 9. Recommended commit strategy

For this planning stream, use small commits:

1. archive external input
2. add distilled roadmap
3. add version-specific todo when implementation starts
4. ship feature branches by capability, not by giant "v1.7 all-in-one" change sets

Good branch examples:

- `codex/v1.7-positive-style`
- `codex/v1.7-protected-spans`
- `codex/v1.7-residual-audit`
- `codex/v1.7-real-samples-pilot`

Avoid:

- one branch that rewrites `SKILL.md`, README, evals, install docs, and growth docs all at once

## 10. Immediate next step

Recommended next implementation unit:

1. create `tasks/todo-v1.7.md`
2. ship `Positive Style Contract`
3. ship `Protected Spans`
4. then evaluate whether `Residual Audit` can land safely in the same version
