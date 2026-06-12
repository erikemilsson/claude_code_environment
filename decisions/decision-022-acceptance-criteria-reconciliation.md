---
id: DEC-022
title: Spec acceptance-criteria ↔ phase-verification reconciliation (authority + DEC-016 box-tick carveout)
status: implemented
category: process
created: 2026-06-12
decided: 2026-06-12
implemented: 2026-06-12
related:
  tasks: []
  decisions: [DEC-016, DEC-013, DEC-004, DEC-021]
  feedback: [FB-097]
implementation_anchors:
  - file: ".claude/rules/spec-workflow.md"
    description: "§ Acceptance-criteria authority (DEC-022) — the doctrine (Option A)"
  - file: ".claude/support/reference/dashboard-regeneration.md"
    description: "### Acceptance Criteria render note — authoritative acceptance-status surface"
  - file: ".claude/commands/health-check.md"
    description: "Part 1 acceptance-status authority note"
  - file: ".claude/CLAUDE.md"
    description: "Critical Invariant — phase acceptance status authority"
  - file: ".claude/commands/audit-coherence.md"
    description: "7th lens — acceptance-reconciliation (Option C)"
  - file: ".claude/version.json"
    description: "template_version 4.26.0 (MINOR)"
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Spec acceptance-criteria ↔ phase-verification reconciliation (authority + DEC-016 box-tick carveout)

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Declare authority — `verification-result.json` `criteria[]` (rendered as the dashboard's `### Acceptance Criteria`) is authoritative for phase acceptance *status*; spec inline `- [ ]` acceptance boxes are authored/informational. Document it; add a `/health-check` note. Lowest churn; leaves the spec visibly stale on box state.
- [ ] Option B: Orchestrator ticks boxes at phase-level PASS as an infrastructure operation, with an explicit DEC-016 carveout clause for "acceptance-box state-sync." Keeps the source-of-truth doc honest; amends DEC-016. **Research-disrecommended (unsafe mapping + drift cost).**
- [ ] Option C: Detection-only — an advisory `/audit-coherence` lens that flags spec-box vs `criteria[]` divergence and routes reconciliation through `/iterate`. Catches drift without deciding authority; weakest alone.
- [x] Option D: Composite **A + C** — declare authority (A) + advisory detection lens (C). **Research-recommended.** Mirrors DEC-016's "declaration + safety net" shape.

*Check one box above, then fill in the Decision section below.*

---

## Background

**Trigger:** FB-097 (bridged from flirty-gym, template_version 4.7.1). The template keeps **two representations** of phase acceptance-criteria state and never reconciles them:

1. The spec's **authored** acceptance criteria — prescribed as a spec section by the template (`.claude/spec_v1.md` "Acceptance Criteria (how you'll know it works)"; `.claude/support/reference/spec-checklist.md` "no acceptance criteria = no definition of done"). A project may render these per-phase as inline `- [ ]` checkboxes (flirty-gym did). **The template does not mandate the checkbox rendering** (verified — see Q3).
2. `verification-result.json`'s **`criteria[]`** — verify-agent writes a per-criterion PASS/FAIL table (`.claude/agents/verify-agent.md` § "Required artifact" + return schema `criteria[]`/`criteria_passed`/`criteria_failed`), which the dashboard renders as a `### Acceptance Criteria` `[x]`/`[ ]` checklist (`dashboard-regeneration.md:308–316`).

After phase-level verification PASSES, the completion flow updates `verification-result.json`, the dashboard, and — at the final phase only — the spec `status:` frontmatter. It **never** touches the spec's inline acceptance boxes. Three things are left undefined:

- **Authority:** which artifact is the source of truth for "this phase's acceptance criteria are met"? `spec-workflow.md` calls the spec "the living source of truth," yet nothing keeps the inline boxes in sync with the verifier — so the source-of-truth document silently goes stale/false.
- **Tick responsibility:** if the inline boxes are meant to be ticked post-verification, by whom and at what step? verify-agent can't write the spec (DEC-004); the `/work` orchestrator's completion flow doesn't do it today.
- **DEC-016 classification:** ticking a `- [ ]` → `- [x]` in spec **body** text is, by DEC-016's literal carveout (which names only archiving / version transitions / frontmatter updates), a substantive text edit → routes through `/iterate` AND trips the structural `permissions.ask` gate on `.claude/spec_v*.md`.

No `/health-check` or `/audit-coherence` lens detects the divergence (confirmed), so it accrues silently.

**Evidence (real bite):** In flirty-gym (template v4.7.1), Phase 1's spec acceptance boxes are all `[x]` but Phase 2's are all `[ ]` — despite BOTH phases having a recorded phase-level `verification-result.json` PASS (Phase 2 = 7/7). The spec asserts Phase 2 is incomplete while every other artifact says it passed.

**Why a decision record:** the FB-097 capture leaned toward Option B, which **amends DEC-016's carveout enumeration** — a governance boundary that cannot be changed by direct edit. Multiple viable approaches with real trade-offs → decision record.

## Questions to Research

*(Answered in `## Research Findings` below. Full methodology + sources in `decisions/.archive/decision-022-research-2026-06-12.md`.)*

1. **DEC-016 carveout mechanics (LOAD-BEARING)** — does Option B clear both the behavioral carveout and the structural `permissions.ask` gate, and at what friction?
2. **Mapping fidelity `criteria[]` ↔ inline boxes (LOAD-BEARING)** — can the orchestrator reliably map a PASS to the right box?
3. **Convention scope** — does the template mandate inline boxes; rule vs optional-convention guidance?
4. **External precedent** — how do RTM / BDD / DOORS reconcile authored criteria vs verified results?
5. **Drift-detection interaction** — does ticking a box change the section fingerprint and generate drift noise?
6. **Doctrinal coherence** with "spec is the living source of truth."
7. **Scope vs per-task verification** — is there an analogous per-task gap?

## Research Findings

*Per-question summary; full methodology and sources in the archive. Research-agent, 2026-06-12.*

**Q1 — DEC-016 carveout mechanics: B is implementable but inherits a gate it cannot scope.** Two layers: the *behavioral* rule (`spec-workflow.md` — box-tick is body text, not in the autonomous carveout → B requires adding "acceptance-box state-sync" to the enumeration = the DEC-016 amendment) AND the *structural* `permissions.ask` gate (`.claude/settings.json` gates `Edit(.claude/spec_v*.md)`; `ask` rules **cannot be scoped to a sub-operation**, so the orchestrator's tick prompts exactly like any spec edit). Friction is small — ~1 click per phase-closing session via platform-native "Yes, don't ask again." **But** provenance is not platform-trackable, so the gate can't tell "blessed box-tick" from "Claude rationalizing a spec edit" — B trains click-through on the exact path DEC-016 hardened. Not friction-disqualified; a thumb on the scale away from B.

**Q2 — Mapping fidelity: UNSAFE (decisive against B).** `criteria[]` entries are `{name, status, notes}` where `name` is **free text the verifier composes** (no `criterion_id`, no `spec_box_ref`, no line anchor), and phase-level verification explicitly **re-segments** (split per-task / merged / reworded; `verify-agent.md:561,572–583,690`). Mapping a PASS to a specific inline box would require **fuzzy string match** — the exact semantic-name-matching that `task-management.md § "Audit Tasks"` and DEC-016 flag as a recurring false-positive source. Failure modes: N:1/1:N correspondence, partial PASS (some boxes must stay `[ ]`), authored-but-unverified boxes (B silently leaves them `[ ]` — reproducing the flirty-gym symptom it set out to fix), orphan ticks. To make B *safe* you must first add stable criterion↔box IDs to both the spec convention and the `criteria[]` schema — at which point you've built C's trace-link and demoted the box to A's derived view anyway.

**Q3 — Convention scope: the template does NOT mandate inline boxes.** `spec_v1.md` lists "Acceptance Criteria" as a suggested section with no checkbox syntax; `spec-checklist.md` requires *testability*, never *rendering*. The only acceptance checklist the template *generates* is the dashboard's `### Acceptance Criteria` from `criteria[]`. So a heavyweight spec-writing mechanism (B) is disproportionate for an optional rendering; the right shape is a doctrinal declaration (A) + optional-convention guidance.

**Q4 — External precedent: dominant pattern is "single source + derived status view"; B is the anti-pattern.** RTM tools (status as a matrix *column*, not edits to requirement text), BDD/Gherkin living documentation (`.feature` is the stable authored source; pass/fail in a separate execution surface), and DOORS (verification status as a *separate attribute* + trace links; IBM guidance *cautions against* embedding status in requirement table cells) all keep the authored artifact stable. "single source + derived view" → A; "trace-link carrying status" → C; "bidirectional sync of authored doc" → B is the **least-attested** and explicitly discouraged.

**Q5 — Drift-detection interaction: cost unique to B.** `section_fingerprint = sha256(heading + content)` — a `- [ ]`→`- [x]` tick is inside that content, so it changes the hash, re-flagging the section's tasks for reconciliation. Per `drift-reconciliation.md`, applying reconciliation to a Finished task **clears its `task_verification` and resets it to Pending** — so a naive tick could prompt to reset verified work. This is the same tension `feature-retirement.md` solved by *not* mutating the body. B would be the template's first sanctioned spec-body mutation outside `/iterate` and needs a drift-suppression carveout (at `### ` granularity too, per DEC-021). A and C never touch the spec → clean.

**Q6 — Doctrinal coherence: A is coherent; B is in tension.** The canonical statement is "the spec is the living source of truth, **or it is updated intentionally**." Acceptance *criteria* (authored intent) ≠ acceptance *status* (verified PASS/FAIL); the spec was never wired to maintain runtime status. A auto-flip on every PASS is *incidental* mirroring — the opposite of "updated intentionally," so B is the option in tension; A preserves the principle. A's only cost is cosmetic staleness of inline boxes, bounded to projects that opt into rendering them — which is exactly what C patches.

**Q7 — Scope: bounded to phase-level; per-task already reconciled.** No per-task acceptance-box exists; the structural gate is `task_verification.result == "pass"` (enforced in `work.md`, `health-check.md` Part 1, `task-management.md`, Critical Invariants). The FB-097 gap is exclusively phase-level. This *reinforces* A: the template's verification doctrine already treats the structured artifact as authoritative and the rendering as derived — A extends that to phase level.

## Options Comparison

Scoring: ✓✓ strong / ✓ acceptable / – neutral-conditional / ✗ weak. **D = A + C.**

| Criterion | A — Declare authority | B — Orchestrator ticks (DEC-016 amend) | C — Detection lens | D — Composite (A + C) |
|---|---|---|---|---|
| Implementation complexity | ✓✓ Low (prose, no code) | – Medium (amend + tick logic + drift-suppress + fuzzy match) | ✓ Low–med (one read-only lens) | ✓ Low–med (A + C; no spec-mutating code) |
| Keeps source-of-truth honest (status) | – Boxes stay visibly stale; "read dashboard for status" | ✓✓ Boxes reflect PASS *if* mapping right (Q2 risk) | ✓ Surfaces divergence + prompts reconcile | ✓✓ Doctrine clean (A) + divergence caught (C) |
| DEC-016 amendment required | ✓✓ None | ✗ Yes (Q1) | ✓✓ None (read-only) | ✓✓ None |
| Drift-detection interaction | ✓✓ None (Q5) | ✗ Must suppress; risk resetting Finished→Pending | ✓✓ None | ✓✓ None |
| Mapping safety (`criteria[]`↔box) | ✓✓ N/A (boxes not state-bearing) | ✗ Unsafe — free-text, re-segmented, no ID (Q2) | ✓ Advisory only (human judges) | ✓✓ A removes need; C advisory |
| Friction per phase-close | ✓✓ Zero | ✓ ~1 click/phase; trains click-through on DEC-016 path | ✓✓ Zero (on-demand) | ✓✓ Zero added at phase-close |
| Reversibility | ✓✓ Trivial | ✓ Revert prose + logic + un-amend | ✓✓ Trivial | ✓✓ Easy (remove either half) |
| Works under auto mode | ✓✓ Behavioral | – Box-tick still prompts | ✓✓ Read-only | ✓✓ Yes |
| Doctrinal coherence (Q6) | ✓✓ Coherent ("updated intentionally") | – Tension (incidental mirroring) | ✓ Neutral (routes fixes via `/iterate`) | ✓✓ A coherent + C proper-flow |
| External-precedent alignment (Q4) | ✓✓ "single source + derived view" | ✗ "mutate authored doc" (discouraged) | ✓ "trace-link carrying status" | ✓✓ A + C both attested |
| Solves flirty-gym symptom | ✓ Reframes (dashboard was right: 7/7) | – Only if mapping ticks right boxes (Q2) | ✓✓ Detects & surfaces the divergence | ✓✓ Reframed (A) + flagged (C) |
| Habituation / protection erosion | ✓✓ None | ✗ Trains "yes" on spec-edit prompts | ✓✓ None | ✓✓ None |

## Option Details

### Option A: Declare authority (boxes informational)

**Description:** Declare `verification-result.json criteria[]` (and its dashboard `### Acceptance Criteria` rendering) the authoritative status surface for "phase acceptance met." Inline `- [ ]` boxes are *authored input*, not a live status field. Document in `spec-workflow.md` + `dashboard.md`; add a `/health-check` informational note.

**Strengths:** Lowest churn; no code; zero friction; no DEC-016 amendment; no drift interaction; matches the dominant industry pattern *and the template's own existing dashboard surface*; doctrinally coherent (Q6). Reframes flirty-gym as "the dashboard was right; the inline boxes were never wired to update."

**Weaknesses:** A project that renders inline boxes *and* reads the spec (not the dashboard) for status sees stale `[ ]`. Purely cosmetic, bounded to opt-in-box projects — but real for a spec skimmer. (Exactly what C patches.)

**Research notes:** A formalizes a pattern the template already half-implements; lowest blast radius, strongest external backing.

### Option B: Orchestrator ticks boxes at phase PASS (infra op + DEC-016 carveout amendment)

**Description:** At phase-level PASS, the completion flow edits the spec to flip the relevant `- [ ]`→`- [x]`. Requires (a) amending DEC-016's carveout to add "acceptance-box state-sync," (b) a fuzzy `criteria[]`→box matcher, (c) a drift-suppression step, (d) ~1 `ask` click/phase.

**Strengths:** If everything works, the spec body itself shows live PASS — the most "honest document" of the four. Friction is genuinely small (Q1).

**Weaknesses (decisive):** Mapping unsafe (Q2). Must suppress drift or risk resetting Finished→Pending (Q5). Amends a governance boundary and trains click-through on the path DEC-016 hardened (Q1). Least-attested industry pattern; closest analogue explicitly discouraged (Q4). Making B *safe* requires first adding stable criterion↔box IDs — at which point you've built C + A anyway.

**Research notes:** The capture's lean toward B does not survive Q2/Q5.

### Option C: Detection-only lens

**Description:** A read-only `acceptance-reconciliation` lens in `/audit-coherence` (and/or a `/health-check` check) that — when a project renders inline boxes — compares their state against `criteria[]` and flags divergence (e.g., "Phase 2: 0/4 boxes ticked but `criteria[]` is 7/7 PASS"), routing reconciliation through `/iterate` (boxes are spec body → DEC-016). Fuzzy match is **advisory** (human judges) → Q2's mapping risk is tolerable here (a wrong guess just shows a divergence to eyeball, never mutates state).

**Strengths:** Catches the exact flirty-gym symptom; zero spec mutation; no DEC-016 amendment; no drift interaction; aligns with "trace-link carrying status" (Q4); slots into the existing audit-coherence lens architecture (no current lens covers this).

**Weaknesses:** Weakest *alone* — detects but doesn't decide authority; without A the "which is the truth?" question stays open. Only helps box-rendering projects.

**Research notes:** The natural safety-net half; advisory framing sidesteps the Q2 problem that disqualifies B.

### Option D: Composite — A + C (recommended)

**Description:** Ship **A** (declare authority + document) **+ C** (advisory audit-coherence lens). Mirrors DEC-016's "declaration + safety net" shape — here "doctrinal declaration + detection safety net."

**Why A+C, not B+C:** B's contribution (auto-mutating spec boxes) is the part every research line argues against (Q2/Q5/Q1/Q4). C already delivers B's *intent* (surface divergence, keep the doc honest) without B's mechanism, and routes the actual reconciliation through `/iterate` where DEC-016 says spec-body changes belong.

**Strengths:** Resolves authority coherently (A) + catches the real symptom (C); no spec mutation, no DEC-016 amendment, no drift cost, no per-phase friction; both halves match attested industry patterns; each independently reversible.

**Weaknesses:** Slightly more surface than A alone (one lens to build + maintain). If the cosmetic-staleness wart is judged negligible, C is deferrable → A-alone is the minimum-change ship.

## Recommendation

**Recommended: Option D = A + C.** Declare `criteria[]` (dashboard `### Acceptance Criteria`) authoritative for phase acceptance *status*, demote inline spec `- [ ]` boxes to authored input, document the split, AND add an advisory `acceptance-reconciliation` lens to `/audit-coherence` that flags box-vs-`criteria[]` divergence and routes reconciliation through `/iterate`.

**Confidence: High** on rejecting B and anchoring on A; **Moderate** on bundling C now vs deferring (user judgment — see "Your Notes & Constraints" → Research Questions).

**Evidence base:** Q2 (unsafe mapping) + Q5 (drift carveout) + Q4 (B is the anti-pattern) jointly disqualify B's *mechanism* despite Q1 showing B is friction-cheap. Q4 (dominant pattern) + the discovery that the template already renders `criteria[]` as `### Acceptance Criteria` make A a formalization of an existing pattern (near-zero conceptual risk). Q6 shows A preserves "updated intentionally" better than B. Q3 shows boxes aren't mandated, so B is disproportionate. Q7 bounds the decision to phase-level and shows A extends the template's existing "structured artifact authoritative, rendering derived" doctrine.

**Minimum-change alternative: Option A alone** — doctrinal declaration + `/health-check` note, no lens. Fully closes the FB-097 governance gaps (authority, tick-responsibility, DEC-016 classification); C is the safety-net upgrade, not a correctness requirement. Conservative ship; add C later if box-divergence is observed annoying in a real multi-phase project.

**Against the capture's lean:** FB-097 leaned Option B. The research does not support B's mechanism — implementable (Q1) but unsafe as specified (Q2) and doctrinally/operationally costlier (Q5/Q1/Q4) than alternatives. For "keep the source-of-truth honest," C achieves the intent without B's mechanism.

**Version bump on promotion:** MINOR (new doctrine + optional lens; no permission-layer or task-schema change — contrast DEC-016's MAJOR, which touched the permission layer).

### Implementation surface sketch (D = A + C)

*Option A (doctrine):* (1) `.claude/rules/spec-workflow.md` — declare status authority = `criteria[]`/dashboard; inline boxes = authored input; spec still source of truth for the *criteria*. (2) `.claude/rules/dashboard.md` — note `### Acceptance Criteria` is the authoritative acceptance-status view. (3) `.claude/commands/health-check.md` — informational note. (4) `.claude/CLAUDE.md` Critical Invariants — optional 1-line cross-reference. (5) this record → `implemented` + anchors. (6) `.claude/version.json` MINOR bump.

*Option C (lens):* (7) `.claude/commands/audit-coherence.md` — add a 7th `acceptance-reconciliation` lens (finding `kind: decision` → fix routes via `/iterate`; advisory fuzzy match; cluster per phase). (8) shared audit-contract touch only if needed.

*Zero edits* to `verify-agent.md`, `work.md` completion flow, `settings.json`, or `drift-reconciliation.md` — the economy of A+C over B.

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision. This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
- This is the **template repo**: the decision changes template workflow/governance, not a project build. No project spec to revise; the "source of truth" is `system-overview.md` + the rules files.
- Option B amends DEC-016 — keep the existing `/iterate`-routing and `permissions.ask` behavior intact for genuine substantive edits; only the narrow "acceptance-box state-sync" reflection would be carved out.

**Preferences (none locked in yet):**
- FB-097 triage recommendation leaned toward Option B; the research recommends against it (see Recommendation).

**Research Questions (from research-agent — answering these narrows the choice):**
1. **Bundle C now, or ship A alone and add C on signal?** A alone fully closes the FB-097 *governance* gaps; C is the safety net for the *cosmetic* divergence (single-project symptom so far). Lean: A now is sufficient; C is a clean follow-up — but D is defensible if you want divergence actively surfaced.
2. **Should the template take a position on rendering inline acceptance boxes at all?** A could go further and advise projects *not* to render acceptance criteria as inline `- [ ]` boxes (the dashboard is the live surface), eliminating the false-state affordance and making C largely moot. Prefer "boxes are fine, treated as authored input" (needs C) or "prefer not to render boxes; read the dashboard" (simpler, C unnecessary)?
3. **Confirm B is off the table?** If you have a strong reason to want the spec body itself to show live PASS (e.g., readers who never open the dashboard), that would justify the larger investment of first adding stable criterion↔box IDs to the spec convention + `criteria[]` schema (prerequisite to make B safe) — meaningfully bigger scope than A+C.

**FB-097 captured directions (verbatim, for reference):**
> (A) declare the inline boxes authored-only and verification-result.json authoritative, document it, add a /health-check note that inline boxes are informational (lowest churn; leaves the source-of-truth doc visibly stale). (B) the /work orchestrator ticks the spec's phase boxes at phase-level PASS as an infrastructure operation (state-reflection of a verifier result — same class as the `status:` flip), with an explicit DEC-016 carveout clause for "acceptance-box state-sync" (keeps the source of truth honest without an /iterate cycle; needs the DEC-016 amendment). (C) detection-only: a /health-check or /audit-coherence lens that flags spec-box vs verification-result.json divergence and prompts reconciliation (catches drift without deciding authority; weakest).

## Decision

**Selected: Option D — Composite (A + C).** User selection 2026-06-12, confirming the research-agent recommendation. Declare `verification-result.json criteria[]` (rendered as the dashboard's `### Acceptance Criteria`) authoritative for phase acceptance *status*; demote inline spec `- [ ]` acceptance boxes to authored input; document the split; AND add an advisory `acceptance-reconciliation` lens to `/audit-coherence` that flags box-vs-`criteria[]` divergence and routes reconciliation through `/iterate`.

**Rationale:**

- **Q2 (mapping) + Q5 (drift) + Q4 (anti-pattern) disqualify Option B's mechanism.** `criteria[]` are free-text, re-segmented, and carry no ID linking them to inline boxes, so auto-ticking depends on unsafe fuzzy matching; ticking a box changes the section fingerprint (risking Finished→Pending resets); and "write status into the authored doc" is the pattern RTM/BDD/DOORS deliberately avoid.
- **A formalizes an existing template surface.** The dashboard already renders `criteria[]` as `### Acceptance Criteria`; A names it authoritative rather than building a new sync engine.
- **A preserves doctrine better than B (Q6).** "The spec is the living source of truth, or it is updated intentionally" — an auto-flip on every PASS is *incidental* mirroring, the opposite of intentional update. A keeps the principle; B strains it.
- **C is the safe safety-net.** Its fuzzy match is advisory (surfaces a divergence for human judgment, never mutates state), so the Q2 mapping risk that disqualifies B is tolerable in C.
- **A + C, not B + C** — C already delivers B's intent (keep the doc honest) without B's mechanism, and routes the actual fix through `/iterate` where DEC-016 says spec-body changes belong.

## Trade-offs

**Gaining:**

- A clear authority rule: phase acceptance *status* = `verification-result.json criteria[]` (dashboard `### Acceptance Criteria`); the spec remains source of truth for the *criteria themselves*. Closes FB-097's authority / tick-responsibility / DEC-016-classification gaps.
- An advisory `/audit-coherence` lens that detects the flirty-gym symptom (spec boxes `[ ]` despite a phase PASS) and routes reconciliation through `/iterate`.
- Zero spec mutation, no DEC-016 amendment, no drift-detection interaction, no per-phase friction — alignment with attested industry patterns (single source + derived view; trace-link carrying status).

**Giving Up:**

- Projects that render inline acceptance boxes *and* read the spec (not the dashboard) for status still see cosmetically stale `[ ]` between the verifier PASS and a manual reconciliation. The lens surfaces this but doesn't auto-fix it (auto-fix is the unsafe Option B mechanism declined here).
- One new audit lens to build and maintain (the C half). Deferrable if a future call judges the cosmetic divergence negligible — A alone remains the documented minimum-change fallback.

## Impact

**Implementation Notes:**

Shipped in template_version 4.26.0 (2026-06-12), MINOR — new doctrine + optional lens; no permission-layer or task-schema change. Status `implemented`; `implementation_anchors` populated above.

Planned files:

*Option A (doctrine):*
1. `.claude/rules/spec-workflow.md` — new subsection declaring phase acceptance *status* authority = `criteria[]`/dashboard; inline `- [ ]` boxes = authored input; spec remains source of truth for the criteria. Cite DEC-022.
2. `.claude/rules/dashboard.md` — note the `### Acceptance Criteria` checklist is the authoritative acceptance-status view (from `verification-result.json`), distinct from any inline spec boxes.
3. `.claude/commands/health-check.md` — informational note: inline acceptance boxes are authored input; live status is the dashboard.
4. `.claude/CLAUDE.md` Critical Invariants — optional 1-line cross-reference to the new spec-workflow declaration.

*Option C (lens):*
5. `.claude/commands/audit-coherence.md` — add a 7th `acceptance-reconciliation` lens (finding `kind: decision` → fix via `/iterate`; advisory fuzzy match; cluster per phase).

*Bookkeeping:*
6. `.claude/version.json` — bump 4.25.0 → 4.26.0 (MINOR).
7. This record → `implemented` + populate `implementation_anchors`; FB-097 → `promoted` in `template-maintenance/feedback-archive.md`; ship-log entry; root `CLAUDE.md` Active Follow-ups update.

**Affected Areas:**

- Template doctrine (spec-workflow / dashboard rules), `/health-check` + `/audit-coherence` command surfaces. No project task impact (template-maintenance decision).
- Downstream projects pick up the doctrine + lens on next sync.

**Risks:**

- The advisory lens's fuzzy `criteria[]`↔box match can mis-cluster on heavily re-segmented criteria — mitigated by its advisory framing (human adjudicates; never auto-mutates).
- Cosmetic-staleness of inline boxes persists by design; if it proves annoying, the follow-up is to advise projects against rendering inline acceptance boxes (research Q2; deferred).
