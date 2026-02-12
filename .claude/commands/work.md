# Work Command

The intelligent entry point for all project work. Handles spec-checking, state detection, task decomposition, task completion, and routing to specialist agents.

For workflow concepts (phases, agent synergy, checkpoints), see `.claude/support/reference/workflow.md`.

## Usage
```
/work                    # Auto-detect what needs doing
/work {task-id}          # Work on specific task
/work {request}          # Handle ad-hoc request
/work complete           # Complete current in-progress task
/work complete {id}      # Complete specific task
```

## What It Does

1. **Checks against spec** - Every request is validated against the specification
2. **Analyzes project state** - Reads dashboard, spec, and current progress
3. **Decomposes spec into tasks** - When spec is ready but no tasks exist
4. **Completes tasks** - Marks tasks as finished with `/work complete`
5. **Routes to specialists** - Reads and follows implement-agent or verify-agent workflows
6. **Surfaces misalignments** - Points out when requests don't fit the spec
7. **Auto-syncs dashboard** - Regenerates dashboard.md after any task changes

---

## Process

### Step 0: Session Recovery Check

Before gathering context, scan for tasks left in recoverable states by a previous session. This handles agent crashes, turn exhaustion, and session interruptions.

**Scan all non-archived task-*.json files and check for:**

```
1. STATUS: "Awaiting Verification"
   (Agent crashed after implementation, before verification completed)

   → Auto-recover: spawn verify-agent for this task
   → Log: "⚡ Recovering task {id} — spawning verification (previous session incomplete)"
   → Continue to Step 1 after recovery spawns complete

2. STATUS: "Blocked" WITH notes containing "[VERIFICATION TIMEOUT]"
   AND verification_attempts < 3
   (Verify-agent ran out of turns — implementation is done, verification needs retry)

   → Auto-recover: set status to "Awaiting Verification", spawn verify-agent with max_turns: 40 (extended from 30)
   → Clear the [VERIFICATION TIMEOUT] note
   → Log: "⚡ Retrying verification for task {id} with extended turn limit"

3. STATUS: "Blocked" WITH notes containing "[VERIFICATION TIMEOUT]"
   AND verification_attempts >= 3
   (Verify-agent failed 3 times — needs human review)

   → Replace note: "[VERIFICATION ESCALATED] 3 verification attempts exhausted — requires human review"
   → Log: "Task {id} escalated to human review after 3 failed verification attempts"

4. STATUS: "Blocked" WITH notes containing "[AGENT TIMEOUT]"
   (Parallel agent timed out — task may be too complex or need breakdown)

   → Present to user:
   │  Task {id} "{title}" timed out in a previous session.
   │  [R] Retry (set to Pending for next dispatch)
   │  [B] Break down (run /breakdown {id})
   │  [S] Skip (stays Blocked)

5. STATUS: "Blocked" WITH notes containing "[VERIFICATION ESCALATED]"
   (Intentional escalation — already surfaced, no auto-action)

   → Report only: "Task {id} awaiting human review (3 verification attempts exhausted)"

6. STATUS: "In Progress" WITH updated_date older than 24 hours
   AND no agent currently running for this task
   (Abandoned by a crashed implement-agent)

   → Present to user:
   │  Task {id} "{title}" has been In Progress for {N} days without activity.
   │  [C] Continue (keep In Progress, /work will route to implement-agent)
   │  [P] Reset to Pending (start fresh)
   │  [H] Put On Hold
```

**After recovery actions complete, proceed to Step 1.**

**Note:** Cases 1 and 2 are auto-recovered because the implementation is already done — we only need to run verification. Cases 4 and 6 present options because the implementation state is uncertain.

### Step 1: Gather Context

**Version discovery:** Determine the current spec version:
```
1. Glob for .claude/spec_v*.md
2. Parse version numbers from filenames
3. Use the highest N as the current spec
4. If zero matches → no spec exists
5. If multiple matches → use highest, flag anomaly (should be exactly one)
```

Read and analyze:
- `.claude/spec_v{N}.md` - The specification (source of truth)
- `.claude/dashboard.md` - Task status and progress
- `.claude/support/questions/questions.md` - Pending questions

**Scale optimization (50+ tasks):** When the task directory contains many files, avoid reading all task JSON upfront. Instead:
1. Glob for `task-*.json` files to get the file count
2. Compare file count against dashboard metadata `task_count` — if they match, the dashboard is likely fresh; skip the full hash computation in Step 1a and trust dashboard data for completed task totals
3. Only read non-Finished task files for routing decisions (use dashboard task table for finished task statuses when dashboard is fresh)
4. Read completed task files only when needed for specific dependency checks
5. If file count differs from `task_count`, fall back to full hash computation (Step 1a) and read all tasks

This reconciles with Step 1a: the file count check is a lightweight gate that avoids the full O(N) hash computation in most cases. After auto-archive runs (threshold: 100), archived tasks are excluded automatically.

**Malformed task file handling:** When reading task JSON files, if any file fails to parse (invalid JSON, truncated, encoding errors):
1. Skip the file — do not abort the entire scan
2. Report the error prominently: "Task file `task-{id}.json` could not be read: {error}. Run `/health-check` for details."
3. Exclude the corrupted file from all calculations (progress counts, phase completion, dependency checks, dashboard)
4. If other tasks depend on the corrupted task, treat those dependencies as unresolvable (task effectively Blocked)

This prevents one bad file from halting all work while ensuring the problem is visible to the user.

### Step 1a: Dashboard Freshness Check

Verify the dashboard is current before using its data. Compute a SHA-256 hash of all task IDs and statuses, compare against the dashboard's `<!-- DASHBOARD META -->` block. If the hash differs or no metadata exists, regenerate the dashboard from task JSON files before continuing.

**Full procedure:** `.claude/support/reference/drift-reconciliation.md` § "Dashboard Freshness Check"

### Step 1b: Spec Drift Detection (Granular)

After reading the spec, perform section-level drift detection. Compare the current spec's SHA-256 fingerprint against task fingerprints. If different, parse both current spec and decomposition snapshot into `##` sections, compare per-section fingerprints, identify which sections changed, and group affected tasks by changed section. Tasks without fingerprints fall back to full-spec comparison.

**Full procedure:** `.claude/support/reference/drift-reconciliation.md` § "Spec Drift Detection"

### Step 1c: Spec State Summary

After drift detection completes, always output a brief status line so the user knows where things stand:

```
If no tasks exist:
  "Spec: v{N} (draft) — no tasks yet"

If tasks exist and spec is aligned:
  "Spec: v{N} (active) — aligned with tasks ✓"
  "Tasks: {total} total ({finished} finished, {in_progress} in progress, {pending} pending{, N on hold}{, N absorbed})"

If tasks exist and spec has changed:
  "Spec: v{N} (active) — {M} sections changed since decomposition"
  "Tasks: {total} total ({finished} finished, {in_progress} in progress, {pending} pending{, N on hold}{, N absorbed})"

If version transition detected (tasks reference older spec version):
  "Spec: v{N} (draft) — new version, tasks reference v{N-1}"
  "Tasks: {total} total — migration needed (see below)"
```

This runs AFTER drift detection (Step 1b) so it can accurately report section changes.

### Substantial Change Detection

Before showing the reconciliation UI, evaluate change magnitude. Changes are "substantial" when >50% of sections changed, sections were added/deleted, or the spec has been active >7 days with >3 sections changed. Substantial changes trigger a version bump suggestion (`[V]` Create v{N+1} / `[C]` Continue as v{N}). Non-substantial changes proceed directly to reconciliation.

**Full procedure:** `.claude/support/reference/drift-reconciliation.md` § "Substantial Change Detection"

### Task Migration on Version Transition

When tasks reference an older spec version, migrate them: finished tasks keep old provenance; pending/in-progress tasks are checked against the new spec (section exists and matches → update fingerprints; section changed → flag for reconciliation; section deleted → present options to user).

**Full procedure:** `.claude/support/reference/drift-reconciliation.md` § "Task Migration on Version Transition"

### Drift Budget Enforcement

Prevents drift from accumulating indefinitely. Deferred reconciliations are tracked in `drift-deferrals.json`. On each `/work` run, check active deferrals against limits (default: max 3 sections, max 14 days). If exceeded or expired, block all actions until reconciliation completes.

**Full procedure:** `.claude/support/reference/drift-reconciliation.md` § "Drift Budget Enforcement"

### Granular Reconciliation UI

When section-level drift is detected, present a per-section UI with diff and affected tasks. Options per section: `[A]` Apply, `[R]` Review individually, `[S]` Skip. Edge cases: new section → suggest new tasks; deleted section → flag tasks for out-of-spec/deletion.

**Full procedure:** `.claude/support/reference/drift-reconciliation.md` § "Granular Reconciliation UI"

**Post-reconciliation In Progress warning:** After reconciliation completes, check if any "In Progress" tasks had their section fingerprints updated (i.e., their requirements changed while work was underway). If so, warn the user before continuing:

```
⚠️ Task {id} "{title}" is In Progress but its spec section changed during reconciliation.
  Review the task's partial work against the updated requirements before continuing.
```

This is a warning, not a gate — the user can proceed or reset the task manually. The intent is visibility: don't silently dispatch an agent to continue work against changed requirements.

### Step 2: Spec Check (if request provided)

When the user provides a request or task:

```
Check request against spec:
├─ Clearly aligned → Proceed
├─ Minor/trivial addition → Proceed (doesn't need spec change)
└─ Significant but not in spec → Surface it:
   "This isn't covered in the spec. Options:
    1. Add to spec: [suggested addition]
    2. Proceed anyway (won't be verified against spec)
    3. Skip for now"
```

**If user selects "Proceed anyway":**
- Create task with `"out_of_spec": true`
- Dashboard shows ⚠️ prefix for these tasks
- Health check reports out-of-spec tasks separately

**What counts as "significant":**
- New features or capabilities
- Changes to architecture or data model
- New integrations or dependencies
- Anything that affects acceptance criteria

**What's "minor/trivial":**
- Bug fixes
- Code cleanup
- Small improvements within existing scope
- Documentation

### Step 2b: Phase and Decision Check

Check whether phases or unresolved decisions block any intended work:

```
1. Read all decision-*.md files from .claude/support/decisions/
2. Read all task-*.json files

3. PHASE CHECK:
   Determine current active phase by walking phases ascending:
   ├─ Group tasks by `phase` field
   ├─ Sort phases numerically (ascending)
   │
   │  FOR each phase P (ascending):
   │    IF all tasks in phase P are "Finished":
   │      IF tasks exist in a higher phase (next_phase exists):
   │        1. Read dashboard for approved marker: <!-- PHASE GATE:{P}→{next_phase} APPROVED -->
   │        2. IF APPROVED marker exists:
   │             → Already approved. Continue to next phase.
   │        3. Read dashboard for phase gate marker: <!-- PHASE GATE:{P}→{next_phase} -->
   │        4. IF marker exists, check ALL checkboxes within the gate:
   │             - Parse all `- [x]` and `- [ ]` lines between gate markers
   │             - **Normalize checkboxes before evaluation:**
   │               - Treat `[x]`, `[X]`, `[✓]`, `[✔]` all as checked
   │               - Treat `[ ]`, `[]` as unchecked
   │               - Any other content inside brackets → treat as unchecked (safe default)
   │             - IF ALL checkboxes are checked [x]:
   │               → Phase transition approved.
   │               → Replace gate content with: <!-- PHASE GATE:{P}→{next_phase} APPROVED -->
   │               → Log: "Phase {P} → {next_phase} approved"
   │               → Execute Version Transition Procedure (see iterate.md § "Version Transition Procedure")
   │               → Suggest running /iterate to flesh out Phase {next_phase} sections
   │               → Continue to next phase
   │             - IF any checkbox is unchecked [ ]:
   │               → Log: "Phase gate {P}→{next_phase}: {N} of {M} conditions met. Waiting for remaining approvals."
   │               → STOP — do not dispatch any tasks
   │        5. IF marker absent:
   │             → Regenerate dashboard with phase gate in Action Required (see `dashboard-regeneration.md` § "Regeneration Steps" Step 3)
   │             → Log: "Phase {P} complete. Review conditions and approve transition in dashboard, then run /work."
   │             → STOP — do not dispatch any tasks
   │      ELSE (final phase, all tasks Finished):
   │        → Fall through to Step 3 routing (phase-level verification → completion)
   │    ELSE (phase P has non-Finished tasks):
   │      → This is the active phase
   │
   │  For target task(s):
   │  IF task.phase > active_phase:
   │    "Task {id} is in Phase {task.phase}, but Phase {active_phase} is still in progress.
   │     {N} tasks remaining in Phase {active_phase}."
   │    → Skip this task, work on active-phase tasks instead

4. DECISION CHECK:
   For target task(s), check `decision_dependencies`:
   ├─ Read each referenced decision record
   ├─ Check if decision has a checked box in "## Select an Option"
   │
   │  IF any decision is unresolved (no checked box):
   │    📋 Decision {id} ({title}) blocks {N} task(s).
   │    Open the decision doc to review options and check your selection:
   │    → [decision doc link]
   │    Then run `/work` again.
   │
   │  IF decision has a checked box AND frontmatter status is NOT "approved"/"implemented":
   │    → AUTO-UPDATE FRONTMATTER:
   │      1. Extract selected option name from the checked line (text after `[x] `)
   │      2. Update frontmatter fields:
   │         - status: approved
   │         - decided: [today's date, YYYY-MM-DD]
   │      3. Log: "Decision {id} resolved → status updated to 'approved' (selected: {option_name})"
   │    → Run post-decision check (see Step 2b-post below)
   │
   │  IF decision has a checked box AND frontmatter status is already "approved"/"implemented":
   │    → Already processed. Run post-decision check if dependent tasks are still blocked.

5. LATE DECISION CHECK (reverse cross-reference):
   For each decision-*.md file, read `related.tasks` array:
   ├─ For each referenced task ID:
   │  ├─ Read task JSON
   │  ├─ Check if decision ID is in task's `decision_dependencies`
   │  │
   │  │  IF NOT (task doesn't know about this decision):
   │  │    Check task status:
   │  │    ├─ "Finished" or "In Progress":
   │  │    │    ⚠️ Decision {id} ({title}) was created after task {task_id} began.
   │  │    │
   │  │    │    Status:
   │  │    │    - Task {id}: "{status}" — {impact description}
   │  │    │
   │  │    │    Options:
   │  │    │    [1] Add {DEC-ID} as dependency + pause/flag affected tasks
   │  │    │    [2] Proceed as-is (risk: rework if decision contradicts implementation)
   │  │    │    [3] Review affected task(s) before deciding
   │  │    │
   │  │    │    IF user picks [1]:
   │  │    │      - Add decision ID to task's decision_dependencies
   │  │    │      - "In Progress" tasks → set to "Pending" (now blocked)
   │  │    │      - "Finished" tasks → add note: "Review after {DEC-ID} resolved — may need rework"
   │  │    │      - Regenerate dashboard
   │  │    │
   │  │    └─ "Pending":
   │  │         Silently fixable — add decision_dependencies and continue
   │  │
   │  └─ IF YES: task already tracks this decision → no issue

6. IF phase, decision, and late decision checks pass:
   → Proceed to Step 2c
```

### Step 2b-post: Post-Decision Check

When `/work` detects a resolved decision (status `approved` or `implemented`) that has dependent tasks:

```
1. Read the decision record
2. Check `inflection_point` field in frontmatter

IF inflection_point: false (or absent):
  → Pick-and-go: unblock dependent tasks, continue to Step 2c
  → Log: "Decision {id} resolved → {N} tasks unblocked"

IF inflection_point: true:
  → Check `spec_revised` field in frontmatter
  │
  │  IF spec_revised: true
  │    → Spec already updated for this decision. Unblock dependent tasks.
  │    → Log: "Decision {id} (inflection point) resolved and spec revised → {N} tasks unblocked"
  │    → Continue to Step 2c
  │
  │  IF spec_revised is false OR absent:
  │    → Pause execution
  │    │
  │    │  ⚠️ Decision {id} ({title}) was an inflection point.
  │    │  The outcome may change what needs to be built.
  │    │
  │    │  Run `/iterate` to review affected spec sections,
  │    │  then `/work` to continue.
  │    │
  │    └─ Do NOT proceed. Wait for user to run `/iterate`.
```

**Session resilience:** The `spec_revised` field is the durable checkpoint. Across session boundaries, `/work` re-reads the decision record and checks this field — no conversation state needed. The decision stays blocking until the spec has been explicitly revised.

### Step 2c: Parallelism Eligibility Assessment

After phase and decision checks, assess whether multiple tasks can be dispatched in parallel. Read `parallel_execution` from spec frontmatter (defaults: `enabled: true`, `max_parallel_tasks: 3`). If disabled, skip to Step 3.

**Eligible tasks** must be: Pending (not On Hold, Absorbed, Blocked, or Broken Down), not human-owned, all deps Finished, in active phase, all decision deps resolved, difficulty < 7.

**Batch building:** Pairwise-compare `files_affected` using the file conflict detection algorithm (exact match or directory containment). Tasks with conflicts are held back; tasks with empty `files_affected` and no `parallel_safe: true` are excluded. If batch >= 2, set `parallel_mode = true`.

**Full procedure:** `.claude/support/reference/parallel-execution.md` § "Parallelism Eligibility Assessment"

### Step 3: Determine Action

**If a specific request was provided** (and passed spec check):
1. Create a task for the request (or find existing matching task)
2. Route to the "If Executing" section in Step 4 (read and follow implement-agent workflow)
3. Continue to Step 5 (questions) and Step 6 (health check)

**If no request provided** (auto-detect mode):

| Condition | Action |
|-----------|--------|
| No spec exists, no tasks | Stop — direct user to create spec via `/iterate` |
| No spec exists, tasks exist | **Stop and warn** — tasks without a spec cannot be verified. Present options (see below). |
| Spec incomplete | Stop — prompt user to complete spec |
| Spec complete, no tasks | **Decompose** — create tasks from spec |
| Phase transition pending approval (phase gate unchecked in dashboard) | **Stop** — direct user to approve phase transition in dashboard *(enforced by Step 2b before reaching Step 3)* |
| Any spec task in "Awaiting Verification" status | **Verify (per-task)** — read & follow verify-agent per-task workflow (see Step 4) |
| Spec tasks pending (and none awaiting verification), parallel batch >= 2 | **Execute (Parallel)** — dispatch parallel batch (see Step 4 "If Executing (Parallel)") |
| Spec tasks pending (and none awaiting verification), no parallel batch | **Execute** — read & follow implement-agent workflow (see Step 4) |
| All spec tasks "Finished" with passing per-task verification, no valid phase verification result | **Verify (phase-level)** — read & follow verify-agent phase-level workflow (see Step 4) |
| Phase-level verification result is `"fail"` (in-spec fix tasks exist) | **Execute** — fix tasks need implementation before re-verification |
| All spec tasks finished, valid phase verification result | **Complete** — report project complete, present final checkpoint |

**Priority order matters.** Per-task verification takes priority over executing the next task. This ensures verification is not deferred.

**CRITICAL: Verification enforcement.** Before routing to phase-level verification or completion, you MUST verify that EVERY "Finished" spec task has `task_verification.result == "pass"`. Tasks in "Awaiting Verification" status must complete per-task verification first. Never skip this check.

**State detection logic:** A task "needs per-task verification" when:
- It has status "Awaiting Verification", OR
- It has status "Finished" AND does NOT have a `task_verification` field (legacy edge case)

**Explicit routing algorithm:**
```
1. Get all spec tasks (exclude out_of_spec: true, exclude status "Absorbed")
2. awaiting_verification = tasks where status == "Awaiting Verification"
3. IF awaiting_verification is not empty:
   → Route to verify-agent (per-task) for first task in "Awaiting Verification"
   → Do NOT proceed to phase-level or completion
4. finished_tasks = tasks where status == "Finished"
5. unverified_finished = finished_tasks where task_verification does not exist (legacy edge case)
6. IF unverified_finished is not empty:
   → Route to verify-agent (per-task) for first unverified task
   → Do NOT proceed to phase-level or completion
7. ELSE IF all spec tasks are "Finished" AND all have task_verification.result == "pass":
   → Check verification-result.json
   → IF file missing → Route to verify-agent (phase-level)
   → IF result == "fail" → Route to implement-agent (fix tasks were created, need implementation)
   → IF spec_fingerprint mismatch OR tasks updated after timestamp → Route to verify-agent (re-verification needed)
   → IF result == "pass" or "pass_with_issues" → Route to completion
8. ELSE IF parallel_mode (from Step 2c):
   → Route to parallel execution (see "If Executing (Parallel)")
9. ELSE:
   → Route to implement-agent for next pending task (sequential)
```

**Spec-less project handling:** If tasks exist but no spec file is found, do NOT proceed. Present options: `[S]` Create spec via `/iterate`, `[M]` Mark all tasks out-of-spec, `[X]` Stop. This prevents completing without verification.

**Important — spec tasks vs out-of-spec tasks:** Phase routing is based on **spec tasks only** (tasks without `out_of_spec: true`). Out-of-spec tasks (recommendations from verify-agent or user requests that bypassed the spec) are excluded from phase detection. This prevents the verify → execute → verify infinite loop.

**Phase-level verification result check:** Read `.claude/verification-result.json`. A result is valid when `result` is `"pass"` or `"pass_with_issues"`, `spec_fingerprint` matches the current spec, and no tasks changed since `timestamp`. See verify-agent Phase-Level Step 7 for the file format.

**Out-of-spec task handling:** After phase routing completes (or at phase boundaries), check for pending out-of-spec tasks and present them with options: `[A]` Accept (sets `out_of_spec_approved: true`), `[R]` Reject (archives task with reason), `[D]` Defer (skips for now), `[AA]` Accept all.

**Reject behavior:** When the user selects `[R]`:
1. Prompt for optional rejection reason: "Reason (optional):"
2. Set `out_of_spec_rejected: true` on the task JSON
3. If reason provided, set `rejection_reason` field
4. Move task file to `.claude/tasks/archive/`
5. Task is preserved for audit trail but excluded from active processing and dashboard

**Rule:** Never auto-execute an out-of-spec task. Always require explicit user approval first.

### Step 4: Execute Action

#### If Decomposing (spec → tasks)

Break the spec into granular tasks:

1. **Run setup checklist** - Read `.claude/support/reference/setup-checklist.md` and run through its checks. Report any warnings inline. Continue regardless (advisory, not blocking).
2. **Read spec thoroughly** - Understand all requirements and acceptance criteria
3. **Compute spec fingerprint** - SHA-256 hash of spec content (see Step 1b)
4. **Save spec snapshot** - Copy current spec to `.claude/support/previous_specifications/spec_v{N}_decomposed.md`
5. **Parse spec into sections** - Extract ## level headings and their content
6. **Compute section fingerprints** - SHA-256 hash of each section (heading + content)
7. **Identify work items** - Each distinct piece of functionality per section
8. **Create task files** - One JSON per task, difficulty ≤ 6, with full provenance:
   - `spec_fingerprint` - Hash of full spec computed in step 3
   - `spec_version` - Filename of spec (e.g., "spec_v1")
   - `spec_section` - Originating section heading (e.g., "## Authentication")
   - `section_fingerprint` - Hash of specific section computed in step 6
   - `section_snapshot_ref` - Snapshot filename (e.g., "spec_v1_decomposed.md")
   - **Important:** Create all task JSON files before regenerating the dashboard. Every task must have a `task-*.json` file — the dashboard is generated from these files, never the other way around.
9. **Map dependencies** - What must complete before what
10. **Regenerate dashboard** - Follow `.claude/support/reference/dashboard-regeneration.md` in full (backup, generate, restore, metadata, footer)

**Task creation guidelines:**
- Clear, actionable titles ("Add user validation" not "Backend stuff")
- Difficulty 1-6 (break down anything larger)
- Explicit dependencies
- Owner: claude/human/both
- Include all spec provenance fields (fingerprint, version, section, section_fingerprint, section_snapshot_ref)
- **Phase field:** Assign `phase` based on spec section structure (e.g., tasks from "## Phase 1: Data Pipeline" get `"phase": "1"`)
- **Decision dependencies:** If a task depends on an unresolved decision, add the decision ID to `decision_dependencies` array. Note whether the decision is an inflection point in task notes.

**Spec status transitions during decomposition:**

When decomposition begins, update the spec metadata `status` from `draft` to `active`:
```yaml
---
version: 1
status: active
---
```

This signals that the spec is being implemented. The transition to `complete` happens in the "If Completing" section below.

#### If Executing

**You must use the implement-agent workflow. Do not implement directly.**

Execute these steps in order:

1. **Read the agent file now:** Use the Read tool to read `.claude/agents/implement-agent.md` in full. Do not skip this step or work from memory.
2. **Follow every numbered step** in the agent's Workflow section (Steps 1 through 6). Each step produces a required artifact:
   - Step 1: Task selected (logged)
   - Step 1b: Validation checks passed
   - Step 3: Task JSON updated to `"In Progress"` **before any implementation begins**
   - Step 4: Implementation done
   - Step 5: Self-review completed
   - Step 6a: Task JSON updated to `"Awaiting Verification"`
   - Step 6b: verify-agent **spawned as a separate Task agent** (fresh context, no implementation memory) → status becomes `"Finished"` if pass
   - Step 6c: Dashboard regenerated
3. **Context to provide:** Current task, relevant spec sections, constraints/notes

#### If Executing (Parallel)

When Step 2c produces a parallel batch of >= 2 tasks, execute them concurrently. Log the dispatch, set all batch tasks to "In Progress", annotate held-back tasks with `conflict_note`, spawn one `Task` agent per task (`model: "opus"`, `max_turns: 40`), and poll for completion with incremental re-dispatch (newly-unblocked tasks start as earlier ones finish). After all agents complete: final parent auto-completion check, single dashboard regeneration, operational checks (Step 6), then loop back to Step 2c.

**Key rules:**
- Each parallel agent reads `implement-agent.md` and runs Steps 2/4/5/6a/6b independently
- Agents must NOT regenerate dashboard, select next task, or check parent auto-completion
- Passed tasks stay "Finished"; failed tasks return to "In Progress" for next batch
- Timed-out agents (60 poll iterations) → task set to "Blocked"

**Full procedure:** `.claude/support/reference/parallel-execution.md` § "Parallel Dispatch"

#### If Verifying (Per-Task)

**You must spawn verify-agent as a separate agent. Do not verify inline.**

Spawn a verify-agent using the `Task` tool (same pattern as implement-agent Step 6b):

```
Task tool call:
  subagent_type: "general-purpose"
  model: "opus"
  max_turns: 30
  description: "Verify task {id}"
  prompt: |
    You are the verify-agent. Read `.claude/agents/verify-agent.md` and follow
    the Per-Task Verification Workflow (Steps T1-T8) for this task.

    Task file: .claude/tasks/task-{id}.json
    Spec file: .claude/spec_v{N}.md (section: "{spec_section}")

    TURN BUDGET: You have 30 turns. If you reach turn 25 without completing:
    - Stop new verification checks
    - Write task_verification to the task JSON with whatever checks you completed
    - Set result to "fail" with note: "Verification incomplete — {N} of 5 checks completed"
    - Return your partial report immediately

    Verify the implementation independently. Do NOT assume correctness.
    Write your verification result to the task JSON (task_verification field).
    Update task status to "Finished" (pass) or "In Progress" (fail).
    Return your T8 report.
```

**Timeout handling:** If verify-agent exhausts `max_turns` (30) without completing, treat as verification failure — increment `verification_attempts` on the task JSON, set task to "Blocked" with note `[VERIFICATION TIMEOUT]`, and report to user. Incrementing the counter ensures repeated timeouts eventually trigger the 3-attempt escalation limit (see verify-agent.md Step T7).

**After per-task verification completes:**
- If **pass**: Check the task's `owner` field. If `owner: "both"`, verify that `user_review_pending: true` was set by verify-agent (the task remains in "Your Tasks" until the user runs `/work complete`). Proceed to select next pending task (loop back to Execute routing).
- If **fail**: Task is set back to "In Progress". Route to implement-agent to fix the issues. After fix, route back to verify-agent for re-verification. This loop continues until pass.
- Regenerate dashboard after any status change, per `.claude/support/reference/dashboard-regeneration.md`.

**Fail → Fix → Re-Verify Loop:**
```
Task Finished → verify-agent → FAIL → implement-agent fixes → verify-agent re-verifies → ...
                           ↓
                         PASS → next task
```
This loop is mandatory. A task cannot be considered done until it passes verification.

#### If Verifying (Phase-Level)

**You must use the verify-agent phase-level workflow. Do not verify directly.**

**MANDATORY: Reconciliation Gate**

Before starting phase-level verification, ALL drift must be reconciled:

```
1. Check drift-deferrals.json
2. IF any deferrals exist:
   ├─ Cannot proceed to phase-level verification with unreconciled drift
   │
   │  Phase-level verification requires spec alignment.
   │  You have N deferred section(s) that must be reconciled first.
   │
   │  Deferred sections:
   │  - ## Authentication (deferred 2026-01-20, 3 tasks affected)
   │  - ## API Endpoints (deferred 2026-01-25, 1 task affected)
   │
   │  [R] Reconcile all now (REQUIRED to proceed)
   │
   └─ Block phase-level verification until all deferrals cleared
```

**Why:** Verifying against a spec that doesn't match task definitions produces unreliable results. Reconciliation ensures tasks actually reflect what the spec says before verification runs.

Spawn a verify-agent using the `Task` tool:

```
Task tool call:
  subagent_type: "general-purpose"
  model: "opus"
  max_turns: 50
  description: "Phase-level verification"
  prompt: |
    You are the verify-agent. Read `.claude/agents/verify-agent.md` and follow
    the Phase-Level Verification Workflow (Steps 1-8).

    Spec file: .claude/spec_v{N}.md
    Task directory: .claude/tasks/

    TURN BUDGET: You have 50 turns. If you reach turn 43 without completing:
    - Stop evaluating new criteria
    - Write verification-result.json with results for criteria evaluated so far
    - Set result to "fail" with note: "Verification incomplete — evaluated {N} of {M} criteria"
    - Create a single fix task: "Complete phase-level verification"
    - Return your partial report immediately

    Validate the full implementation against spec acceptance criteria.
    Required outputs:
    - Step 3: Per-criterion pass/fail table
    - Step 5: Issue categorization (critical/major/minor counts)
    - Step 7: Write verification-result.json with all required fields
    - Step 8: Return the verification report

    Create fix tasks for any issues found. Do NOT implement fixes yourself.
```

**Timeout handling:** Phase-level verification has a higher `max_turns` (50) because it covers the entire implementation. The verify-agent has its own timeout handling protocol (see verify-agent.md § "Timeout Handling") that prioritizes writing a partial `verification-result.json` before exhausting turns. If the agent still exits without writing the file, report to user and suggest retrying or running `/health-check`.

**After phase-level verification completes:**

Check `.claude/verification-result.json`:

| Result | Action |
|--------|--------|
| `pass` | Proceed to "If Completing" section |
| `pass_with_issues` | Proceed to "If Completing" section. Present any out-of-spec recommendation tasks for user approval. |
| `fail` | In-spec fix tasks were created. Loop back to Execute: route to implement-agent for fix tasks, then re-verify when all spec tasks are finished again. |

**In-spec fix tasks vs out-of-spec recommendations:**
- Fix tasks for bugs (spec requires it but implementation is broken) are regular tasks — they route to execute automatically.
- Recommendation tasks (beyond spec) are `out_of_spec: true` — they require user approval at phase boundaries.

#### If Completing

When all tasks are finished and verification conditions are met:

**MANDATORY GATE — Check before proceeding:**

1. **Verify per-task verification completeness:** Every "Finished" spec task must have `task_verification.result == "pass"`. If any task fails this check, route to verify-agent per-task mode.

2. **Verify phase-level verification exists and is valid:** `.claude/verification-result.json` must exist with `result` of "pass" or "pass_with_issues", matching `spec_fingerprint`, and no tasks modified after `timestamp`. If any check fails, route to verify-agent phase-level mode.

**Once both gates pass:**

1. **Update spec status** to `complete`:
   ```yaml
   ---
   version: 1
   status: complete
   updated: YYYY-MM-DD
   ---
   ```

2. **Regenerate dashboard with completion summary:** Update header to show "Complete" stage, replace Progress section's critical path with final stats (task count, verification date, spec status).

3. **Present final checkpoint:** Report completion with verification summary. Note how to continue (update spec, run `/work`).

4. **Stop** — do not route to any agent. The project is done.

### Step 5: Handle Questions

Questions accumulate in `.claude/support/questions/questions.md` during work.

**Check for questions at these points:**
- After completing a task (before selecting the next one)
- At phase boundaries (Execute → Verify, Verify → Complete)
- When a `[BLOCKING]` question is added
- When quality gate fails (tests fail, spec violation)

**Process:**

1. **Read `.claude/support/questions/questions.md`** — check for unresolved questions (items under Requirements, Technical, Scope, or Dependencies that aren't in the Answered table)

2. **If questions exist, present them:**
   ```
   Questions for you (from questions.md):

   ## Requirements
   - [2026-01-15] Should login require email verification?

   ## Technical
   - [2026-01-20] [BLOCKING] What caching solution to use?

   Please answer, or [S] Skip for now.
   ```

3. **After user answers:**
   - Move the question and answer to the "Answered Questions" table in `questions.md`
   - If the answer affects the spec, note it: "Consider updating spec section [X]"
   - If the answer affects a task, update the task notes
   - Continue with the next action

4. **If no questions or user skips:** Continue to Step 6.

**Blocking questions:** Questions prefixed with `[BLOCKING]` halt work until answered. `/work` will not proceed to the next task or phase while blocking questions remain unresolved.

**Dashboard integration:** Unresolved questions (especially blocking ones) appear in the dashboard's "Action Required" → "Reviews" sub-section during regeneration.

### Step 6: Operational Checks

<!-- TODO: Define operational checks inline here during work.md deep dive.
     These were previously delegated to health-check.md Part 6, which has been removed.
     health-check.md is now a standalone manual maintenance tool.
     The operational checks that /work needs should be defined directly in this step. -->

Run quick validation after task dispatch to catch issues before they compound. Use `/health-check` for full maintenance validation (Parts 1-5).

---

## Spec Alignment Examples

- **Aligned:** "Add password validation" when spec says "User authentication with email and password" → proceed
- **Minor:** "Fix typo in login error" when spec doesn't mention errors → proceed (within scope)
- **Misaligned:** "Add Google login" when spec says only email/password → surface options (add to spec, proceed anyway, skip)

---

## Decomposition Guidelines

When breaking spec into tasks:

- Each task has clear "done" criteria
- Tasks are independently testable
- Dependencies are explicit
- Difficulty ≤ 6 (break down anything larger)

Organize tasks into implementation stages (Foundation → Core → Polish → Validation). See `.claude/support/reference/workflow.md` for stage definitions.

For the difficulty scale, see `.claude/support/reference/shared-definitions.md`.

### Critical Path Generation

Renders the critical path as a one-liner in the Progress section. Owners: `❗` (human), `🤖` (Claude), `👥` (both). Parallel branches use `[step A | step B]` notation. >5 steps → show first 3 + "... N more → Done".

**Full algorithm:** `.claude/support/reference/dashboard-regeneration.md` § "Critical Path Generation"

### Project Overview Diagram

Inline Mermaid `graph LR` diagram in the Progress section when 4+ tasks remain. Completed phases collapse to single nodes; active tasks show individually with ownership prefixes. >15 nodes → clump by phase/area. Phase gates use hexagon nodes (`{{}}`). Nodes styled with `classDef`: done (green), active (blue), human-owned (yellow), blocked (grey).

**Full rules:** `.claude/support/reference/dashboard-regeneration.md` § "Project Overview Diagram"

---

## Output

Reports:
- Current phase and what was done
- Any spec misalignments surfaced
- Questions requiring human input
- Next steps or blockers

## Examples

```
# Auto-detect and continue work
/work

# Work on specific task
/work 5

# Handle ad-hoc request (gets spec-checked)
/work "Add rate limiting to the API"

# Complete the current in-progress task
/work complete

# Complete a specific task
/work complete 5

# After answering questions, continue
/work
```

---

## Task Completion (`/work complete`)

Use `/work complete` for manual task completion outside of implement-agent's workflow. This is useful when:
- Completing human-owned tasks
- Marking tasks done that were worked on outside the normal flow
- Quick tasks that don't need the full implement-agent process

**Note:** When implement-agent executes tasks, it handles completion internally (Steps 3-6 of its workflow). You don't need to run `/work complete` after implement-agent finishes.

### Process

1. **Identify task** - If no ID provided, use current "In Progress" task
2. **Validate task is completable:**
   - Status must be "In Progress", OR "Finished" with `user_review_pending: true` (user reviewing a `both`-owned task)
   - Reject: "Pending", "Broken Down", "On Hold", "Absorbed", or "Finished" without `user_review_pending`
   - For quick tasks, first set status to "In Progress", then complete
   - Dependencies must all be "Finished"
3. **Check work** - Review all changes made for this task
   - Look for bugs, edge cases, inefficiencies
   - If issues found, fix them before proceeding
3b. **Capture inline feedback** - Read dashboard for `<!-- FEEDBACK:{id} -->` markers matching the completing task
   - If non-empty content found (user wrote feedback between the markers), save it to the task JSON `user_feedback` field in Step 4
   - This ensures feedback is captured before dashboard regeneration clears the inline area
4. **Update task file:**
   ```json
   {
     "status": "Finished",
     "completion_date": "YYYY-MM-DD",
     "updated_date": "YYYY-MM-DD",
     "notes": "What was done, any follow-ups needed",
     "user_feedback": "Use OAuth2 instead of JWT. The client requires SSO support."
   }
   ```
   - If `user_review_pending` is `true`, clear it (set to `false` or remove the field). This signals the user has reviewed the task.
5. **Check parent auto-completion:**
   - If parent_task exists and all non-Absorbed sibling subtasks are "Finished"
   - Set parent status to "Finished"
6. **Regenerate dashboard** - Follow `.claude/support/reference/dashboard-regeneration.md`
   - Additional completion requirements:
     - Update overall completion percentage
     - Recalculate critical path line in Progress section with remaining incomplete tasks
     - Add completed task to Recently Completed with completion_date
7. **Auto-archive check** - If active task count > 100, archive old tasks
8. **Operational checks** - Run quick validation (see Step 6 in main process)

### Rules

- Never work on "Broken Down", "On Hold", or "Absorbed" tasks directly
- Parent tasks auto-complete when all non-Absorbed subtasks finish
- Always add notes about what was actually done

---

## Auto-Archive

After regenerating the dashboard, check if archiving is needed:

1. **Count active tasks** - All non-archived task-*.json files
2. **If count > 100:**
   - Identify finished tasks older than 7 days
   - Move to `.claude/tasks/archive/`
   - Update archive-index.json with lightweight summaries
   - Regenerate dashboard again

### Archive Structure

```
.claude/tasks/archive/
├── task-1.json           # Full task data (preserved)
├── task-2.json
└── archive-index.json    # Lightweight summary
```

### Referencing Archived Tasks

When a task ID is referenced but not found in active tasks:
- Check `.claude/tasks/archive/` for context
- Read archived task for reference (provides historical context)
- Archived tasks are read-only reference material
