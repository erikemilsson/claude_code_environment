# Health Check

Combined system health check for tasks, decisions, and CLAUDE.md.

## Usage
```
/health-check                    # Run all checks, offer fixes
/health-check --report           # Show issues only, no fix prompts
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

Validates that dashboard.md follows the canonical template defined in `.claude/support/reference/dashboard-patterns.md`.

**Read the Section Definitions table** from dashboard-patterns.md and validate:
- Each required section header exists (exact heading text including emoji)
- Sections appear in the correct order
- Flag missing or out-of-order sections
- Suggest regenerating dashboard.md

**Single source of truth:** The canonical section headings and emojis are defined in `dashboard-patterns.md` only. Both this health check and `/work` dashboard regeneration reference that file. Do not hardcode section names here.

### 6. Status Rules

| Status | Rules |
|--------|-------|
| `Pending` | No special requirements |
| `In Progress` | Only ONE task should have this status at a time |
| `Awaiting Verification` | Transitional only — must proceed to verification immediately. **ERROR** if task has been in this status for > 1 hour |
| `Blocked` | Should have `notes` explaining the blocker |
| `Broken Down` | Must have non-empty `subtasks` array |
| `Finished` | MUST have `task_verification.result` of "pass" or "pass_with_issues". If has subtasks, all subtasks must also be `Finished` |

### 7. Difficulty Range

- Must be integer 1-10
- Tasks with difficulty >= 7 should be `"Broken Down"` or have subtasks
- Subtasks should have difficulty <= 6

### 8. Workflow Compliance

Detects tasks that may have bypassed the implement-agent or verify-agent workflows.

**Implement-agent compliance checks:**
- Tasks with status `"Finished"` should have non-empty `notes` (self-review artifact)
- Tasks should not jump from `"Pending"` to `"Finished"` without evidence of `"In Progress"` transition (check if `updated_date` differs from `created_date`, or notes contain implementation details)

**Verify-agent compliance checks:**
- If all spec tasks are `"Finished"`, a `.claude/verification-result.json` file should exist
- The verification result should have `criteria_passed + criteria_failed > 0` (real criteria were checked, not just a summary)
- The `spec_fingerprint` in the result should match the current spec

**Per-task verification compliance checks (ERRORS, not warnings):**
- Finished tasks MUST have a `task_verification` field with `result` of `"pass"` or `"pass_with_issues"`
- `task_verification.checks` should have all 4 keys (`files_exist`, `spec_alignment`, `code_quality`, `integration_ready`) with pass/fail values
- If any finished task lacks `task_verification`: **ERROR** — "Verification debt: N finished tasks missing verification"
- If any finished task has `task_verification.result == "fail"`: **ERROR** — "Verification debt: N finished tasks have failed verification"
- If a task was sent back to "In Progress" by verification, notes should contain `[VERIFICATION FAIL]` prefix

**Verification debt calculation:**
```
verification_debt = count of tasks where:
  - status == "Finished" AND (
    - task_verification does not exist, OR
    - task_verification.result == "fail", OR
    - task_verification.result not in ["pass", "pass_with_issues"]
  )
```

**Completion gate compliance checks:**
- If dashboard shows "Project Complete" or "100%" completion:
  - `.claude/verification-result.json` MUST exist with `result` of "pass" or "pass_with_issues"
  - ALL finished tasks MUST have `task_verification.result == "pass"`
  - If either condition fails: ERROR — "Project marked complete without verification"
- If spec frontmatter has `status: complete`:
  - Same verification requirements apply
  - If verification is missing: ERROR — "Spec marked complete without verification"
- Check for status mismatch: spec says "active" but dashboard shows "Complete" (or vice versa)

**Report format:**
```
[Warning] Workflow compliance issues
  - 3 finished tasks have empty notes (possible skipped self-review)
  - No verification-result.json found (all tasks finished but no verification run)
```

**Note:** These are warnings, not errors. Some tasks (especially trivial ones) may legitimately have brief notes. The intent is to surface patterns of workflow bypass, not block individual tasks.

### 9. Questions and Workspace Staleness

**Stale Questions:**
- Questions in `.claude/support/questions.md` older than 14 days
- Warning: "N questions have been pending for over 14 days"
- Suggests reviewing and answering or removing outdated questions

**Stale Workspace Files:**
- Files in `.claude/support/workspace/` older than 30 days
- Warning: "N workspace files are over 30 days old"
- Suggests graduating drafts to final locations or deleting scratch files

### 10. Semantic Validation (for 20+ task projects)

These checks detect drift and staleness in large collaborative projects:

### 11. Spec Fingerprint Validation (Granular)

Detects when the specification has changed since tasks were decomposed, with section-level granularity.

**Algorithm:** Uses the same drift detection as `/work` Step 1b. See that section for full implementation details (hash computation, section parsing, comparison logic).

**Report includes:**
- Per-section change status (CHANGED/unchanged)
- Affected tasks grouped by section
- New sections detected (no tasks yet)
- Deleted sections (orphaned tasks)
- Summary counts

**Behavior:**
- Tasks without `spec_fingerprint`: treated as legacy, no warning
- Tasks without `section_fingerprint`: fall back to full-spec comparison
- Only warn for projects with 10+ tasks

### 12. Section Fingerprint Field Validation

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

### 13. Out-of-Spec Task Tracking

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

### 14. Drift Budget Enforcement

Checks for accumulated drift that exceeds configured limits:

**Check:**
1. Read `.claude/drift-deferrals.json` (if exists)
2. Read drift policy from spec frontmatter (defaults: `max_deferred_sections: 3`, `max_deferral_age_days: 14`)
3. Count active deferrals
4. Check for expired deferrals

**Report format (budget exceeded):**
```
[ERROR] Drift Budget Exceeded (BLOCKS WORK)
  - Active deferrals: 4 (max: 3)
  - Sections needing reconciliation:
    - ## Authentication (deferred 2026-01-10, 18 days ago — EXPIRED)
    - ## API Endpoints (deferred 2026-01-20)
    - ## Database (deferred 2026-01-22)
    - ## Deployment (deferred 2026-01-25)

  Must reconcile at least 2 sections before continuing.
  Run /work to start reconciliation.
```

**Report format (within budget):**
```
[Checkmark] Drift budget OK (1 of 3 max deferrals)
```

### 15. Dashboard Staleness Check

Validates that the dashboard is current with task state:

**Check:**
1. Compute current task state hash: `SHA-256(sorted list of task_id + ":" + status)`
2. Read dashboard metadata block (if exists)
3. Compare hashes

**Report format (stale):**
```
[Warning] Dashboard is stale
  - Dashboard task_hash: sha256:abc123...
  - Current task_hash: sha256:def456...
  - Dashboard generated: 2026-01-25 10:30 UTC
  - Tasks modified since: 3

  Dashboard may not reflect current project state.
  Run /work or regenerate manually.
```

**Report format (current):**
```
[Checkmark] Dashboard is current (generated 2026-01-28 14:30 UTC)
```

**Report format (no metadata):**
```
[Warning] Dashboard missing metadata block
  - Cannot verify dashboard freshness
  - Suggest regenerating dashboard via /work
```

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

## Task Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Dashboard doesn't match JSON | Regenerate dashboard.md |
| Dashboard structure invalid | Regenerate dashboard.md |
| Dashboard stale (task_hash mismatch) | Regenerate dashboard.md with fresh metadata |
| Dashboard missing metadata block | Regenerate dashboard.md with metadata |
| Parent missing subtask in array | Add subtask ID to parent's subtasks array |
| Subtask missing parent_task field | Add parent_task field |
| "Broken Down" with empty subtasks | Change status to "Pending" |
| All subtasks Finished but parent not | Set parent status to "Finished" |
| Missing created_date | Add current date |
| Multiple "In Progress" tasks | Ask which to keep, set others to "Pending" |
| Nested `.claude/.claude/` directory | Flag as error, recommend deletion |
| Orphan dependency reference | Remove invalid dependency ID from array |

## Verification & Drift Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Verification debt (missing verification) | Route to /work to trigger verify-agent for affected tasks |
| Verification debt (failed verification) | Route to /work to re-verify after fixes |
| Stale "Awaiting Verification" (> 1 hour) | Trigger verify-agent immediately for task |
| Drift budget exceeded | Present reconciliation UI (REQUIRED before continuing) |
| Expired deferral | Force reconciliation for expired section |

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
READ .claude/spec_v{N}.md (current spec)
READ .claude/drift-deferrals.json (if exists)
READ CLAUDE.md
READ all .claude/support/decisions/decision-*.md files
```

### Step 2: Run Checks

Run critical checks (always, block if failed):
- Verification debt (finished tasks missing verification)
- Drift budget (deferrals exceeding limit or expired)
- Stale "Awaiting Verification" (tasks stuck > 1 hour)
- Dashboard staleness (task_hash mismatch)

Run all checks:
- Schema validation for each task file
- Relationship integrity
- ID uniqueness
- Overview consistency
- Status rules
- Difficulty ranges

Run semantic validation (if task count >= 20):
- Stale "In Progress" detection
- Owner-capability mismatch detection
- Orphan dependency detection
- Workflow diagram staleness check

Run questions and workspace staleness (always):
- Questions older than 14 days in `.claude/support/questions.md`
- Files older than 30 days in `.claude/support/workspace/`

Run CLAUDE.md audit:
- Line counts
- Section sizes
- Code block lengths

Run decision validation:
- Schema validation for each decision file
- Dashboard consistency checks
- Staleness detection
- Completeness verification

### Step 3: Report

**Report sections:**
- Task System - Schema & Integrity (checks passed/warnings/errors)
- Task System - Verification Debt (ERROR if any debt exists — blocks completion)
- Task System - Drift Budget (ERROR if exceeded or expired — blocks work)
- Task System - Dashboard Freshness (ERROR if stale — data unreliable)
- Task System - Semantic Validation (stale tasks, owner mismatches, orphan deps)
- Task System - Drift Detection (per-section changes, new/deleted sections, out-of-spec tasks)
- Questions & Workspace (stale questions, old workspace files)
- CLAUDE.md (line counts, flagged sections/code blocks)
- Decision System (schema validation, staleness, completeness, anchors)
- Summary (overall status: HEALTHY / NEEDS ATTENTION / CRITICAL ISSUES)

**Verification Debt Report Format:**
```
### Task System - Verification Debt

[ERROR] Verification Debt: 3 tasks (BLOCKS COMPLETION)
  - Task 5: "Login flow" — missing task_verification
  - Task 8: "API endpoints" — task_verification.result is "fail"
  - Task 12: "Database schema" — missing task_verification

⚠️ Project cannot complete until verification debt is 0.
   Run /work to trigger verification for these tasks.
```

**If no debt:**
```
### Task System - Verification Debt

[Checkmark] No verification debt (all finished tasks verified)
```

**Drift Budget Report Format:**
```
### Task System - Drift Budget

[ERROR] Drift Budget Exceeded (BLOCKS WORK)
  - Active deferrals: 4 (max: 3)
  - Expired deferrals: 1

  Sections needing reconciliation:
  - ## Authentication (deferred 2026-01-10, 18 days — EXPIRED)
  - ## API Endpoints (deferred 2026-01-20, 8 days)
  - ## Database (deferred 2026-01-22, 6 days)
  - ## Deployment (deferred 2026-01-25, 3 days)

⚠️ Must reconcile at least 2 sections before continuing.
   Run /work to start reconciliation.
```

**If within budget:**
```
### Task System - Drift Budget

[Checkmark] Drift budget OK (1 of 3 max deferrals)
```

**Dashboard Freshness Report Format:**
```
### Task System - Dashboard Freshness

[ERROR] Dashboard is stale
  - Dashboard task_hash: sha256:abc123...
  - Current task_hash:   sha256:def456...
  - Dashboard generated: 2026-01-25 10:30 UTC
  - Tasks modified since: 3

⚠️ Dashboard may not reflect current project state.
   Auto-fix: Regenerate dashboard
```

**If current:**
```
### Task System - Dashboard Freshness

[Checkmark] Dashboard current (generated 2026-01-28 14:30 UTC, hash matches)
```

Each section uses `[Checkmark]` for passes, `[Warning]` for issues, `[Error]` for blockers.

### Step 4: Offer Fixes

For each fixable issue, present options and apply immediately before moving to next.

If `--report` flag is set, skip this step and show report only.

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

Reports: record count, schema validation, dashboard consistency, staleness (draft >30d, proposed >14d), completeness (approved/implemented need Decision section), and anchor validation.

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

## Part 4: Lightweight Health Checks (Continuous)

A subset of checks designed to run automatically after `/work`, `/work complete`, and `/breakdown` commands.

### Purpose

Catch common issues immediately without the overhead of a full health check.

### Checks Performed

| Check | What It Detects | Severity |
|-------|-----------------|----------|
| Verification debt | Finished tasks missing verification or with failed verification | **CRITICAL** |
| Drift budget exceeded | More deferrals than allowed, or expired deferrals | **CRITICAL** |
| Stale "Awaiting Verification" | Task stuck in Awaiting Verification for > 1 hour | **CRITICAL** |
| Dashboard staleness | Dashboard task_hash doesn't match current state | **ERROR** |
| Workflow compliance | Task jumped Pending→Finished without In Progress; empty notes | Warning |
| Single "In Progress" rule | More than one task in progress | Warning |
| Spec fingerprint comparison | Spec changed since decomposition (full spec level) | Warning |
| Section change count | Number of sections that changed (if section fingerprints exist) | Warning |
| Orphan dependency detection | References to deleted/missing tasks | Warning |
| Out-of-spec count | Number of tasks marked out-of-spec | Info |
| Completion gate integrity | Project/spec marked complete but verification-result.json missing | **CRITICAL** |

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

**Critical issues (block work):**
```
Quick check: ❌ CRITICAL
  - Verification debt: 2 tasks (tasks 16, 17)
  - Drift budget exceeded: 4 deferrals (max 3)
  - Task 5 stuck in "Awaiting Verification" (> 1 hour)
  - Dashboard stale (task_hash mismatch)
```

**Blocking issues (block completion):**
```
Quick check: ❌ BLOCKS COMPLETION
  - Project shows "Complete" but verification-result.json missing
  - Spec marked complete but 3 tasks have verification debt
```

### When Run Automatically

- After `/work` completes (Step 6)
- After `/work complete` (Step 8)
- After `/breakdown` completes

### Comparison to Full Health Check

| Aspect | Lightweight | Full (`/health-check`) |
|--------|-------------|------------------------|
| Execution time | < 1 second | Several seconds |
| Checks | 6 critical checks | All validations |
| Auto-fix | No | Yes (prompts for fixes) |
| Report | Single line + issues | Full report with sections |

---

## Edge Cases

**Empty task list:** Reports "0 tasks - all checks pass" (healthy state for new projects)

**Large CLAUDE.md (>120 lines):** Flags as error, suggests moving sections to reference/

**Subtask ID collisions:** Detects `5_1` already exists before creating duplicate

**< 20 tasks:** Semantic validation (stale tasks, owner mismatch) skipped - only needed for larger projects

**No decision records:** Reports "0 decisions - all checks pass" (healthy state for new projects)

**Malformed frontmatter:** Flags as error, requires manual YAML fix

---

## When to Run

- Start of a work session
- After extensive task operations
- When something feels "off"
- Before major handoffs
- Periodically (weekly recommended for tasks, monthly for CLAUDE.md)
- **For template updates**, use `/update-template`

## Reference

Task schema: `.claude/support/reference/task-schema.md`
Difficulty guide: `.claude/support/reference/shared-definitions.md`
Workflow guide: `.claude/support/reference/workflow.md`
Decision template: `.claude/support/reference/decision-template.md`
Decision guide: `.claude/support/reference/decision-guide.md`
Template sync: `/update-template`
