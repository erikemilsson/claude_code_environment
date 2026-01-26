# Health Check

Combined system health check for tasks, decisions, and CLAUDE.md.

## Usage
```
/health-check                    # Run all checks (tasks, CLAUDE.md, decisions)
/health-check --tasks            # Only task system validation (schema + semantic)
/health-check --claude-md        # Only CLAUDE.md audit
/health-check --decisions        # Only decision system validation
/health-check --semantic         # Only semantic validation (staleness, ownership, orphans)
/health-check --sync-check       # Compare local files against template repo
/health-check --report-only      # Show report without fix prompts
```

## Purpose

Over time, task systems drift from standards, decision records become stale, and CLAUDE.md files accumulate bloat. This command catches all these issues in one pass.

---

## Part 1: Task System Validation

Detects and fixes drift from task management standards.

## Validation Checks

### 1. Task JSON Schema Validation

Validates required fields (id, title, status, difficulty) and optional fields per `.claude/support/reference/task-schema.md`.

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

### 4. Dashboard Consistency

- Every task JSON has a corresponding row in dashboard
- Every row in dashboard has a corresponding task JSON
- Status, title, and difficulty match between JSON and dashboard
- Summary count is accurate

### 5. Dashboard Structure

Validates that dashboard.md follows the canonical template structure:

**Required sections (in order):**
1. `# Dashboard` - Title
2. `## 🚨 Needs Your Attention` - Consolidated attention section
3. `## 🎯 Milestones` - Project phase progress and targets
4. `## ⏰ Timeline` - Deadlines and milestones
5. `## Quick Status` - Summary table
6. `## 🤖 Claude Status` - Claude tasks
7. `## 📊 Progress This Week` - Recent activity
8. `## 📋 All Decisions` - Decision log
9. `## 📝 All Tasks` - Full task table
10. `## 💡 Notes & Ideas` - User section (preserved on sync)

**Validation:**
- Check each required section header exists
- Verify sections appear in correct order
- Flag missing or out-of-order sections
- Suggest regenerating dashboard.md

### 6. Status Rules

| Status | Rules |
|--------|-------|
| `Pending` | No special requirements |
| `In Progress` | Only ONE task should have this status at a time |
| `Blocked` | Should have `notes` explaining the blocker |
| `Broken Down` | Must have non-empty `subtasks` array |
| `Finished` | If has subtasks, all subtasks must also be `Finished` |

### 7. Difficulty Range

- Must be integer 1-10
- Tasks with difficulty >= 7 should be `"Broken Down"` or have subtasks
- Subtasks should have difficulty <= 6

### 8. Questions and Workspace Staleness

**Stale Questions:**
- Questions in `.claude/support/questions.md` older than 14 days
- Warning: "N questions have been pending for over 14 days"
- Suggests reviewing and answering or removing outdated questions

**Stale Workspace Files:**
- Files in `.claude/support/workspace/` older than 30 days
- Warning: "N workspace files are over 30 days old"
- Suggests graduating drafts to final locations or deleting scratch files

### 9. Semantic Validation (for 20+ task projects)

These checks detect drift and staleness in large collaborative projects:

### 10. Spec Fingerprint Validation (Granular)

Detects when the specification has changed since tasks were decomposed, with section-level granularity.

**See also:** `/work` Step 1b performs the same drift detection during normal workflow. Keep algorithms in sync.

**Full spec check:**
- Compute current spec SHA-256 hash
- Compare against `spec_fingerprint` field in task files
- If different, proceed to section-level analysis

**Section-level check (when full spec differs):**
- Load snapshot from `section_snapshot_ref` (if exists)
- Parse both current spec and snapshot into sections
- Compare `section_fingerprint` for each task against current section hash
- Identify which specific sections changed
- Group affected tasks by section

**Report format:**
```
[Warning] Spec has changed since tasks were decomposed

Per-section analysis:
  ## Authentication - CHANGED (3 tasks affected)
    - Task 3: Implement login flow
    - Task 4: Password validation
    - Task 7: Session management

  ## API Endpoints - CHANGED (1 task affected)
    - Task 12: Create REST endpoints

  ## Database Schema - unchanged (2 tasks)
  ## Deployment - unchanged (1 task)

Summary:
  Changed sections: 2
  Affected tasks: 4
  Unchanged tasks: 3
```

**New section detection:**
```
[Info] New section detected: ## OAuth Integration
  This section was added after task decomposition.
  Consider creating new tasks for this functionality.
```

**Deleted section detection:**
```
[Warning] Section removed: ## Legacy Support
  2 tasks reference this deleted section:
    - Task 15: Maintain backward compatibility
    - Task 16: Legacy API wrapper
  Consider marking these tasks as out-of-spec or deleting them.
```

**Behavior:**
- Tasks without `spec_fingerprint` field: treated as legacy, no warning
- Tasks without `section_fingerprint` field: fall back to full-spec comparison
- Only warn for projects with 10+ tasks (avoid noise for small projects)

### 11. Section Fingerprint Field Validation

For tasks created after this feature was implemented:

**Check:**
- Tasks with `spec_fingerprint` should also have `section_fingerprint`
- Tasks with `section_fingerprint` should have `section_snapshot_ref`
- Snapshot file in `section_snapshot_ref` should exist

**Report format:**
```
[Warning] 3 tasks missing section-level fingerprints
  - Task 5: has spec_fingerprint but missing section_fingerprint
  - Task 8: has section_fingerprint but missing section_snapshot_ref
  - Task 12: section_snapshot_ref points to missing file
```

**Note:** This is informational only - tasks without section fingerprints work fine using full-spec comparison.

### 12. Out-of-Spec Task Tracking

Reports tasks that were created outside the spec:

**Check:**
- Find all tasks with `"out_of_spec": true`
- List in separate section of report

**Report format:**
```
[Warning] 3 tasks marked out-of-spec
  - Task 15: "Add social login" (not in spec)
  - Task 23: "Custom analytics" (not in spec)
  - Task 31: "Premium features" (not in spec)
```

**Note:** Out-of-spec tasks are valid but won't be verified against spec acceptance criteria.

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

**Workflow Diagram Staleness** (if diagram exists)
- `workflow-diagram.md` timestamp vs latest task modification
- Warns if diagram is > 24 hours older than task changes
- Suggests manually updating the diagram

## Task Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Dashboard doesn't match JSON | Regenerate dashboard.md |
| Dashboard structure invalid | Regenerate dashboard.md |
| Parent missing subtask in array | Add subtask ID to parent's subtasks array |
| Subtask missing parent_task field | Add parent_task field |
| "Broken Down" with empty subtasks | Change status to "Pending" |
| All subtasks Finished but parent not | Set parent status to "Finished" |
| Missing created_date | Add current date |
| Multiple "In Progress" tasks | Ask which to keep, set others to "Pending" |
| Stale workflow diagram | Prompt user to update diagram manually |
| Orphan dependency reference | Remove invalid dependency ID from array |

## Semantic Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Stale "In Progress" (> 7 days) | Ask user: mark Pending, Blocked, or keep In Progress |
| Owner-capability mismatch | Suggest changing owner to "human" (requires confirmation) |
| Stale questions (> 14 days) | List questions, ask user to answer or mark as no longer relevant |
| Stale workspace files (> 30 days) | List files, ask user: graduate to final location, or delete |

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

1. **Move** - Create `.claude/support/reference/{section-slug}.md`, replace with link
2. **Keep** - Mark as explicitly kept
3. **Condense** - Rewrite to fewer lines
4. **Skip** - No changes

## What Belongs Inline

Keep in CLAUDE.md:
- Project overview (2-3 sentences)
- Critical commands (one-liners)
- Key conventions (brief list)
- Navigation pointers

Move to support/reference/:
- Detailed schemas (>8 lines)
- Verbose examples
- Full procedure documentation
- Technology deep-dives

---

## Process

### Step 1: Scan

```
READ all .claude/tasks/task-*.json files
READ .claude/dashboard.md
READ CLAUDE.md
READ all .claude/support/decisions/decision-*.md files
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

Run questions and workspace staleness (always):
- Questions older than 14 days in `.claude/support/questions.md`
- Files older than 30 days in `.claude/support/workspace/`

Run CLAUDE.md audit (if not `--tasks` and not `--decisions`):
- Line counts
- Section sizes
- Code block lengths

Run decision validation (if not `--tasks` and not `--claude-md`):
- Schema validation for each decision file
- Dashboard consistency checks
- Staleness detection
- Completeness verification

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

### Task System - Drift Detection
[Checkmark] Spec fingerprint matches (or no fingerprints tracked)
[Warning] Spec changed since decomposition

Per-section analysis:
  ## Authentication - CHANGED (3 tasks affected)
    - Task 3, Task 4, Task 7
  ## API Endpoints - CHANGED (1 task affected)
    - Task 12
  ## Database Schema - unchanged
  ## Deployment - unchanged

[Info] 1 new section detected
  - ## OAuth Integration (no tasks yet)
[Warning] 1 section removed
  - ## Legacy Support (2 orphaned tasks)

[Warning] 3 tasks marked out-of-spec
  - Task 15: "Add social login"
  - Task 23: "Custom analytics"
  - Task 31: "Premium features"

### Questions & Workspace
[Checkmark] No stale questions
[Warning] 2 workspace files over 30 days old
  - workspace/drafts/api-design.md (45 days)
  - workspace/scratch/notes.md (32 days)

### CLAUDE.md
- Total lines: N [status]
- Sections: N flagged
- Code blocks: N flagged

[List specific issues]

### Decision System
[Checkmark] N decision records found
[Checkmark] Schema validation passed
[Warning] N dashboard inconsistencies
[Warning] N stale decisions
[Warning] N incomplete decisions
[Warning] N missing implementation anchors
  - DEC-003: implemented but no anchors
[Warning] N anchor files not found
  - DEC-007: src/auth/oauth.ts not found

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
         ".claude/support/reference/shared-definitions.md",
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
  [Checkmark] .claude/commands/work.md - matches
  [Warning] .claude/commands/breakdown.md - differs (12 lines changed)
  [Checkmark] .claude/agents/implement-agent.md - matches
  [Warning] .claude/agents/verify-agent.md - differs (new file in template)
  [Checkmark] .claude/support/reference/shared-definitions.md - matches

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
cp /tmp/template/.claude/specification_creator/*.md .claude/specification_creator/
cp /tmp/template/.claude/support/reference/*.md .claude/support/reference/
cp /tmp/template/.claude/support/learnings/README.md .claude/support/learnings/
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

## Part 4: Decision System Validation

Validates the decision documentation system for schema compliance and consistency.

### Validation Checks

#### 1. Decision Record Schema

Each `decision-*.md` file must have valid frontmatter:

**Required fields:**
- `id` - Format: `DEC-NNN` (e.g., DEC-001, DEC-042)
- `title` - Non-empty string
- `status` - One of: `draft`, `proposed`, `approved`, `implemented`, `superseded`
- `category` - One of: `architecture`, `technology`, `process`, `scope`, `methodology`, `vendor`
- `created` - Valid date in YYYY-MM-DD format

**Optional fields:**
- `decided` - Date when decision was finalized
- `related.tasks` - Array of task IDs
- `related.decisions` - Array of decision IDs

#### 2. Dashboard Consistency

**Every decision file must have dashboard entry:**
- Scan `.claude/support/decisions/decision-*.md` files
- Compare against entries in dashboard's "All Decisions" table
- Flag files missing from dashboard

**Every dashboard entry must have file:**
- Parse decision log table in dashboard
- Verify each entry has corresponding `decision-{NNN}-*.md` file
- Flag orphan dashboard entries

**Status match:**
- Status in file frontmatter must match status in dashboard table
- Flag mismatches

#### 3. Staleness Detection

**Draft staleness:**
- Decisions with status `draft` created > 30 days ago
- Warning: "DEC-001 has been in draft for 45 days"

**Proposed staleness:**
- Decisions with status `proposed` created > 14 days ago without resolution
- Warning: "DEC-002 awaiting approval for 21 days"

#### 4. Completeness (for approved/implemented)

Decisions with status `approved` or `implemented` must have:
- Non-empty Decision section (selected option and rationale)
- At least one option in the comparison table (Options Comparison section)

#### 5. Implementation Anchor Validation

Validates that implemented decisions have traceable code anchors:

**Check for `implemented` decisions:**
- Must have non-empty `implementation_anchors` array
- Each anchor file path must exist in the codebase
- Warn if anchor file is missing

**Report format:**
```
[Warning] DEC-003: implemented but missing anchors
[Warning] DEC-007: anchor file not found: src/auth/oauth.ts
```

**Auto-fix options:**
- Remove missing anchor from array
- Mark decision for review
- Suggest reverting status to `approved` if no valid anchors remain

### Decision Report Format

```
### Decision System
[Checkmark] N decision records found
[Checkmark] Schema validation passed
[Warning] 1 dashboard inconsistency
  - DEC-003: missing from dashboard
[Warning] 2 stale decisions
  - DEC-001: draft for 45 days
  - DEC-002: proposed for 21 days
[Warning] 1 incomplete decision
  - DEC-004: approved but missing Decision section
```

### Decision Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| File missing from dashboard | Add entry to dashboard's All Decisions with data from frontmatter |
| Dashboard entry missing file | Remove orphan entry from dashboard |
| Status mismatch | Ask user which is correct, update the other |
| Stale draft (> 30 days) | Ask user: delete, or set reminder |
| Stale proposed (> 14 days) | Ask user: approve, reject, or extend |
| Implemented without anchors | Ask user: add anchors, or revert to approved |
| Anchor file not found | Ask user: update path, remove anchor, or mark for review |

### Non-Fixable Issues (Manual Required)

| Issue | Why Manual |
|-------|------------|
| Invalid frontmatter syntax | Need to examine YAML |
| Invalid status value | Need to determine correct status |
| Invalid category value | Need to determine correct category |
| Invalid ID format | Need to determine correct ID |
| Missing required field | Need human input for value |
| Incomplete approved decision | Need to add Decision section content |

---

## Part 5: Lightweight Health Checks (Continuous)

A subset of checks designed to run automatically after `/work`, `/work complete`, and `/breakdown` commands.

### Purpose

Catch common issues immediately without the overhead of a full health check.

### Checks Performed

| Check | What It Detects |
|-------|-----------------|
| Single "In Progress" rule | More than one task in progress |
| Spec fingerprint comparison | Spec changed since decomposition (full spec level) |
| Section change count | Number of sections that changed (if section fingerprints exist) |
| Orphan dependency detection | References to deleted/missing tasks |
| Out-of-spec count | Number of tasks marked out-of-spec |

### Output Format

**All clear:**
```
Quick check: ✓
```

**Issues found:**
```
Quick check: ⚠️ 2 issues
  - Spec changed: 2 sections modified (4 tasks affected)
  - 3 tasks marked out-of-spec
```

### When Run Automatically

- After `/work` completes (Step 6)
- After `/work complete` (Step 8)
- After `/breakdown` completes

### Comparison to Full Health Check

| Aspect | Lightweight | Full (`/health-check`) |
|--------|-------------|------------------------|
| Execution time | < 1 second | Several seconds |
| Checks | 5 critical checks | All validations |
| Auto-fix | No | Yes (prompts for fixes) |
| Report | Single line + issues | Full report with sections |

---

## Edge Cases

**Empty task list:** Reports "0 tasks - all checks pass" (healthy state for new projects)

**Missing version.json:** Sync check skipped with note: "Create .claude/version.json to enable template sync"

**Missing sync-manifest.json:** Sync check skipped with note: "Create .claude/sync-manifest.json to enable template sync"

**Large CLAUDE.md (>120 lines):** Flags as error, suggests moving sections to reference/

**Subtask ID collisions:** Detects `5_1` already exists before creating duplicate

**< 20 tasks:** Semantic validation (stale tasks, owner mismatch) skipped - only needed for larger projects

**Workflow diagram missing:** If `.claude/support/workflow-diagram.md` doesn't exist, staleness check skipped

**No decision records:** Reports "0 decisions - all checks pass" (healthy state for new projects)

**Malformed frontmatter:** Flags as error, requires manual YAML fix

---

## When to Run

- Start of a work session
- After extensive task operations
- When something feels "off"
- Before major milestones or handoffs
- Periodically (weekly recommended for tasks, monthly for CLAUDE.md)
- **Periodically check for template updates** with `--sync-check`

## Reference

Task schema: `.claude/support/reference/task-schema.md`
Difficulty guide: `.claude/support/reference/shared-definitions.md`
Workflow guide: `.claude/support/reference/workflow.md`
Decision template: `.claude/support/reference/decision-template.md`
Decision guide: `.claude/support/reference/decision-guide.md`
Version info: `.claude/version.json`
Sync manifest: `.claude/sync-manifest.json`
