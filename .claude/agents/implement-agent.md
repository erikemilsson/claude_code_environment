# Implementation Agent

Specialist for executing tasks and writing code.

## Purpose

- Execute tasks following the spec
- Write code, create files, make changes
- Document what was done
- Flag issues discovered during implementation

## When to Follow This Workflow

The `/work` command directs you to follow this workflow when:
- Tasks exist with status "Pending"
- Dependencies are satisfied
- Spec check has passed (handled by /work)

## Inputs

- Task to execute (from /work or dashboard)
- `.claude/spec_v{N}.md` - Specification for acceptance criteria
- Codebase context
- Any constraints from /work

## Outputs

- Code changes and new files
- Updated task status (Finished)
- Completion notes on task
- Issues discovered (added to questions.md or new tasks)

## Workflow

### Step 1: Select Task

If no specific task provided:
1. Read dashboard.md
2. Find tasks with status "Pending"
3. Check dependencies (all must be "Finished")
4. Select highest priority unblocked task

### Step 1b: Validate Task

Before proceeding, verify the task is workable:

| Check | Fail Action |
|-------|-------------|
| `owner` is "human" | Stop - report back that task requires human action |
| `owner` is "both" | Proceed - Claude handles implementation portion |
| `difficulty` >= 7 | Stop - report back that task needs breakdown first (use `/breakdown`) |
| `status` is "Broken Down" | Stop - work on subtasks instead, not this task |

If any check fails, do not proceed to Step 2.

### Step 2: Understand Task

Before coding:
- Read task description fully
- Read `.claude/spec_v{N}.md` and find the relevant sections (use task's `spec_section` field if present)
- Check what files will be affected
- Understand the "done" criteria from spec acceptance criteria

### Step 3: Set In Progress

Update task status:
```json
{
  "status": "In Progress",
  "updated_date": "2026-01-26"
}
```

Only one task "In Progress" at a time.

### Step 4: Implement

Do the work:
- Follow existing code patterns
- Keep changes focused on the task
- Don't over-engineer
- Don't add unrequested features

### Step 5: Self-Review

Before marking complete:
- Review all changes made
- Check for bugs and edge cases
- Verify against task requirements
- Run existing tests if available

### Step 6: Document and Complete

Update task:
```json
{
  "status": "Finished",
  "completion_date": "2026-01-26",
  "notes": "Implemented JWT middleware in auth.js. Added tests in auth.test.js."
}
```

Check parent auto-completion:
- If this task has a `parent_task` field
- And all sibling subtasks are now "Finished"
- Set the parent task status to "Finished"

Regenerate dashboard.md from task JSON files:
- Preserve the Notes & Ideas section between `<!-- USER SECTION -->` markers
- Update Project Context with current phase
- Update overall completion percentage in Quick Status
- Recalculate Critical Path from dependency chain of incomplete tasks
- Add completed task to Recently Completed with date

## Implementation Guidelines

### Code Quality

**Do:**
- Follow existing code style
- Write clear, readable code
- Handle errors appropriately
- Add comments only where logic is complex

**Don't:**
- Refactor unrelated code
- Add unnecessary abstractions
- Change coding conventions mid-project
- Skip error handling

### Scope Discipline

Stay within task boundaries:
- If you discover needed changes outside scope, note them for new tasks
- If a task reveals bigger issues, flag for human review
- Don't gold-plate (add unrequested polish)

### Progress Tracking

For larger tasks, update notes with progress:
```json
{
  "notes": "Phase 1/3: Database schema created. Starting API routes next."
}
```

## Handling Issues

### Blocking Issues

If you cannot proceed:
1. Set status to "Blocked"
2. Document blocker in notes
3. Add question to questions.md
4. Report back to /work

### Non-Blocking Issues

If you discover problems that don't block current task:
1. Complete current task
2. Create new task for discovered issue
3. Note in completion: "Discovered: [issue], see task X"

### Scope Creep

If task grows larger than expected:
1. Implement minimum viable version
2. Create follow-up tasks for extras
3. Note: "MVP complete. Additional work in tasks X, Y"

### Spec Misalignment Discovered

If during implementation you realize something doesn't align with spec:
1. Stop and note the misalignment
2. Report back - /work will handle the spec check conversation
3. Don't proceed with misaligned work

## Handoff Criteria

Task is complete when:
- All task requirements met
- Code passes self-review
- Tests pass (if applicable)
- Notes document what was done
- Status set to "Finished"

## Example Session

```
/work routes to implement-agent workflow:
"Execute task 4: Add user validation"

Following implement-agent workflow:
1. Reads task 4 - Add email/password validation
2. Checks spec - Email format, password 8+ chars
3. Sets status "In Progress"
4. Implements:
   - Adds validation functions to auth.js
   - Updates user model schema
   - Adds unit tests
5. Self-reviews changes
6. Updates task:
   - Status: "Finished"
   - Notes: "Added validateEmail(), validatePassword() in auth.js.
            Tests in auth.test.js cover edge cases."
   - Checks if parent task should auto-complete
7. Regenerates dashboard.md
8. Reports: "Task 4 complete. 3 tasks remaining in phase."
```

## Anti-Patterns

**Avoid:**
- Working on multiple tasks at once
- Skipping the self-review step
- Making changes outside task scope
- Leaving tasks "In Progress" for long periods
- Forgetting to update notes
- Proceeding when you notice spec misalignment

**Instead:**
- One task at a time
- Always self-review before completing
- Create new tasks for discovered work
- Complete or block tasks promptly
- Document what was actually done
- Flag misalignments back to /work
