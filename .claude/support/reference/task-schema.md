# Task Schema

## Minimal Task

```json
{
  "id": "1",
  "title": "Brief description",
  "status": "Pending",
  "difficulty": 3
}
```

## Full Task

```json
{
  "id": "1",
  "title": "Brief description",
  "description": "Detailed explanation of what needs to be done",
  "status": "Pending",
  "difficulty": 3,
  "owner": "claude",
  "priority": "medium",
  "due_date": "2026-02-15",
  "estimated_hours": 4,
  "created_date": "2026-01-15",
  "updated_date": "2026-01-15",
  "completion_date": null,
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "files_affected": [],
  "external_dependency": null,
  "phase": "1",
  "decision_dependencies": [],
  "notes": "",
  "user_feedback": "",
  "spec_fingerprint": "sha256:a1b2c3d4...",
  "spec_version": "spec_v1",
  "spec_section": "## Authentication",
  "section_fingerprint": "sha256:e5f6g7h8...",
  "section_snapshot_ref": "spec_v1_decomposed.md",
  "verification_attempts": 1,
  "task_verification": {
    "result": "pass",
    "timestamp": "2026-01-28T15:30:00Z",
    "checks": {
      "files_exist": "pass",
      "spec_alignment": "pass",
      "output_quality": "pass",
      "integration_ready": "pass",
      "scope_validation": "pass"
    },
    "issues": [],
    "notes": "All files created as specified."
  }
}
```

## Field Definitions

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| id | String | Number for top-level ("1"), underscore for subtasks ("1_1") |
| title | String | Brief description of what needs to be done |
| status | String | Pending, In Progress, Awaiting Verification, Blocked, On Hold, Absorbed, Broken Down, Finished |
| difficulty | Number | 1-10 scale (see shared-definitions.md) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| description | String | Detailed explanation when title isn't enough |
| owner | String | claude (default), human, or both - see Owner Values below |
| priority | String | low, medium (default), high, critical - see Priority Values below |
| due_date | String | YYYY-MM-DD deadline for the task |
| estimated_hours | Number | Rough planning estimate in hours |
| created_date | String | YYYY-MM-DD format |
| updated_date | String | YYYY-MM-DD format |
| completion_date | String | YYYY-MM-DD format, set when Finished |
| dependencies | Array | Task IDs that must finish first |
| subtasks | Array | Task IDs (only when Broken Down) |
| parent_task | String | Parent task ID if this is a subtask |
| files_affected | Array | File paths this task will modify |
| external_dependency | Object | External blocker - see External Dependencies below |
| notes | String | Context, warnings, or completion notes |
| user_feedback | String | Feedback provided by the user via dashboard inline areas or during /work complete |
| spec_fingerprint | String | SHA-256 hash of spec at task decomposition (drift detection) |
| spec_version | String | Spec filename when task was created (e.g., "spec_v1") |
| spec_section | String | Originating section heading from spec |
| section_fingerprint | String | SHA-256 hash of the specific section content at decomposition |
| section_snapshot_ref | String | Reference to snapshot file for generating diffs (e.g., "spec_v1_decomposed.md") |
| out_of_spec | Boolean | Task not aligned with spec (user chose "proceed anyway") |
| absorbed_into | String | Task ID this task was absorbed into (required when status is "Absorbed") |
| phase | String | Phase this task belongs to (e.g., "1" or "Data Pipeline"). Tasks in Phase N+1 are blocked until all Phase N tasks complete. |
| decision_dependencies | Array | Decision IDs that block this task (e.g., ["DEC-002"]). Task remains blocked until all referenced decisions are resolved. |
| parallel_safe | Boolean | When true, task is eligible for parallel execution even with empty `files_affected`. Use for research/analysis tasks with no file side effects. |
| conflict_note | String | **Transient.** Set during parallel dispatch when a task is held back due to file conflicts (e.g., `"Held: file conflict with Task 3 on src/models.py"`). Cleared when the task is dispatched or during post-parallel cleanup. Surfaced in the dashboard Status column. |
| verification_attempts | Number | Count of per-task verification attempts (incremented by verify-agent on each run). Escalates to human review at >= 3 (initial + 2 retries). Default: 0 (omit until first verification). |
| task_verification | Object | Per-task verification result recorded by verify-agent |

## Owner Values

The `owner` field determines who is responsible and where tasks appear in the dashboard:

| Value | Emoji | Dashboard Location | When to Use |
|-------|-------|-------------------|-------------|
| `claude` | 🤖 | Tasks section | Tasks Claude can do autonomously (default) |
| `human` | ❗ | Action Required → Your Tasks | Requires human action (config, decisions, external) |
| `both` | 👥 | Action Required + Tasks | Collaborative work (appears in both sections) |

### Examples by Owner

**`claude`** (default - omit field if this):
- Implement features, create deliverables
- Research, analysis, comparisons
- Create tests, documentation
- Refactor, fix issues

**`human`**:
- Configure API keys, secrets
- Make business decisions
- External actions (deploy, purchase, contact)
- Review and approve

**`both`**:
- Design work (human provides direction, Claude implements)
- Content requiring human judgment (Claude drafts, human refines)

## Priority Values

| Value | Emoji | Meaning |
|-------|-------|---------|
| critical | 🔴 | Blocking other work, immediate attention required |
| high | 🟠 | Important, should be done soon |
| medium | (none) | Normal priority (default when omitted) |
| low | (none) | Nice to have, do when time permits |

Priority affects display order in Ready sections - critical tasks appear first.
Only critical and high show emoji prefixes in the dashboard to reduce visual noise.

## Drift Prevention Fields

These fields track spec-to-task alignment and detect when specs evolve after tasks are created:

### spec_fingerprint

SHA-256 hash of the spec file content when tasks were decomposed:

```json
{
  "spec_fingerprint": "sha256:a1b2c3d4..."
}
```

When `/work` runs, it compares the current spec hash against task fingerprints. If different, the spec has changed since decomposition.

### spec_version and spec_section

Track which spec and section a task originated from:

```json
{
  "spec_version": "spec_v1",
  "spec_section": "## Authentication"
}
```

Enables tracking which tasks need review when specific sections change.

### section_fingerprint and section_snapshot_ref

Enable granular per-section drift detection:

```json
{
  "section_fingerprint": "sha256:abc123...",
  "section_snapshot_ref": "spec_v1_decomposed.md"
}
```

| Field | Purpose |
|-------|---------|
| `section_fingerprint` | SHA-256 hash of the specific section content at decomposition time. Allows detecting changes to individual sections without triggering alerts for unrelated changes. |
| `section_snapshot_ref` | Reference to the snapshot file in `.claude/support/previous_specifications/`. Used to generate diffs showing exactly what changed in a section. |

**How it works:**
1. When tasks are decomposed from spec, each task's originating section is hashed
2. The full spec is saved as a snapshot (e.g., `spec_v1_decomposed.md`)
3. When `/work` runs, it compares current section fingerprints against task fingerprints
4. Only tasks from changed sections are flagged for review

This provides more targeted drift detection than full-spec fingerprinting alone.

### out_of_spec

Marks tasks that don't align with the spec but were created anyway:

```json
{
  "out_of_spec": true
}
```

Set when user selects "proceed anyway" on spec misalignment. Dashboard shows ⚠️ prefix for these tasks. Health check reports them separately.

## Task Verification Field

Per-task verification result recorded by verify-agent when a task is in "Awaiting Verification" status. Upon passing, the task status transitions to "Finished". This enables Tier 1 (per-task) verification in the two-tier verification system.

```json
{
  "task_verification": {
    "result": "pass",
    "timestamp": "2026-01-28T15:30:00Z",
    "checks": {
      "files_exist": "pass",
      "spec_alignment": "pass",
      "output_quality": "pass",
      "integration_ready": "pass",
      "scope_validation": "pass"
    },
    "issues": [],
    "notes": "All files created as specified."
  }
}
```

### Sub-fields

| Sub-field | Type | Values | Description |
|-----------|------|--------|-------------|
| `result` | String | `"pass"`, `"fail"`, `"pass_with_issues"` | Overall per-task verification outcome |
| `timestamp` | String | ISO 8601 | When verification completed |
| `checks` | Object | Keys: `files_exist`, `spec_alignment`, `output_quality`, `integration_ready`, `scope_validation` | Per-check pass/fail |
| `checks.*` | String | `"pass"` or `"fail"` | Individual check result |
| `issues` | Array | Issue objects `{severity, description}` | Issues found during verification |
| `notes` | String | Free text | Brief summary of verification |

### State Detection

A task "needs per-task verification" when:
- It has status "Awaiting Verification", OR
- It has status "Finished" AND does NOT have a `task_verification` field (legacy edge case)

### Failure Handling

When per-task verification fails:
- `verification_attempts` is incremented (verify-agent increments this before writing the result)
- Task status is set back to "In Progress"
- Verification failure notes are prepended with `[VERIFICATION FAIL #{N}]` in the task `notes` field (where N = current attempt count)
- `completion_date` is cleared
- `updated_date` is updated
- Dashboard is regenerated
- **Escalation rule:** When `verification_attempts >= 3` (initial attempt + 2 re-attempts), set status to "Blocked" with note `[VERIFICATION ESCALATED] 3 attempts exhausted — requires human review` instead of retrying

### Verification Debt

Tasks that bypass verification create "verification debt":

| Debt Condition | Description |
|----------------|-------------|
| Finished without `task_verification` | Task marked complete but never verified |
| Finished with `task_verification.result == "fail"` | Verification failed, not re-verified |
| Finished with `task_verification.result == "pass_with_issues"` and critical issues | Passed with issues that should block |

**Debt is tracked in the dashboard** under "Action Required" → "Verification Debt" and **blocks project completion**.

## External Dependencies

For tasks blocked by external factors (not other tasks):

```json
{
  "external_dependency": {
    "type": "permit|vendor|approval|delivery",
    "contact": "who to follow up with",
    "requested_date": "2026-01-20",
    "expected_date": "2026-01-28",
    "notes": "Awaiting production API keys"
  }
}
```

| Type | When to Use |
|------|-------------|
| permit | Legal, regulatory, compliance approvals |
| vendor | Third-party service, API access, contracts |
| approval | Internal stakeholder sign-off |
| delivery | Physical items, hardware, materials |

## Status Rules

1. Only work on tasks with status "Pending" or "In Progress"
2. Never work directly on "Broken Down", "On Hold", or "Absorbed" tasks
3. "Broken Down" tasks auto-complete when all subtasks are "Finished"
4. Document blockers when setting status to "Blocked"
5. Document reason when setting status to "On Hold"
6. "Awaiting Verification" is a transitional status — tasks must proceed to verification immediately
7. "Absorbed" requires the `absorbed_into` field referencing the absorbing task
8. "On Hold" tasks are excluded from auto-routing — only a user can move them back to "Pending"

### Status Flow

```
Pending → In Progress → Awaiting Verification → [verify-agent] → Finished
  ↕             ↓                                  ↓ (fail)
On Hold      Blocked                          In Progress (fix & retry)

Any non-Finished status → Absorbed (when scope is folded into another task)
```

**"Awaiting Verification"** is the transitional status between implementation completion and verification. Tasks in this status:
- Have completed implementation but not yet been verified
- Must proceed to verify-agent immediately (cannot remain in this status)
- Are set automatically by implement-agent Step 6a

### On Hold

Tasks placed on hold are excluded from all routing. Only a user can resume them.

```json
{
  "id": "7",
  "status": "On Hold",
  "notes": "Deferring until Q2 budget approval"
}
```

- `/work` skips On Hold tasks entirely (not counted as pending, blocked, or actionable)
- On Hold tasks still appear in the dashboard Tasks section with ⏸️ prefix
- Health check warns if On Hold > 30 days (may be forgotten)
- To resume: user sets status back to "Pending" (or "In Progress" if partially done)

### Absorbed

When a task's scope is folded into another task (discovered during breakdown, overlap found, or reorganization):

```json
{
  "id": "4",
  "status": "Absorbed",
  "absorbed_into": "3",
  "notes": "Scope covered by task 3 after breakdown"
}
```

- Requires `absorbed_into` field with the absorbing task's ID
- Absorbed tasks are excluded from routing, completion checks, and phase progress
- Absorbed subtasks don't block parent auto-completion
- Preserves audit trail (vs deletion, which loses history)
- Dashboard shows absorbed tasks in a collapsed/dimmed style or omits them from active counts

### Verification Requirement for Finished Status

**CRITICAL:** A task can only have `status: "Finished"` if it has a valid `task_verification` field with `result: "pass"` or `result: "pass_with_issues"`.

| Status | Verification Requirement |
|--------|-------------------------|
| Pending | None |
| In Progress | None |
| Awaiting Verification | Must proceed to verification immediately |
| Blocked | None |
| On Hold | None (paused — verification not applicable until resumed) |
| Absorbed | None (scope folded into another task — that task carries verification) |
| Broken Down | None (subtasks are verified individually) |
| **Finished** | **REQUIRED:** `task_verification.result` must be `"pass"` or `"pass_with_issues"` |

**Enforcement:**
- `/health-check` treats missing or failed verification on Finished tasks as an **ERROR** (not warning)
- `/work` will not route to completion phase if any Finished task lacks valid verification
- The "verification debt" metric tracks tasks that violate this rule

**Why this matters:** Without structural enforcement, verification can be bypassed by marking tasks Finished directly. This rule makes the verification artifact mandatory, not just detected post-facto.

## Task Archiving

For large projects (100+ tasks), finished tasks are automatically archived.

### Archive Structure

```
.claude/
├── dashboard.md          # Auto-generated summary
└── tasks/
    ├── task-*.json       # Active tasks
    └── archive/
        ├── task-*.json       # Archived task files
        └── archive-index.json # Lightweight summary
```

### Auto-Archive Behavior

When active task count exceeds 100, `/work` automatically:
1. Identifies finished tasks older than 7 days
2. Moves them to `.claude/tasks/archive/`
3. Updates archive-index.json

Archived tasks remain available for reference but don't clutter the dashboard.
