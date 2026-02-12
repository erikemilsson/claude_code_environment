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

**Dashboard regeneration:** After significant state changes, dashboard.md is regenerated per `.claude/support/reference/dashboard-regeneration.md` § "When to Regenerate".

---

## Process

### Step 0: Session Recovery Check

Check for tasks left in recoverable states by a previous session. Read `.claude/support/reference/session-recovery.md` and follow its procedure:
1. **Check session sentinel** (`.claude/tasks/.last-clean-exit.json`) — if clean exit, skip full scan
2. **If sentinel missing or stale** — run full recovery scan (6-case logic in the reference file)
3. **After recovery actions complete** — proceed to Step 1

**Malformed files during scan:** If a task file fails to parse during Step 0, skip it and continue. Report the error in Step 1.

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
- `.claude/dashboard.md` - Task status and progress (read the `<!-- DASHBOARD META -->` block)
- `.claude/support/questions/questions.md` - Pending questions

**Fast-path optimization:** If dashboard META block shows matching task_count and spec_fingerprint, skip Steps 1a/1b and jump to Step 1c. Always check drift-deferrals.json for stale deferrals even on fast-path. Full procedure: `.claude/support/reference/work-fastpath.md`.

**Malformed task file handling:** When reading task JSON files, if any file fails to parse:
1. Skip the file — do not abort the entire scan
2. Report the error prominently: "Task file `task-{id}.json` could not be read: {error}. Run `/health-check` for details."
3. Exclude the corrupted file from all calculations
4. If other tasks depend on the corrupted task, treat those dependencies as unresolvable (task effectively Blocked)

### Step 1a: Dashboard Freshness Check

Verify the dashboard is current before using its data. Compute a SHA-256 hash of all task IDs and statuses, compare against the dashboard's `<!-- DASHBOARD META -->` block. If the hash differs or no metadata exists, regenerate the dashboard from task JSON files before continuing.

**Full procedure:** `.claude/support/reference/drift-reconciliation.md` § "Dashboard Freshness Check"

### Step 1b: Spec Drift Detection

Compare the current spec's SHA-256 fingerprint against task fingerprints. If different, perform section-level analysis to identify which sections changed and group affected tasks.

**Full procedure:** `.claude/support/reference/drift-reconciliation.md` § "Spec Drift Detection"

### Step 1c: Spec State Summary

After drift detection completes (or was skipped by fast-path), output a brief status line:

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

### Drift Reconciliation (if triggered)

When Step 1b detects spec drift, the following checks run in sequence. Each delegates to `drift-reconciliation.md` for the full procedure:

1. **Substantial change detection** — evaluates change magnitude, may suggest version bump. § "Substantial Change Detection"
2. **Task migration** (version transitions only) — migrates task provenance to new spec version. § "Task Migration on Version Transition"
3. **Drift budget enforcement** — checks deferred reconciliations against limits. § "Drift Budget Enforcement"
4. **Granular reconciliation UI** — per-section options: `[A]` Apply, `[R]` Review, `[S]` Skip. § "Granular Reconciliation UI"

**Post-reconciliation In Progress warning:** After reconciliation completes, check if any "In Progress" tasks had their section fingerprints updated. If so, warn:

```
⚠️ Task {id} "{title}" is In Progress but its spec section changed during reconciliation.
  Review the task's partial work against the updated requirements before continuing.
```

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

**Scope significance:** New features, architecture changes, new integrations, acceptance criteria changes = significant. Bug fixes, cleanup, small improvements = minor/trivial.

### Step 2b: Phase and Decision Gate

Check whether phases or unresolved decisions block any intended work.

Read `.claude/support/reference/phase-decision-gates.md` and follow its procedure. The reference file contains:
- Phase check (walking phases ascending, gate conditions)
- Decision dependency check (resolving checked boxes, auto-updating frontmatter)
- Late decision check (reverse cross-reference for new decisions)
- Post-decision check (inflection point handling)
- Early-exit conditions (skip when no phases or no decisions exist)

**When a decision blocks work**, present options including research:
```
Decision {DEC-NNN}: "{title}" is unresolved and blocks Task {id}.
  [R] Research options (spawns research-agent to investigate and populate the decision record)
  [S] Skip (you'll research manually — non-blocked tasks still dispatch normally)
```

If user selects `[R]`: Gather context (decision record, spec, related tasks/decisions), then spawn research-agent. See `.claude/commands/research.md` Steps 2-4 for the delegation flow. After research completes, re-present the decision for user selection. If user selects via checkbox, auto-update frontmatter per the phase-decision-gates procedure and continue.

If all checks pass → proceed to Step 2c.

### Step 2c: Parallelism Eligibility Assessment

After phase and decision checks, assess whether multiple tasks can be dispatched in parallel.

**Full procedure:** `.claude/support/reference/parallel-execution.md` § "Parallelism Eligibility Assessment"

**Summary:** Read `parallel_execution` from spec frontmatter (defaults: `enabled: true`, `max_parallel_tasks: 3`). Eligible tasks must be Pending, not human-owned, all deps Finished, in active phase, all decision deps resolved, difficulty < 7. Build conflict-free batch by pairwise-comparing `files_affected`. If batch >= 2, set `parallel_mode = true`.

### Step 3: Determine Action

**If a specific request was provided** (and passed spec check):
1. Create a task for the request (or find existing matching task)
2. Route to the "If Executing" section in Step 4
3. Continue to Step 5 (questions) and Step 6 (validation)

**If no request provided** (auto-detect mode):

| Condition | Action |
|-----------|--------|
| No spec exists, no tasks | Stop — direct user to create spec via `/iterate` |
| No spec exists, tasks exist | **Stop and warn** — tasks without a spec cannot be verified. Options: `[S]` Create spec, `[M]` Mark all out-of-spec, `[X]` Stop. |
| Spec incomplete | Stop — prompt user to complete spec |
| Spec complete, no tasks | **Decompose** — read and follow `decomposition.md` |
| Phase transition pending approval | **Stop** — direct user to approve phase gate in dashboard *(enforced by Step 2b)* |
| Any spec task in "Awaiting Verification" | **Verify (per-task)** — see Step 4 |
| Spec tasks pending, parallel batch >= 2 | **Execute (Parallel)** — see Step 4 |
| Spec tasks pending, no parallel batch | **Execute** — see Step 4 |
| All spec tasks "Finished" with passing verification, no valid phase verification result | **Verify (phase-level)** — see Step 4 |
| Phase-level verification `"fail"` (fix tasks exist) | **Execute** — fix tasks need implementation |
| All spec tasks finished, valid phase verification result | **Complete** — see Step 4 |

**Priority order matters.** Per-task verification takes priority over executing the next task.

**CRITICAL: Verification enforcement.** Before routing to phase-level verification or completion, EVERY "Finished" spec task must have `task_verification.result == "pass"`. Never skip this check.

**Note on enforcement mechanism:** This verification requirement is enforced *procedurally* through workflow ordering (the routing algorithm below), not *structurally* at the file-write level. The workflow ensures compliance through status transition sequencing: tasks can only reach "Finished" after passing per-task verification. `/health-check` detects violations after the fact (verification debt), but the primary enforcement is through the explicit routing checks below that prevent bypassing verification during normal operation.

**Explicit routing algorithm:**
```
1. Get all spec tasks (exclude out_of_spec: true, exclude status "Absorbed")
2. awaiting_verification = tasks where status == "Awaiting Verification"
3. IF awaiting_verification is not empty:
   → Route to verify-agent (per-task) for first task
   → Do NOT proceed to phase-level or completion
4. finished_tasks = tasks where status == "Finished"
5. unverified_finished = finished_tasks where task_verification does not exist
6. IF unverified_finished is not empty:
   → Route to verify-agent (per-task) for first unverified task
7. ELSE IF all spec tasks are "Finished" AND all have passing verification:
   → Check verification-result.json
   → IF file missing → Route to verify-agent (phase-level)
   → IF result == "fail" → Route to implement-agent (fix tasks)
   → IF spec_fingerprint mismatch OR tasks updated after timestamp → Re-verify
   → IF result == "pass" → Route to completion
8. ELSE IF parallel_mode (from Step 2c):
   → Route to parallel execution
9. ELSE:
   → Route to implement-agent for next pending task
```

**Important — spec tasks vs out-of-spec tasks:** Phase routing is based on spec tasks only (excluding `out_of_spec: true`). Out-of-spec tasks are excluded from phase detection to prevent a verify → execute → verify infinite loop.

**Out-of-spec task handling:** After phase routing completes (or at phase boundaries), check for pending out-of-spec tasks: `[A]` Accept (sets `out_of_spec_approved: true`), `[R]` Reject, `[D]` Defer, `[AA]` Accept all. Never auto-execute out-of-spec tasks.

**Reject behavior (`[R]`):**
1. Prompt for optional rejection reason
2. Set `out_of_spec_rejected: true` and `rejection_reason` (if provided) on task JSON
3. Move task file to `.claude/tasks/archive/`
4. Task preserved for audit trail but excluded from active processing and dashboard

### Step 4: Execute Action

#### If Decomposing (spec → tasks)

Read `.claude/support/reference/decomposition.md` and follow its 10-step procedure to break the spec into granular tasks with full provenance fields.

#### If Executing

Read `.claude/agents/implement-agent.md` and follow Steps 1-6. Required artifacts:
   - Step 1: Task selected (logged)
   - Step 1b: Validation checks passed
   - Step 3: Task JSON updated to `"In Progress"` **before any implementation begins**
   - Step 4: Implementation done
   - Step 5: Self-review completed
   - Step 6a: Task JSON updated to `"Awaiting Verification"`
   - Step 6b: verify-agent **spawned as a separate Task agent** (fresh context)
   - Step 6c: Dashboard regenerated
3. **Context to provide:** Current task, relevant spec sections, constraints/notes

#### If Executing (Parallel)

When Step 2c produces a parallel batch of >= 2 tasks, execute them concurrently.

**Full procedure:** `.claude/support/reference/parallel-execution.md` § "Parallel Dispatch"

**Key rules:**
- Each parallel agent reads `implement-agent.md` and runs Steps 2/4/5/6a/6b independently
- Agents must NOT regenerate dashboard, select next task, or check parent auto-completion
- After all agents complete: final parent auto-completion, single dashboard regeneration, Step 6

#### If Verifying (Per-Task)

**You must spawn verify-agent as a separate agent. Do not verify inline.**

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

    Verify the implementation independently. Do NOT assume correctness.
```

**Timeout handling:** If verify-agent exhausts `max_turns` without completing, treat as verification failure — increment `verification_attempts`, set task to "Blocked" with `[VERIFICATION TIMEOUT]` note, report to user.

**After per-task verification completes:**
- **Pass**: If `owner: "both"`, verify `user_review_pending: true` was set. Proceed to next pending task.
- **Fail**: Task set to "In Progress". Route to implement-agent to fix, then re-verify. Loop until pass.
- Regenerate dashboard after status changes (per `dashboard-regeneration.md` § "When to Regenerate").

#### If Verifying (Phase-Level)

**You must use the verify-agent phase-level workflow. Do not verify directly.**

**MANDATORY: Reconciliation Gate** — Before starting phase-level verification, ALL drift must be reconciled. Check `drift-deferrals.json`; if any deferrals exist, block verification until reconciled.

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

    Validate the full implementation against spec acceptance criteria.
    Create fix tasks for any issues found. Do NOT implement fixes yourself.
```

**After phase-level verification completes:** Check `.claude/verification-result.json`:

| Result | Action |
|--------|--------|
| `pass` | Proceed to "If Completing". Present any out-of-spec recommendations for user approval. |
| `fail` | Fix tasks created. Loop back to Execute, then re-verify when all spec tasks finished. |

#### If Completing

When all tasks are finished and verification conditions are met:

**MANDATORY GATE — Check before proceeding:**

1. **Verify per-task completeness:** Every "Finished" spec task must have `task_verification.result == "pass"`. If any fails, route to verify-agent per-task.
2. **Verify phase-level result:** `.claude/verification-result.json` must exist with passing result, matching `spec_fingerprint`, no tasks modified after `timestamp`. If any fails, route to verify-agent phase-level.

**Once both gates pass:**

1. **Update spec status** to `complete` (set `status: complete`, `updated: YYYY-MM-DD` in frontmatter)
2. **Regenerate dashboard** with completion summary
3. **Present final checkpoint** — report completion with verification summary
4. **Stop** — do not route to any agent. The project is done.

### Step 5: Handle Questions

Questions accumulate in `.claude/support/questions/questions.md` during work.

**Check for questions at these points:**
- After completing a task (before selecting the next one)
- At phase boundaries (Execute → Verify, Verify → Complete)
- When a `[BLOCKING]` question is added
- When quality gate fails (tests fail, spec violation)

**Process:**

1. **Read `.claude/support/questions/questions.md`** — check for unresolved questions
2. **If questions exist, present them** grouped by category. Include `[S]` Skip option.
3. **After user answers:** Move to "Answered Questions" table, update affected spec/task notes
4. **If no questions or user skips:** Continue to Step 6.

**Blocking questions** prefixed with `[BLOCKING]` halt work until answered.

### Step 6: Post-Dispatch Validation

Run quick validation after task dispatch to catch issues early:

1. **Task file integrity** — Verify the task JSON that was just modified is valid JSON and parseable
2. **Dashboard exists** — Confirm `.claude/dashboard.md` exists and has a `<!-- DASHBOARD META -->` block
3. **Session sentinel** — Write `.claude/tasks/.last-clean-exit.json` with current timestamp and in-progress task list (enables fast-path recovery check on next `/work` run)

For full maintenance validation (schema checks, decision integrity, template sync), use `/health-check`.

---

## Spec Alignment Examples

- **Aligned:** "Add password validation" when spec says "User authentication with email and password" → proceed
- **Minor:** "Fix typo in login error" when spec doesn't mention errors → proceed (within scope)
- **Misaligned:** "Add Google login" when spec says only email/password → surface options (add to spec, proceed anyway, skip)

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
   - Status must be "In Progress", OR "Finished" with `user_review_pending: true`
   - Reject: "Pending", "Broken Down", "On Hold", "Absorbed", or "Finished" without `user_review_pending`
   - For quick tasks, first set status to "In Progress", then complete
   - Dependencies must all be "Finished"
3. **Check work** - Review all changes made for this task
   - Look for bugs, edge cases, inefficiencies
   - If issues found, fix them before proceeding
3b. **Capture inline feedback** - Read dashboard for `<!-- FEEDBACK:{id} -->` markers matching the completing task
   - If non-empty content found, save to task JSON `user_feedback` field
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
   - If `user_review_pending` is `true`, clear it.
5. **Check parent auto-completion:**
   - If parent_task exists and all non-Absorbed sibling subtasks are "Finished"
   - Set parent status to "Finished"
6. **Regenerate dashboard** - Follow `.claude/support/reference/dashboard-regeneration.md`
7. **Auto-archive check** - If active task count > 100, archive old tasks
8. **Post-dispatch validation** - Run Step 6 checks

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
