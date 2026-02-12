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

### Step 1a: Dashboard Freshness Check

Before using dashboard data, verify it's current:

1. **Compute current task state hash:**
   ```
   task_hash = SHA-256(sorted list of: task_id + ":" + status for each task-*.json)
   ```

2. **Read dashboard metadata** (if present):
   ```markdown
   <!-- DASHBOARD META
   generated: 2026-01-28T14:30:00Z
   task_hash: sha256:abc123...
   -->
   ```

3. **Compare hashes:**
   ```
   If dashboard has no META block OR task_hash differs:
   ├─ Log: "Dashboard stale — regenerating"
   ├─ Backup user section to .claude/support/workspace/dashboard-notes-backup.md
   ├─ Regenerate dashboard from task JSON files
   └─ Continue with fresh dashboard
   ```

**Why this matters:** Dashboard can become stale if tasks are modified outside `/work`. This check ensures you always work from accurate data.

### Step 1b: Spec Drift Detection (Granular)

After reading the spec, perform section-level drift detection:

1. **Compute current spec fingerprint** - SHA-256 hash of spec file content
2. **Check existing tasks** - Read `spec_fingerprint` and `section_fingerprint` from task files
3. **Compare fingerprints:**

```
If tasks exist with spec_fingerprint:
├─ Full spec fingerprint matches → Continue normally
└─ Full spec fingerprint differs → Perform granular section analysis:
   1. Parse current spec into sections (## level headings)
   2. Load snapshot from section_snapshot_ref (if exists)
   3. Parse snapshot spec into sections
   4. For each section, compare fingerprints
   5. Identify which sections changed
   6. Group affected tasks by changed section
   7. Present granular reconciliation UI
```

**Hash computation:**
```bash
# Use shasum (available on macOS and Linux; sha256sum is Linux-only)
shasum -a 256 .claude/spec_v{N}.md | cut -d' ' -f1
# Prefix with "sha256:" → "sha256:a1b2c3d4..."
```

**Section fingerprint computation:**
```bash
# For each ## section, hash: heading + all content until next ## or EOF
printf '%s' "## Authentication\nContent here..." | shasum -a 256 | cut -d' ' -f1
# Prefix with "sha256:" → "sha256:e5f6g7h8..."
```

**Note:** Tasks without `spec_fingerprint` are treated as legacy (no warning). Tasks without `section_fingerprint` fall back to full-spec comparison.

### Step 1c: Spec State Summary

After drift detection completes, always output a brief status line so the user knows where things stand:

```
If no tasks exist:
  "Spec: v{N} (draft) — no tasks yet"

If tasks exist and spec is aligned:
  "Spec: v{N} (active) — aligned with tasks ✓"
  "Tasks: {total} total ({finished} finished, {in_progress} in progress, {pending} pending)"

If tasks exist and spec has changed:
  "Spec: v{N} (active) — {M} sections changed since decomposition"
  "Tasks: {total} total ({finished} finished, {in_progress} in progress, {pending} pending)"

If version transition detected (tasks reference older spec version):
  "Spec: v{N} (draft) — new version, tasks reference v{N-1}"
  "Tasks: {total} total — migration needed (see below)"
```

This runs AFTER drift detection (Step 1b) so it can accurately report section changes.

### Substantial Change Detection

Before showing the reconciliation UI, evaluate the magnitude of changes and respond accordingly.

**Heuristic — changes are "substantial" when ANY of:**
- More than 50% of sections have changed fingerprints
- New sections were added (scope expansion)
- Sections were deleted (scope reduction)
- Spec has been `active` for > 7 days AND > 3 sections changed

**If changes are NOT substantial:**

Proceed directly to the Granular Reconciliation UI (below). Small edits are absorbed into the current version via normal drift reconciliation.

**If changes ARE substantial:**

Present a version bump suggestion before reconciliation:

```
Spec has changed significantly since tasks were created:
  - {X} of {Y} sections modified
  - {A} new sections added / {B} sections deleted
  - Estimated {P}% of content changed

This may warrant a new spec version.

[V] Create spec v{N+1} (archives current version, then reconcile)
[C] Continue as v{N} (reconcile changes in place)
```

- **If user picks [V]:** Execute the Version Transition Procedure (see `iterate.md` § "Version Transition Procedure"), then run Task Migration (below), then proceed to reconciliation against the new version.
- **If user picks [C]:** Proceed directly to the Granular Reconciliation UI. Changes are absorbed into the current version.

Either choice preserves the user's edits. The version bump is about organizational clarity, not data safety.

### Task Migration on Version Transition

When `/work` detects that existing tasks reference an older spec version (tasks have `spec_version: "spec_v{M}"` but current spec is `spec_v{N}` where N > M), perform task migration:

```
For each task:
  IF status == "Finished":
    → Leave provenance unchanged (historical record)
    → These tasks were verified against the old spec — that's correct

  IF status == "Pending" or "In Progress":
    → Check if task's spec_section heading still exists in new spec
    │
    ├─ Section exists, content matches:
    │  → Update task: spec_version, spec_fingerprint, section_fingerprint
    │  → Task continues normally
    │
    ├─ Section exists, content changed:
    │  → Update spec_version reference
    │  → Flag for reconciliation (handled by Granular Reconciliation UI)
    │
    └─ Section does not exist in new spec:
       → Present to user:
       │
       │  Task {id} "{title}" references section "{spec_section}"
       │  which no longer exists in spec v{N}.
       │
       │  [D] Delete task
       │  [O] Keep as out-of-spec
       │  [R] Reassign to different section
```

**After migration:** Update the decomposed snapshot reference. Create `spec_v{N}_decomposed.md` if decomposition runs, or update `section_snapshot_ref` on migrated tasks to point to the new spec version's snapshot.

### Drift Budget Enforcement

To prevent drift from accumulating indefinitely, enforce a drift budget:

**Configuration (in spec frontmatter):**
```yaml
---
version: 1
status: active
drift_policy:
  max_deferred_sections: 3      # Max sections that can be deferred
  max_deferral_age_days: 14     # Max days a deferral can persist
---
```

**Default values (if not configured):** `max_deferred_sections: 3`, `max_deferral_age_days: 14`

**Tracking deferred reconciliations:**

When user selects "Skip section" during reconciliation, record it:
```json
// In .claude/drift-deferrals.json
{
  "deferrals": [
    {
      "section": "## Authentication",
      "deferred_date": "2026-01-20",
      "affected_tasks": ["3", "4", "7"]
    }
  ]
}
```

**Enforcement logic:**
```
On each /work run:
1. Read drift-deferrals.json (if exists)
2. Count active deferrals (not yet reconciled)
3. Check for expired deferrals (older than max_deferral_age_days)

IF active_deferrals > max_deferred_sections OR any deferral expired:
  ├─ ERROR: Drift budget exceeded
  │
  │  You have deferred reconciliation for N sections (max: M).
  │  [OR] Deferral for "## SectionName" has expired (deferred N days ago, max: M days).
  │
  │  Must reconcile at least 1 section before continuing.
  │
  │  [R] Reconcile now (REQUIRED)
  │
  └─ Block all other actions until reconciliation completes
```

**Clearing deferrals:** When a section is reconciled (user selects Apply or reviews individually and applies), remove it from `drift-deferrals.json`.

**See also:**
- `/health-check` performs the same drift detection as a validation check. Keep algorithms in sync.
- `.claude/support/reference/workflow.md` § "Spec Change and Feature Addition Workflow" for the end-to-end process (user edits spec → detection → confirmation → task updates → implementation → verification).

### Granular Reconciliation UI

When section-level drift is detected, present a targeted UI showing:
- Section name and number of affected tasks
- Diff of changed content
- Table of affected tasks with suggested actions

**Options per section:** `[A]` Apply suggestions, `[R]` Review individually, `[S]` Skip section

**Individual task review options:** `[A]` Apply, `[E]` Edit, `[S]` Skip, `[O]` Mark out-of-spec

**Edge cases:** New section → suggest new tasks. Section deleted → flag tasks for out-of-spec or deletion. Section renamed → detected as delete + add. No snapshot → fall back to full-spec comparison.

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
   Determine current active phase:
   ├─ Group tasks by `phase` field
   ├─ Find lowest phase number where any task is not "Finished"
   ├─ This is the active phase
   │
   │  For target task(s):
   │  IF task.phase > active_phase:
   │    "Task {id} is in Phase {task.phase}, but Phase {active_phase} is still in progress.
   │     {N} tasks remaining in Phase {active_phase}."
   │    → Skip this task, work on active-phase tasks instead
   │
   │  IF no tasks remain in active phase and all are "Finished":
   │    IF tasks exist in a higher phase (next_phase exists):
   │      1. Read dashboard for phase gate marker: <!-- PHASE GATE:{active_phase}→{next_phase} -->
   │      2. IF marker contains checked box [x]:
   │           → Phase transition approved. Clear the marker from dashboard.
   │           → Log: "Phase {active_phase} → {next_phase} approved"
   │           → Execute Version Transition Procedure (see iterate.md § "Version Transition Procedure")
   │           → Suggest running /iterate to flesh out Phase {next_phase} sections
   │      3. IF marker absent OR contains unchecked box [ ]:
   │           → Regenerate dashboard with phase gate in Action Required (see Dashboard Regen § Phase Transitions)
   │           → Log: "Phase {active_phase} complete. Approve transition in dashboard, then run /work."
   │           → STOP — do not dispatch Phase {next_phase} tasks
   │    ELSE (single-phase project or final phase):
   │      → Fall through to Step 3 routing (phase-level verification → completion)

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

After phase and decision checks, assess whether multiple tasks can be dispatched in parallel.

**1. Read configuration:**
```
Read parallel_execution from spec frontmatter:
├─ enabled: true (default)
├─ max_parallel_tasks: 3 (default)
└─ If not present, use defaults
```

If `enabled: false`, skip to Step 3 (sequential mode).

**2. Gather eligible tasks:**
```
eligible = tasks where ALL of:
  - status == "Pending"
  - owner != "human"
  - all dependencies have status "Finished"
  - task.phase <= active_phase (no phase dependency blocks the task)
  - all decision_dependencies are resolved
  - difficulty < 7
```

**3. Build conflict-free batch:**

**File conflict detection algorithm:**

Two paths conflict if either could affect the other's output. The comparison uses **normalized paths** and **directory containment**:

```
FUNCTION paths_conflict(path_a, path_b) -> bool:
  # 1. Normalize both paths: resolve "." and "..", lowercase on case-insensitive
  #    filesystems (macOS), strip trailing slashes
  a = normalize(path_a)
  b = normalize(path_b)

  # 2. Exact match
  IF a == b: return true

  # 3. Directory containment: if either path is a prefix of the other
  #    (a directory contains a file, or vice versa)
  #    e.g., "src/" conflicts with "src/auth.py"
  #    e.g., "src/models/" conflicts with "src/models/user.py"
  IF a.startswith(b + "/") OR b.startswith(a + "/"): return true

  # 4. No conflict
  return false
```

**Rules:**
- Paths are relative to project root (no leading `./ `)
- `src/auth.py` vs `src/auth.py` → conflict (exact match)
- `src/` vs `src/auth.py` → conflict (directory containment)
- `src/auth.py` vs `src/models.py` → no conflict (different files)
- `.env` vs `.env.example` → no conflict (different files)
- Glob patterns in `files_affected` (e.g., `src/*.py`) are expanded before comparison

```
batch = []
held_back = []  # tracks tasks skipped due to file conflicts

For each eligible task (sorted by priority, then ID):
  conflicts = false
  conflict_with = null
  conflict_files = []
  For each task already in batch:
    For each pair (file_a from task.files_affected, file_b from batch_task.files_affected):
      IF paths_conflict(file_a, file_b):
        conflicts = true
        conflict_with = batch_task.id
        conflict_files.append(file_a + " vs " + file_b)
        break
    IF conflicts: break
  IF task has empty files_affected AND parallel_safe != true:
    skip (unknown file impact — not safe for parallel)
  ELSE IF conflicts:
    held_back.append({
      task_id: task.id,
      blocked_by: conflict_with,
      conflict_files: conflict_files
    })
  ELSE IF len(batch) < max_parallel_tasks:
    add task to batch
```

**4. Determine dispatch mode:**
```
IF len(batch) >= 2:
  → parallel_mode = true
  → Log: "Parallel dispatch: {batch_size} tasks eligible"
  → IF held_back is non-empty:
      Log for each: "Task {id} held back — file conflict with Task {conflict_with} on: {conflict_files}"
ELSE:
  → parallel_mode = false
  → Fall back to sequential execution in Step 3
```

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
| Phase transition pending approval (phase gate unchecked in dashboard) | **Stop** — direct user to approve phase transition in dashboard |
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
1. Get all spec tasks (exclude out_of_spec: true)
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
7b. Check for pending phase gate:
   → IF Step 2b detected a phase transition needing approval (gate unchecked or absent):
     → STOP — direct user to approve phase transition in dashboard
     → Do NOT proceed to steps 8 or 9
8. ELSE IF parallel_mode (from Step 2c):
   → Route to parallel execution (see "If Executing (Parallel)")
9. ELSE:
   → Route to implement-agent for next pending task (sequential)
```

**Spec-less project handling:** If tasks exist but no spec file is found, do NOT proceed. Present options: `[S]` Create spec via `/iterate`, `[M]` Mark all tasks out-of-spec, `[X]` Stop. This prevents completing without verification.

**Important — spec tasks vs out-of-spec tasks:** Phase routing is based on **spec tasks only** (tasks without `out_of_spec: true`). Out-of-spec tasks (recommendations from verify-agent or user requests that bypassed the spec) are excluded from phase detection. This prevents the verify → execute → verify infinite loop.

**Phase-level verification result check:** Read `.claude/verification-result.json`. A result is valid when `result` is `"pass"` or `"pass_with_issues"`, `spec_fingerprint` matches the current spec, and no tasks changed since `timestamp`. See verify-agent Phase-Level Step 7 for the file format.

**Out-of-spec task handling:** After phase routing completes (or at phase boundaries), check for pending out-of-spec tasks and present them with options: `[A]` Accept (sets `out_of_spec_approved: true`), `[R]` Reject (deletes task), `[D]` Defer (skips for now), `[AA]` Accept all.

**Rule:** Never auto-execute an out-of-spec task. Always require explicit user approval first.

### Step 4: Execute Action

#### If Decomposing (spec → tasks)

Break the spec into granular tasks:

1. **Read spec thoroughly** - Understand all requirements and acceptance criteria
2. **Compute spec fingerprint** - SHA-256 hash of spec content (see Step 1b)
3. **Save spec snapshot** - Copy current spec to `.claude/support/previous_specifications/spec_v{N}_decomposed.md`
4. **Parse spec into sections** - Extract ## level headings and their content
5. **Compute section fingerprints** - SHA-256 hash of each section (heading + content)
6. **Identify work items** - Each distinct piece of functionality per section
7. **Create task files** - One JSON per task, difficulty ≤ 6, with full provenance:
   - `spec_fingerprint` - Hash of full spec computed in step 2
   - `spec_version` - Filename of spec (e.g., "spec_v1")
   - `spec_section` - Originating section heading (e.g., "## Authentication")
   - `section_fingerprint` - Hash of specific section computed in step 5
   - `section_snapshot_ref` - Snapshot filename (e.g., "spec_v1_decomposed.md")
   - **Important:** Create all task JSON files before regenerating the dashboard. Every task must have a `task-*.json` file — the dashboard is generated from these files, never the other way around.
8. **Map dependencies** - What must complete before what
9. **Regenerate dashboard** - Read all task-*.json files and regenerate dashboard.md
   - **Follow the Dashboard Regeneration Procedure** below — use exact section headings, emojis, and the Section Format Reference for all formatting rules
   - **Check section toggles** — read the dashboard checklist (between `<!-- SECTION TOGGLES -->` markers) and respect `build`/`exclude` modes per section. Falls back to spec frontmatter `dashboard_sections` if no checklist exists.
   - **Atomicity rules:**
     - Tasks: Only include tasks that have corresponding `task-*.json` files. Never add a task to the dashboard without creating its JSON file first.
     - Decisions: Only include decisions that have corresponding `decision-*.md` files in `.claude/support/decisions/`. If a decision is significant enough for the dashboard, create the file first.
   - **User section backup** (see below)
   - Preserve the Notes section between `<!-- USER SECTION -->` markers
   - Update the **header lines** with project name from spec, current phase, and overall completion percentage
   - Group tasks by phase in **Tasks** section with per-phase progress lines
   - Show **Decisions** with `ID | Decision | Status | Selected` format (selected option name for decided, link for pending)
   - Generate **Progress** section: phase breakdown table, critical path one-liner, and "This week" activity line
   - Populate **Action Required** sub-sections — only show sub-sections that have content (omit empty categories entirely)
   - **Add dashboard metadata** (see below)

**User section backup process:**
```
1. Before regenerating, extract user section:
   - Find content between <!-- USER SECTION --> and <!-- END USER SECTION --> markers
   - Save to .claude/support/workspace/dashboard-notes-backup.md
   - Include timestamp: "# Dashboard Notes Backup\n*Backed up: YYYY-MM-DD HH:MM*\n\n{content}"

2. Regenerate dashboard from task JSON

3. Restore user section:
   - Insert saved content between markers
   - If markers were missing in old dashboard, append backup content with warning comment

4. Cleanup: Keep last 3 backups (dashboard-notes-backup.md, dashboard-notes-backup-1.md, dashboard-notes-backup-2.md)
```

**Dashboard metadata block:**

Add at the very top of dashboard.md (after title):
```markdown
<!-- DASHBOARD META
generated: 2026-01-28T14:30:00Z
task_hash: sha256:abc123...
task_count: 15
verification_debt: 0
drift_deferrals: 0
-->
```

This enables staleness detection in Step 1a.

**Footer line:**

Add at the very bottom of dashboard.md:
```markdown
---
*2026-01-28 14:30 UTC · 15 tasks · [Spec aligned](# "0 drift deferrals, 0 verification debt")*
```

#### Dashboard Regeneration Procedure

Every dashboard regeneration MUST follow this procedure. All commands and agents reference this section for consistency.

**Section Toggle Configuration:**

The primary source for section toggles is the **dashboard.md section toggle checklist** — a visible, editable checklist near the top of the dashboard between `<!-- SECTION TOGGLES -->` and `<!-- END SECTION TOGGLES -->` markers.

**Reading logic:**
1. Parse the checklist between the markers
2. `- [x] Section Name` → `build` mode (actively generate)
3. `- [ ] Section Name` → `exclude` mode (skip during regeneration)
4. Notes section: always `preserve` regardless of checkbox state (enforced)
5. Fallback: if no checklist exists, check spec frontmatter `dashboard_sections` or `.claude/CLAUDE.md`

**First regeneration (replacing template example):**

Detection: the dashboard is still the template example if it contains the line `> **This is a format example**`. On first regeneration, compute toggle defaults from project state instead of using static defaults:

```
Action Required  → [x] always (core section)
Progress         → [x] always (core section)
Tasks            → [x] always (core section)
Decisions        → [x] if any decision-*.md files exist, [ ] otherwise
Notes            → [x] always (preserve mode)
Timeline         → [x] if any task has due_date or external_dependency.expected_date, [ ] otherwise
Custom Views     → [ ] always (user opts in when they want custom views)
```

**On phase transitions:**

When `/work` detects a phase transition (all Phase N tasks "Finished", Phase N+1 becoming active), check whether toggle suggestions are warranted:
- If Phase N+1 introduces decision dependencies and Decisions is unchecked → suggest: "Phase {N+1} has pending decisions. Consider enabling the Decisions section in the dashboard."
- If Phase N+1 tasks have due dates and Timeline is unchecked → suggest: "Phase {N+1} has deadlines. Consider enabling the Timeline section."
- Suggestions are logged, never auto-toggled. The user's checkbox state is always authoritative.

**During regeneration (all subsequent):**
- Preserve the toggle checklist between its markers (never overwrite user's checkbox state)
- Only generate sections that are checked (`[x]`)
- The Notes section is always preserved regardless of toggle state

| Mode | Behavior |
|------|----------|
| `build` | Actively generate from source data on every regeneration (default, `[x]`) |
| `maintain` | Keep existing content, only update if data changes significantly (via spec frontmatter override only) |
| `exclude` | Skip this section entirely during regeneration (`[ ]`) |
| `preserve` | Never modify (Notes always uses this) |

The checkbox UI maps to `build`/`exclude`. Users who need `maintain` mode can set it via spec frontmatter `dashboard_sections` override, which takes precedence over the checklist for that section.

**Regeneration Steps:**

1. **Read source data**
   - All `task-*.json` files (tasks)
   - All `decision-*.md` files in `.claude/support/decisions/` (decisions)
   - `drift-deferrals.json` (if exists)
   - `verification-result.json` (if exists)
   - `.claude/support/questions/questions.md` (scan for blocking questions)

2. **Backup user section**
   - Extract content between `<!-- USER SECTION -->` and `<!-- END USER SECTION -->`
   - Save to `.claude/support/workspace/dashboard-notes-backup.md`
   - Rotate old backups (keep last 3)

2b. **Backup custom views instructions**
   - Extract content between `<!-- CUSTOM VIEWS INSTRUCTIONS -->` and `<!-- END CUSTOM VIEWS INSTRUCTIONS -->` markers
   - Save to `.claude/support/workspace/dashboard-custom-views-backup.md`
   - Rotate old backups (keep last 3)

2c. **Backup inline feedback**
   - Scan dashboard for `<!-- FEEDBACK:{id} -->` / `<!-- END FEEDBACK:{id} -->` marker pairs
   - For each pair, extract the content between the markers, keyed by task ID
   - Store in memory alongside the user section backup (used in Step 5c)

2d. **Backup phase gate markers**
   - Scan dashboard for `<!-- PHASE GATE:{X}→{Y} -->` / `<!-- END PHASE GATE:{X}→{Y} -->` marker pairs
   - For each pair, extract the content between the markers (preserves user's checkbox state)
   - Store in memory alongside other backups (used in Step 5d)

3. **Generate dashboard**
   - Follow the Section Format Reference below for all formatting rules
   - Use exact section headings: `# Dashboard`, `## 🚨 Action Required`, `## 📊 Progress`, `## 📋 Tasks`, `## 📋 Decisions`, `## 💡 Notes`
   - Optional section heading (when enabled, placed between Decisions and Notes): `## 👁️ Custom Views`
   - **Timeline sub-section** in Progress: render when any task has `due_date` or `external_dependency.expected_date`
   - **Project Overview sub-section** in Progress: render inline Mermaid diagram when 4+ tasks remain (see § "Project Overview Diagram")
   - Read section toggles from dashboard checklist (between `<!-- SECTION TOGGLES -->` markers) and respect modes
   - Preserve the section toggle checklist between its markers during regeneration
   - Enforce atomicity: only tasks with JSON files, only decisions with MD files
   - On first regeneration (detected by `> **This is a format example**` line): replace the template example with actual project data and compute toggle defaults per the "First regeneration" section above
   - **Inline feedback areas:** When generating "Your Tasks", add feedback markers for each `human`/`both`-owned task:
     ```
     <!-- FEEDBACK:{id} -->
     **Task {id} — Feedback:**
     [Leave feedback here, then run /work complete {id}]
     <!-- END FEEDBACK:{id} -->
     ```
   - **Phase Transitions sub-section:** When all tasks in Phase N are "Finished" AND Phase N+1 tasks exist, render a phase gate with checkbox between markers:
     ```
     <!-- PHASE GATE:{N}→{N+1} -->
     - [ ] **Phase {N} complete** — Review results and approve transition to Phase {N+1}
       - {M} tasks finished, {K} tasks in Phase {N+1} ready
     <!-- END PHASE GATE:{N}→{N+1} -->
     ```
   - **Verification Pending sub-section:** When all spec tasks are "Finished" with passing per-task verification AND no valid `verification-result.json` exists, render:
     ```
     All tasks complete — phase-level verification will run on next `/work`
     ```
   - **Spec Drift sub-section:** When `drift-deferrals.json` exists with active deferrals, render each deferred section:
     ```
     - ⚠️ **{section}** — {N} tasks affected, deferred {M} days ago
     ```

4. **Compute and add metadata block** (after `# Dashboard` title)
   ```
   <!-- DASHBOARD META
   generated: [ISO timestamp]
   task_hash: sha256:[hash of sorted task_id:status pairs]
   task_count: [number]
   verification_debt: [count of tasks needing verification]
   drift_deferrals: [count from drift-deferrals.json]
   -->
   ```

5. **Restore user section**
   - Insert backed-up content between markers
   - If markers missing, append with warning comment

5b. **Restore custom views instructions**
   - Insert backed-up custom views instructions between `<!-- CUSTOM VIEWS INSTRUCTIONS -->` and `<!-- END CUSTOM VIEWS INSTRUCTIONS -->` markers
   - If markers missing, skip (section may be excluded via toggle)
   - Read the restored instructions and generate appropriate rendered content below `<!-- END CUSTOM VIEWS INSTRUCTIONS -->` up to the next `---` separator

5c. **Restore inline feedback**
   - For each feedback entry backed up in Step 2c:
     - If the task still appears in "Your Tasks" (task still active with `human`/`both` owner): restore the backed-up content between its `<!-- FEEDBACK:{id} -->` markers
     - If the task is no longer in "Your Tasks" (completed or removed): write the feedback content to the task JSON `user_feedback` field (preserves feedback that would otherwise be lost)

5d. **Restore phase gate markers**
   - For each phase gate backed up in Step 2d:
     - If the phase gate condition still applies (all Phase X tasks Finished, Phase Y tasks exist): restore the backed-up content between its `<!-- PHASE GATE:{X}→{Y} -->` markers (preserves user's checkbox state)
     - If the phase gate no longer applies (transition was approved or phases changed): discard

6. **Add footer line** (at very end)
   ```
   ---
   *[timestamp] · N tasks · [status indicator]*
   ```
   - Healthy: `[Spec aligned](# "0 drift deferrals, 0 verification debt")`
   - Issues: `⚠️ N drift deferrals, M verification debt`

**Section Format Reference:**

All dashboard formatting rules are documented here. This is the single authoritative source — do not add format comments to the regenerated dashboard.

**Action Item Contract:**
Every item in "Action Required" must be:
1. Actionable — the user can see what to do without guessing
2. Linked — if the action involves a file, include a relative path link
3. Completable — include a checkbox, command, or clear completion signal
4. Contextual — if feedback is needed, provide a feedback area or link

**Review Item Derivation:**
Review items are derived, not stored. During regeneration:
1. Scan for unresolved items — out_of_spec without approval, draft/proposed decisions, blocking questions from `questions.md`
2. Populate Reviews sub-section from current data
3. Never carry forward stale entries — resolved items disappear on next regeneration
4. No dangling references — every item must link to a concrete file
5. Blocking questions: scan `questions.md` for `[BLOCKING]` entries, render each as a review item linking to [questions.md](support/questions/questions.md)
6. Non-blocking unanswered questions: if count > 0, add summary line to Reviews: `- [ ] **N pending questions** → [questions.md](support/questions/questions.md)`

**Section Display Rules:**
- Action Required sub-sections: only render when they have content (omit empty categories entirely)
- Action Required sub-section order: Phase Transitions, Verification Pending, Verification Debt, Spec Drift, Decisions, Your Tasks, Reviews
- Phase Transitions: only render when a phase boundary has been reached (all Phase N tasks Finished, Phase N+1 exists)
- Verification Pending: only render when all spec tasks are Finished with passing per-task verification but no valid verification-result.json
- Spec Drift: only render when drift-deferrals.json has active entries
- Reviews sub-section format: `- [ ] **Item title** — what to do → [link to file](path)`
- Reviews appear for: out_of_spec tasks without approval, draft/proposed decisions, blocking questions from `questions.md` (each linked to the file)
- Timeline sub-section in Progress: only render when tasks have `due_date` or `external_dependency.expected_date`
- Timeline has its own toggle in the section checklist (independent of Progress)
- Phase table in Progress: always show ALL phases (including blocked/future)
- Critical path owners: ❗ (human), 🤖 (Claude), 👥 (both)
- Critical path parallel branches: `[step A | step B]` notation for fork/join points; max 3 branches per group
- Critical path >5 steps (after collapsing parallel branches): show first 3 + "... N more → Done"
- "This week" line: omit when all counts are zero
- Tasks grouped by phase with per-phase progress lines
- Tasks with `conflict_note`: show status as `Pending (held: conflict with Task {id})` during parallel dispatch
- Decisions: status display mapping: `approved`/`implemented` → "Decided", `draft`/`proposed` → "Pending". Decided → show selected option name; Pending → link to doc in Selected column
- Out-of-spec tasks: prefix title with ⚠️
- Footer: healthy = spec aligned tooltip; issues = ⚠️ with counts
- Custom Views section: user-defined instructions (preserved between markers) followed by Claude-generated content based on those instructions (when enabled). Multiple views are rendered as `###` sub-sections, one per bold-labeled instruction.

**Per-Section Format:**

| Section | Columns / Format |
|---------|-----------------|
| Action Required → Phase Transitions | `- [ ] **Phase N complete** — description` with `<!-- PHASE GATE -->` markers |
| Action Required → Verification Pending | Plain text status message |
| Action Required → Verification Debt | `Task \| Title \| Issue` |
| Action Required → Spec Drift | `- ⚠️ **{section}** — {N} tasks affected, deferred {M} days ago` |
| Action Required → Decisions | `Decision \| Question \| Doc` |
| Action Required → Your Tasks | `Task \| What To Do \| Where` |
| Action Required → Reviews | `- [ ] **Item title** — what to do → [link](path)` — derived, not stored |
| Progress → Phase table | `Phase \| Done \| Total \| Status` — status: Complete, Active, Blocked (reason) |
| Progress → Timeline | `Date \| Item \| Status \| Notes` — sorted chronologically, overdue: strikethrough date + ⚠️ OVERDUE prefix, external deps with contact info, human tasks marked with ❗ |
| Tasks → Per phase | `ID \| Title \| Status \| Diff \| Owner \| Deps` — grouped by phase headers |
| Decisions | `ID \| Decision \| Status \| Selected` |
| Progress → Project Overview | Inline Mermaid `graph LR` diagram — see Project Overview Diagram rules below |
| Custom Views | Preserved instruction block between `<!-- CUSTOM VIEWS INSTRUCTIONS -->` markers + rendered `###` sub-sections generated from those instructions (one per bold-labeled view) |

**Domain Agnosticism:**
This format works for any project type — software, research, procurement, renovation, event planning. Use language appropriate to the project domain. No code-specific assumptions are built in.

**Spec snapshot process:**
```
1. Create directory if needed: .claude/support/previous_specifications/
2. Copy: .claude/spec_v{N}.md → .claude/support/previous_specifications/spec_v{N}_decomposed.md
3. This snapshot is used later for generating diffs when sections change
```

Task creation guidelines:
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

When Step 2c produces a parallel batch of >= 2 tasks, execute them concurrently:

**1. Log the parallel dispatch:**
```
Dispatching N tasks in parallel:
  - Task {id}: "{title}" → files: [{files_affected}]
  - Task {id}: "{title}" → files: [{files_affected}]
  ...
  File conflicts: none between batch members (verified in Step 2c)

Held back (file conflicts):
  - Task {id}: "{title}" — conflict with Task {conflict_with} on [{conflict_files}]
  (Or: "None" if held_back is empty)
```

**2. Set ALL batch tasks to "In Progress" and annotate held-back tasks:**

Before spawning agents, update every task in the batch:
```json
{
  "status": "In Progress",
  "updated_date": "YYYY-MM-DD"
}
```

For each held-back task, add a temporary `conflict_note` to the task JSON:
```json
{
  "conflict_note": "Held: file conflict with Task {id} on {files}. Auto-clears when conflict resolves."
}
```

This note is surfaced in the dashboard Tasks section (appended to the task's Status column as a tooltip or parenthetical) and removed when the task is dispatched.

**3. Spawn parallel agents:**

Use Claude Code's `Task` tool to spawn one agent per task. **Always set `model: "opus"` and `max_turns: 40`** to ensure agents run on Claude Opus 4.6 with a bounded turn limit. Each agent receives:
- The task JSON to execute
- Instructions to read `.claude/agents/implement-agent.md`
- Instructions to follow Steps 2, 4, 5, 6a, and 6b (understand, implement, self-review, mark awaiting verification, spawn verify-agent as a sub-agent for per-task verification)
- **Explicit instruction: "DO NOT regenerate dashboard. DO NOT select next task. DO NOT check parent auto-completion. Return results when verification completes."**
- **Note:** Each parallel implement-agent will spawn its own verify-agent sub-agent (nested Task call). This is expected — verification separation applies in parallel mode too.

All agents run concurrently via parallel `Task` tool calls with `model: "opus"`.

**4. Collect results with incremental re-dispatch:**

Use `run_in_background: true` for each agent's `Task` call, then poll for completion:

```
active_agents = {task_id: {agent_id, spawned_at} for each spawned agent}
AGENT_TIMEOUT_POLLS = 60  # max poll iterations before declaring an agent timed out

WHILE active_agents is non-empty:
  Check each agent for completion (read output file or use TaskOutput with block: false)

  For each completed agent:
    1. Record result (task ID, status, verification result, files modified, issues)
    2. Remove from active_agents
    3. Check parent auto-completion for finished tasks
    4. INCREMENTAL RE-DISPATCH:
       - Re-run Step 2c eligibility assessment with current state
         (completed tasks are now "Finished", their files are released)
       - Any previously held-back tasks whose conflicts are now resolved
         become eligible
       - If new eligible tasks found AND len(active_agents) < max_parallel_tasks:
         Spawn new agents for newly-eligible tasks
         Add to active_agents
       - Clear conflict_note from newly-dispatched tasks

  For each agent that has exceeded AGENT_TIMEOUT_POLLS iterations without completing:
    1. Log: "Agent for task {id} timed out after {N} poll iterations"
    2. Read the task JSON — if still "In Progress" (agent didn't finish):
       - Set status to "Blocked"
       - Add note: "[AGENT TIMEOUT] Parallel agent did not complete within polling limit"
    3. Remove from active_agents
    4. Report to user: "Task {id} timed out — may need manual investigation or retry"

  Brief pause before next poll iteration (avoid busy-waiting)
```

This enables **incremental re-dispatch**: when Task A completes and releases its files, Task C (which was held back due to conflict with A) can start immediately — even while Tasks B and D are still running.

**5. Post-parallel cleanup:**

After all agents complete (active_agents is empty):

```
1. Final parent auto-completion check

2. Single dashboard regeneration:
   Regenerate dashboard.md per the Dashboard Regeneration Procedure in Step 4
   - Remove all conflict_note fields from task JSONs (cleanup)

3. Lightweight health check (Step 6)

4. Loop back to Step 2c:
   Reassess remaining tasks for next parallel batch or phase transition
```

**6. Handling mixed results:**

When some tasks pass and others fail verification:
- Passed tasks remain "Finished" — they are done
- Failed tasks are set back to "In Progress" by verify-agent within their thread
- On the next loop iteration, failed tasks are re-eligible for dispatch (potentially in a new parallel batch)

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

    Verify the implementation independently. Do NOT assume correctness.
    Write your verification result to the task JSON (task_verification field).
    Update task status to "Finished" (pass) or "In Progress" (fail).
    Return your T8 report.
```

**Timeout handling:** If verify-agent exhausts `max_turns` (30) without completing, treat as verification failure — set task to "Blocked" with note `[VERIFICATION TIMEOUT]` and report to user.

**After per-task verification completes:**
- If **pass**: Proceed to select next pending task (loop back to Execute routing)
- If **fail**: Task is set back to "In Progress". Route to implement-agent to fix the issues. After fix, route back to verify-agent for re-verification. This loop continues until pass.
- Regenerate dashboard after any status change, per the Dashboard Regeneration Procedure in Step 4.

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

### Step 6: Lightweight Health Check

Run quick validation checks after completing the main action:

**Checks performed:**
- **Workflow compliance** (new):
  - If a task was just completed: Was it set to "In Progress" before "Finished"? (Check `updated_date` changed at least twice, or task notes reflect the workflow steps.)
  - Is the dashboard freshly regenerated? (Dashboard timestamp should match current session.)
- Parallel eligibility rule (multiple "In Progress" only when files don't overlap, deps satisfied, within max limit)
- Spec fingerprint comparison (current spec vs task fingerprints)
- Section change count (if section fingerprints exist)
- Orphan dependency detection (references to non-existent tasks)
- Out-of-spec task count

**Output format:**
```
Quick check: ✓
```
or
```
Quick check: ⚠️ 2 issues
  - Spec changed: 2 sections modified (4 tasks affected)
  - 3 tasks marked out-of-spec
```

**Note:** This is a lightweight subset of `/health-check`. Use `/health-check` for full validation.

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

The critical path is rendered as a single line in the **Progress** section: owner-tagged steps joined by `→`, with parallel branches shown in `[ | ]` notation.

1. **Build dependency graph** — include all incomplete tasks and their dependencies (both task deps and decision deps). Unresolved decisions appear as nodes (e.g., `❗ Resolve DEC-001`)
2. **Compute longest path** — walk the graph to find the longest chain from any current entry point to "Done". This is the critical path (determines project duration)
3. **Detect parallel branches** — find fork/join points along the critical path:
   - A **fork** is a node whose completion enables 2+ independent successors
   - A **join** is a node with 2+ predecessors that must all complete before it starts
   - Show parallel branches when they share the same fork and join nodes (the branches reconverge)
   - Branches that don't reconverge are separate sequential paths — pick the longest
4. **Format as one-liner:**
   - Sequential: `❗ Resolve DEC-001 → 🤖 Build API → Done`
   - Parallel branches: `[🤖 Rough plumbing | ❗ Resolve DEC-002] → [❗ Inspection | 🤖 Install] → 👥 Walkthrough → Done`
   - Owners: `❗` (human), `🤖` (Claude), `👥` (both)
   - **Step count** = total unique nodes in the rendered path (each branch member counts as 1): `*(N steps)*`
   - For complex paths (>5 steps after collapsing parallel branches), show first 3 + "... N more → Done"
5. **Prioritize human-owned steps** — surfaces blockers the user can act on

**Decision dependencies as path nodes:** Unresolved decisions appear on the critical path as `❗ Resolve {DEC-ID}` steps. Once resolved, they are removed and their successor tasks become direct successors of the decision's predecessors.

**Parallel branch rules:**
- Max 3 branches in a single `[ | ]` group (more than 3 → collapse to `[🤖 3 parallel tasks]`)
- Nested parallelism: don't nest `[ ]` — flatten to separate `[ | ]` groups joined by `→`
- If parallel branches have different owners, show each: `[❗ Review | 🤖 Build]`
- Branches of unequal length: show each by its first step (the branch content is what matters, not padding)

**Edge cases:** No dependencies → "All tasks can start now". No incomplete AND no valid verification-result.json → "🤖 Phase verification → Done" *(1 step)*. No incomplete AND valid passing verification-result.json → "All tasks complete! ✓". Single task → just that task → Done. No parallelism detected → pure sequential format (no brackets).

### Project Overview Diagram

An inline Mermaid diagram in the Progress section showing the project's dependency structure at a glance. Placed after the critical path one-liner, before the "This week" activity line, under a `### Project Overview` sub-heading.

**Generation rules:**

1. **Completed phases** → Collapse into a single node: `["✅ Phase Name (N/N)"]`
2. **Completed tasks in active phases** → Fold away. Reroute their connections: connect their predecessors directly to their incomplete successors. This keeps the diagram focused on remaining work.
3. **Active/pending tasks** → Show individually with ownership prefix: `🤖` (claude), `❗` (human), `👥` (both)
4. **Decisions** → Diamond nodes: `{"❓ Decision title"}`
5. **Dependencies** → Arrows between nodes following task dependency data
6. **Date constraints** → Annotate nodes with deadlines when present: `["🤖 Task title<br/><small>Due: 2026-02-15</small>"]`
7. **Clumping** → When >15 active nodes would result, group related tasks into subgraph clusters by phase or functional area to reduce visual noise
8. **Direction** → Always `graph LR` (left to right)
9. **Labels** → Keep short: ownership emoji + task title. No status text in labels.

**Edge cases:** No tasks → omit diagram. All tasks complete → omit diagram (project done). Single task → omit diagram (one-liner is sufficient). Fewer than 4 remaining tasks → omit diagram (one-liner covers it).

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
   - Status must be "In Progress" (not "Pending", "Broken Down", or "Finished")
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
5. **Check parent auto-completion:**
   - If parent_task exists and all sibling subtasks are "Finished"
   - Set parent status to "Finished"
6. **Regenerate dashboard** - Follow the Dashboard Regeneration Procedure in Step 4
   - Additional completion requirements:
     - Update overall completion percentage
     - Recalculate critical path line in Progress section with remaining incomplete tasks
     - Add completed task to Recently Completed with completion_date
7. **Auto-archive check** - If active task count > 100, archive old tasks
8. **Lightweight health check** - Run quick validation (see Step 6 in main process)
   - Output: `Quick check: ✓` or `Quick check: ⚠️ N issues`

### Rules

- Never work on "Broken Down" tasks directly - work on their subtasks
- Parent tasks auto-complete when all subtasks finish
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
