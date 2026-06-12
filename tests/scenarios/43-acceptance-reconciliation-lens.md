# Scenario 43 — Acceptance-criteria reconciliation lens (DEC-022)

Conceptual trace test for DEC-022 Option D (A + C): the authority doctrine (`verification-result.json` `criteria[]` is the acceptance-*status* surface; inline spec `- [ ]` boxes are authored input) and the new advisory `acceptance-reconciliation` lens in `/audit-coherence`. Verifies the lens flags the flirty-gym symptom, stays silent for the common (box-less) case, never mutates the spec, and that the authority split is applied consistently.

## Setup / State

- A project with `.claude/spec_v2.md` that renders per-phase acceptance criteria as inline `- [ ]` checkboxes (an *optional* project convention — the template does not mandate it). flirty-gym shape: Phase 1 boxes all `[x]`, **Phase 2 boxes all `[ ]`**.
- `.claude/verification-result.json` exists with `result: "pass"` and `criteria[]` 7/7 `pass` (the latest phase-level result — Phase 2).
- The dashboard renders `### Acceptance Criteria` as 7/7 passed (from that file).

## Trace A — lens flags the box-vs-`criteria[]` divergence (the flirty-gym symptom)

Command path: `commands/audit-coherence.md` Phase 1 capture step 9 → Lens prompts → "Lens 7 — `acceptance-reconciliation`" → Synthesizer.

1. Capture copies `.claude/verification-result.json` → `inputs/verification-result.json`.
2. The lens scans the active spec for inline `- [ ]` / `- [x]` boxes grouped by phase, then reads the verification result.
3. Phase 2's boxes are all `- [ ]` while `verification-result.json` records `result: "pass"` (7/7) → divergence.
4. The lens matches box labels to `criteria[].name` **advisorily** (fuzzy text similarity; free-text names, no ID link), labelling the correspondence as *suspected* for human review.

**Expected:** ONE finding clustered at Phase 2 — *"Phase 2: 0/N inline acceptance boxes ticked, but verification-result.json records result=pass (7/7 criteria)."* Source anchor = spec § Phase 2; `files_to_touch` = `spec_v*.md` → the synthesizer's HARD RULE classifies it `kind: decision`; suggested fix routes via `/iterate`.

**Pass criteria:** clustered per phase (not one finding per box); `kind: decision` (never `bundle-eligible` — spec path); the box↔criterion match is presented as suspected, not asserted; the lens emits text only and never edits the spec.

## Trace B — no inline boxes → `Findings: 0` (the common case, Q3)

Command path: "Lens 7 — `acceptance-reconciliation`" prompt § "This lens only applies when…".

State: the spec has an "Acceptance Criteria" section but renders **no** inline `- [ ]` boxes (the majority case — boxes are optional; the template never mandated them).

1. The lens scans for inline checkboxes → none found.

**Expected:** `Findings: 0` ("nothing to reconcile — inline boxes are an optional project convention"). The lens also returns `Findings: 0` when `inputs/verification-result.json` is `{}` / absent (no verified phase yet).

**Pass criteria:** the lens is silent for box-less specs and for unverified projects — no false positives on the common case; the optional-convention reality (DEC-022 Q3) is honored.

## Trace C — advisory match never mutates the spec (Q2 safety + DEC-016)

Command path: Lens 7 prompt (advisory match) + Synthesizer HARD RULE (`commands/audit-coherence.md § "Synthesizer prompt"` step 5 + sanity check 1).

State: Phase 3 renders 4 boxes; the latest `verification-result.json` is a **partial** PASS for Phase 3 (`criteria_failed > 0`, e.g. 3/4), and the fuzzy box↔criterion match is ambiguous (criteria were re-segmented per-task).

1. The lens flags the divergence but explicitly notes where it **cannot confidently match** a box to a criterion (free-text, re-segmented, no ID — DEC-022 Q2) rather than guessing.
2. The synthesizer sees `files_to_touch` includes a spec path → HARD RULE → `kind: decision`; never `bundle-eligible`; never inline-applied (`[Fix it]` is unavailable for this kind).

**Expected:** the finding surfaces for human judgment through `/iterate`; **no** spec box is auto-ticked, and partial-PASS boxes are not blindly flipped. The unsafe-mapping risk that disqualified DEC-022 Option B is contained precisely because the lens never auto-mutates state.

**Pass criteria:** advisory only; reconciliation is a human decision via `/iterate`; the hard rule prevents any inline spec edit regardless of match confidence.

## Trace D — authority doctrine (A): dashboard is the status surface, not the inline boxes

Command path: `rules/spec-workflow.md § "Acceptance-criteria authority (DEC-022)"` + `commands/health-check.md` Part 1 acceptance-status note + `.claude/CLAUDE.md` Critical Invariant.

State: Phase 2 verified PASS (`criteria[]` 7/7); spec Phase 2 inline boxes still `- [ ]`.

1. `/health-check` Part 1 completion-gate does **not** treat the unticked spec boxes as a completion failure (the note: boxes are authored input; live status is the dashboard `### Acceptance Criteria`).
2. A reader/agent consults the dashboard `### Acceptance Criteria` (7/7) for *status*, and the spec for the *criteria text*.

**Expected:** unticked inline boxes never block completion or raise a false "phase incomplete" signal; the authoritative acceptance-status is `verification-result.json` `criteria[]`.

**Pass criteria:** the authority split is applied consistently (spec = criteria authorship; `verification-result.json` / dashboard = status); no artifact treats stale inline boxes as authoritative status.

## Known scope (honest caveat)

The lens reconciles against the **current** `.claude/verification-result.json`, which holds only the **latest** phase-level result (it is overwritten each phase). Earlier phases whose results have been overwritten are not reconciled by this lens — it catches the live/most-recent case (the flirty-gym Phase 2 symptom), not full phase history. Full historical reconciliation would additionally cross-check per-task `task_verification` (persisted per task JSON); that was deliberately left out of DEC-022's scope.

## Invariant checks

- The lens **never edits the spec** — reconciliation routes through `/iterate` (DEC-016 unchanged; spec/decision/vision remain read-only outside `/iterate`).
- **Zero** changes to `agents/verify-agent.md`, `commands/work.md` completion flow, `.claude/settings.json`, or `support/reference/drift-reconciliation.md` — A+C adds doctrine + a read-only advisory lens only (the economy of A+C over the rejected Option B).
- The lens returns `Findings: 0` for box-less specs — an opt-in convention, not a mandate (Q3); it adds no friction to the majority of projects.
- HARD RULE holds: any finding whose `files_to_touch` includes a spec path is `kind: decision`, never `bundle-eligible` — no inline auto-fix path exists for acceptance-box reconciliation.
