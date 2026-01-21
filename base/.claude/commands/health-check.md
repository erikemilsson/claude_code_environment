# Health Check

Combined system health check for task management and CLAUDE.md.

## Usage
```
/health-check              # Run both checks
/health-check --tasks      # Only task system validation
/health-check --claude-md  # Only CLAUDE.md audit
```

## Purpose

Over time, task systems drift from standards and CLAUDE.md files accumulate bloat. This command catches both issues in one pass.

---

# Part 1: Task System Validation

Detects and fixes drift from task management standards.

## Validation Checks

### 1. Task JSON Schema Validation

**Required fields:**
| Field | Type | Valid Values |
|-------|------|--------------|
| `id` | string | Top-level: `"1"`, `"2"`, etc. Subtasks: `"1_1"`, `"1_2"`, etc. |
| `title` | string | Non-empty |
| `status` | string | `"Pending"`, `"In Progress"`, `"Blocked"`, `"Broken Down"`, `"Finished"` |
| `difficulty` | number | 1-10 |

**Optional fields:**
| Field | Type | Format |
|-------|------|--------|
| `description` | string | - |
| `created_date` | string | YYYY-MM-DD |
| `dependencies` | array | Task ID strings |
| `subtasks` | array | Task ID strings |
| `parent_task` | string/null | Parent task ID |
| `files_affected` | array | File paths |
| `notes` | string | - |

### 2. Relationship Integrity

**Parent-subtask consistency:**
- If task has `parent_task`, parent must exist and list this task in `subtasks`
- If task has `subtasks`, each subtask must exist and reference this task as `parent_task`
- `"Broken Down"` status requires non-empty `subtasks` array
- Subtasks should not have `"Broken Down"` as status (only top-level)

**Dependency validity:**
- All task IDs in `dependencies` array must exist
- No circular dependencies

### 3. ID Safety (Breakdown Protection)

When breaking down tasks, IDs must not collide:
- Subtask IDs use format `{parent_id}_{n}` (e.g., `5_1`, `5_2`, `5_3`)
- Check for ID uniqueness across all task files
- Verify no orphaned task files exist

### 4. Task Overview Consistency

- Every task JSON has a corresponding row in overview
- Every row in overview has a corresponding task JSON
- Status, title, and difficulty match between JSON and overview
- Summary count is accurate

### 5. Status Rules

| Status | Rules |
|--------|-------|
| `Pending` | No special requirements |
| `In Progress` | Only ONE task should have this status at a time |
| `Blocked` | Should have `notes` explaining the blocker |
| `Broken Down` | Must have non-empty `subtasks` array |
| `Finished` | If has subtasks, all subtasks must also be `Finished` |

### 6. Difficulty Range

- Must be integer 1-10
- Tasks with difficulty >= 7 should be `"Broken Down"` or have subtasks
- Subtasks should have difficulty <= 6

## Task Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Overview doesn't match JSON | Run /sync-tasks |
| Parent missing subtask in array | Add subtask ID to parent's subtasks array |
| Subtask missing parent_task field | Add parent_task field |
| "Broken Down" with empty subtasks | Change status to "Pending" |
| All subtasks Finished but parent not | Set parent status to "Finished" |
| Missing created_date | Add current date |
| Multiple "In Progress" tasks | Ask which to keep, set others to "Pending" |

---

# Part 2: CLAUDE.md Audit

Detects bloat and offers guided cleanup.

## Thresholds

| Metric | Warning | Error |
|--------|---------|-------|
| Total lines | 80 | 120 |
| Section lines | 15 | 25 |
| Code blocks | 10 | 20 |
| Inline schemas | 8 | Always flag |

## Audit Checks

1. **Total lines** - Compare against thresholds
2. **Section sizes** - Check each ## section for line count
3. **Code blocks** - Check each code block for length
4. **Inline schemas** - Flag JSON schemas >8 lines

## Fix Options (per issue)

1. **Move** - Create `.claude/reference/{section-slug}.md`, replace with link
2. **Keep** - Mark as explicitly kept
3. **Condense** - Rewrite to fewer lines
4. **Skip** - No changes

## What Belongs Inline

Keep in CLAUDE.md:
- Project overview (2-3 sentences)
- Critical commands (one-liners)
- Key conventions (brief list)
- Navigation pointers

Move to reference/:
- Detailed schemas (>8 lines)
- Verbose examples
- Full procedure documentation
- Technology deep-dives

---

# Process

## Step 1: Scan

```
READ all .claude/tasks/task-*.json files
READ .claude/tasks/task-overview.md
READ CLAUDE.md
```

## Step 2: Run Checks

Run task validation checks (if not `--claude-md`):
- Schema validation for each task file
- Relationship integrity
- ID uniqueness
- Overview consistency
- Status rules
- Difficulty ranges

Run CLAUDE.md audit (if not `--tasks`):
- Line counts
- Section sizes
- Code block lengths

## Step 3: Report

```
## Health Check Report

### Task System
✅ N checks passed
⚠️ N warnings
❌ N errors

[List specific issues]

### CLAUDE.md
- Total lines: N [✅/⚠️/❌]
- Sections: N flagged
- Code blocks: N flagged

[List specific issues]

### Summary
Overall status: [HEALTHY / NEEDS ATTENTION / ISSUES FOUND]
```

## Step 4: Offer Fixes

For each fixable issue, present options and apply immediately before moving to next.

---

# When to Run

- Start of a work session
- After extensive task operations
- When something feels "off"
- Before major milestones or handoffs
- Periodically (weekly recommended for tasks, monthly for CLAUDE.md)

## Reference

Task schema: `.claude/reference/task-schema.md`
Difficulty guide: `.claude/reference/difficulty-guide.md`
CLAUDE.md guide: `.claude/reference/claude-md-guide.md`
