# Work Command

The intelligent entry point for all project work. Handles spec-checking, state detection, task decomposition, and routing to specialist agents.

## Usage
```
/work                    # Auto-detect what needs doing
/work {task-id}          # Work on specific task
/work {request}          # Handle ad-hoc request
```

## What It Does

1. **Checks against spec** - Every request is validated against the specification
2. **Analyzes project state** - Reads task-overview, spec, and current progress
3. **Decomposes spec into tasks** - When spec is ready but no tasks exist
4. **Routes to specialists** - Invokes implement-agent or verify-agent as needed
5. **Surfaces misalignments** - Points out when requests don't fit the spec

## Core Principle

**The spec is the living source of truth.** All work should align with it, or the spec should be updated intentionally.

---

## Process

### Step 1: Gather Context

Read and analyze:
- `.claude/spec_v{N}.md` - The specification (source of truth)
- `.claude/tasks/task-overview.md` - Task status and progress
- `.claude/support/questions.md` - Pending questions

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
2. **Identify work items** - Each distinct piece of functionality
3. **Create task files** - One JSON per task, difficulty ≤ 6
4. **Map dependencies** - What must complete before what
5. **Run /sync-tasks** - Generate overview

Task creation guidelines:
- Clear, actionable titles ("Add user validation" not "Backend stuff")
- Difficulty 1-6 (break down anything larger)
- Explicit dependencies
- Owner: claude/human/both

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

# After answering questions, continue
/work
```
