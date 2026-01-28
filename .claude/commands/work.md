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

**See also:**
- `/health-check` performs the same drift detection as a validation check. Keep algorithms in sync.
- `.claude/support/reference/workflow.md` § "Spec Change and Feature Addition Workflow" for the end-to-end process (user edits spec → detection → confirmation → task updates → implementation → verification).

### Granular Reconciliation UI

When section-level drift is detected, present a targeted UI:

```
## Spec Drift Detected

### Changed: ## Authentication (3 tasks affected)

**Diff:**
- User authentication with email and password
+ User authentication with email, password, or OAuth (Google, GitHub)
+ Session timeout: 30 minutes of inactivity

**Affected Tasks:**
| ID | Title | Suggested Action |
|----|-------|------------------|
| 3 | Implement login flow | Review: OAuth added |
| 4 | Password validation | No change needed |
| 7 | Session management | Review: Timeout added |

[A] Apply suggestions  [R] Review individually  [S] Skip section

### Changed: ## API Endpoints (1 task affected)
...
```

**Options per section:**
- **Apply suggestions** - Auto-update task descriptions with suggested changes
- **Review individually** - Step through each affected task
- **Skip section** - Acknowledge change, keep tasks as-is

**Individual task review (when [R] selected):**
```
## Task 3: Implement login flow

Current description: Create login endpoint with email/password

Spec change: OAuth support (Google, GitHub) added

Suggested update: Create login endpoint supporting email/password and OAuth

[A] Apply  [E] Edit  [S] Skip  [O] Mark out-of-spec
```

**Edge cases:**
| Scenario | Handling |
|----------|----------|
| New section added | Report: "New section '## NewFeature' - may need new tasks" |
| Section deleted | Flag affected tasks, suggest mark as out-of-spec or delete |
| Section renamed | Detected as delete + add; user manually reassigns tasks |
| No snapshot file | Fall back to full-spec comparison (legacy behavior) |

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
| Any spec task "Finished" without passing per-task verification | **Verify (per-task)** — read & follow verify-agent per-task workflow (see Step 4) |
| Spec tasks pending (and none awaiting per-task verification) | **Execute** — read & follow implement-agent workflow (see Step 4) |
| All spec tasks finished with passing per-task verification, no valid phase verification result | **Verify (phase-level)** — read & follow verify-agent phase-level workflow (see Step 4) |
| All spec tasks finished, valid phase verification result | **Complete** — report project complete, present final checkpoint |

**Priority order matters.** Per-task verification takes priority over executing the next task. This ensures verification is not deferred.

**State detection logic:** A task "needs per-task verification" when:
- It has status "Finished" AND does NOT have a `task_verification` field, OR
- It has status "Finished" AND has `task_verification.result == "fail"` AND `updated_date` is more recent than `task_verification.timestamp` (meaning it was fixed and needs re-verification)

**Spec-less project handling:** If tasks exist but no spec file is found, do NOT proceed with execution. Instead:
```
Tasks exist but no specification found.

Without a spec, the verify phase cannot validate acceptance criteria
and the project cannot reach "Complete" status.

Options:
[S] Create a spec - Run /iterate to document requirements
[M] Mark all tasks out-of-spec - Proceed without verification gate
[X] Stop - Don't proceed until this is resolved
```
This prevents the scenario where all tasks execute and "complete" without any verification being possible.

**Important — spec tasks vs out-of-spec tasks:** Phase routing is based on **spec tasks only** (tasks without `out_of_spec: true`). Out-of-spec tasks (recommendations from verify-agent or user requests that bypassed the spec) are excluded from phase detection. This prevents the verify → execute → verify infinite loop.

**Phase-level verification result check:** Read `.claude/verification-result.json`. A result is valid when `result` is `"pass"` or `"pass_with_issues"`, `spec_fingerprint` matches the current spec, and no tasks changed since `timestamp`. See verify-agent Phase-Level Step 7 for the file format.

**Out-of-spec task handling:** After phase routing completes (or at phase boundaries), check for pending out-of-spec tasks and present them to the user:

```
Recommendations (not in spec):
| ID | Task | Source | Action |
|----|------|--------|--------|
| 13 | Add unit tests for CI | verify-agent | [Accept] [Reject] [Defer] |
| 14 | Document installation | verify-agent | [Accept] [Reject] [Defer] |

Options:
[A] Accept - Approve and execute this task
[R] Reject - Remove this task
[D] Defer - Keep for later, don't execute now
[AA] Accept all
```

**Actions:**
- **Accept**: Set `out_of_spec_approved: true` on the task. `/work` can now execute it.
- **Reject**: Delete the task file.
- **Defer**: Leave as-is. Task remains pending but is skipped during auto-detect.

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
   - Preserve the Notes & Ideas section between `<!-- USER SECTION -->` markers
   - Update **Project Context** with project name from spec and current phase
   - Calculate **Overall completion** percentage for Quick Status
   - Generate **Critical Path** from dependency chain of incomplete tasks (see below)
   - List **Recently Completed** tasks with completion dates in Progress This Week

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
   - Step 6: Task JSON updated to `"Finished"`, dashboard regenerated
3. **Context to provide:** Current task, relevant spec sections, constraints/notes

**Why this matters:** Implementing directly skips the self-review, status tracking, and dashboard regeneration. The agent workflow exists to ensure consistent quality and observable state transitions.

#### If Verifying (Per-Task)

**You must use the verify-agent per-task workflow. Do not verify directly.**

Execute these steps in order:

1. **Read the agent file now:** Use the Read tool to read `.claude/agents/verify-agent.md` in full.
2. **Identify the mode:** This is a **per-task** verification. Follow the "Per-Task Verification Workflow" section (Steps T1 through T8).
3. **Context to provide:** The specific task JSON that needs verification, its spec section, and completion notes.

**After per-task verification completes:**
- If **pass**: Proceed to select next pending task (loop back to Execute routing)
- If **fail**: Task is set back to "In Progress". Route to implement-agent to fix the issues.
- Regenerate dashboard after any status change.

**Why this matters:** Per-task verification catches issues while the implementation is fresh, before subsequent tasks build on potentially flawed work.

#### If Verifying (Phase-Level)

**You must use the verify-agent phase-level workflow. Do not verify directly.**

Execute these steps in order:

1. **Read the agent file now:** Use the Read tool to read `.claude/agents/verify-agent.md` in full. Do not skip this step or work from memory.
2. **Identify the mode:** This is a **phase-level** verification. Follow the "Phase-Level Verification Workflow" section (Steps 1 through 8). Required outputs:
   - Step 3: Per-criterion pass/fail table (not just a summary)
   - Step 5: Issue categorization (critical/major/minor counts)
   - Step 7: `verification-result.json` written with all required fields
   - Step 8: Verification report displayed to user
3. **Context to provide:** List of completed work with per-task verification results, spec acceptance criteria, test commands

**Why this matters:** Skipping phase-level verification means the project completes without confirming the full implementation matches the spec's acceptance criteria. The verification result file gates the Complete phase — without it, the project cannot finish.

#### If Completing

When all tasks are finished and a valid verification result exists:

1. **Update spec status** to `complete`:
   ```yaml
   ---
   version: 1
   status: complete
   updated: YYYY-MM-DD
   ---
   ```

2. **Regenerate dashboard with completion summary:**
   - Update Project Context stage to "Complete"
   - Replace Critical Path with completion summary
   - Show final stats (total tasks, completion date, verification result)

   ```markdown
   ## 🛤️ Critical Path

   **Project Complete** ✅

   - All tasks finished: [count] tasks
   - Verification passed: [date from verification-result.json]
   - Spec status: complete

   To add new features, update the spec and run `/work` to decompose new tasks.
   ```

3. **Present final checkpoint to user:**
   ```
   Project complete! All [N] tasks finished and verification passed.

   Summary:
   - [verification summary from verification-result.json]
   - Spec status updated to complete

   To continue working on this project:
   - Update the spec with new requirements
   - Run /work to detect changes and create new tasks
   ```

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

### Example 1: Aligned Request
```
User: /work "Add password validation"
Spec says: "User authentication with email and password"

→ Aligned. Create task, proceed to implement.
```

### Example 2: Minor Addition
```
User: /work "Fix the typo in the login error message"
Spec: Doesn't mention error messages specifically

→ Minor fix within existing scope. Proceed without spec change.
```

### Example 3: Significant Misalignment
```
User: /work "Add social login with Google"
Spec says: "User authentication with email and password"

→ Surface it:
  "The spec defines email/password auth but doesn't mention social login.
   This seems significant. Options:
   1. Add to spec - I'd suggest: 'Support OAuth with Google as alternative login'
   2. Proceed anyway (won't verify against spec)
   3. Skip for now"
```

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
2. **Build dependency chains** - For each, trace what depends on it recursively
3. **Identify longest chain** - This is the critical path
4. **Format with owners** - Show who owns each step:
   - `❗ **You**:` for human-owned tasks
   - `🤖 **Claude**:` for Claude-owned tasks
   - `👥 **Both**:` for collaborative tasks
5. **Show blocking relationships** - Indicate what each step blocks

**Edge cases:**
| Scenario | Handling |
|----------|----------|
| No dependencies (all parallel) | Show all pending tasks as "can start now", no blocking chain |
| Multiple equal-length paths | Pick the path with most human-owned tasks first (surfaces blockers) |
| No incomplete tasks | Show "All tasks complete!" |
| Single task remaining | Show just that task without "blocks" annotation |

**Example output:**
```markdown
## 🛤️ Critical Path

**Next steps to completion:**

1. ❗ **You**: Review API design doc - *blocks step 2*
2. 🤖 **Claude**: Implement API endpoints - *blocks step 3*
3. 👥 **Both**: Integration testing
```

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
6. **Regenerate dashboard** - Read all task-*.json files and update dashboard.md following the canonical template in `.claude/support/reference/dashboard-patterns.md`
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
