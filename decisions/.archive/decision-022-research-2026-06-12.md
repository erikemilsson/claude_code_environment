# DEC-022 Research Archive — Spec acceptance-criteria ↔ phase-verification reconciliation

**Decision:** `decisions/decision-022-acceptance-criteria-reconciliation.md`
**Date:** 2026-06-12
**Investigator:** research-agent (general-purpose, opus[1m]), dispatched by `/research` (template-maintenance adaptation)
**Source feedback:** FB-097 (bridged from flirty-gym, template_version 4.7.1)

---

## Methodology

Template-internal design decision: most evidence is from reading the template's own files; one bounded external pass on requirements-traceability precedent (Q4).

**Files read (read-only):** `decisions/decision-022-*.md` (drafted record + 7 questions); `decisions/decision-016-spec-file-edit-guardrail.md` (the decision Option B amends — two-layer structure, Q1/Q4/Q7 findings); `.claude/rules/spec-workflow.md` (DEC-016 section + "Source of Truth"); `.claude/agents/verify-agent.md` (`criteria[]` artifact + return schema, phase-level mode); `.claude/commands/work.md` + `.claude/support/reference/work-procedures.md` (completion flow / `status:` flip); `.claude/support/reference/drift-reconciliation.md` (fingerprint + reconciliation reset); `.claude/settings.json` (`permissions.ask` globs); `.claude/commands/health-check.md` + `.claude/commands/audit-coherence.md` (lens sites; confirmed no existing coverage); `.claude/rules/feature-retirement.md` (don't-mutate-spec-body precedent); `.claude/spec_v1.md` + `.claude/support/reference/spec-checklist.md` (Q3 — boxes not mandated); `.claude/support/reference/dashboard-regeneration.md` (the existing `### Acceptance Criteria` rendering); `.claude/support/reference/task-schema.md` + `decomposition.md` + `implement-agent.md` (Q7 — no per-task box).

**External searches (Q4):** requirements-traceability matrix status handling; BDD/Gherkin living documentation; IBM DOORS verification-status reconciliation. Sources listed at the foot of this document.

---

## Detailed findings per question

### Q1 — DEC-016 carveout mechanics (LOAD-BEARING)

**Finding: Option B is implementable, but inherits a structural gate it cannot scope to "box-tick only."**

Two layers, confirmed by direct read:

- *Behavioral* (`spec-workflow.md § "Direct edits to spec, decision, and vision files (DEC-016)"`): substantive spec text edits route through `/iterate`; "infrastructure operations remain autonomous — archiving, version transitions, and frontmatter updates." A box-tick is **body text**, not frontmatter → NOT in the autonomous carveout today. Option B requires *adding* "acceptance-box state-sync" to that enumeration. That addition is itself a DEC-016-governed change → correctly routed via this decision record, not a direct edit.
- *Structural* (`.claude/settings.json`): `"Edit(.claude/spec_v*.md)"` + `"Write(.claude/spec_v*.md)"` in `permissions.ask`. Per DEC-016 Q3, `ask` rules **cannot be scoped to a sub-operation** — there is no "Edit-that-only-flips-a-checkbox" predicate. The orchestrator's box-tick Edit hits the prompt.

**Quantified friction:** File-modification `ask` prompts support session-bounded "Yes, don't ask again" (DEC-016 Q4/Q7). A phase-close is rare → ~1 click per phase-closing `/work` session, on par with `/iterate apply`. **Not friction-disqualified.**

**Caveats unique to B:** (a) provenance not platform-trackable (DEC-016 Q1 re-confirmed: `PreToolUse` JSON has no slash-command-source field) — the gate can't distinguish "blessed box-tick" from "Claude rationalizing a spec edit," so every phase-close trains the user to click "yes" on a spec-edit prompt (habituation erosion on the exact path DEC-016 hardened); (b) `ask` pre-empts the auto-mode classifier, so the click is carried into auto-mode too.

**Verdict:** clears the implementability bar; inherits a gate it cannot narrow; trains click-through. A thumb on the scale away from B, not disqualifying by itself.

### Q2 — Mapping fidelity `criteria[]` ↔ inline boxes (LOAD-BEARING) — decisive against B

**Finding: No reliable structural mapping exists. The correspondence is free-text and re-segmented by design.**

From `verify-agent.md`: `criteria[]` entries are `{"name": "...", "status": "pass"|"fail", "notes": "..."}` (Step 7 schema, line 690), `name` is **verifier-composed free text**, not a stable ID. Step 3 (lines 572–583) builds the table from "each acceptance criterion," but phase-level verification **re-segments**: "Focus phase-level verification on cross-task integration and end-to-end acceptance criteria" (line 561); criteria may be split per-task / merged / reworded. No `criterion_id`, `spec_box_ref`, or line anchor links a `criteria[]` entry to an inline box. Matching ⇒ fuzzy string match between verifier-composed `name` and spec box text — the semantic-name-matching that `task-management.md § "Audit Tasks"` and DEC-016 both flag as a recurring false-positive source.

**Failure modes B would introduce:** N:1 / 1:N correspondence (merge/split — which box ticks?); partial PASS (`criteria_failed > 0` — some boxes must stay `[ ]`, fuzzy matcher must route each correctly); authored-but-unverified boxes (folded into "end-to-end" coverage → B leaves them `[ ]` forever, silently reproducing the flirty-gym symptom); orphan ticks.

**Implication:** B's safety depends on a mapping the system doesn't structurally support. To make B safe you'd first add stable criterion↔box IDs to *both* the spec convention *and* the `criteria[]` schema — a far larger change that itself pushes toward a trace-link (C) + derived-view (A) model. **This is the strongest single argument against B.**

### Q3 — Convention scope

**Finding: The template prescribes an "Acceptance Criteria" section but never mandates `- [ ]` rendering.** `spec_v1.md` (full read) lists `Acceptance Criteria (how you'll know it works)` in an HTML-comment scaffold with no checkbox syntax and explicit "use whatever structure fits." `spec-checklist.md` requires *testability* ("Acceptance criteria map to clear verification steps"), never *rendering*. The only `- [x]`/`- [ ]` acceptance checklist the template *generates* is the dashboard's `### Acceptance Criteria` from `criteria[]` (`dashboard-regeneration.md:308–316`). **The template's own acceptance-status surface is the dashboard, not the spec.** ⇒ a heavyweight orchestrator-writes-spec mechanism (B) is disproportionate for an optional rendering; favor declaration (A) + optional-convention guidance.

### Q4 — External precedent

**Finding: Dominant pattern across RTM / BDD / DOORS is "single source + derived status view"; writing pass/fail into authored prose is the anti-pattern.**

- **RTM tools** (TestRail, Parasoft, Stell): the matrix carries `status`/`verification method` as **columns** — a derived projection linking requirement ID → test cases → results. Requirement text is not edited with checkmarks.
- **BDD/Gherkin living documentation** (Cucumber/SpecFlow/Serenity, TestQuality): `.feature` is the single authored source; pass/fail tracked in a **separate execution surface**; the feature file is edited for *meaning* during refinement, never annotated per-run with results.
- **DOORS** (IBM ERM): verification status is a **separate attribute** + links to test cases/results; reconciliation marks test cases "suspect" rather than rewriting requirement text. IBM guidance *discourages* embedding status in requirement table cells — a direct caution against B.

**Mapping:** "single source + derived view" → A (and the template already implements its mechanism via the dashboard); "trace-link carrying status" → C; "bidirectional sync of authored doc" → B, the least-attested and explicitly cautioned-against pattern.

### Q5 — Drift-detection interaction

**Finding: B generates drift noise it must actively suppress; A and C are clean.**

`drift-reconciliation.md`: `section_fingerprint = sha256(heading + all content until next ## or EOF)`. A checkbox line is inside that content → a tick changes the hash. Consequence: a changed section groups its tasks for reconciliation, and **applying reconciliation to a Finished task clears its `task_verification` and resets it to Pending** (lines 294–300). So a naive box-tick on a section containing Finished tasks could, on the next `/work` Step 1b, prompt to **reset verified work to Pending** — the precise harm `feature-retirement.md § "Spec Annotation (do NOT excise)"` warns about. B would be the template's first sanctioned spec-body mutation outside `/iterate` and needs a drift-suppression carveout (re-baseline `section_fingerprint`/`subsection_fingerprint` for affected tasks, or exclude checkbox-only diffs from hashing) — fiddly, and at `### ` granularity too (DEC-021). A declares boxes informational → no spec edit; C only reads → no spec edit. **Only B pays this cost.**

### Q6 — Doctrinal coherence with "spec is the living source of truth"

**Finding: A is consistent with the principle; B is in tension.**

Canonical statement (`spec-workflow.md:5`): *"The spec is the living source of truth. All work aligns with it, **or the spec is updated intentionally.** Tasks follow the spec, not the other way around."*

Two reasons A is coherent: (1) acceptance *criteria* (authored "what must be true") ≠ acceptance *status* (verified "is it true now"); the spec is authoritative for the criteria, never for runtime PASS/FAIL state — which the template routes to `verification-result.json` + dashboard. Declaring inline boxes "authored, informational on status" doesn't demote the spec as source of truth for *criteria*. (2) "updated intentionally" means deliberate flows (`/iterate`), not automated status reflection — an auto-flip on every PASS is *incidental* mirroring, so B is the option in tension; A preserves the clause. A's only cost is cosmetic staleness, bounded to box-rendering projects — which C patches.

### Q7 — Scope vs per-task verification

**Finding: No analogous per-task gap; per-task is structurally reconciled.** Spec acceptance criteria are read as *input* by implement-agent/decomposition (`implement-agent.md:52,95`, `decomposition.md:11`), not maintained as a per-task checklist. Task schema has no `acceptance[]`/inline-box field; the structural artifact is `task_verification`, and `Finished ⇔ task_verification.result == "pass"` is enforced in `work.md`, `health-check.md` Part 1 check 7, `task-management.md`, and the Critical Invariants. The FB-097 gap is exclusively phase-level. Reinforces A: the template already treats the structured verification artifact as authoritative and the rendering as derived.

---

## Full options comparison matrix (13 criteria)

Scoring: ✓✓ strong / ✓ acceptable / – neutral-conditional / ✗ weak. D = A + C.

| Criterion | A | B | C | D (A+C) |
|---|---|---|---|---|
| Implementation complexity | ✓✓ Low (prose) | – Medium (amend + tick + drift-suppress + fuzzy match) | ✓ Low–med (read-only lens) | ✓ Low–med (no spec-mutating code) |
| Keeps source-of-truth honest (status) | – Stale; "read dashboard" | ✓✓ Reflects PASS if mapping right (Q2) | ✓ Surfaces + prompts | ✓✓ Doctrine clean + caught |
| DEC-016 amendment required | ✓✓ None | ✗ Yes | ✓✓ None | ✓✓ None |
| Drift-detection interaction | ✓✓ None | ✗ Suppress; risk Finished→Pending | ✓✓ None | ✓✓ None |
| Mapping safety | ✓✓ N/A | ✗ Unsafe (Q2) | ✓ Advisory | ✓✓ A removes need; C advisory |
| Friction per phase-close | ✓✓ Zero | ✓ ~1 click; trains click-through | ✓✓ Zero | ✓✓ Zero added |
| Reversibility | ✓✓ Trivial | ✓ Revert + un-amend | ✓✓ Trivial | ✓✓ Easy |
| Works under auto mode | ✓✓ Behavioral | – Still prompts | ✓✓ Read-only | ✓✓ Yes |
| Doctrinal coherence (Q6) | ✓✓ Coherent | – Tension | ✓ Neutral | ✓✓ Coherent + proper-flow |
| External-precedent alignment (Q4) | ✓✓ single-source+derived | ✗ mutate-doc (discouraged) | ✓ trace-link | ✓✓ both attested |
| Blast radius | ✓✓ Doc-only | – Completion flow + permission doctrine | ✓✓ Additive lens | ✓ Doc + lens |
| Solves flirty-gym symptom | ✓ Reframes | – Only if mapping right | ✓✓ Detects & surfaces | ✓✓ Reframed + flagged |
| Habituation / protection erosion | ✓✓ None | ✗ Trains "yes" on spec edits | ✓✓ None | ✓✓ None |

---

## Recommendation (full)

**Option D = A + C.** Confidence: **High** on rejecting B / anchoring on A; **Moderate** on bundling C now vs deferring.

**Evidence base:** (1) Q2 + Q5 + Q4 jointly disqualify B's mechanism despite Q1's cheap friction — can't safely auto-tick from free-text re-segmented `criteria[]` without first building criterion↔box IDs, which converts the design into A+C anyway. (2) Q4 + the template already rendering `criteria[]` as `### Acceptance Criteria` → A formalizes an existing pattern. (3) Q6 → A preserves "updated intentionally" better than B. (4) Q3 → boxes not mandated, B disproportionate. (5) Q7 → bounded to phase-level; A extends the template's existing doctrine.

**Minimum-change alternative: A alone** — declaration + `/health-check` note, no lens. Fully closes the FB-097 governance gaps; C is the safety-net upgrade, not a correctness requirement. Ship A; add C if box-divergence is observed annoying in a real multi-phase project.

**Against the capture's lean:** FB-097 leaned B; the research does not support B's mechanism (implementable but unsafe as specified + costlier). For "keep the source-of-truth honest," C achieves the intent without B's mechanism.

**Version bump:** MINOR (new doctrine + optional lens; no permission-layer or task-schema change — contrast DEC-016's MAJOR).

## Implementation surface (D = A + C)

*A (doctrine):* `.claude/rules/spec-workflow.md` (declare status authority); `.claude/rules/dashboard.md` (note `### Acceptance Criteria` authoritative); `.claude/commands/health-check.md` (informational note); `.claude/CLAUDE.md` Critical Invariants (optional 1-line xref); the decision record (→ implemented + anchors); `.claude/version.json` (MINOR).
*C (lens):* `.claude/commands/audit-coherence.md` (7th `acceptance-reconciliation` lens; finding `kind: decision` → fix via `/iterate`; advisory fuzzy match; cluster per phase); shared audit-contract touch only if needed.
*Zero edits* to `verify-agent.md`, `work.md` completion flow, `settings.json`, `drift-reconciliation.md`.

## Open questions for the user

1. Bundle C now (D), or ship A alone with C gated on a 2nd observed occurrence?
2. Should the template advise *against* rendering inline acceptance boxes at all (dashboard is the live surface) — which would make C largely moot?
3. Confirm B is off the table (or is there a strong reason to want the spec body to show live PASS, justifying the larger criterion↔box-ID prerequisite)?

---

## External sources (Q4)

- TestRail — Requirements Traceability Matrix guide: https://www.testrail.com/blog/requirements-traceability-matrix/
- Parasoft — DO-178C requirements traceability: https://www.parasoft.com/learning-center/do-178c/requirements-traceability/
- Stell Engineering — RTM blog: https://stell-engineering.com/blog/requirements-traceability-matrix
- lastminute.com tech — Living documentation with BDD / Cucumber / Serenity: https://technology.lastminute.com/living-doc-bdd-cucumber-serenity/
- TestQuality — Gherkin user stories & acceptance criteria guide: https://testquality.com/gherkin-user-stories-acceptance-criteria-guide/
- IBM Jazz.net — Reconcile requirement collections with DOORS test plans: https://jazz.net/help-dev/clm/topic/com.ibm.rational.test.qm.doc/topics/t_reconcile_reqcolls_doors.html
- IBM Jazz.net — Managing Traceability to Test Cases and Test Results (DOORS): https://jazz.net/doors-general/html/599%20-%20Managing%20Traceability%20to%20Test%20Cases%20and%20Test%20Results.html
