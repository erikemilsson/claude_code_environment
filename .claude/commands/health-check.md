# Health Check

Combined system health check for tasks, decisions, `.claude/CLAUDE.md`, and template sync.

## Usage
```
/health-check                    # Run all checks, offer fixes
/health-check --report           # Show issues only, no fix prompts
```

## Purpose

Over time, task systems drift from standards, decision records become stale, `.claude/CLAUDE.md` files accumulate bloat, and template workflow files fall behind. This command catches all these issues in one pass.

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

Validate dashboard.md section structure:

**Required sections (exact headings, in this order):**
1. `# Dashboard`
2. `## 🚨 Action Required`
3. `## 📊 Progress`
4. `## 📋 Tasks`
5. `## 📋 Decisions`
6. `## 💡 Notes`

Checks:
- Each heading exists (exact text including emoji)
- Sections in correct order
- Flag missing or out-of-order
- Sections with unchecked toggles (`[ ]`) in the dashboard's section toggle checklist (between `<!-- SECTION TOGGLES -->` and `<!-- END SECTION TOGGLES -->` markers) are allowed to be missing. Falls back to `dashboard_sections` config if no checklist exists.
- Optional section (`## 📑 Sub-Dashboards`) may appear between Decisions and Notes when its toggle is checked — do not flag it as unexpected

### 6. Status Rules

| Status | Rules |
|--------|-------|
| `Pending` | No special requirements |
| `In Progress` | Multiple allowed only when parallel-eligible: `files_affected` don't overlap, all deps satisfied, within `max_parallel_tasks` limit. **ERROR** if parallel conditions violated (overlapping files, unsatisfied deps). |
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
- Tasks should not jump from `"Pending"` to `"Finished"` without passing through `"In Progress"` and `"Awaiting Verification"` (check if `updated_date` differs from `created_date`, or notes contain implementation details)
- Tasks with status `"Awaiting Verification"` for > 1 hour indicate a stalled verification process (ERROR)

**Verify-agent compliance checks:**
- If all spec tasks are `"Finished"`, a `.claude/verification-result.json` file should exist
- The verification result should have `criteria_passed + criteria_failed > 0` (real criteria were checked, not just a summary)
- The `spec_fingerprint` in the result should match the current spec

**Per-task verification compliance checks (ERRORS, not warnings):**
- Finished tasks MUST have a `task_verification` field with `result` of `"pass"` or `"pass_with_issues"`
- `task_verification.checks` should have all 5 keys (`files_exist`, `spec_alignment`, `output_quality`, `integration_ready`, `scope_validation`) with pass/fail values
- If any finished task lacks `task_verification`: **ERROR** — "Verification debt: N finished tasks missing verification"
- If any finished task has `task_verification.result == "fail"`: **ERROR** — "Verification debt: N finished tasks have failed verification"
- If a task was sent back to "In Progress" by verification, notes should contain `[VERIFICATION FAIL #N]` prefix (where N = attempt number from `verification_attempts` field)

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
- Questions in `.claude/support/questions/questions.md` older than 14 days
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
- For parallel batches: check if the batch was dispatched but never completed (all tasks in batch are stale together)

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
| Multiple "In Progress" tasks (parallel-ineligible) | Check parallelism eligibility first — if files overlap or deps unsatisfied, ask which to keep, set others to "Pending". If all parallel conditions are met, no fix needed. |
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

## Part 2: .claude/CLAUDE.md Audit

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

## Process

### Step 1: Scan

```
READ all .claude/tasks/task-*.json files
READ .claude/dashboard.md
READ .claude/spec_v{N}.md (current spec)
READ .claude/drift-deferrals.json (if exists)
READ .claude/CLAUDE.md
READ all .claude/support/decisions/decision-*.md files
READ .claude/version.json (template version info)
READ .claude/sync-manifest.json (file categories)
SCAN .claude/support/previous_specifications/ for archived specs
SCAN for misplaced spec files in non-canonical locations
FETCH template repo (shallow clone for comparison — skip if offline)
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
- Questions older than 14 days in `.claude/support/questions/questions.md`
- Files older than 30 days in `.claude/support/workspace/`

Run `.claude/CLAUDE.md` audit:
- Line counts
- Section sizes
- Code block lengths

Run decision validation:
- Schema validation for each decision file
- Dashboard consistency checks
- Staleness detection
- Completeness verification

Run archive validation:
- Spec version continuity (v1 to v{N-1} all exist in canonical location)
- Misplaced spec file detection (specs in wrong directories)
- Optional: decomposed spec snapshot validation

Run template sync check:
- Compare local version against template repo
- Diff sync-category files
- Report modified/new/local-only files

### Step 3: Report

**Report sections:**
- Task System - Schema & Integrity (checks passed/warnings/errors)
- Task System - Verification Debt (ERROR if any debt exists — blocks completion)
- Task System - Drift Budget (ERROR if exceeded or expired — blocks work)
- Task System - Dashboard Freshness (ERROR if stale — data unreliable)
- Task System - Semantic Validation (stale tasks, owner mismatches, orphan deps)
- Task System - Drift Detection (per-section changes, new/deleted sections, out-of-spec tasks)
- Questions & Workspace (stale questions, old workspace files)
- `.claude/CLAUDE.md` (line counts, flagged sections/code blocks)
- Decision System (schema validation, staleness, completeness, anchors)
- Archive Validation (spec version continuity, misplaced files)
- Template Sync (version comparison, file status, updates available)
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
- `spec_revised` - Boolean, set to `true` after `/iterate` processes an inflection point and user updates spec
- `spec_revised_date` - Date when spec was revised for this decision

#### 2. Dashboard Consistency

**Every decision file must have dashboard entry:**
- Scan `.claude/support/decisions/decision-*.md` files
- Compare against entries in dashboard's "Decisions" table
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

Validates that implemented decisions have traceable anchors:

**Check for `implemented` decisions:**
- Must have non-empty `implementation_anchors` array
- Each anchor file path must exist in the project
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

#### 6. Decision-Task Cross-Reference (Late Decision Detection)

Detects the anti-pattern where a decision record is created *after* related work has already started or completed — meaning tasks were executed without the decision gating them.

**Algorithm:**
```
For each decision-*.md file:
  1. Read related.tasks array (list of task IDs this decision affects)
  2. For each referenced task ID:
     a. Read the task JSON
     b. Check if task has decision's ID in its decision_dependencies array
     c. IF NOT:
        │  This is a cross-reference mismatch.
        │  The decision claims to affect this task, but the task
        │  was created without knowing about the decision.
        │
        │  Check task status:
        │  ├─ "Finished"     → ERROR: work completed without decision
        │  ├─ "In Progress"  → ERROR: work ongoing without decision
        │  ├─ "Pending"      → WARNING: can still be fixed
        │  └─ Other          → WARNING: review needed
```

**Report format (issues found):**
```
[ERROR] Late decision detected — work proceeded without decision gating

  DEC-001 (Analysis Method) references tasks [4, 5, 6]
  But these tasks have no decision_dependencies for DEC-001:

  - Task 4 "Run statistical analysis" — status: Finished ❌
    Work completed before this decision existed. May need rework.
  - Task 5 "Calculate effect sizes" — status: In Progress ⚠️
    Currently being built without decision resolution.
  - Task 6 "Generate summary statistics" — status: Pending ✓
    Can be fixed by adding decision_dependencies.

  Recommendations:
  1. Add decision_dependencies: ["DEC-001"] to tasks 4, 5, 6
  2. Review task 4 — implementation may not match the eventual decision
  3. Pause task 5 until DEC-001 is resolved
```

**Report format (no issues):**
```
[Checkmark] Decision-task cross-references consistent
```

**Why this matters:** This catches the exact failure mode where decisions are created as afterthoughts rather than during spec review. Without this check, work proceeds on unresolved assumptions and must be rebuilt when the decision resolves.

### Decision Report Format

Reports: record count, schema validation, dashboard consistency, staleness (draft >30d, proposed >14d), completeness (approved/implemented need Decision section), anchor validation, and cross-reference consistency.

### Decision Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| File missing from dashboard | Add entry to dashboard's Decisions table with data from frontmatter |
| Dashboard entry missing file | Remove orphan entry from dashboard |
| Status mismatch | Ask user which is correct, update the other |
| Stale draft (> 30 days) | Ask user: delete, or set reminder |
| Stale proposed (> 14 days) | Ask user: approve, reject, or extend |
| Implemented without anchors | Ask user: add anchors, or revert to approved |
| Anchor file not found | Ask user: update path, remove anchor, or mark for review |
| Late decision — task missing dependency (Pending) | Add decision ID to task's `decision_dependencies` array |
| Late decision — task missing dependency (In Progress) | Add dependency, set task back to "Pending" (blocked), notify user |
| Late decision — task missing dependency (Finished) | Add dependency, add note: "Review after {DEC-ID} resolved — may need rework" |

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

## Part 4: Archive Validation

Validates spec archive consistency and detects misplaced archived files.

### Validation Checks

#### 1. Single-Spec Invariant

There must be exactly one `spec_v{N}.md` file in `.claude/`. Multiple spec files indicate a failed or incomplete version transition.

**Algorithm:**
1. Glob for `.claude/spec_v*.md`
2. Count matches

```
IF count == 0:
  → Info: "No spec file found" (valid for new projects)
IF count == 1:
  → ✓ Single-spec invariant holds
IF count > 1:
  → ERROR: "Multiple spec files found: spec_v1.md, spec_v2.md"
  │
  │  This usually means a version transition was interrupted.
  │  The highest version (v{N}) is treated as current.
  │
  │  Auto-fix: Archive lower versions to previous_specifications/
```

#### 2. Spec Version Continuity

Ensures all previous spec versions are properly archived:

**Algorithm:**
1. Scan `.claude/` for current spec file matching `spec_v{N}.md` pattern
2. Extract current version number N
3. For each version from 1 to N-1:
   - Check if `.claude/support/previous_specifications/spec_v{i}.md` exists
   - If missing, report as error

**Report format (issues found):**
```
Archive validation: ⚠️ Issues found
  - Missing: .claude/support/previous_specifications/spec_v2.md
  - Missing: .claude/support/previous_specifications/spec_v4.md
```

**Report format (all clear):**
```
Archive validation: ✓
```

#### 3. Misplaced Spec Files

Detects spec files in non-canonical locations:

**Locations to scan for misplaced files:**
- `.claude/archive/` (incorrect legacy location)
- `.claude/previous_specifications/` (missing `support/` prefix)
- `.archive/` (root archive, not for specs)
- `.claude/specs/` (incorrect plural form)
- Project root (specs should never be here)

**Detection:**
- Find any files matching `spec_v*.md` pattern in above locations
- Report each as "wrong location" with suggested correct path

**Report format:**
```
Archive validation: ⚠️ Issues found
  - Wrong location: .claude/archive/spec_v3.md (should be in support/previous_specifications/)
  - Wrong location: .claude/previous_specifications/spec_v1.md (should be in support/previous_specifications/)
```

#### 4. Decomposed Spec Validation

Optionally checks for decomposed spec snapshots:

**Algorithm:**
1. For each archived spec `spec_v{i}.md` in previous_specifications/
2. If tasks exist that reference spec version i (via `spec_version` field)
3. Check if `spec_v{i}_decomposed.md` exists in previous_specifications/
4. Report missing decomposed files as warnings (not errors)

**Report format:**
```
[Warning] Missing decomposed snapshots:
  - spec_v2_decomposed.md (tasks 5-12 reference v2)
```

### Archive Report Format

**All clear:**
```
### Archive Validation

Archive validation: ✓
  - Spec versions: v1-v4 all archived
  - No misplaced files detected
```

**Issues found:**
```
### Archive Validation

Archive validation: ⚠️ Issues found
  - Missing: .claude/support/previous_specifications/spec_v2.md
  - Wrong location: .claude/archive/spec_v3.md (should be in support/previous_specifications/)
```

### Archive Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Multiple spec files in `.claude/` | Archive lower versions to `previous_specifications/`, keep highest as current |
| Spec in wrong location | Move file to `.claude/support/previous_specifications/` |
| Missing archived spec | Cannot auto-fix (spec content unknown) — warn user |
| Missing decomposed spec | Cannot auto-fix — informational only |

### Non-Fixable Issues (Manual Required)

| Issue | Why Manual |
|-------|------------|
| Missing archived spec | Original content may be lost; user needs to locate or recreate |
| Spec content mismatch | Need to determine which version is authoritative |

---

## Part 5: Template Sync Check

Checks whether the project's workflow files are up to date with the template repository.

### Purpose

Over time, the upstream template may improve commands, agents, and reference docs. This check detects when your project's workflow infrastructure is behind, and suggests updates — all within the health check flow, no separate command needed.

### Requirements

- `.claude/version.json` - Contains `template_repo` and `template_version`
- `.claude/sync-manifest.json` - Lists files in `sync` category
- `gh` CLI installed and authenticated (or GitHub MCP tools)

### Process

#### 1. Gather Information

Read local configuration:
- `.claude/version.json` → `template_repo`, `template_version`
- `.claude/sync-manifest.json` → `categories.sync` file patterns

Check remote version first (lightweight API call):
```bash
gh api repos/{owner}/{repo}/contents/.claude/version.json
```

If remote `template_version` matches local → report up to date, skip file comparison.

If versions differ, fetch files for comparison:
```bash
git clone --depth 1 {template_repo} /tmp/template-check-{timestamp}
```

Cleanup: Remove `/tmp/template-check-{timestamp}` after comparison completes (or on error).

If offline or fetch fails → report as informational, skip remaining template checks.

#### 2. Compare Files

For each file matching a `sync` category pattern:

| Category | Meaning |
|----------|---------|
| **Up to date** | Local matches template |
| **Modified** | Template has changes |
| **New in template** | File added in template, doesn't exist locally |
| **Local only** | File exists locally but not in template |

#### 3. Report

**All current:**
```
### Template Sync

[Checkmark] Template up to date (v1.5.0)
  All 12 sync files match template.
```

**Updates available:**
```
### Template Sync

[Warning] Template updates available (v1.5.0 local → v1.6.0 template)

  Modified in template (3 files):
    .claude/commands/work.md (+15 -8 lines)
    .claude/agents/implement-agent.md (+23 -5 lines)
    .claude/commands/health-check.md (+45 -12 lines)

  New in template (1 file):
    .claude/commands/new-feature.md

  Local only (1 file):
    .claude/commands/my-custom.md (kept — not in template)
```

**Offline:**
```
### Template Sync

[Warning] Cannot reach template repository
  - Check network connection
  - Verify gh CLI: gh auth status
  - Skipping template checks
```

#### 4. Offer Updates (unless `--report`)

If updates are available and not in `--report` mode, offer to apply:

```
[U] Update all modified/new files
[P] Preview diffs first
[S] Select files individually
[K] Keep current (no changes)
```

### Safety Principles

1. **No silent deletions** — Local-only files are never removed without explicit confirmation
2. **Preview before apply** — Shows diffs before making changes
3. **Sync category only** — Never touches `customize` or `ignore` category files
4. **Preserves local additions** — Files not in template are kept
5. **Backup before update** — Creates backup in `.claude/support/workspace/sync-backup-{timestamp}/` (auto-deleted after 7 days)

### Conflict Handling

If a sync file has local modifications that differ from the expected template version:

```
Conflict: .claude/commands/work.md

This file has local changes not in the template.
Updating will overwrite your modifications.

[O] Overwrite with template
[K] Keep local version
[D] Show diff
```

### Post-Update

After applying updates:
```
Updated:
  ✓ .claude/commands/work.md
  ✓ .claude/agents/implement-agent.md

Version: v1.5.0 → v1.6.0

Backup: .claude/support/workspace/sync-backup-20260127-143022/
```

Updates `.claude/version.json` with new `template_version`.

### Template Sync Auto-Fixes

| Issue | Auto-Fix |
|-------|----------|
| Modified files in template | Offer update (with preview/selection) |
| New files in template | Offer to add |
| Missing version.json | Skip with note: "Create .claude/version.json to enable template sync" |
| Missing sync-manifest.json | Skip with note: "Create .claude/sync-manifest.json to enable template sync" |

---

## Part 6: Lightweight Health Checks (Continuous)

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
| Parallel eligibility rule | Multiple "In Progress" with overlapping files or unsatisfied deps | Warning |
| Spec fingerprint comparison | Spec changed since decomposition (full spec level) | Warning |
| Section change count | Number of sections that changed (if section fingerprints exist) | Warning |
| Orphan dependency detection | References to deleted/missing tasks | Warning |
| Out-of-spec count | Number of tasks marked out-of-spec | Info |
| Completion gate integrity | Project/spec marked complete but verification-result.json missing | **CRITICAL** |
| Late decision cross-reference | Decision's `related.tasks` references tasks missing `decision_dependencies` | **ERROR** |
| Single-spec invariant | Multiple `spec_v*.md` files in `.claude/` | **ERROR** |

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
| Checks | 13 fast checks (4 critical, 3 error, 5 warning, 1 info) | All validations (Parts 1–5) |
| Auto-fix | No | Yes (prompts for fixes) |
| Report | Single line + issues | Full report with sections |

---

## Edge Cases

**Empty task list:** Reports "0 tasks - all checks pass" (healthy state for new projects)

**Large `.claude/CLAUDE.md` (>120 lines):** Flags as error, suggests moving sections to reference/

**Subtask ID collisions:** Detects `5_1` already exists before creating duplicate

**< 20 tasks:** Semantic validation (stale tasks, owner mismatch) skipped - only needed for larger projects

**No decision records:** Reports "0 decisions - all checks pass" (healthy state for new projects)

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
