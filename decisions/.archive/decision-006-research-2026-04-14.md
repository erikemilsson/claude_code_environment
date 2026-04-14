# Research Archive: DEC-006 — Phase gate flexibility for cross-phase long-running tasks

**Date:** 2026-04-14
**Researcher:** research-agent
**Decision record:** `decisions/decision-006-phase-gate-flexibility.md`
**Status when archived:** proposed

---

## Investigation Methodology

Investigation focused on the codebase (no web research needed — Q1/Q2 are answerable from the template's own domain coverage and the SIREN case in FB-013). The phase-gate semantics live in five touch points and each was inspected to understand cascade effects per option:

1. `task-schema.md` line 122 — the literal hard-gate rule and `phase` field definition
2. `phase-decision-gates.md` lines 11-56 — the enforcement procedure used by `/work` Step 2b
3. `commands/work.md` Step 2b/2c/3 routing — eligibility filters and dispatch
4. `parallel-execution.md` lines 22-32 — `eligible` filter currently includes `task.phase <= active_phase`
5. `verify-agent.md` Phase-Level Verification Workflow — when Tier 2 fires

Cross-checked rules: `rules/task-management.md` (parallel eligibility — uses dependency + file-conflict, no phase reference), `rules/spec-workflow.md` (no phase reference), `system-overview.md` lines 25, 107-110 (phase boundaries are real and Tier 2 fires per phase), `commands/breakdown.md` (subtasks inherit spec provenance from parent — phase inheritance is implicit), `decomposition.md` lines 42-75 (phase is assigned from spec section headings).

---

## Findings Per Question

### Q1: How common is the cross-phase pattern in non-software domains?

The pattern is structural to any domain where work is partly gated by external timelines. Concrete recurring task types:

- **Recruitment / participant scheduling** (research, workshops, user studies): SIREN case is canonical. Lead times of 2-6 weeks are the norm because invitations, scheduling polls, consent forms, and reminders all need elapsed wall-clock time independent of project milestones.
- **Procurement / vendor sourcing** (renovation, infrastructure, hardware): RFQs, vendor responses, contract negotiation, lead-time delivery. Often initiated in "design" phase but the artifact arrives during "build" phase.
- **Regulatory / legal approvals** (research IRB, planning permits, compliance review): Submission is early; approval timing is external.
- **Stakeholder coordination** (large org programs, public consultations): Pre-engagement, scheduling, follow-up cycles span planning and execution.

In all four categories, the task is almost always `owner: human` because Claude has no agency to actually execute the long-running activity — it can draft, prepare, remind, but the calendar time itself is owned by external actors. The few exceptions (e.g., Claude-drafted invitations, follow-up emails) are short, in-phase tasks in their own right.

**The mapping `cross-phase ⇔ owner: human` is high (~90%) but not perfect.** See Q2 for the residual.

### Q2: Software-domain cross-phase examples?

Yes, but rarer. The clearest are infrastructure/dependency tasks where Claude can act:

- **Vendor procurement for infrastructure** (managed DB account creation, third-party API key request, domain registration): often spans "design" and "build" — owner can be `human` (purchasing) or `both` (Claude drafts the request, human signs it).
- **Build/CI provisioning** (set up CI runner pool, request increased quotas, provision GPU instances): often `human` in regulated orgs, `claude` if Claude has the credentials.
- **Long-running data ingest / migration** (initial data backfill that runs hours/days): `claude`-owned but its "completion" can span phase boundaries — the migration starts in Phase 1 setup but doesn't finish until Phase 2 verification.
- **Documentation / changelogs that span phases** (e.g., "maintain ADR log throughout build"): `claude` or `both`-owned background work.

The Claude-owned cross-phase case is real but uncommon. A field-based mechanism handles it; an owner-only rule does not.

**External tools for comparison (general PM patterns, from prior knowledge):**
- Asana/Notion/Linear treat milestones and tasks as orthogonal — a task can carry a milestone but is not gated by it. The "phase gate" concept doesn't exist at the platform level; it's a project convention. Cross-milestone tasks are normal.
- Jira's release/version is similar — version is metadata, not a gate.
- Gantt-style tools (MS Project, OmniPlan) model "lag" and "lead" between dependent tasks; long-running activities are explicitly modeled with start/end dates that can overlap phases.
- CPM (critical path method) treats phases as reporting groupings, not eligibility constraints.

The template's hard-gate is unusually strict by industry norms — appropriate for software where build→test ordering is real, but not the dominant PM pattern.

### Q3: Auditability story per option

This is the most important differentiator. The dashboard currently has strong phase-boundary semantics (per `dashboard-regeneration.md` § "Phase Transitions"): tasks are grouped by phase, completed phases collapse, the phase table shows Done/Total/Status per phase, and phase gates render in Action Required.

**Option A (`cross_phase: true`):**
- A flagged task remains visible in its declared phase (e.g., "Phase 2 — Workshop") but is *eligible for dispatch* during Phase 1.
- Dashboard can render with a small visual marker (e.g., `🔀` or `(cross-phase)` annotation) so a Phase 2 task running during Phase 1 is unambiguous.
- Phase gate computation: when the gate evaluates "all Phase 1 tasks Finished?", it ignores the Phase 2 cross-phase task because that task isn't *in* Phase 1 — no semantic confusion.
- Audit trail: explicit. The flag is in the task JSON, surfaced in the dashboard, traceable in git history.
- **Confusion risk: low.** The user has explicitly opted in per task.

**Option B (weaken gate for `owner: human`):**
- A `human`-owned Phase 2 task can start during Phase 1 with no flag and no annotation. Just shows up in "Your Tasks" while Phase 1 is the "active phase".
- Dashboard's phase grouping becomes mildly misleading: "Phase 2" header now shows tasks that the user is actively working on, while the project state still reads "Phase 1 active".
- Phase table needs a new state — Phase 2 isn't "Active" (Phase 1 still is) but isn't "Blocked" either. Closest existing state is `Partially Actionable` (already defined in `dashboard-regeneration.md` line 165).
- **Confusion risk: medium.** The behavior is implicit. A user reviewing the dashboard might wonder "why is a Phase 2 task in Your Tasks if we're still in Phase 1?" The answer requires understanding the rule.
- **Mitigation:** the dashboard could explicitly note "Cross-phase: Phase 2 human tasks are open in parallel."

**Option C (both):**
- Best auditability per case (per-task explicit override + sensible automatic behavior for human tasks) but the user has to learn two mechanisms. When does `cross_phase` apply if `owner: human` already floats? Answer: only for Claude-owned cross-phase work — rare.
- **Confusion risk: low for the running project but moderate at the schema level** — two flags doing related-but-not-identical things invite "which do I use?" questions during decomposition.

### Q4: Tier 2 phase verification timing

This is the subtle one. From `verify-agent.md` line 555 + `system-overview.md` lines 107-110:

> Tier 2 runs after each phase completes — before the phase gate. This catches integration problems within Phase N before Phase N+1 builds on top of them.

And from `commands/work.md` Step 3 routing logic: Tier 2 fires when "all spec tasks are Finished AND all have passing verification" *for the current phase context*. The phase scope is implicit in which tasks belong to phase N.

**Option A:** When Phase N's tasks are all Finished, Tier 2 fires for Phase N — simple. The cross-phase task is in Phase N+1, so Phase N's Tier 2 is not waiting for it. Phase N+1's Tier 2 will eventually run when *all* Phase N+1 tasks are Finished, including the cross-phase one. Clean.

**Option B:** When Phase N's `claude`/`both` tasks are Finished but a `human` Phase N task is still pending (because it floats), what does the gate do? Two interpretations:

- *Strict B:* `human` tasks still count for Phase N completion — they just don't *block* Phase N+1 from starting. So Phase N's Tier 2 still waits for the human task. This is awkward: Phase N+1 work is happening, but Phase N is "not done" for verification purposes.
- *Loose B:* `human` tasks are excluded from phase completion checks entirely. Tier 2 fires when Phase N's non-human tasks complete. Then if a human task later updates a deliverable, there's no re-verification trigger. This breaks the "verify catches integration before next phase builds" guarantee.

Neither is clean. Option B forces a choice between weakening the verification trigger and weakening the float guarantee. **This is a real cost of Option B.**

Symmetric scenario for Option B applied to floating Phase N+1 human tasks: their Tier 2 belongs to Phase N+1, fires only when *all* Phase N+1 tasks (including those started early during Phase N) complete. That's fine — the floating task just gets verified as part of its declared phase, which is what we want.

**Option A handles Q4 cleanly because the task's `phase` field is the source of truth for which Tier 2 it belongs to. The `cross_phase` flag only changes eligibility, not phase membership.**

### Q5: Spec decomposition implications

**Option A (explicit flag):**
- `decomposition.md` would gain a paragraph: "If a task has external timing constraints (recruitment, procurement, approvals, long lead-times) and could reasonably start before its declared phase becomes active, set `cross_phase: true`."
- Decomposition heuristics: detect candidates by (a) `owner: human` + keywords like "recruit", "procure", "approve", "schedule", "engage", or (b) `external_dependency.expected_date` more than 2 weeks out, or (c) tasks the user has marked with priority "high" in a non-active phase.
- Suggestions can be presented as: "Task {id} ('{title}') looks long-lead. Mark as `cross_phase: true` so it can start during Phase {N-1}? [Y/N]".
- User can also add the flag via `/iterate` retrospectively.

**Option B (implicit by owner):**
- No decomposition change needed for the common case — `human` tasks float automatically.
- But decomposition still needs to *signal* to the user that some Phase N+1 tasks are open right now, otherwise the user won't know to pick them up. This is a UX problem more than a schema problem.
- For the rare Claude-owned cross-phase case, no mechanism exists — user must manually rephase the task.

**Option C (both):**
- Decomposition logic is the union: suggest the flag for Claude-owned long-leads, rely on owner for human tasks. But then the `cross_phase` flag is *redundant* on human tasks (no effect — they already float). Decomposition guidance has to clarify this. Likely confusing.

`/work` cannot reliably *infer* `cross_phase` from owner + dependency structure alone — the inference would need to know "this dependency would have been on a Phase N task that's already done" plus "this task's external timeline implies early start is desired." Both are project-context judgments. So if Option A is chosen, the flag is set during decomposition with user confirmation, not auto-inferred at dispatch time.

---

## Cascade Effects Per Option

What downstream files would each option require changing?

### Option A
- `task-schema.md` — add `cross_phase: bool` to optional fields table, reword line 122 to "Tasks in Phase N+1 are blocked until all Phase N tasks complete, *unless* `cross_phase: true`."
- `phase-decision-gates.md` — phase check loop unchanged, but task-skip logic at the bottom adds: "IF task.cross_phase: true → ignore phase gate, evaluate task-level eligibility only."
- `parallel-execution.md` line 29 — change `task.phase <= active_phase` to `task.phase <= active_phase OR task.cross_phase == true`.
- `commands/work.md` Step 3 routing — eligibility check needs the same OR clause.
- `commands/breakdown.md` — subtasks of a `cross_phase` parent inherit the flag.
- `decomposition.md` — heuristic guidance for when to suggest the flag.
- `dashboard-regeneration.md` — render `🔀` or `(cross-phase)` annotation in Tasks section; phase table unchanged because cross-phase task still belongs to its declared phase.
- `system-overview.md` line 25 — note exists in "Open questions" already; replace with the resolved policy.

### Option B
- `task-schema.md` line 122 — reword: "Tasks in Phase N+1 are blocked until all Phase N tasks with `owner: claude` or `owner: both` complete. `owner: human` tasks float across phases."
- `phase-decision-gates.md` — phase check needs to filter `owner != "human"` when computing "all tasks finished". Also need to define what happens to the Tier 2 trigger (see Q4).
- `parallel-execution.md` line 29 — change to `task.phase <= active_phase OR task.owner == "human"`.
- `commands/work.md` Step 3 + Step 1d (fast path) — affected: Step 1d "no Claude-actionable work" detection becomes more nuanced because human tasks across phases now all show up.
- `dashboard-regeneration.md` — likely needs a "Cross-phase work" annotation explaining why Phase N+1 human tasks appear during Phase N. Phase table needs treatment for Phase N+1 being "Partially Actionable due to floating human tasks."
- `verify-agent.md` Phase-Level Verification — needs explicit decision on whether Tier 2 waits for floating human tasks (see Q4).
- `system-overview.md` — note resolved policy; the gate semantics weaken.

### Option C
- Union of A + B + an explanatory section about which mechanism to use when. Largest doc surface area.

---

## Discarded Considerations

- **Spec-level "Phase 2 may begin during Phase 1" declarations** (FB-013 mentioned this): rejected as a bigger schema change. Belongs to spec frontmatter and adds parser complexity, while only solving one direction (whole-phase overlap, not per-task).
- **"Document the workaround" (move tasks to fit phases)**: rejected by FB-013 refinement — bends project structure to template, not vice versa.
- **Auto-inferring `cross_phase` from owner + dependency graph**: insufficient signal (see Q5).

---

## Recommended Path

**Option A.** Reasoning summarized in the decision record's Recommendation section. Key reasons:

1. Cleanly solves Q4 (Tier 2 timing) — the cross-phase flag changes eligibility without changing phase membership.
2. Handles both Q1 (common human-owned case) and Q2 (rare Claude-owned case) with one mechanism.
3. Smaller doc surface area than C, lower confusion risk than B.
4. Explicit and per-task — matches the template's overall preference for explicit configuration over implicit behavior (see e.g., `parallel_safe`, `interaction_hint`, `out_of_spec`).
5. Reversible: if the flag proves cumbersome, the next iteration could add Option B's owner-based default *on top* (auto-set `cross_phase: true` for human tasks during decomposition). Going B-first is harder to retreat from.

**Confidence:** moderate-to-high. The main residual uncertainty is decomposition UX — whether users will reliably set the flag without prompting. Mitigated by decomposition heuristics that suggest the flag.

---

## Sources Consulted

- `/Users/erikemilsson/Developer/claude_code_environment/.claude/support/reference/task-schema.md` (line 122 in particular)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/support/reference/phase-decision-gates.md`
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/support/reference/parallel-execution.md` (line 29)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/support/reference/decomposition.md` (lines 42-75)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/support/reference/dashboard-regeneration.md` (phase rendering)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/commands/work.md` (Steps 2b, 2c, 3, 1d)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/agents/verify-agent.md` (Phase-Level Verification, lines 555-705)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/rules/task-management.md`
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/rules/spec-workflow.md`
- `/Users/erikemilsson/Developer/claude_code_environment/system-overview.md` (lines 25, 49-110)
- `/Users/erikemilsson/Developer/claude_code_environment/.claude/support/feedback/feedback.md` (FB-013)
- General PM-tool prior knowledge for Q2 (Asana, Linear, Jira, Gantt-based tools)
