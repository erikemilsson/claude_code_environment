# Command: update-executive-summary

## Purpose
Refresh the executive summary files (phases.md and decisions.md) based on recent project work, ensuring they remain accurate and up-to-date.

## When to Use
- After completing several tasks that affect project structure
- After defining new phases or modifying existing ones
- After making architectural decisions
- Before running /sync-tasks (to ensure task overview reflects current structure)
- Periodically (e.g., weekly) to keep summaries current

## Prerequisites
- `.claude/context/phases.md` exists
- `.claude/context/decisions.md` exists
- Recent tasks have been completed (or new work has been done)

## Process

### Step 1: Analyze Recent Changes
Read the following to understand what has changed:

#### 1.1 Completed Tasks
Read `.claude/tasks/task-*.json` files with:
- `status: "finished"`
- `updated` date within last [N] days or since last summary update

Extract:
- Which phases were affected (`related_phases`)
- Which decisions were affected (`related_decisions`)
- New components implemented
- New requirements discovered

#### 1.2 Current Executive Summaries
Read current state:
- `.claude/context/phases.md`
- `.claude/context/decisions.md`

#### 1.3 User Edits
Check if user has made manual edits:
- Compare change log timestamps with file modification times
- Flag any manual edits not in change log (requires user confirmation)

### Step 2: Identify Proposed Changes
Based on analysis, identify changes needed:

#### For phases.md:
- **Phase status updates**:
  - If all related tasks for phase-N are finished → status: completed
  - If any related tasks for phase-N are in_progress → status: active
- **New components**:
  - Tasks may have created components not listed in phases
- **New related tasks**:
  - Update "Related Tasks" list to include new tasks
- **Phase flow changes**:
  - If new phases were defined via tasks
  - If phase order changed

#### For decisions.md:
- **Decision status updates**:
  - If decision-N related tasks are all finished → status: implemented
  - If decision-N tasks are in_progress → status: approved
- **New decisions**:
  - If user has added decision entries not yet in change log
- **New related tasks**:
  - Update "Related Tasks" for each decision
- **Decision matrix updates**:
  - Ensure matrix reflects all decisions and current statuses

### Step 3: Show Proposed Changes (REQUIRE APPROVAL)
**CRITICAL**: Do NOT make changes automatically. Show user a diff.

Format:
```diff
## Proposed Changes to .claude/context/phases.md

### Phase 1: Data Ingestion
- Status: active → completed
+ Related Tasks: [task-001, task-002, task-003] → [task-001, task-002, task-003, task-004]

### Phase 2: Data Transformation
- Status: pending → active
+ New component: component-2-4: Error recovery module (from task-007)

## Proposed Changes to .claude/context/decisions.md

### Decision 001: Database Technology Selection
- Status: approved → implemented
+ Related Tasks: [task-001, task-002] → [task-001, task-002, task-015]

### Decision 005: API Architecture Pattern
+ Status: approved (newly documented)
+ Related Tasks: [task-008, task-009]
```

Ask user:
```
I've identified updates needed for the executive summaries based on recent work.

Changes proposed:
- phases.md: 2 status updates, 1 new component, 3 task link updates
- decisions.md: 1 status update, 1 new decision documented, 2 task link updates

See diff above. Approve these changes?

Options:
1. Approve all
2. Review each change individually
3. Cancel (no changes)
```

### Step 4: Apply Approved Changes
After user approval:

#### 4.1 Update phases.md
- Apply status changes
- Add new components
- Update related task lists
- Update change log:
  ```yaml
  ## Change Log
  - 2025-12-29: Phase 1 marked as completed (all tasks finished)
  - 2025-12-29: Added component-2-4 to Phase 2 (error recovery module)
  - 2025-12-29: Updated task references across phases
  ```

#### 4.2 Update decisions.md
- Apply status changes
- Add new decision entries (if user created them manually)
- Update related task lists
- Update decision matrix table
- Update change log:
  ```yaml
  ## Change Log
  - 2025-12-29: Decision 001 marked as implemented
  - 2025-12-29: Decision 005 documented and approved
  - 2025-12-29: Updated task references for decisions 001, 002, 005
  ```

#### 4.3 Verify Bidirectional Links
Ensure consistency:
- If `phases.md` says task-042 relates to phase-2...
- Then `task-042.json` should have `"related_phases": ["phase-2"]`
- If mismatch found, flag to user

Similarly for decisions.

### Step 5: Run /sync-tasks
After updating executive summaries, automatically run `/sync-tasks` to update the task overview table with new phase/decision information.

### Step 6: Confirm Completion
Show user:
```
✓ Executive summaries updated

Updated:
- .claude/context/phases.md
  - Phase 1 status: active → completed
  - Added component-2-4 to Phase 2
  - Updated task links

- .claude/context/decisions.md
  - Decision 001 status: approved → implemented
  - Documented Decision 005
  - Updated task links

✓ Task overview refreshed

Change logs updated in both files.

Next steps:
- Continue working on tasks
- Run this command periodically to keep summaries current
```

## Output Location
- `.claude/context/phases.md` (updated)
- `.claude/context/decisions.md` (updated)
- `.claude/tasks/task-overview.md` (refreshed via /sync-tasks)

## Options/Flags

### --auto-approve-status
Automatically approve status changes (active → completed, approved → implemented) without asking:
```
/update-executive-summary --auto-approve-status
```
Still requires approval for structural changes (new phases, new decisions).

### --dry-run
Show proposed changes without applying them:
```
/update-executive-summary --dry-run
```

### --since [date]
Only consider changes since a specific date:
```
/update-executive-summary --since 2025-12-20
```

## Example Interaction

```
User: /update-executive-summary

Claude: Analyzing recent project changes...

Checking:
- Completed tasks since last update (5 tasks)
- Current phases.md structure
- Current decisions.md entries

Found updates needed:

## Proposed Changes to .claude/context/phases.md

### Phase 1: Data Ingestion
- Status: active → completed (all tasks finished)
+ Related Tasks: added task-004

### Phase 2: Data Transformation
- Status: pending → active (task-005 in progress)
+ New Component: component-2-4: Error recovery module (implemented in task-007)

## Proposed Changes to .claude/context/decisions.md

### Decision 001: Database Technology Selection
- Status: approved → implemented (task-001, task-002 complete)

Summary:
- 2 phase status updates
- 1 new component added
- 1 decision status update
- 4 task link updates

Approve these changes?

User: Yes

Claude: Applying changes...

✓ Updated .claude/context/phases.md
  - Phase 1: active → completed
  - Phase 2: pending → active
  - Added component-2-4 to Phase 2
  - Updated task references

✓ Updated .claude/context/decisions.md
  - Decision 001: approved → implemented
  - Updated task references

✓ Change logs updated in both files

Running /sync-tasks to refresh task overview...

✓ Task overview updated

Executive summaries are now current!

Next: Continue working on Phase 2 tasks (task-006, task-007 pending)
```

## Example with Manual Edits

```
User: /update-executive-summary

Claude: Analyzing recent project changes...

⚠ Warning: I detected manual edits to .claude/context/phases.md that aren't in the change log:
- Phase 3 was added manually on 2025-12-28

Additionally, based on completed tasks, I propose:
- Phase 1 status: active → completed

Would you like me to:
1. Add both changes to the change log and update
2. Only add my proposed changes (ignore manual Phase 3 addition)
3. Review each change individually

User: Option 1

Claude: Updating change log with manual edits and task-based updates...

✓ Updated .claude/context/phases.md
  - Documented manual addition of Phase 3 (2025-12-28)
  - Phase 1: active → completed (2025-12-29)
  - Change log updated

✓ Executive summaries current
```

## Notes
- **Never** update executive summaries without explicit user approval
- Status changes (active → completed) can be auto-approved with `--auto-approve-status` flag
- Structural changes (new phases, new components, new decisions) always require approval
- This command should be run periodically to prevent summaries from drifting too far from reality
- If user makes manual edits to executive summaries, this command will detect and ask how to handle them
- Change logs are critical for traceability - always update them
- Bidirectional link verification helps catch inconsistencies between tasks and summaries
