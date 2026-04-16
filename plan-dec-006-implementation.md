# DEC-006 Implementation Plan — `cross_phase` field (Option A)

**Purpose:** Execute DEC-006 Option A across 9 files. Add an optional `cross_phase: true` boolean field to the task schema that exempts a task from the phase gate on eligibility checks while preserving its phase membership for verification. A fresh session can read this plan and execute without re-deriving context.

**Status:** Ready to execute
**Created:** 2026-04-17
**Upstream:** Template upgrade tracker `template-upgrade-2026-04.md`, Phase 1
**Cleanup tag:** DELETE-AFTER (tracked in upgrade tracker's Cleanup Manifest)

**Note:** DEC-006 is an **inflection point**. After commit, `/work` behaviour change is observable to downstream projects. The commit message + post-execution tracker update note that users running `/work` may be nudged toward `/iterate` when they next hit a phase boundary.

---

## Context to Load Before Executing

Read these in order at session start:

1. `template-upgrade-2026-04.md` — upgrade phase state
2. `decisions/decision-006-phase-gate-flexibility.md` — decision + full research (option A selected)
3. Current state of the 9 target files listed in Per-File Change Specs

Then execute this plan.

---

## Approved Context

### The decision (locked)

DEC-006 Option A: **Add an optional `cross_phase: true` boolean field on individual tasks.** When `true`, the task is exempt from the phase gate — eligible to start when its task-level dependencies are met, regardless of prior phase completion. Default: `false` (absent → treated as `false`). Opt-in, per-task.

### Why Option A works (verified research, still current)

- Preserves Tier 2 verification timing: cross-phase tasks change *eligibility* without changing *phase membership*. Phase N's Tier 2 fires when Phase N's own tasks are done; the cross-phase task is verified as part of its declared phase (N+1 or later).
- Handles both common cases (human-owned recruitment/procurement) and rare cases (Claude-owned infrastructure provisioning) with one mechanism.
- Reversible: if the flag proves cumbersome, Option B (weaken gate for human tasks) can layer on top later. Going B-first is hard to retreat from.
- Pattern matches existing template idioms (`parallel_safe`, `interaction_hint`, `out_of_spec` — all opt-in flags defaulting to absent/false).

### Approved judgment calls (locked for execution)

1. **Dashboard annotation style:** text suffix `(cross-phase)` after the task title in the Tasks section. No emoji glyph. Example row: `| 2.3 | Recruit workshop participants (cross-phase) | Pending | …`. The phase table remains unchanged (task still belongs to its declared phase).
2. **Decomposition auto-suggest:** when a task matches `owner: human` AND (title/notes contain recruit/procure/approve/schedule/coordinate/stakeholder/vendor/contract OR `external_dependency.expected_date` more than 14 days out), decomposition surfaces a suggestion: `"Task {id} looks like long-lead work. Mark as cross_phase: true? [Y/N]"`. Never set silently.
3. **Subtask inheritance:** subtasks of a `cross_phase: true` parent inherit the flag automatically during `/breakdown`. Subtask JSON includes `cross_phase: true` at creation time. User can manually remove it from individual subtasks if needed.
4. **Health-check validation (minor addition beyond the decision record):** Part 1 Check 1 gets one line noting that `cross_phase` must be a boolean when present. Consistent with how other optional boolean fields are currently validated.
5. **Field defaulting rule:** absent `cross_phase` or `cross_phase: false` → same behaviour (current phase gate applies). Only `cross_phase: true` activates the exemption. No schema migration for existing tasks.

---

## Design Contract — Field Behaviour

**Schema:**
```json
{
  "id": "2.3",
  "phase": "2",
  "cross_phase": true,
  ...
}
```

**Semantics:**
- **Phase membership:** unchanged. Task belongs to `phase: "2"` for all dashboard rendering, Tier 2 verification grouping, phase completion detection.
- **Eligibility:** exempt from the phase gate. `/work` Step 2b does not block the task on "Phase 1 still in progress." Standard task-level dependencies (`dependencies`, `decision_dependencies`, `files_affected` conflicts) still apply.
- **Tier 2 verification:** task is included in its declared phase's Tier 2 verification bundle. If Phase 2's Tier 2 fires, the cross-phase task must have passing per-task verification like any other Phase 2 task.
- **Dashboard:** task appears in its declared phase section with `(cross-phase)` suffix. No separate section, no phase-table column change.

**Deliberately not included in this decision:**
- Auto-setting `cross_phase: true` during decomposition (only *suggest*, never silent-set)
- Floating all `owner: human` tasks (that would be Option B)
- New phase gate informational note ("Phase 2 has 1 cross-phase task running") — proposed in decision's "Research Questions for later" but not approved in this commit

---

## Per-File Change Specs

### File 1: `.claude/support/reference/task-schema.md`

**Editing strategy:** Two targeted `Edit` calls.

**Edit 1 — update the `phase` field row (line 122):** append a sentence about the `cross_phase` escape hatch.

**Before:**
```
| phase | String | Phase identifier this task belongs to (e.g., "1", "2"). Tasks in Phase N+1 are blocked until all Phase N tasks complete. |
```

**After:**
```
| phase | String | Phase identifier this task belongs to (e.g., "1", "2"). Tasks in Phase N+1 are blocked until all Phase N tasks complete, unless the task has `cross_phase: true` (see below). |
```

**Edit 2 — add new `cross_phase` row to the fields table:** place it alphabetically adjacent to `parallel_safe` (line 125) since both are opt-in eligibility flags. Suggested position: immediately after the `parallel_safe` row.

**New row:**
```
| cross_phase | Boolean | When true, task is exempt from the phase gate — eligible when its `dependencies`/`decision_dependencies` are met, regardless of prior phase completion. Phase membership is unchanged (task still belongs to its declared phase for verification and dashboard rendering). Use for long-lead work (procurement, recruitment, approvals) that must start before prior phase is fully done. Default: false. |
```

**Verify after edits:** grep confirms both changes; the `phase` row mentions `cross_phase`; the new row is present with correct Boolean type.

---

### File 2: `.claude/support/reference/phase-decision-gates.md`

**Editing strategy:** Targeted `Edit` in the Phase Check procedure (line 51-55).

**Before:**
```
   For target task(s):
   IF task.phase > active_phase:
     "Task {id} is in Phase {task.phase}, but Phase {active_phase} is still in progress.
      {N} tasks remaining in Phase {active_phase}."
     → Skip this task, work on active-phase tasks instead
```

**After:**
```
   For target task(s):
   IF task.phase > active_phase AND task.cross_phase != true:
     "Task {id} is in Phase {task.phase}, but Phase {active_phase} is still in progress.
      {N} tasks remaining in Phase {active_phase}."
     → Skip this task, work on active-phase tasks instead

   IF task.phase > active_phase AND task.cross_phase == true:
     → Cross-phase task — bypass gate. Proceed to task-level dependency/decision checks.
     → Log: "Task {id} is cross-phase (Phase {task.phase}) — eligible despite active Phase {active_phase}."
```

**Also add** a short section at the end of the Phase Check block (before the `---` separator at line 58) explaining the exemption:

```markdown

### Cross-Phase Tasks

Tasks with `cross_phase: true` (see `task-schema.md`) are exempt from the phase gate on eligibility checks only. They still belong to their declared phase for verification and dashboard rendering. Typical use: long-lead human work (recruitment, procurement, approvals) that must start before the prior phase is fully done.
```

---

### File 3: `.claude/support/reference/parallel-execution.md`

**Editing strategy:** Single targeted `Edit` to line 29 in the eligibility block.

**Before:**
```
  - task.phase <= active_phase (no phase dependency blocks the task)
```

**After:**
```
  - task.phase <= active_phase OR task.cross_phase == true (no phase dependency blocks the task)
```

No other changes to this file.

---

### File 4: `.claude/commands/work.md`

**Editing strategy:** Single targeted `Edit` to the Step 2c summary line (line 367).

**Before:**
```
**Summary:** Read `parallel_execution` from spec frontmatter (defaults: `enabled: true`, `max_parallel_tasks: 3`). Eligible tasks must be Pending, not human-owned, all deps Finished, in active phase, all decision deps resolved, difficulty < 7. Build conflict-free batch by pairwise-comparing `files_affected`. If batch >= 2, set `parallel_mode = true`.
```

**After:**
```
**Summary:** Read `parallel_execution` from spec frontmatter (defaults: `enabled: true`, `max_parallel_tasks: 3`). Eligible tasks must be Pending, not human-owned, all deps Finished, in active phase (or `cross_phase: true`), all decision deps resolved, difficulty < 7. Build conflict-free batch by pairwise-comparing `files_affected`. If batch >= 2, set `parallel_mode = true`.
```

No other changes to `work.md` — Step 3's routing logic delegates phase checks to Step 2b (now updated via File 2), and Step 3's routing algorithm (lines 396-429) already references eligibility without hard-coding the phase rule.

---

### File 5: `.claude/commands/breakdown.md`

**Editing strategy:** Targeted `Edit` to add subtask inheritance note.

**Insert** after the "Important: Copy all spec provenance fields from the parent task" note (line 34), before the Step 4 "Update parent task" block.

**New content to add:**
```markdown

   **Also copy eligibility flags from parent:**
   - If parent has `cross_phase: true`, each subtask inherits `cross_phase: true`. User can remove it from individual subtasks manually if needed.
   - If parent has `parallel_safe: true`, inheritance is per-subtask based on whether the subtask has file side effects (do not auto-inherit).
```

Verify the parent block in the "Rules" section does not need edits (it does not currently cover flag inheritance).

---

### File 6: `.claude/support/reference/decomposition.md`

**Editing strategy:** Targeted `Edit` to add a new bullet in the "Task Creation Guidelines" section.

**Insert** a new bullet after the existing `Decision dependencies:` bullet (line 45), at the end of the Task Creation Guidelines list:

**New bullet:**
```markdown
- **Cross-phase flag:** Consider suggesting `cross_phase: true` for long-lead tasks that must start before prior phase completion. Heuristic: `owner: human` tasks whose title or notes contain recruit/procure/approve/schedule/coordinate/stakeholder/vendor/contract, OR any task with `external_dependency.expected_date` more than 14 days out. When the heuristic fires, ask the user: `"Task {id} looks like long-lead work. Mark as cross_phase: true? [Y/N]"`. Never set silently. See `task-schema.md` § `cross_phase` for semantics.
```

No other changes to this file. The "Organizing Tasks Into Stages" and "Decomposition Quality Checks" sections do not need updates — cross-phase is an eligibility flag, not a stage or quality attribute.

---

### File 7: `.claude/support/reference/dashboard-regeneration.md`

**Editing strategy:** Targeted `Edit` in the "Section Display Rules" block (around line 388-391).

**Insert** a new bullet in the Section Display Rules list, placed immediately after the "Tasks with `conflict_note`:" bullet (line 389):

**New bullet:**
```markdown
- Tasks with `cross_phase: true`: append ` (cross-phase)` suffix after the task title in the Tasks section. Task still appears in its declared phase group. Phase table and phase counts are unchanged — the flag affects eligibility only, not phase membership.
```

No other changes to this file. Phase Transitions sub-section (line 204+) does not need updates — cross-phase tasks don't affect gate rendering since they belong to their declared phase.

---

### File 8: `system-overview.md`

**Editing strategy:** One targeted `Edit` to close out the DEC-006 pending-decisions bullet.

**Before (after DEC-005 removal, current state):**
```
- **Subagent capability contract** — whether subagents spawned by `/work` own task state transitions (implement-agent Steps 6a/6b) or the orchestrator does. Relates to FB-010.
- **Phase gate flexibility** — how to let long-running human-owned tasks cross phase boundaries without breaking the software-domain invariant. Relates to FB-013.
```

**After:**
```
- **Subagent capability contract** — whether subagents spawned by `/work` own task state transitions (implement-agent Steps 6a/6b) or the orchestrator does. Relates to FB-010.
```

(The DEC-004 bullet remains — its cleanup is tied to the Phase 5 decisions-folder purge per tracker instruction. Leave it.)

---

### File 9: `.claude/commands/health-check.md`

**Editing strategy:** Targeted `Edit` in Part 1 Check 1 (Task JSON Schema Validation).

**Before (line 25):**
```
Validates required fields (id, title, status, difficulty) and optional fields per `.claude/support/reference/task-schema.md`.
```

**After:**
```
Validates required fields (id, title, status, difficulty) and optional fields per `.claude/support/reference/task-schema.md`. Boolean fields (`parallel_safe`, `out_of_spec`, `out_of_spec_rejected`, `cross_phase`, `user_review_pending`) must be booleans when present — flag non-boolean values as schema violations.
```

No other changes to health-check.md.

---

## Execution Order

Recommended order (Files 1-2 establish the contract, Files 3-7 consume it, Files 8-9 are cleanup/validation):

1. **Read** DEC-006, tracker, and current state of Files 1-9
2. **File 1** (`task-schema.md`) — add `cross_phase` row + update `phase` row description
3. **File 2** (`phase-decision-gates.md`) — add skip rule + Cross-Phase Tasks section
4. **File 3** (`parallel-execution.md`) — OR clause in eligibility
5. **File 4** (`commands/work.md`) — Step 2c summary line
6. **File 5** (`commands/breakdown.md`) — subtask inheritance note
7. **File 6** (`decomposition.md`) — heuristic bullet
8. **File 7** (`dashboard-regeneration.md`) — annotation rule
9. **File 8** (`system-overview.md`) — remove Pending Decisions bullet
10. **File 9** (`commands/health-check.md`) — schema boolean check
11. **Verify:** grep for `cross_phase` — should appear in Files 1, 2, 3, 4, 5, 6, 7, 9 but NOT in File 8; phase-decision-gates has both the `!= true` skip and `== true` bypass branches; parallel-execution eligibility line has the OR clause
12. **Update tracker:** Session Log entry, Current State → Phase 1 complete / Phase 2 next, mark DEC-006 checkbox done, strike DEC-006 column entries in File Collision Map
13. **Commit:** see commit message below

---

## Verification Checklist (Post-Execution)

Before commit, confirm:

- [ ] `task-schema.md` — `phase` row mentions `cross_phase`; new `cross_phase` row exists with Boolean type and long-lead-work description
- [ ] `phase-decision-gates.md` — Phase Check block has both `!= true` (skip) and `== true` (bypass) branches; new `### Cross-Phase Tasks` sub-section added
- [ ] `parallel-execution.md` line 29 — has `OR task.cross_phase == true`
- [ ] `work.md` Step 2c summary — has `(or cross_phase: true)` inside the eligibility list
- [ ] `breakdown.md` — has subtask inheritance note covering `cross_phase` and `parallel_safe`
- [ ] `decomposition.md` — has cross-phase heuristic bullet with keywords and 14-day threshold
- [ ] `dashboard-regeneration.md` — Section Display Rules has `(cross-phase)` suffix bullet
- [ ] `system-overview.md` Pending Template Decisions — no longer contains DEC-006 bullet; DEC-004 bullet remains
- [ ] `health-check.md` Part 1 Check 1 — lists `cross_phase` among boolean-validated fields
- [ ] No new JSON schema file changes — `cross_phase` is documented in `task-schema.md` only (consistent with how other optional fields are handled)
- [ ] Pre-commit hook warning about version.json is expected — version bump deferred to Phase 5

---

## Commit Message

```
DEC-006: add cross_phase field for long-lead tasks (inflection point)

Per Option A, add an optional `cross_phase: true` boolean field to the
task schema. When true, the task is exempt from the phase gate on
eligibility checks — it can start when its own dependencies are met,
regardless of prior phase completion. Phase membership is unchanged
(the task still belongs to its declared phase for verification and
dashboard rendering).

Typical use: long-lead human work (recruitment, procurement, approvals,
stakeholder coordination) that must start before the prior phase is
fully done. Also covers rare Claude-owned cross-phase work (e.g.,
infrastructure provisioning).

Rationale: preserves Tier 2 verification semantics (cross-phase task is
verified as part of its declared phase), handles both common and rare
cases with one explicit mechanism, and is reversible. Option B's
"float all human tasks" approach would have weakened the phase gate's
guarantees and introduced Tier 2 timing ambiguity; per-task opt-in
avoids both.

Closes FB-013. This decision is an inflection point: projects with
long-lead work can now model their real timelines without reshuffling
tasks across phases. Running `/iterate` is recommended after the first
project encounters a cross-phase candidate, to ensure the spec's phase
structure still reflects intent.

Changes:
- support/reference/task-schema.md: new cross_phase field row + phase row update
- support/reference/phase-decision-gates.md: skip rule + Cross-Phase Tasks section
- support/reference/parallel-execution.md: OR clause in eligibility
- commands/work.md: Step 2c summary updated
- commands/breakdown.md: subtask inheritance note
- support/reference/decomposition.md: heuristic for auto-suggest during decomposition
- support/reference/dashboard-regeneration.md: (cross-phase) suffix rendering rule
- system-overview.md: DEC-006 removed from Pending Template Decisions
- commands/health-check.md: Part 1 boolean-field validation covers cross_phase

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Post-Execution Tracker Updates

After successful commit:

1. Update `template-upgrade-2026-04.md`:
   - Add Session Log entry for DEC-006 execution
   - Update Current State → "Phase 1 complete — proceed to Phase 2 (new input intake)"
   - Mark DEC-006 checkbox in Phase 1 as `[x]` with commit SHA
   - Update File Collision Map: strike through DEC-006 column entries (done); note that the `rules/task-management.md`, `rules/spec-workflow.md`, and `commands/iterate.md` entries in the DEC-006 column turned out to be stale (no changes needed — the approved Option A's touchpoints are narrower than the collision map anticipated, which itself was based on an earlier scope of the decision)
2. Confirm this plan file is in the Cleanup Manifest as DELETE-AFTER (add the entry if missing)
3. Note inflection-point follow-up: if the user has active downstream projects, flag that running `/iterate` is suggested once the new field is first used — this can be surfaced on their next `/health-check` via the template sync prompt.
