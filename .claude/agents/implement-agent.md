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
- Updated task status ("Awaiting Verification" after implementation, then "Finished" after verification passes)
- Completion notes on task
- Issues discovered (added to questions.md or new tasks)

## How This Workflow Is Invoked

This file is read by `/work` during the Execute phase. **You are reading this file because `/work` directed you here.** Follow every step below in order — do not skip steps or implement directly without going through this workflow.

Each step produces an observable artifact (a file change, status update, or output). These artifacts allow health-check and /work to verify the workflow was followed.

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

**Required artifact:** Update task JSON file to "In Progress" **before writing any implementation code.** This is the checkpoint that proves the workflow is being followed — a task that jumps directly from "Pending" to "Finished" without passing through "In Progress" indicates the workflow was bypassed.

Update task status:
```json
{
  "status": "In Progress",
  "updated_date": "YYYY-MM-DD"
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

**Required artifact:** Document the review in the task notes (even briefly). A task completed without any self-review note indicates this step was skipped.

Before marking complete:
- Review all changes made
- Check for bugs and edge cases
- Verify against task requirements
- Run existing tests if available

Note: After self-review, the task will be set to "Awaiting Verification" and
verify-agent will run per-task verification (Step 6). Self-review is your
chance to catch issues before verification. Verification failures send the
task back to "In Progress."

### Step 6: Document and Trigger Verification

Implementation and verification are now a single atomic operation. A task only reaches "Finished" if verification passes.

#### Step 6a: Mark Ready for Verification

Update task with transitional status:
```json
{
  "status": "Awaiting Verification",
  "completion_date": "2026-01-26",
  "updated_date": "2026-01-26",
  "notes": "Implemented JWT middleware in auth.js. Added tests in auth.test.js."
}
```

**Why "Awaiting Verification":**
- A task is not truly "Finished" until it passes verification
- This intermediate status makes the verification requirement structurally visible
- Tasks cannot remain in "Awaiting Verification" — they must proceed to verification immediately

**IMPORTANT — Separation of concerns:**
- Do NOT write `task_verification` field — that is verify-agent's exclusive responsibility
- Do NOT write `verification-result.json` — that is verify-agent's exclusive responsibility

#### Step 6b: Trigger Per-Task Verification (MANDATORY)

Immediately after setting "Awaiting Verification", trigger verification:

1. **Read the verify-agent file:** Use the Read tool to read `.claude/agents/verify-agent.md`
2. **Follow per-task verification workflow:** Execute Steps T1-T8 from verify-agent's "Per-Task Verification Workflow" section
3. **Handle the result:**

| Result | What Happens |
|--------|--------------|
| **Pass** | verify-agent sets status to "Finished" with `task_verification.result = "pass"` |
| **Fail** | verify-agent sets status to "In Progress" with `[VERIFICATION FAIL]` notes. Return to Step 4 to fix issues, then re-verify. |

**This is now atomic:** implement → verify. The gap where tasks could be "Finished" without verification no longer exists.

#### Step 6c: Post-Verification Cleanup

After verification completes (pass or fail):

**If verification passed:**
- Check parent auto-completion:
  - If this task has a `parent_task` field
  - And all sibling subtasks are now "Finished"
  - Set the parent task status to "Finished"

**Always (pass or fail):**
- Regenerate dashboard.md from task JSON files, following the canonical template in `.claude/support/reference/dashboard-patterns.md`:
  - **Source of truth:** Only include tasks that have corresponding `task-*.json` files
  - **User section backup:** Save existing user section before regenerating (see work.md)
  - Preserve the Notes & Ideas section between `<!-- USER SECTION -->` markers
  - Use exact section headings, emojis, and table formats from dashboard-patterns.md
  - Update Project Context with current phase
  - Update overall completion percentage in Quick Status
  - Update Spec Alignment section with drift status
  - Update Verification Debt in Needs Your Attention section
  - Recalculate Critical Path from dependency chain of incomplete tasks
  - Add completed task to Recently Completed with date
  - Add dashboard metadata block and footer line

**MANDATORY: Return control to `/work` after completing this step.**
- Do NOT proceed to the next task
- `/work` will select the next task or route to phase-level verification if all tasks done

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

### Decisions Made During Implementation

If you make a significant choice during implementation:
1. Read `.claude/support/reference/decision-template.md` for the format and example
2. Create a `decision-*.md` file in `.claude/support/decisions/` using that template
3. Add the decision to the dashboard's All Decisions section
4. **Rule:** Never reference a decision ID on the dashboard without a corresponding file

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
- Status set to "Finished" (after passing verification)
- Per-task verification passes (Step 6b triggers verify-agent as part of this workflow)

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
