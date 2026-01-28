# Breakdown Task

Split a complex task into smaller subtasks.

## Usage
```
/breakdown {id}
```

## When to Use
- Task difficulty >= 7
- Task feels too big to complete in one session
- Multiple distinct pieces of work

## Process

1. Read the task and understand scope
2. Identify logical components (aim for 3-6 subtasks)
3. Create subtask files (inheriting spec provenance from parent):
   ```json
   {
     "id": "{parent_id}_{n}",
     "title": "Specific subtask title",
     "status": "Pending",
     "difficulty": 4,
     "parent_task": "{parent_id}",
     "spec_fingerprint": "{copy from parent}",
     "spec_version": "{copy from parent}",
     "spec_section": "{copy from parent}",
     "section_fingerprint": "{copy from parent}",
     "section_snapshot_ref": "{copy from parent}"
   }
   ```

   **Important:** Copy all spec provenance fields from the parent task. This ensures subtasks are tracked for spec drift detection.
4. Update parent task:
   ```json
   {
     "status": "Broken Down",
     "subtasks": ["1_1", "1_2", "1_3"],
     "notes": "Broken down into 3 subtasks"
   }
   ```
5. **Regenerate dashboard** - Follow the Regeneration Checklist in `.claude/support/reference/dashboard-patterns.md`
   - This ensures metadata block, footer, user section backup, and section toggles are handled consistently

## Example

**Before:** Task 5 "Build auth system" (difficulty 8)

**After:**
- Task 5: status = "Broken Down", subtasks = ["5_1", "5_2", "5_3"]
- Task 5_1: "Setup OAuth providers" (difficulty 5)
- Task 5_2: "Create login/logout flows" (difficulty 4)
- Task 5_3: "Add session management" (difficulty 5)

## Rules
- Keep subtask difficulty <= 6
- Subtasks should be independently completable
- Parent auto-completes when all subtasks finish
