# Command: Update Tasks (Phase 1)

## Purpose
Validate task structure, fix inconsistencies, and mark outdated tasks.

## Usage
```
@.claude/commands/update-tasks.md
```

## Process

### 1. Load All Tasks
Scan `.claude/tasks/` for all `task-*.json` files.

### 2. Validation Checks

Run comprehensive validation:

#### A. Structural Validation
```
- [ ] All task files are valid JSON
- [ ] All required fields present (id, title, description, difficulty, status)
- [ ] Task IDs are sequential (no gaps)
- [ ] Task IDs match filenames
```

#### B. Parent-Child Relationship Validation
```
- [ ] Parents have "Broken Down" status
- [ ] Parents list valid subtask IDs
- [ ] Subtasks reference valid parent IDs
- [ ] No orphaned subtasks (parent doesn't list them)
- [ ] No nested subtasks (subtasks cannot have subtasks)
```

#### C. Dependency Validation
```
- [ ] All dependencies reference valid task IDs
- [ ] No circular dependencies
- [ ] No self-dependencies
- [ ] Dependencies are acyclic (forms valid DAG)
```

#### D. Status Validation
```
- [ ] "In Progress" tasks have start_date
- [ ] "Finished" tasks have completion_date
- [ ] "Broken Down" tasks have subtasks array
- [ ] Parent completion matches subtask completion
```

#### E. Difficulty Validation
```
- [ ] Difficulty between 1-10
- [ ] Subtasks have difficulty ≤6
- [ ] High-difficulty pending tasks (≥7) flagged
```

### 3. Auto-Fix Common Issues

**Issue 1: Parent Status Incorrect**
```
Problem: Parent has subtasks but status is "Pending"
Fix: Set status to "Broken Down"
```

**Issue 2: Parent Should Auto-Complete**
```
Problem: All subtasks "Finished" but parent still "Broken Down"
Fix: Set parent status to "Finished", set completion_date
```

**Issue 3: Missing Dates**
```
Problem: Task status "Finished" but no completion_date
Fix: Use current date (or date of last git commit touching file)
```

**Issue 4: Orphaned Subtasks**
```
Problem: Subtask references parent, but parent doesn't list it
Fix: Add subtask to parent's subtasks array
```

**Issue 5: Invalid Dependencies**
```
Problem: Task depends on non-existent task ID
Fix: Remove invalid dependency
```

### 4. Flag Issues Requiring Manual Review

**Issue: Circular Dependencies**
```
⚠️ MANUAL REVIEW REQUIRED

Circular dependency detected:
Task 5 → Task 7 → Task 10 → Task 5

This cannot be auto-fixed. Please review dependencies and break the cycle.
```

**Issue: Task Difficulty Mismatch**
```
⚠️ MANUAL REVIEW REQUIRED

Task 8 has difficulty 9 and status "In Progress"

High-difficulty tasks should be broken down first.
Consider: @.claude/commands/breakdown.md 8
```

**Issue: Outdated Task**
```
ℹ️ REVIEW SUGGESTED

Task 12: "Implement feature X"
Created: 3 months ago
Status: Pending

This task may be outdated or no longer relevant.
Review if still needed or mark as cancelled.
```

### 5. Identify Stale Tasks

Flag tasks that might be outdated:
- Created >30 days ago and still "Pending"
- Status "In Progress" >7 days with no updates
- Description mentions deprecated approaches

Present flagged tasks:
```
⏱️ Potentially Stale Tasks:

Task 15: "Set up legacy API connection"
- Created: 45 days ago
- Status: Pending
- Reason: Old task, possibly superseded by newer approach

Task 18: "Implement workaround for bug XYZ"
- Created: 20 days ago
- Status: In Progress (since 10 days)
- Reason: No recent activity

Recommended: Review these tasks, complete or archive them.
```

### 6. Optimization Suggestions

```
💡 Optimization Opportunities:

1. Task 7 and 8 have no dependencies and same priority
   → Could be worked on in parallel

2. Task 10 has difficulty 8
   → Consider breaking down before starting

3. Critical path: Tasks 1 → 3 → 5 → 6
   → Prioritize these for faster project completion

4. Task 12 has been blocked for 15 days waiting on Task 9
   → Check if Task 9 can be expedited
```

### 7. Generate Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Validation Status:** [PASS / ISSUES FOUND]

## Auto-Fixed Issues: [Count]

✅ Fixed parent status for Task 5 (Pending → Broken Down)
✅ Auto-completed parent Task 8 (all subtasks done)
✅ Added completion_date to Task 12
✅ Removed invalid dependency: Task 7 → Task 99 (doesn't exist)

## Manual Review Required: [Count]

⚠️ Task 15: Circular dependency (see details above)
⚠️ Task 20: High difficulty (9) still pending - needs breakdown

## Stale Tasks: [Count]

⏱️ Task 18: In progress for 10 days with no activity
⏱️ Task 22: Pending for 45 days, possibly outdated

## Optimization Suggestions: [Count]

💡 Tasks 7,8 could run in parallel
💡 Critical path identified: 1→3→5→6
💡 Task 10 should be broken down (difficulty 8)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Next Actions

1. Review manual issues and fix as needed
2. Address stale tasks (complete or archive)
3. Consider optimization suggestions
4. Run: @.claude/commands/sync-tasks.md to update overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 8. Update Task Files
Save all auto-fixed tasks back to their JSON files.

### 9. Trigger Sync
Automatically run `sync-tasks.md` to update task-overview.md.

## Validation Rules

### Parent Task Rules
1. Status must be "Broken Down" if has subtasks
2. Cannot have status "In Progress" or "Finished" if subtasks incomplete
3. Auto-completes when all subtasks "Finished"
4. Hours = sum of subtask hours

### Subtask Rules
1. Must reference valid parent
2. Parent must list subtask in its subtasks array
3. Difficulty must be ≤6
4. Cannot have their own subtasks (flat hierarchy)

### Dependency Rules
1. Must form valid DAG (no cycles)
2. Cannot depend on self
3. Cannot depend on non-existent tasks
4. Cannot depend on "Broken Down" parents (depend on subtasks instead)

### Status Transitions
Valid transitions:
- Pending → In Progress → Finished
- Pending → Broken Down → Finished (auto)
- Pending → Cancelled (manual)

Invalid transitions:
- Finished → Pending (cannot un-finish)
- Broken Down → In Progress (work on subtasks instead)

## Output Files

**Modified:**
- `.claude/tasks/task-*.json` - Any auto-fixed tasks
- `.claude/tasks/task-overview.md` - Via sync-tasks

**Created:**
- `.claude/tasks/_validation-report.md` - Detailed validation log

## When to Run

**Run periodically:**
- Before starting major work session
- After manually editing task files
- Weekly for long projects
- When task-overview.md seems incorrect

**Run after:**
- Manually creating tasks
- Manually editing task dependencies
- Git pull (if collaborating)

## Notes

- **Safe to run frequently** - only fixes clear issues
- **Always backs up** - before modifying task files
- **Manual review required** for complex issues
- **Non-destructive** - flags issues, doesn't delete tasks
- **Idempotent** - safe to run multiple times
- Use this before `sync-tasks.md` for best results
