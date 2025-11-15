# Command: Sync Task Overview

## Purpose
Update task-overview.md to reflect current state of all task JSON files.

## Context Required
- `.claude/tasks/*.json` (all task files)
- `.claude/context/validation-rules.md`

## Process
1. Read all task JSON files in `.claude/tasks/` using @.claude/tasks/*.json
2. Sort by task ID (numerical order)
3. Validate each task against validation rules
4. Generate markdown table with columns:
   - ID / File (linked)
   - Task (title)
   - Difficulty
   - Dependencies (comma-separated IDs)
   - Status
5. Add status indicators:
   - 🔴 for difficulty ≥7 without "Broken Down" status
   - 🔵 for "Broken Down" tasks (show subtask progress)
   - 🟡 for blocked tasks
   - 🟢 for completed tasks
6. **For "Broken Down" tasks, calculate and show completion progress:**
   - Count finished subtasks vs total subtasks
   - Format status as: "Broken Down (X/Y done)"
   - Example: "Broken Down (3/5 done)"
7. Include summary statistics:
   - Total tasks
   - Average difficulty
   - Blocked count
   - Completion percentage

## Output Location
- `.claude/tasks/task-overview.md` (overwrite completely)

## Example Output

```markdown
# Project Tasks Overview

## Summary
- Total Tasks: 8
- Top-level Tasks: 3
- Subtasks: 5
- Average Difficulty: 5.2
- Blocked: 0
- Complete: 37%

## All Tasks

| ID / File | Task | Difficulty | Dependencies | Status |
|-----------|------|------------|--------------|--------|
| 12. [task-12.json](task-12.json) | Build emissions ETL | 8 🔵 | | Broken Down (3/5 done) |
| 13. [task-13.json](task-13.json) | ↳ Design pipeline architecture | 4 | | Finished 🟢 |
| 14. [task-14.json](task-14.json) | ↳ Build API connectors | 5 | 13 | Finished 🟢 |
| 15. [task-15.json](task-15.json) | ↳ Implement Polars transforms | 6 | 14 | In Progress |
| 16. [task-16.json](task-16.json) | ↳ Create Azure SQL loader | 5 | 15 | Pending |
| 17. [task-17.json](task-17.json) | ↳ Add error handling | 4 | 15,16 | Pending |

### Legend
- 🔴 High risk (difficulty ≥7) - needs breakdown
- 🔵 Broken Down - work on subtasks
- 🟡 Blocked - needs resolution
- 🟢 Complete
- ↳ Indicates subtask (indented under parent)

### Difficulty Scale
1-2: Trivial | 3-4: Low | 5-6: Moderate | 7-8: High | 9-10: Extreme
```
