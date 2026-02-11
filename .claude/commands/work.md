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
- `.claude/support/questions.md` - Pending questions

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
sha256sum .claude/spec_v{N}.md | cut -d' ' -f1
# Prefix with "sha256:" → "sha256:a1b2c3d4..."
```

**Section fingerprint computation:**
```bash
# For each ## section, hash: heading + all content until next ## or EOF
echo -n "## Authentication\nContent here..." | sha256sum | cut -d' ' -f1
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
   │      Log: "Phase {active_phase} complete — Phase {next_phase} tasks are now eligible"
   │      → Execute Version Transition Procedure (see iterate.md § "Version Transition Procedure")
   │      → Suggest running /iterate to flesh out Phase {next_phase} sections
   │    ELSE (single-phase project or final phase):
   │      → Fall through to Step 3 routing (phase-level verification → completion)

4. DECISION CHECK:
   For target task(s), check `decision_dependencies`:
   ├─ Read each referenced decision record
   ├─ Check if decision has a checked box in "## Select an Option"
   │
   │  IF any decision is unresolved:
   │    📋 Decision {id} ({title}) blocks {N} task(s).
   │    Open the decision doc to review options and check your selection:
   │    → [decision doc link]
   │    Then run `/work` again.
   │
   │  IF decision was previously pending and is now resolved:
   │    → Run post-decision check (see Step 2b-post below)

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
```
batch = []
For each eligible task (sorted by priority, then ID):
  conflicts = false
  For each task already in batch:
    IF files_affected overlap (any shared paths):
      conflicts = true
      break
  IF task has empty files_affected AND parallel_safe != true:
    skip (unknown file impact — not safe for parallel)
  ELSE IF NOT conflicts AND len(batch) < max_parallel_tasks:
    add task to batch
```

**4. Determine dispatch mode:**
```
IF len(batch) >= 2:
  → parallel_mode = true
  → Log: "Parallel dispatch: {batch_size} tasks eligible"
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
   - **Follow the Dashboard Regeneration Procedure** below — use exact section headings, emojis, and format hints from dashboard.md
   - **Check section toggles** — if `dashboard_sections` config exists (in spec frontmatter or `.claude/CLAUDE.md`), respect `build`/`maintain`/`exclude`/`preserve` modes per section.
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
*Dashboard generated: 2026-01-28 14:30 UTC | Tasks: 15 | [Spec aligned](# "0 drift deferrals, 0 verification debt")*
```

#### Dashboard Regeneration Procedure

Every dashboard regeneration MUST follow this procedure. All commands and agents reference this section for consistency.

**Section Toggle Configuration:**

Users can control which sections Claude builds via `dashboard_sections` in spec frontmatter or `.claude/CLAUDE.md`:

```yaml
dashboard_sections:
  action_required: build        # actively create/update
  claude: build
  progress: build
  tasks: build
  decisions: maintain           # preserve existing, minor updates only
  notes: preserve               # always preserved (never overwritten)
```

| Mode | Behavior |
|------|----------|
| `build` | Actively generate from source data on every regeneration (default) |
| `maintain` | Keep existing content, only update if data changes significantly |
| `exclude` | Skip this section entirely during regeneration |
| `preserve` | Never modify (Notes always uses this) |

Default: all sections `build` if no configuration exists. Configure in spec frontmatter (takes precedence) or `.claude/CLAUDE.md`.

**Regeneration Steps:**

1. **Read source data**
   - All `task-*.json` files (tasks)
   - All `decision-*.md` files in `.claude/support/decisions/` (decisions)
   - `drift-deferrals.json` (if exists)
   - `verification-result.json` (if exists)

2. **Backup user section**
   - Extract content between `<!-- USER SECTION -->` and `<!-- END USER SECTION -->`
   - Save to `.claude/support/workspace/dashboard-notes-backup.md`
   - Rotate old backups (keep last 3)

3. **Generate dashboard**
   - Use exact section headings from dashboard.md template (including emojis): `# Dashboard`, `## 🚨 Action Required`, `## 🤖 Claude`, `## 📊 Progress`, `## 📋 Tasks`, `## 📋 Decisions`, `## 💡 Notes`
   - **Header lines** (before first section): project name, stage, start date on line 1; overall completion %, task count, decision count on line 2
   - **Action Required sub-sections:** Only render sub-sections that have content. Empty categories are omitted entirely — no placeholder lines. Sub-sections: Verification Debt, Decisions, Your Tasks, Reviews, Spec Drift
   - **Claude section:** Compact format — one line per state (Working on / Up next / Blocked). Omit empty lines.
   - **Progress section:** Phase breakdown table + critical path one-liner + "This week" activity line. Omit "This week" if all counts are zero.
   - Check `dashboard_sections` config and respect modes
   - Enforce atomicity: only tasks with JSON files, only decisions with MD files

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

6. **Add footer line** (at very end)
   ```
   ---
   *[timestamp] · N tasks · [status indicator]*
   ```
   - Healthy: `[Spec aligned](# "0 drift deferrals, 0 verification debt")`
   - Issues: `⚠️ N drift deferrals, M verification debt`

**Action Item Contract:**

Every item in "Action Required" must be:
- **Actionable** — the user can see what to do without guessing
- **Linked** — if the action involves a file, include a link
- **Completable** — include a checkbox, command, or clear completion signal
- **Contextual** — if feedback is needed, provide a feedback area or link

**Review Item Derivation:**

Review items are derived, not stored. During regeneration:
1. Scan for unresolved items — `out_of_spec: true` without `out_of_spec_approved`, decision files with `draft`/`proposed` status, blocking questions in questions.md
2. Populate Reviews sub-section from current data
3. Never carry forward stale entries — resolved items disappear on next regeneration
4. No dangling references — every item must link to a concrete file

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
   - Step 6b: verify-agent runs per-task verification → status becomes `"Finished"` if pass
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
  File conflicts: none (verified in Step 2c)
```

**2. Set ALL batch tasks to "In Progress":**

Before spawning agents, update every task in the batch:
```json
{
  "status": "In Progress",
  "updated_date": "YYYY-MM-DD"
}
```

**3. Spawn parallel agents:**

Use Claude Code's `Task` tool to spawn one agent per task. **Always set `model: "opus"`** to ensure agents run on Claude Opus 4.6. Each agent receives:
- The task JSON to execute
- Instructions to read `.claude/agents/implement-agent.md`
- Instructions to follow Steps 2, 4, 5, 6a, and 6b (understand, implement, self-review, mark awaiting verification, trigger per-task verification)
- **Explicit instruction: "DO NOT regenerate dashboard. DO NOT select next task. DO NOT check parent auto-completion. Return results when verification completes."**

All agents run concurrently via parallel `Task` tool calls with `model: "opus"`.

**4. Collect results:**

Wait for all agents to return. Each agent reports:
- Task ID and final status ("Finished" if verification passed, "In Progress" if failed)
- Verification result (pass/fail)
- Files modified
- Issues encountered

**5. Post-parallel cleanup:**

After all agents complete:

```
1. Check parent auto-completion:
   For each finished task with a parent_task:
     IF all sibling subtasks are "Finished":
       Set parent status to "Finished"

2. Single dashboard regeneration:
   Regenerate dashboard.md per the Dashboard Regeneration Procedure in Step 4

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

**You must use the verify-agent per-task workflow. Do not verify directly.**

Execute these steps in order:

1. **Read the agent file now:** Use the Read tool to read `.claude/agents/verify-agent.md` in full.
2. **Identify the mode:** This is a **per-task** verification. Follow the "Per-Task Verification Workflow" section (Steps T1 through T8).
3. **Context to provide:** The specific task JSON that needs verification, its spec section, and completion notes.

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

Execute these steps in order:

1. **Read the agent file now:** Use the Read tool to read `.claude/agents/verify-agent.md` in full. Do not skip this step or work from memory.
2. **Identify the mode:** This is a **phase-level** verification. Follow the "Phase-Level Verification Workflow" section (Steps 1 through 8). Required outputs:
   - Step 3: Per-criterion pass/fail table (not just a summary)
   - Step 5: Issue categorization (critical/major/minor counts)
   - Step 7: `verification-result.json` written with all required fields
   - Step 8: Verification report displayed to user
3. **Context to provide:** List of completed work with per-task verification results, spec acceptance criteria, test commands

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

Questions accumulate in `.claude/support/questions.md` during work.

**Check for questions at these points:**
- After completing a task (before selecting the next one)
- At phase boundaries (Execute → Verify, Verify → Complete)
- When a `[BLOCKING]` question is added
- When quality gate fails (tests fail, spec violation)

**Process:**

1. **Read `.claude/support/questions.md`** — check for unresolved questions (items under Requirements, Technical, Scope, or Dependencies that aren't in the Answered table)

2. **If questions exist, present them:**
   ```
   Questions for you (from questions.md):

   ## Requirements
   - Should login require email verification?

   ## Technical
   - [BLOCKING] What caching solution to use?

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

The critical path is rendered as a single line in the **Progress** section: owner-tagged steps joined by `→`.

1. **Find unblocked incomplete tasks** - Tasks with no unfinished dependencies
2. **Build dependency chains** - Trace what depends on each recursively
3. **Identify longest chain** - This is the critical path
4. **Format as one-liner** - `❗ Resolve DEC-001 → 🤖 Build API layer → 🤖 Phase verification → Done *(N steps)*`
   - Owners: `❗` (human), `🤖` (Claude), `👥` (both)
   - For complex paths (>5 steps), show first 3 + "... N more → Done"
5. **Prioritize human-owned steps** - Surfaces blockers the user can act on

**Edge cases:** No dependencies → "All tasks can start now". No incomplete → "All tasks complete!". Single task → just that task → Done.

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
4. **Update task file:**
   ```json
   {
     "status": "Finished",
     "completion_date": "YYYY-MM-DD",
     "updated_date": "YYYY-MM-DD",
     "notes": "What was done, any follow-ups needed"
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
