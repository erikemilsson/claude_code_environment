# Update Executive Summary Command

Use this command to keep high-level project summaries current.

## Purpose

Refresh executive summary files (phases.md, decisions.md) based on recent project work.

## When to Use

- After completing several tasks that affect project structure
- After making architectural decisions
- Before syncing tasks (to ensure alignment)
- Periodically to keep summaries current

## Process

### Step 1: Analyze Recent Changes

Read completed tasks to understand:
- Which phases were affected
- Which decisions were affected
- New components implemented
- New requirements discovered

### Step 2: Identify Proposed Changes

For **phases.md**:
- Phase status updates (pending -> active -> completed)
- New components added
- Related tasks updated
- Phase flow changes

For **decisions.md**:
- Decision status updates (proposed -> approved -> implemented)
- New decisions documented
- Related tasks updated
- Decision matrix updates

### Step 3: Show Diff and Get Approval

**Critical**: Never auto-update executive summaries. Always show proposed changes:

```diff
## Proposed Changes to phases.md

### Phase 1: Data Ingestion
- Status: active -> completed
+ Related Tasks: added task-004

### Phase 2: Data Transformation
- Status: pending -> active
+ New component: Error recovery module
```

Ask user to:
1. Approve all changes
2. Review each change individually
3. Cancel (no changes)

### Step 4: Apply Approved Changes

Update the files with approved changes and update change logs:

```markdown
## Change Log
- 2025-01-15: Phase 1 marked as completed (all tasks finished)
- 2025-01-15: Added error recovery component to Phase 2
```

### Step 5: Run Sync Tasks

After updating summaries, run `/sync-tasks` to update task overview.

## Options

### --auto-approve-status
Automatically approve status changes without asking:
```
/update-executive-summary --auto-approve-status
```

### --dry-run
Show proposed changes without applying:
```
/update-executive-summary --dry-run
```

## Rules

1. **Never** update executive summaries without user approval
2. Status changes can be auto-approved with flag
3. Structural changes (new phases, new decisions) always require approval
4. Always update change logs
5. Run sync-tasks after updating

## Example

```
User: /update-executive-summary

Claude: Analyzing recent project changes...

Found updates needed:

## Proposed Changes to phases.md

### Phase 1: Data Ingestion
- Status: active -> completed (all tasks finished)

## Proposed Changes to decisions.md

### Decision 001: Database Selection
- Status: approved -> implemented

Approve these changes?

User: Yes

Claude: Applying changes...

- Updated phases.md
- Updated decisions.md
- Change logs updated
- Running /sync-tasks...

Executive summaries are now current!
```
