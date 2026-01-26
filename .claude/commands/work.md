# Work Command

The intelligent entry point for all project work. Handles spec-checking, state detection, task decomposition, task completion, and routing to specialist agents.

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
5. **Routes to specialists** - Invokes implement-agent or verify-agent as needed
6. **Surfaces misalignments** - Points out when requests don't fit the spec
7. **Auto-syncs dashboard** - Regenerates dashboard.md after any task changes

## Core Principle

**The spec is the living source of truth.** All work should align with it, or the spec should be updated intentionally.

---

## Process

### Step 1: Gather Context

Read and analyze:
- `.claude/spec_v{N}.md` - The specification (source of truth)
- `.claude/dashboard.md` - Task status and progress
- `.claude/support/questions.md` - Pending questions

### Step 1b: Spec Drift Detection

After reading the spec, compute and check its fingerprint:

1. **Compute current spec fingerprint** - SHA-256 hash of spec file content
2. **Check existing tasks** - Read `spec_fingerprint` from task files
3. **Compare fingerprints:**

```
If tasks exist with spec_fingerprint:
├─ Fingerprints match → Continue normally
└─ Fingerprints differ → Surface drift warning:
   "The spec has changed since tasks were decomposed.
    Options:
    1. Review changes - Show what's different
    2. Re-decompose - Create new tasks from updated spec
    3. Acknowledge - Mark tasks as reviewed against new spec
    4. Continue anyway - Proceed with warning noted"
```

**Hash computation:**
```bash
sha256sum .claude/spec_v{N}.md | cut -d' ' -f1
# Prefix with "sha256:" → "sha256:a1b2c3d4..."
```

**Note:** Tasks without `spec_fingerprint` are treated as legacy (no warning).

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
2. Invoke implement-agent on that task
3. Skip to Step 5 (questions)

**If no request provided** (auto-detect mode):

| Condition | Action |
|-----------|--------|
| No spec exists | Stop - direct user to create spec via `specification_creator/` |
| Spec incomplete | Stop - prompt user to complete spec |
| Spec complete, no tasks | **Decompose** - create tasks from spec |
| Tasks pending | **Execute** - invoke implement-agent on next available task |
| All tasks finished | **Verify** - invoke verify-agent |

### Step 4: Execute Action

#### If Decomposing (spec → tasks)

Break the spec into granular tasks:

1. **Read spec thoroughly** - Understand all requirements and acceptance criteria
2. **Compute spec fingerprint** - SHA-256 hash of spec content (see Step 1b)
3. **Identify work items** - Each distinct piece of functionality
4. **Create task files** - One JSON per task, difficulty ≤ 6, with provenance:
   - `spec_fingerprint` - Hash computed in step 2
   - `spec_version` - Filename of spec (e.g., "spec_v1")
   - `spec_section` - Originating section heading (e.g., "## Authentication")
5. **Map dependencies** - What must complete before what
6. **Regenerate dashboard** - Read all task-*.json and milestone-*.json files and regenerate dashboard.md
   - Preserve the Notes & Ideas section between `<!-- USER SECTION -->` markers
   - Calculate milestone progress (finished tasks / total tasks per milestone)
   - Determine milestone status: ⏳ Pending → 🔄 In Progress → ✅ Complete (or ⚠️/🔴 if past target)

Task creation guidelines:
- Clear, actionable titles ("Add user validation" not "Backend stuff")
- Difficulty 1-6 (break down anything larger)
- Explicit dependencies
- Owner: claude/human/both
- Include spec provenance fields (fingerprint, version, section)

#### If Executing

Invoke implement-agent with:
- Current task context
- Relevant spec sections
- Any constraints or notes

#### If Verifying

Invoke verify-agent with:
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
- Orphan dependency detection (references to non-existent tasks)
- Out-of-spec task count

**Output format:**
```
Quick check: ✓
```
or
```
Quick check: ⚠️ 2 issues
  - Spec has changed since tasks were decomposed
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

### Good Decomposition
- Each task has clear "done" criteria
- Tasks are independently testable
- Dependencies are explicit
- Difficulty ≤ 6

### Task Difficulty Scale

See `.claude/support/reference/shared-definitions.md` for the difficulty scale.

Key rule: Tasks with difficulty 7+ must be broken down before starting.

### Implementation Stages
Organize execute-phase tasks into logical stages:

```
Stage 1: Foundation
- Setup, core infrastructure, basic scaffolding

Stage 2: Core Features
- Main functionality from spec

Stage 3: Polish
- Edge cases, error handling, UX

Stage 4: Validation
- Testing, documentation, verification
```

Note: These are organizational stages for tasks, not to be confused with workflow phases (Spec → Execute → Verify).

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
   (including milestone progress calculations)
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
