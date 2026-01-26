# Health Check

Combined system health check for task management and CLAUDE.md.

## Usage
```
/health-check                # Run all checks
/health-check --tasks        # Only task validation
/health-check --claude-md    # Only CLAUDE.md audit
/health-check --sync-check   # Compare local files against template repo
/health-check --report-only  # Show report without fix prompts
```

## Purpose

Catches drift from task management standards and CLAUDE.md bloat in one pass.

---

## Part 1: Task System Validation

### 1. Task JSON Schema Validation

Validates required fields per `.claude/reference/task-schema.md`:
- `id`, `title`, `status`, `difficulty` (required)
- `description`, `created_date`, `dependencies`, `subtasks`, `parent_task` (optional)

### 2. Relationship Integrity

**Parent-subtask consistency:**
- If task has `parent_task`, parent must exist and list this task in `subtasks`
- If task has `subtasks`, each subtask must reference this task as `parent_task`
- `"Broken Down"` status requires non-empty `subtasks` array

**Dependency validity:**
- All task IDs in `dependencies` array must exist
- No circular dependencies

### 3. ID Safety

- Subtask IDs use format `{parent_id}_{n}` (e.g., `5_1`, `5_2`)
- No duplicate IDs across all task files

### 4. Task Overview Consistency

- Every task JSON has a corresponding row in overview
- Status, title, and difficulty match between JSON and overview
- Summary counts are accurate

### 5. Status Rules

| Status | Rules |
|--------|-------|
| `Pending` | No special requirements |
| `In Progress` | Only ONE task at a time |
| `Blocked` | Should have `notes` explaining blocker |
| `Broken Down` | Must have non-empty `subtasks` array |
| `Finished` | If has subtasks, all must also be `Finished` |

### 6. Difficulty Range

- Must be integer 1-10
- Tasks with difficulty >= 7 should be `"Broken Down"` or have subtasks
- Subtasks should have difficulty <= 6

## Task Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Overview doesn't match JSON | Run /sync-tasks |
| Parent missing subtask in array | Add subtask ID to parent |
| Subtask missing parent_task field | Add parent_task field |
| "Broken Down" with empty subtasks | Change status to "Pending" |
| All subtasks Finished but parent not | Set parent to "Finished" |
| Missing created_date | Add current date |
| Multiple "In Progress" tasks | Ask which to keep |

## Non-Fixable Issues (Manual Required)

| Issue | Why Manual |
|-------|------------|
| Missing required field | Need human input for values |
| Invalid JSON syntax | Need to examine file |
| Circular dependencies | Need to understand intent |
| Duplicate task IDs | Need to decide which to keep |

---

## Part 2: CLAUDE.md Audit

### Thresholds

| Metric | Warning | Error |
|--------|---------|-------|
| Total lines | 80 | 120 |
| Section lines | 15 | 25 |
| Code blocks | 10 | 20 |

### What Belongs Inline

**Keep in CLAUDE.md:**
- Project overview (2-3 sentences)
- Critical commands (one-liners)
- Key conventions (brief list)
- Navigation pointers

**Move to reference/:**
- Detailed schemas (>8 lines)
- Verbose examples
- Full procedure documentation

---

## Process

### Step 1: Scan
```
READ all .claude/tasks/task-*.json files
READ .claude/tasks/task-overview.md
READ CLAUDE.md
```

### Step 2: Run Checks

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

### Step 3: Report

```
## Health Check Report

### Task System
[Checkmark] N checks passed
[Warning] N warnings
[Error] N errors

[List specific issues]

### CLAUDE.md
- Total lines: N [status]
- Sections: N flagged
- Code blocks: N flagged

### Summary
Overall status: [HEALTHY / NEEDS ATTENTION / ISSUES FOUND]
```

### Step 4: Offer Fixes

For each fixable issue, present options and apply.

---

## Part 3: Template Sync Check

Compares local `.claude/` files against the template repository to detect drift.

### Requirements

- `.claude/version.json` - Contains `source_repo` and `template_version`
- `.claude/sync-manifest.json` - Lists files in `sync` category
- `gh` CLI installed and authenticated (or use GitHub MCP tools)

### Process

1. **Read local version.json** to get template info:
   ```json
   {
     "template_version": "1.0.0",
     "source_repo": "https://github.com/user/claude_code_environment",
     "template_name": "lite"
   }
   ```

2. **Read sync-manifest.json** to get files to compare:
   ```json
   {
     "categories": {
       "sync": [
         ".claude/commands/*.md",
         ".claude/reference/shared-definitions.md"
       ]
     }
   }
   ```

3. **Fetch template version** from remote repo:
   ```bash
   gh api repos/{owner}/{repo}/contents/lite/.claude/version.json \
     --jq '.content' | base64 -d | jq '.template_version'
   ```

4. **Compare each sync file** against template:
   ```bash
   # For each file in sync category
   gh api repos/{owner}/{repo}/contents/lite/{path} \
     --jq '.content' | base64 -d > /tmp/template-file
   diff local-file /tmp/template-file
   ```

### Sync Report

```
### Template Sync Check

Template: lite v1.0.0 (2026-01-26)
Source: https://github.com/user/claude_code_environment

Version Status:
  Local:  v1.0.0
  Remote: v1.1.0
  [Warning] Template has been updated

File Comparison (sync category):
  [Checkmark] .claude/commands/complete-task.md - matches
  [Warning] .claude/commands/breakdown.md - differs (12 lines changed)
  [Checkmark] .claude/reference/shared-definitions.md - matches

Suggested Actions:
  1. Review changelog for v1.1.0
  2. Update .claude/commands/breakdown.md:
     gh api repos/user/repo/contents/lite/.claude/commands/breakdown.md \
       --jq '.content' | base64 -d > .claude/commands/breakdown.md
  3. Update version.json after applying changes
```

### Update Instructions

**To update a single file:**
```bash
gh api repos/{owner}/{repo}/contents/lite/{path} \
  --jq '.content' | base64 -d > {local-path}
```

**To update all sync files:**
```bash
# Clone template repo temporarily
git clone --depth 1 https://github.com/user/claude_code_environment /tmp/template
# Copy sync files
cp /tmp/template/lite/.claude/commands/*.md .claude/commands/
cp /tmp/template/lite/.claude/reference/shared-definitions.md .claude/reference/
cp /tmp/template/lite/.claude/reference/task-schema.md .claude/reference/
# Update version
cp /tmp/template/lite/.claude/version.json .claude/version.json
# Cleanup
rm -rf /tmp/template
```

### Offline Mode

If GitHub is unavailable, `--sync-check` will report:
```
[Warning] Cannot reach template repository
  - Check network connection
  - Verify gh CLI is authenticated: gh auth status
  - Skip sync check with: /health-check --tasks --claude-md
```

---

## Edge Cases

**Empty task list:** Reports "0 tasks - all checks pass" (healthy state for new projects)

**Missing version.json:** Sync check skipped with note: "Create .claude/version.json to enable template sync"

**Missing sync-manifest.json:** Sync check skipped with note: "Create .claude/sync-manifest.json to enable template sync"

**Large CLAUDE.md (>120 lines):** Flags as error, suggests moving sections to reference/

**Subtask ID collisions:** Detects `5_1` already exists before creating duplicate

---

## When to Run

- Start of a work session
- After extensive task operations
- When something feels "off"
- Before major milestones
- **Periodically check for template updates** with `--sync-check`

## Reference

Task schema: `.claude/reference/task-schema.md`
Definitions: `.claude/reference/shared-definitions.md`
Version info: `.claude/version.json`
Sync manifest: `.claude/sync-manifest.json`
