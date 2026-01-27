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

**See also:** `/health-check` performs the same drift detection as a validation check. Keep algorithms in sync.

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
2. Read `.claude/agents/implement-agent.md` and follow its workflow for that task
3. Continue to Step 5 (questions) and Step 6 (health check)

**If no request provided** (auto-detect mode):

| Condition | Action |
|-----------|--------|
| No spec exists | Stop - direct user to create spec via `specification_creator/` |
| Spec incomplete | Stop - prompt user to complete spec |
| Spec complete, no tasks | **Decompose** - create tasks from spec |
| Tasks pending | **Execute** - read & follow implement-agent workflow (see Step 4) |
| All tasks finished | **Verify** - read & follow verify-agent workflow (see Step 4) |

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
8. **Map dependencies** - What must complete before what
9. **Regenerate dashboard** - Read all task-*.json and milestone-*.json files and regenerate dashboard.md
   - Preserve the Notes & Ideas section between `<!-- USER SECTION -->` markers
   - Update **Project Context** with project name from spec and current phase
   - Calculate **Overall completion** percentage for Quick Status
   - Calculate milestone progress (finished tasks / total tasks per milestone) for Milestones section
   - Determine milestone status: ⏳ Pending → 🔄 In Progress → ✅ Complete (or ⚠️/🔴 if past target)
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

#### If Executing

**CRITICAL:** You must read `.claude/agents/implement-agent.md` and follow its complete workflow. Do not implement directly.

The agent workflow handles: task selection, status updates, implementation, self-review, completion, and dashboard regeneration.

Context to have ready:
- Current task context
- Relevant spec sections (from `.claude/spec_v{N}.md`)
- Any constraints or notes

#### If Verifying

**CRITICAL:** You must read `.claude/agents/verify-agent.md` and follow its complete workflow. Do not verify directly.

Pass to verify-agent:
- List of completed work
- Spec acceptance criteria
- Test commands available

### Step 5: Handle Questions

Questions accumulate in `.claude/support/questions.md` during work.

**Present questions when:**
- Phase boundary reached
- Quality gate failure (tests fail, spec violation)
- Blocked on decision

**Question format:**
```markdown
## Requirements
- [Question about scope or features]

## Technical
- [Question about implementation approach]

## Scope
- [Question about boundaries or priorities]
```

### Step 6: Lightweight Health Check

Run quick validation checks after completing the main action:

**Checks performed:**
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
6. **Regenerate dashboard** - Read all task-*.json and milestone-*.json files and update dashboard.md
   - Update overall completion percentage and per-milestone progress
   - Recalculate Critical Path with remaining incomplete tasks
   - Add completed task to Recently Completed with completion_date
   - Update milestone progress calculations
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
