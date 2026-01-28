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
| Spec tasks pending (and none awaiting verification) | **Execute** — read & follow implement-agent workflow (see Step 4) |
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
8. ELSE:
   → Route to implement-agent for next pending task
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
   - **Follow the canonical template** in `.claude/support/reference/dashboard-patterns.md` — use exact section headings, emojis, and table formats defined there
   - **Check section toggles** — if `dashboard_sections` config exists (in spec frontmatter or CLAUDE.md), respect `build`/`maintain`/`exclude`/`preserve` modes per section. See dashboard-patterns.md for details.
   - **Atomicity rules:**
     - Tasks: Only include tasks that have corresponding `task-*.json` files. Never add a task to the dashboard without creating its JSON file first.
     - Decisions: Only include decisions that have corresponding `decision-*.md` files in `.claude/support/decisions/`. If a decision is significant enough for the dashboard, create the file first.
   - **User section backup** (see below)
   - Preserve the Notes & Ideas section between `<!-- USER SECTION -->` markers
   - Update **Project Context** with project name from spec and current phase
   - Calculate **Overall completion** percentage for Quick Status
   - Generate **Spec Alignment** section from drift status (see dashboard-patterns.md)
   - Generate **Critical Path** from dependency chain of incomplete tasks (see below)
   - List **Recently Completed** tasks with completion dates in Progress This Week
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

#### If Verifying (Per-Task)

**You must use the verify-agent per-task workflow. Do not verify directly.**

Execute these steps in order:

1. **Read the agent file now:** Use the Read tool to read `.claude/agents/verify-agent.md` in full.
2. **Identify the mode:** This is a **per-task** verification. Follow the "Per-Task Verification Workflow" section (Steps T1 through T8).
3. **Context to provide:** The specific task JSON that needs verification, its spec section, and completion notes.

**After per-task verification completes:**
- If **pass**: Proceed to select next pending task (loop back to Execute routing)
- If **fail**: Task is set back to "In Progress". Route to implement-agent to fix the issues. After fix, route back to verify-agent for re-verification. This loop continues until pass.
- Regenerate dashboard after any status change.

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

2. **Regenerate dashboard with completion summary:** Update Project Context to "Complete", replace Critical Path with final stats (task count, verification date, spec status).

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

**Dashboard integration:** Unresolved questions (especially blocking ones) appear in the dashboard's "Needs Your Attention" → "Reviews & Approvals" section during regeneration.

### Step 6: Lightweight Health Check

Run quick validation checks after completing the main action:

**Checks performed:**
- **Workflow compliance** (new):
  - If a task was just completed: Was it set to "In Progress" before "Finished"? (Check `updated_date` changed at least twice, or task notes reflect the workflow steps.)
  - Is the dashboard freshly regenerated? (Dashboard timestamp should match current session.)
- Single "In Progress" task rule (only one allowed)
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

The Critical Path shows the sequence of tasks blocking project completion:

1. **Find unblocked incomplete tasks** - Tasks with no unfinished dependencies
2. **Build dependency chains** - Trace what depends on each recursively
3. **Identify longest chain** - This is the critical path
4. **Format with owners** - `❗ **You**:` (human), `🤖 **Claude**:` (claude), `👥 **Both**:` (both)
5. **Show blocking relationships** - Indicate what each step blocks

**Edge cases:** No dependencies → show all as "can start now". Multiple equal paths → prioritize human-owned (surfaces blockers). No incomplete → "All tasks complete!". Single task → no "blocks" annotation.

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
6. **Regenerate dashboard** - Follow the Regeneration Checklist in `.claude/support/reference/dashboard-patterns.md`
   - Additional completion requirements:
     - Update overall completion percentage
     - Recalculate Critical Path with remaining incomplete tasks
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
