---
id: DEC-006
title: Phase gate flexibility for cross-phase long-running tasks
status: approved
category: architecture
created: 2026-04-14
decided: 2026-04-14
related:
  tasks: []
  decisions: []
  feedback: [FB-013]
implementation_anchors: []
inflection_point: true
spec_revised:
spec_revised_date:
blocks: []
---

# Phase gate flexibility for cross-phase long-running tasks

## Select an Option

Mark your selection by checking one box:

- [x] Option A: Add optional `cross_phase: true` field on individual tasks
- [ ] Option B: Weaken phase gate to only block on `owner: claude` / `owner: both` tasks
- [ ] Option C: Both — `cross_phase` field AND weakened gate

*Check one box above, then fill in the Decision section below.*

---

## Context

The task schema enforces a hard phase gate: *"Tasks in Phase N+1 are blocked until all Phase N tasks complete"* (`task-schema.md` line 122). This works for software, where phase boundaries represent strict dependency transitions (can't test until built).

It breaks for non-software domains. In the SIREN research project, workshop participant recruitment (Phase 2) needed to start weeks before all Phase 1 preparation tasks were done. Two pre-session Phase 1 tasks had zero logical connection to recruitment but the phase gate blocked all of Phase 2. The workaround was to reshuffle tasks across phases — solving the immediate problem but forcing the project's natural structure to bend around the environment's constraints.

This pattern (long-running human work — recruitment, procurement, approvals, stakeholder engagement — that must start early) is representative of research/procurement/stakeholder domains, not a one-off. These tasks are almost always `owner: human` and their timelines are driven by external factors, not phase completion.

`rules/task-management.md` already uses dependency+file-conflict eligibility for parallel execution without referencing phase — FB-013 is consistent with that underlying model. The question is which flexibility mechanism best matches real usage patterns.

## Questions to Research

1. **How common is the cross-phase pattern in non-software domains?** Beyond SIREN, look at what kinds of tasks recur: procurement lead times, legal approvals, recruitment windows, stakeholder coordination. Do these consistently map to `owner: human`?
2. **Are there software-domain examples** where cross-phase tasks also make sense? (E.g., vendor procurement for infrastructure before the build phase begins.)
3. **What's the auditability story** under each option? If a Claude-owned Phase 2 task runs while Phase 1 still has human tasks pending, does that create confusing state in the dashboard/verification?
4. **Does the choice affect Tier 2 phase verification?** Tier 2 runs when "all phase tasks finished with passing Tier 1." If `owner: human` tasks float freely, when does Phase N's Tier 2 fire?
5. **Spec decomposition implications:** does the user need to mark tasks `cross_phase: true` during decomposition, or can `/work` infer it from owner + dependency structure?

## Options Comparison

| Criteria | A: cross_phase field | B: Weaken gate for human | C: Both |
|----------|---------------------|--------------------------|---------|
| Per-task granularity | Yes | No (all human tasks float) | Yes |
| Requires user opt-in | Yes (per task) | No | Partial |
| Schema change | Add 1 field | Reword rule (no field) | Add 1 field + reword rule |
| Matches SIREN case | Yes (flag recruitment) | Yes (human tasks float) | Yes |
| Risk of surprising behavior | Low (explicit) | Medium (implicit) | Low |
| Handles Claude-owned cross-phase | Yes | No | Yes |
| Tier 2 verification timing | Clean — task stays in declared phase | Awkward — see Q4 (forces tradeoff between weak gate and weak Tier 2 trigger) | Clean (uses A's mechanism for the cases that matter) |
| Dashboard confusion risk | Low — small annotation suffices | Medium — Phase N+1 tasks visible during Phase N with no explicit flag | Low |
| Doc surface area touched | 7 files (schema, gates, parallel, work, breakdown, decomposition, dashboard) | 6 files (above minus breakdown/decomposition; adds verify-agent) | Union of both — largest |
| Reversibility | Easy — drop the field | Hard — re-introducing the gate would break projects relying on float | Hard for B leg, easy for A leg |
| Decomposition UX | Heuristics suggest flag for long-leads + user confirms | Automatic for human tasks; nothing for Claude-owned | Two mechanisms — "which do I use?" |
| Overall | Strongest balance | Solves common case but with hidden costs | Most flexible, most complex |

**Recommendation: Option A** — see § Recommendation below.

## Option Details

### Option A: `cross_phase: true` field

**Description:** Add an optional boolean field `cross_phase` to the task schema. When `true`, the task is exempt from the phase gate — eligible to start when its task-level dependencies are met, regardless of prior phase completion. Default: `false` (current behavior). Requires user to flag tasks explicitly, either at decomposition time or via `/iterate`.

**Strengths:**
- Explicit and per-task — no surprising behavior
- Handles Claude-owned cross-phase tasks (rare but possible, e.g., provisioning infrastructure)
- Minimal schema change
- Opt-in preserves existing software-domain guarantees
- Tier 2 verification timing stays clean: cross-phase tasks belong to their declared phase for verification purposes; only their *eligibility* changes
- Pattern matches existing template idioms (`parallel_safe`, `interaction_hint`, `out_of_spec` — all opt-in flags)

**Weaknesses:**
- Requires user to remember to set the flag (mitigated by decomposition heuristics)
- `/work` decomposition must learn when to suggest the flag

**Research Notes:**
Decomposition can suggest the flag when it sees: `owner: human` + keywords like recruit/procure/approve/schedule, or `external_dependency.expected_date` more than 2 weeks out, or task placed in non-active phase with priority "high". `/work` cannot reliably *infer* the flag at dispatch time without project context, so the flag is set during decomposition with user confirmation rather than auto-inferred. Subtask inheritance: subtasks of a `cross_phase` parent inherit the flag (extend `breakdown.md`). Dashboard rendering: small `🔀` or `(cross-phase)` annotation in the Tasks section; phase table rendering is unchanged because the task still belongs to its declared phase. See archive § "Cascade Effects Per Option".

Files affected: `task-schema.md` (line 122 + new field row), `phase-decision-gates.md` (skip rule), `parallel-execution.md` (line 29 OR clause), `commands/work.md` (Step 3 routing eligibility), `commands/breakdown.md` (subtask inheritance), `decomposition.md` (heuristic guidance), `dashboard-regeneration.md` (annotation), `system-overview.md` (line 25 — close out the open question).

Full rationale: `decisions/.archive/decision-006-research-2026-04-14.md`

### Option B: Weaken gate for `owner: human`

**Description:** Change the phase gate rule: only block on `owner: claude` and `owner: both` tasks in Phase N; `owner: human` tasks are allowed to float across phases. Their timelines are external and phase-independent.

**Strengths:**
- No schema change
- No user opt-in required — works automatically for the common case (research/procurement/stakeholder projects)
- Aligns phase gate semantics with what actually blocks downstream work (Claude-owned deliverables)

**Weaknesses:**
- Doesn't handle Claude-owned cross-phase tasks (vendor procurement, infrastructure provisioning, long-running data ingest)
- Implicit — users might be surprised that Phase 2 is "active" while Phase 1 has human tasks pending
- Tier 2 verification timing becomes fuzzy: forces a choice between (a) Tier 2 still waits for floating human tasks (then Phase N is "not done" while Phase N+1 work happens — awkward) or (b) Tier 2 ignores human tasks (breaks the "verify before next phase builds" guarantee)
- Dashboard semantics need rework: phase grouping currently implies "this phase is active right now" — that breaks if Phase N+1 human tasks are open during Phase N
- Hard to retreat from: projects that adopt the float would break if the gate were re-tightened

**Research Notes:**
The Tier 2 timing problem is the deepest cost. From `verify-agent.md` line 555 + `system-overview.md` lines 107-110, Tier 2 fires when all phase tasks complete and runs *before* the phase gate so Phase N+1 doesn't build on unverified Phase N work. If `owner: human` tasks float and are excluded from phase completion, Tier 2 fires without seeing their deliverables; if they're included, Phase N stays in "not done" indefinitely while N+1 progresses. Neither variant is clean. See archive § Q4 for the full analysis.

Dashboard impact: `dashboard-regeneration.md` would need a new "Cross-phase work" annotation explaining why Phase N+1 human tasks appear during Phase N, and the Phase table needs treatment for Phase N+1 being "Partially Actionable due to floating human tasks."

Files affected: `task-schema.md`, `phase-decision-gates.md`, `parallel-execution.md`, `commands/work.md` (Steps 1d, 2b, 3), `dashboard-regeneration.md`, `verify-agent.md` (Tier 2 trigger), `system-overview.md`.

Full rationale: `decisions/.archive/decision-006-research-2026-04-14.md`

### Option C: Both

**Description:** Weaken the gate for `owner: human` (Option B's semantics) AND add `cross_phase: true` for explicit per-task control (Option A's semantics). Most flexible.

**Strengths:**
- Covers every case
- Per-task override available

**Weaknesses:**
- Two mechanisms doing similar things
- Users may be confused when to use which (`cross_phase` is a no-op on `human` tasks under B's float, redundant flag)
- More schema surface area
- Inherits B's Tier 2 timing problem and dashboard rework cost

**Research Notes:**
The composition isn't additive — B's mechanism makes the flag redundant for the most common cases (human tasks already float), so the flag exists primarily for the rare Claude-owned case. That's fine in principle but invites "do I need both?" confusion during decomposition. If the goal is "cover all cases," Option A already does so via the explicit flag — the float in B is a UX shortcut, not a capability A lacks.

Files affected: union of A and B — largest doc surface area.

Full rationale: `decisions/.archive/decision-006-research-2026-04-14.md`

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision.*

**Constraints:**
- Template-maintenance decision record — ephemeral, removed after resolution
- Must work in both software and non-software domains (domain agnosticism is a template principle)
- Should not break Tier 2 phase verification semantics

**Research Questions** (surfaced for user consideration; do not block decision):
- Should the dashboard's phase table get a new column or annotation for cross-phase tasks (regardless of which option), to make their "phase membership vs. eligibility" distinction visible at a glance?
- For Option A: is auto-suggesting `cross_phase: true` during decomposition (with user confirmation) the right level of automation, or should it be entirely manual?
- For Option A: should `cross_phase` tasks appear in the phase gate's "all conditions met" enumeration as an informational note (e.g., "Phase 2 has 1 cross-phase task already running") so the user sees the cross-phase activity at the gate?

## Recommendation

**Recommended: Option A — `cross_phase: true` field.**

Key reasons:

1. **Cleanly solves the Tier 2 verification timing problem (Q4).** A cross-phase task changes its *eligibility* without changing its *phase membership*. Phase N's Tier 2 fires when Phase N's tasks are done; the cross-phase task gets verified as part of Phase N+1 where it belongs. Option B forces a choice between weakening the verification trigger or letting Phase N stay "not done" while N+1 work happens — neither is clean.
2. **Handles both common (Q1 — human-owned recruitment/procurement) and rare (Q2 — Claude-owned infrastructure provisioning) cases with one mechanism.** Option B punts on Q2 entirely.
3. **Lower confusion risk than B.** Per-task explicit opt-in matches the template's overall preference for explicit configuration over implicit behavior — same shape as `parallel_safe`, `interaction_hint`, `out_of_spec`.
4. **Smaller doc surface area than C** with no functional gap.
5. **Reversible.** If the flag proves cumbersome, the next iteration can layer Option B on top (auto-set `cross_phase: true` for human tasks during decomposition). Going B-first is hard to retreat from — projects relying on the float would break if the gate were re-tightened.

**Key tradeoff:** Option A puts a small ongoing cost on decomposition (user must remember the flag, with assistance from heuristics) in exchange for explicit, auditable, low-risk semantics. Option B trades that small ongoing cost for a one-time architectural risk (Tier 2 trigger ambiguity, dashboard semantics rework, irreversibility).

**Confidence:** moderate-to-high. Residual uncertainty is whether decomposition heuristics will reliably surface the flag suggestion — addressable with iteration after first usage.

Full investigation notes: `decisions/.archive/decision-006-research-2026-04-14.md`
