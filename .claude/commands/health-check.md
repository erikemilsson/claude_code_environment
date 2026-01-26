# Health Check

Combined system health check for task management and CLAUDE.md.

## Usage
```
/health-check                    # Run all checks (schema, semantic, CLAUDE.md)
/health-check --tasks            # Only task system validation (schema + semantic)
/health-check --claude-md        # Only CLAUDE.md audit
/health-check --semantic         # Only semantic validation (staleness, ownership, orphans)
/health-check --sync-check       # Compare local files against template repo
/health-check --report-only      # Show report without fix prompts
```

## Purpose

Over time, task systems drift from standards and CLAUDE.md files accumulate bloat. This command catches both issues in one pass.

---

## Part 1: Task System Validation

Detects and fixes drift from task management standards.

## Validation Checks

### 1. Task JSON Schema Validation

Validates required fields (id, title, status, difficulty) and optional fields per `.claude/reference/task-schema.md`.

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

### 7. Semantic Validation (for 20+ task projects)

These checks detect drift and staleness in large collaborative projects:

**Stale "In Progress" Tasks**
- Tasks with status `"In Progress"` for > 7 days without activity
- Indicates abandoned work or forgotten state updates
- Uses `updated_date` field if present, otherwise `created_date`

**Owner-Capability Mismatch**
- Claude-owned tasks that require human-only capabilities:
  - UI tools (Power BI, Excel dashboards, Figma)
  - Physical actions (hardware, deployment to air-gapped systems)
  - External approvals (management sign-off, legal review)
- Detection: Title/description keywords matched against capability patterns

**Orphan Dependencies**
- Tasks referencing dependency IDs that don't exist
- Can happen after manual task deletion or archive errors
- Critical for maintaining dependency graph integrity

**Workflow Diagram Staleness**
- `workflow-diagram.md` timestamp vs latest task modification
- Warns if diagram is > 24 hours older than task changes
- Suggests running `/generate-workflow-diagram`

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
| Stale workflow diagram | Run /generate-workflow-diagram |
| Orphan dependency reference | Remove invalid dependency ID from array |

## Semantic Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Stale "In Progress" (> 7 days) | Ask user: mark Pending, Blocked, or keep In Progress |
| Owner-capability mismatch | Suggest changing owner to "human" (requires confirmation) |

## Non-Fixable Issues (Manual Required)

| Issue | Why Manual |
|-------|------------|
| Missing required field (id, title, status, difficulty) | Need human input for values |
| Invalid JSON syntax | Need to examine file |
| Circular dependencies | Need to understand intent |
| Duplicate task IDs | Need to decide which to keep |
| Unknown status value | Need to determine correct status |

---

## Part 2: CLAUDE.md Audit

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

Run semantic validation (if not `--claude-md` and task count >= 20):
- Stale "In Progress" detection
- Owner-capability mismatch detection
- Orphan dependency detection
- Workflow diagram staleness check

Run CLAUDE.md audit (if not `--tasks`):
- Line counts
- Section sizes
- Code block lengths

### Step 3: Report

```
## Health Check Report

### Task System - Schema & Integrity
[Checkmark] N checks passed
[Warning] N warnings
[Error] N errors

[List specific issues]

### Task System - Semantic Validation
[Checkmark] No stale tasks
[Warning] 2 tasks "In Progress" for > 7 days
  - Task 15: "Build dashboard" (12 days)
  - Task 23: "API refactor" (8 days)
[Warning] 1 potential owner mismatch
  - Task 45: "Configure Power BI" owned by claude (suggests human)
[Checkmark] No orphan dependencies
[Warning] Workflow diagram stale (3 days behind task changes)

### CLAUDE.md
- Total lines: N [status]
- Sections: N flagged
- Code blocks: N flagged

[List specific issues]

### Summary
Overall status: [HEALTHY / NEEDS ATTENTION / ISSUES FOUND]
```

### Step 4: Offer Fixes

For each fixable issue, present options and apply immediately before moving to next.

---

## Part 3: Template Sync Check

Compares local `.claude/` files against the template repository to detect drift from template updates.

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
     "template_name": "standard"
   }
   ```

2. **Read sync-manifest.json** to get files to compare:
   ```json
   {
     "categories": {
       "sync": [
         ".claude/commands/*.md",
         ".claude/reference/shared-definitions.md",
         ".claude/agents/*.md"
       ]
     }
   }
   ```

3. **Fetch template version** from remote repo:
   ```bash
   gh api repos/{owner}/{repo}/contents/.claude/version.json \
     --jq '.content' | base64 -d | jq '.template_version'
   ```

4. **Compare each sync file** against template:
   ```bash
   # For each file in sync category
   gh api repos/{owner}/{repo}/contents/{path} \
     --jq '.content' | base64 -d > /tmp/template-file
   diff local-file /tmp/template-file
   ```

### Sync Report

```
### Template Sync Check

Template: standard v1.0.0 (2026-01-26)
Source: https://github.com/user/claude_code_environment

Version Status:
  Local:  v1.0.0
  Remote: v1.1.0
  [Warning] Template has been updated

File Comparison (sync category):
  [Checkmark] .claude/commands/complete-task.md - matches
  [Warning] .claude/commands/breakdown.md - differs (12 lines changed)
  [Checkmark] .claude/agents/orchestrator.md - matches
  [Warning] .claude/agents/verify-agent.md - differs (new file in template)
  [Checkmark] .claude/reference/shared-definitions.md - matches

Suggested Actions:
  1. Review changelog for v1.1.0
  2. Update changed files from template
  3. Update version.json after applying changes
```

### Update Instructions

**To update a single file:**
```bash
gh api repos/{owner}/{repo}/contents/{path} \
  --jq '.content' | base64 -d > {local-path}
```

**To update all sync files:**
```bash
# Clone template repo temporarily
git clone --depth 1 https://github.com/user/claude_code_environment /tmp/template
# Copy sync files
cp /tmp/template/.claude/commands/*.md .claude/commands/
cp /tmp/template/.claude/agents/*.md .claude/agents/
cp /tmp/template/.claude/reference/shared-definitions.md .claude/reference/
cp /tmp/template/.claude/reference/task-schema.md .claude/reference/
cp /tmp/template/.claude/reference/agent-handoff.md .claude/reference/
cp /tmp/template/.claude/reference/workflow-guide.md .claude/reference/
# Update version
cp /tmp/template/.claude/version.json .claude/version.json
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

**< 20 tasks:** Semantic validation (stale tasks, owner mismatch) skipped - only needed for larger projects

**Workflow diagram missing:** If `.claude/context/workflow-diagram.md` doesn't exist, staleness check skipped

---

## When to Run

- Start of a work session
- After extensive task operations
- When something feels "off"
- Before major milestones or handoffs
- Periodically (weekly recommended for tasks, monthly for CLAUDE.md)
- **Periodically check for template updates** with `--sync-check`

## Reference

Task schema: `.claude/reference/task-schema.md`
Difficulty guide: `.claude/reference/shared-definitions.md`
Workflow guide: `.claude/reference/workflow-guide.md`
Version info: `.claude/version.json`
Sync manifest: `.claude/sync-manifest.json`
