# Health Check

Combined system health check for tasks, decisions, `.claude/CLAUDE.md`, and template sync.

## Usage
```
/health-check                    # Run all checks, offer fixes
/health-check --report           # Show issues only, no fix prompts
```

## Purpose

Over time, task systems drift from standards, decision records become stale, `.claude/CLAUDE.md` files accumulate bloat, and template workflow files fall behind. This command catches all these issues in one pass.

This is a manual maintenance tool. It does not run automatically during `/work` — operational checks that `/work` needs are defined inline in `work.md`.

---

## Part 1: Task System Validation

Detects and fixes drift from task management standards.

### Validation Checks

#### 1. Task JSON Schema Validation

Validates required fields (id, title, status, difficulty) and optional fields per `.claude/support/reference/task-schema.md`.

**Migration detection:** When non-conforming schemas are found (missing required fields, unknown status values, unexpected fields), provide migration guidance:
- Suggest field mappings (e.g., `"done"` → `"Finished"`, `"assignee"` → `"owner"`)
- List specific remediation steps per task
- Never auto-migrate — report issues and let the user decide

#### 2. Relationship Integrity

**Parent-subtask consistency:**
- If task has `parent_task`, parent must exist and list this task in `subtasks`
- If task has `subtasks`, each subtask must exist and reference this task as `parent_task`
- `"Broken Down"` status requires non-empty `subtasks` array
- Subtasks should not have `"Broken Down"` as status (only top-level)

**Dependency validity:**
- All task IDs in `dependencies` array must exist
- No circular dependencies

#### 3. ID Safety (Breakdown Protection)

When breaking down tasks, IDs must not collide:
- Subtask IDs use format `{parent_id}_{n}` (e.g., `5_1`, `5_2`, `5_3`)
- Check for ID uniqueness across all task files
- Verify no orphaned task files exist

#### 4. Dashboard Consistency

**Row matching:**
- Every task JSON has a corresponding row in dashboard
- Every row in dashboard has a corresponding task JSON
- Status, title, and difficulty match between JSON and dashboard
- Summary count is accurate

**Structure validation:**
- Required sections exist: `# Dashboard`, `## 🚨 Action Required`, `## 📊 Progress`, `## 📋 Tasks`, `## 📋 Decisions`, `## 💡 Notes`
- Sections in correct order
- Sections with unchecked toggles in the section toggle checklist are allowed to be missing
- Optional section (`## 👁️ Custom Views`) may appear between Decisions and Notes when toggled on

If dashboard content or structure is inconsistent, the fix is always: regenerate.

#### 4b. Dashboard State Sidecar

- `.claude/dashboard-state.json` should exist if dashboard.md exists
- If missing: WARNING — "Dashboard state sidecar missing. Next dashboard regeneration will create it."
- If present: validate JSON structure (required keys: user_notes, section_toggles, phase_gates, inline_feedback, custom_views_instructions, updated)
- Cross-reference: section_toggles should match the dashboard's SECTION TOGGLES checklist
- Cross-reference: phase_gates entries should match PHASE GATE markers in dashboard

#### 5. Status Rules

| Status | Rules |
|--------|-------|
| `Pending` | No special requirements |
| `In Progress` | Multiple allowed only when parallel-eligible: `files_affected` don't overlap, all deps satisfied, within `max_parallel_tasks` limit. **ERROR** if parallel conditions violated. |
| `Awaiting Verification` | Transitional only — must proceed to verification immediately. Auto-recovered by `/work` Step 0. |
| `Blocked` | Should have `notes` explaining the blocker |
| `On Hold` | Should have `notes` explaining why paused. Not auto-routed by `/work`. Warning if on hold > 30 days. |
| `Absorbed` | Must have `absorbed_into` field referencing a valid task ID that exists. |
| `Broken Down` | Must have non-empty `subtasks` array |
| `Finished` | MUST have `task_verification.result` of "pass" or "pass_with_issues". If has subtasks, all subtasks must also be `Finished` |

#### 6. Difficulty Range

- Must be integer 1-10
- Tasks with difficulty >= 7 should be `"Broken Down"` or have subtasks
- Subtasks should have difficulty <= 6

#### 7. Workflow Compliance

Detects tasks that may have bypassed the implement-agent or verify-agent workflows.

**Verification debt (ERRORS):**
- Finished tasks MUST have a `task_verification` field with `result` of `"pass"` or `"pass_with_issues"`
- `task_verification.checks` should have all 5 keys (`files_exist`, `spec_alignment`, `output_quality`, `integration_ready`, `scope_validation`) with pass/fail values
- If any finished task lacks `task_verification`: **ERROR** — "Verification debt: N finished tasks missing verification"
- If any finished task has `task_verification.result == "fail"`: **ERROR**

**Verification debt calculation:**
```
verification_debt = count of tasks where:
  - status == "Finished" AND (
    - task_verification does not exist, OR
    - task_verification.result == "fail", OR
    - task_verification.result not in ["pass", "pass_with_issues"]
  )
```

**Workflow bypass detection (warnings):**
- Finished tasks with empty `notes` (possible skipped self-review)
- Tasks that appear to have jumped from `"Pending"` to `"Finished"` without passing through `"In Progress"` and `"Awaiting Verification"`

**Completion gate checks (ERRORS):**
- If dashboard shows "Project Complete" or "100%" completion:
  - `.claude/verification-result.json` MUST exist with `result` of "pass" or "pass_with_issues"
  - ALL finished tasks MUST have passing `task_verification`
  - If either condition fails: ERROR — "Project marked complete without verification"
- Check for status mismatch: spec says "active" but dashboard shows "Complete" (or vice versa)

**Note:** Workflow bypass warnings are informational. Some tasks may legitimately have brief notes. The intent is to surface patterns, not block individual tasks.

#### 8. Questions and Workspace Staleness

**Stale Questions:**
- Questions in `.claude/support/questions/questions.md` older than 14 days
- Warning: "N questions have been pending for over 14 days"

**Stale Workspace Files:**
- Files in `.claude/support/workspace/` older than 30 days
- Warning: "N workspace files are over 30 days old"

#### 9. Out-of-Spec Task Tracking

Reports tasks with `"out_of_spec": true` in a separate section of the report. Informational — out-of-spec tasks are valid but won't be verified against spec acceptance criteria.

#### 10. Dashboard Staleness

**Task state hash check:**
1. Compute: `SHA-256(sorted list of task_id + ":" + status)`
2. Read dashboard metadata block (if exists)
3. Compare hashes — if different, dashboard is stale

**Stale "In Progress" tasks:**
- Tasks with status `"In Progress"` where `updated_date` (or `created_date`) is > 7 days old
- Indicates abandoned work or forgotten state updates

### Task Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Dashboard inconsistent or structurally invalid | Regenerate dashboard.md |
| Dashboard stale (hash mismatch or missing metadata) | Regenerate dashboard.md with fresh metadata |
| Parent missing subtask in array | Add subtask ID to parent's subtasks array |
| Subtask missing parent_task field | Add parent_task field |
| "Broken Down" with empty subtasks | Change status to "Pending" |
| All subtasks Finished or Absorbed but parent not | Set parent status to "Finished" |
| Missing created_date | Add current date |
| Multiple "In Progress" (parallel-ineligible) | Check eligibility — if files overlap or deps unsatisfied, ask which to keep |
| Nested `.claude/.claude/` directory | Flag as error, recommend deletion |
| Orphan dependency reference | Remove invalid dependency ID from array |
| Stale "In Progress" (> 7 days) | Ask user: mark Pending, On Hold, Blocked, or keep |
| Stale "On Hold" (> 30 days) | Ask user: resume, absorb, or keep |
| Absorbed without `absorbed_into` | Ask user: provide absorbing task ID, or change status |
| Stale questions (> 14 days) | List questions, ask user to answer or remove |
| Stale workspace files (> 30 days) | List files, ask user: graduate to final location, or delete |
| Dashboard state sidecar missing | Create from current dashboard markers (or defaults if markers broken) |
| Sidecar/dashboard toggle mismatch | Update sidecar from dashboard markers (dashboard is more recent) |
| Stale "Awaiting Verification" (> 1 hour) | Auto-recovered by `/work` Step 0 on next run. If running standalone: trigger verify-agent immediately for task |

### Non-Fixable Issues (Manual Required)

| Issue | Why Manual |
|-------|------------|
| Missing required field (id, title, status, difficulty) | Need human input for values |
| Invalid JSON syntax | Need to examine file |
| Circular dependencies | Need to understand intent |
| Duplicate task IDs | Need to decide which to keep |
| Unknown status value | Need to determine correct status (valid: Pending, In Progress, Awaiting Verification, Blocked, On Hold, Absorbed, Broken Down, Finished) |

---

## Part 2: .claude/CLAUDE.md Audit

Detects bloat and offers guided cleanup.

### Thresholds

| Metric | Warning | Error |
|--------|---------|-------|
| Total lines | 80 | 120 |
| Section lines | 15 | 25 |
| Code blocks | 10 | 20 |
| Inline schemas | 8 | Always flag |

### Audit Checks

1. **Total lines** - Compare against thresholds
2. **Section sizes** - Check each ## section for line count
3. **Code blocks** - Check each code block for length
4. **Inline schemas** - Flag JSON schemas >8 lines

### Fix Options (per issue)

1. **Move** - Create `.claude/support/reference/{section-slug}.md`, replace with link
2. **Keep** - Mark as explicitly kept
3. **Condense** - Rewrite to fewer lines
4. **Skip** - No changes

### What Belongs Inline

Keep in `.claude/CLAUDE.md`:
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

## Part 3: Decision System Validation

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
- `spec_revised` - Boolean, set after `/iterate` processes an inflection point
- `spec_revised_date` - Date when spec was revised

#### 2. Dashboard Consistency

- Every decision file has a corresponding entry in the dashboard's Decisions table
- Every dashboard entry has a corresponding `decision-{NNN}-*.md` file
- Status in file frontmatter matches status in dashboard table

#### 3. Staleness Detection

- Decisions with status `draft` created > 30 days ago
- Decisions with status `proposed` created > 14 days ago without resolution

#### 4. Completeness (for approved/implemented)

Decisions with status `approved` or `implemented` must have:
- Non-empty Decision section (selected option and rationale)
- At least one option in the comparison table

#### 5. Implementation Anchor Validation

For decisions with status `implemented`:
- Must have non-empty `implementation_anchors` array
- Each anchor file path must exist in the project
- Report missing anchors as warnings

#### 6. Decision-Task Cross-Reference

Reports mismatches between decision `related.tasks` and task `decision_dependencies`:
- For each decision, check if referenced tasks have the decision ID in their `decision_dependencies`
- Report mismatches grouped by task status (Finished = most concerning, Pending = auto-fixable)

This is a reporting check. The primary enforcement and interactive resolution happens in `/work` Step 2b.

### Decision Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| File missing from dashboard | Add entry to dashboard's Decisions table |
| Dashboard entry missing file | Remove orphan entry from dashboard |
| Status mismatch | Ask user which is correct, update the other |
| Stale draft (> 30 days) | Ask user: delete, or set reminder |
| Stale proposed (> 14 days) | Ask user: approve, reject, or extend |
| Implemented without anchors | Ask user: add anchors, or revert to approved |
| Anchor file not found | Report for manual review |
| Cross-reference mismatch (Pending task) | Add decision ID to task's `decision_dependencies` |
| Cross-reference mismatch (other status) | Report for manual review |

### Non-Fixable Issues (Manual Required)

| Issue | Why Manual |
|-------|------------|
| Invalid frontmatter syntax | Need to examine YAML |
| Invalid status/category/ID value | Need to determine correct value |
| Missing required field | Need human input |
| Incomplete approved decision | Need Decision section content |

---

## Part 4: Archive Validation

Validates spec archive consistency and detects misplaced files.

### Validation Checks

#### 1. Single-Spec Invariant

There must be exactly one `spec_v{N}.md` file in `.claude/`. Multiple spec files indicate a failed or incomplete version transition.

```
IF count == 0 → Info: "No spec file found" (valid for new projects)
IF count == 1 → ✓ Single-spec invariant holds
IF count > 1  → ERROR: "Multiple spec files found"
               Auto-fix: Archive lower versions to previous_specifications/
```

#### 2. Spec Version Continuity

For each version from 1 to N-1, check that `.claude/support/previous_specifications/spec_v{i}.md` exists.

#### 3. Misplaced Spec Files

Scan non-canonical locations for `spec_v*.md` files:
- `.claude/archive/`, `.claude/previous_specifications/`, `.archive/`, `.claude/specs/`, project root
- Report each with suggested correct path

#### 4. Decomposed Spec Validation

For archived specs where tasks reference that version, check if `spec_v{i}_decomposed.md` exists. Warning-level only.

### Archive Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Multiple spec files in `.claude/` | Archive lower versions, keep highest as current |
| Spec in wrong location | Move to `.claude/support/previous_specifications/` |
| Missing archived spec | Cannot auto-fix — warn user |
| Missing decomposed spec | Informational only |

---

## Part 5: Template Sync Check

Checks whether the project's `.claude/` workflow files are up to date with the template repository.

### Purpose

The upstream template may improve commands, agents, and reference docs. This check compares your project's `.claude/` files against the template repo and suggests updates.

### Requirements

- `.claude/version.json` — contains `template_repo` and `template_version`
- `.claude/sync-manifest.json` — defines `sync` (updatable) vs `customize` (user-owned) file categories
- `gh` CLI installed and authenticated

### Process

#### 1. Check for Updates

Read local `.claude/version.json` for `template_repo` and `template_version`.

Check remote version:
```bash
gh api repos/{owner}/{repo}/contents/.claude/version.json
```

If remote `template_version` matches local → report up to date, done.

If versions differ → fetch the `.claude/` folder contents for comparison.

If offline or fetch fails → report as informational, skip remaining checks.

#### 2. Compare Files

Only compare files matching `sync` category patterns in `sync-manifest.json`. Never touch `customize` or `ignore` category files.

For each sync file, determine status:
- **Up to date** — local matches template
- **Modified** — template has changes
- **New in template** — doesn't exist locally
- **Local only** — exists locally but not in template (kept, never flagged)

#### 3. Present Changes

**Small changes** (single-file edits, minor updates) — present as a simple list:

```
Template updates available (v1.5.0 → v1.6.0):

  Modified:
    .claude/commands/work.md (+15 -8 lines)
    .claude/support/reference/paths.md (+3 -1 lines)

  New:
    .claude/support/reference/new-feature.md

Apply these changes? [Y/N]
```

**Bigger changes** (structural changes, multi-file updates) — aggregate related changes and explain impact:

```
Template updates available (v1.5.0 → v1.6.0):

1. Verification workflow update (3 files)
   - .claude/commands/work.md — new verification step
   - .claude/agents/verify-agent.md — updated check criteria
   - .claude/support/reference/workflow.md — updated process docs

   Impact: Adds scope validation to the verification process.
   Tasks in "Awaiting Verification" would use the new criteria.

2. New reference file
   - .claude/support/reference/new-feature.md

   Impact: Documentation only. No effect on existing workflow.

Apply all / Select individually / Skip?
```

**Grouping heuristic:** Changes are "related" when they touch the same workflow area (e.g., multiple files in the verification pipeline, or a command and its referenced reference doc).

#### 4. Apply Updates

For accepted changes:
- Update the local files
- Update `template_version` in `.claude/version.json`
- Report what was changed

### Key Rules

- **Sync category only** — never touch `customize` or `ignore` category files
- **Local-only files are kept** — never suggest removing files that aren't in the template
- **No silent changes** — always present changes and get confirmation before applying

### Report Format

**Up to date:**
```
### Template Sync

✓ Template up to date (v1.5.0)
```

**Offline:**
```
### Template Sync

⚠️ Cannot reach template repository — skipping template checks
```

**Missing config:**
```
### Template Sync

ℹ️ Template sync not configured (missing version.json or sync-manifest.json)
```

---

## Part 5b: Command Collision Detection

Detects when custom commands in `.claude/commands/` overlap with template commands.

### Process

1. **Identify template commands** — known set: `work.md`, `iterate.md`, `breakdown.md`, `health-check.md`, `status.md`
2. **Scan `.claude/commands/`** for all `.md` files not in the template set
3. **Detect collisions:**
   - **Name collision:** custom file has same name as template command
   - **Functional overlap:** filename or content suggests overlap (e.g., `plan.md` → `/iterate`, `complete.md` → `/work complete`)
4. **Report** — list custom commands with any overlap warnings

Never delete or rename custom commands without user consent.

---

## Part 5c: Settings Conflict Detection

Checks for existing user settings files and confirms the template doesn't interfere.

### Process

1. Check for `.claude/settings.local.json` and `.claude/settings.json`
2. If found: report presence, confirm template doesn't ship settings files, note any restrictions that might affect agent workflows (e.g., restricted `Bash` may prevent test execution)
3. If not found: report as informational

---

## Process

### Step 1: Scan

```
READ all .claude/tasks/task-*.json files
READ .claude/dashboard.md
READ .claude/spec_v{N}.md (current spec — for completion gate checks)
READ .claude/CLAUDE.md
READ all .claude/support/decisions/decision-*.md files
READ .claude/version.json (template version info)
READ .claude/sync-manifest.json (file categories)
SCAN .claude/support/previous_specifications/ for archived specs
SCAN .claude/support/questions/questions.md for stale questions
SCAN .claude/support/workspace/ for stale files
SCAN for misplaced spec files in non-canonical locations
CHECK template repo for updates (skip if offline)
```

### Step 2: Run Checks

- Part 1: Task system validation (checks 1-10)
- Part 2: `.claude/CLAUDE.md` audit
- Part 3: Decision system validation (checks 1-6)
- Part 4: Archive validation (checks 1-4)
- Part 5: Template sync + collision + settings checks

### Step 3: Report

**Report sections:**
- Task System — Schema & Integrity (checks 1-6)
- Task System — Verification Debt (check 7)
- Task System — Dashboard Freshness (check 10)
- Task System — Out-of-Spec Tasks (check 9, if any exist)
- Questions & Workspace (check 8)
- `.claude/CLAUDE.md` Audit (Part 2)
- Decision System (Part 3)
- Archive Validation (Part 4)
- Template Sync (Part 5)
- Command & Settings (Parts 5b, 5c)
- Summary (overall status: HEALTHY / NEEDS ATTENTION / CRITICAL ISSUES)

Each section uses `✓` for passes, `⚠️` for warnings, `❌` for errors.

### Step 4: Offer Fixes

For each fixable issue, present options and apply immediately before moving to next.

If `--report` flag is set, skip this step and show report only.

---

## Edge Cases

**Empty task list:** Reports "0 tasks — all checks pass" (healthy state for new projects)

**Large `.claude/CLAUDE.md` (>120 lines):** Flags as error, suggests moving sections to reference/

**Subtask ID collisions:** Detects `5_1` already exists before creating duplicate

**No decision records:** Reports "0 decisions — all checks pass" (healthy state for new projects)

**Malformed frontmatter:** Flags as error, requires manual YAML fix

**Missing version.json or sync-manifest.json:** Template sync skipped with informational note

**Template repo unreachable:** Template sync skipped gracefully, other checks still run

---

## When to Run

- Start of a work session
- After extensive task operations
- When something feels "off"
- Before major handoffs
- Periodically (weekly recommended for tasks and template sync, monthly for `.claude/CLAUDE.md`)

## Reference

Task schema: `.claude/support/reference/task-schema.md`
Difficulty guide: `.claude/support/reference/shared-definitions.md`
Workflow guide: `.claude/support/reference/workflow.md`
Decisions reference: `.claude/support/reference/decisions.md`
Template config: `.claude/version.json`, `.claude/sync-manifest.json`
