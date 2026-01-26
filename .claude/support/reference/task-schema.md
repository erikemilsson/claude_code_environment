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
  "milestone": null,
  "external_dependency": null,
  "notes": "",
  "spec_fingerprint": "sha256:a1b2c3d4...",
  "spec_version": "spec_v1",
  "spec_section": "## Authentication",
  "section_fingerprint": "sha256:e5f6g7h8...",
  "section_snapshot_ref": "spec_v1_decomposed.md"
}
```

## Field Definitions

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| id | String | Number for top-level ("1"), underscore for subtasks ("1_1") |
| title | String | Brief description of what needs to be done |
| status | String | Pending, In Progress, Blocked, Broken Down, Finished |
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
| milestone | String | Milestone ID this task belongs to (e.g., "M1") |
| external_dependency | Object | External blocker - see External Dependencies below |
| notes | String | Context, warnings, or completion notes |
| spec_fingerprint | String | SHA-256 hash of spec at task decomposition (drift detection) |
| spec_version | String | Spec filename when task was created (e.g., "spec_v1") |
| spec_section | String | Originating section heading from spec |
| section_fingerprint | String | SHA-256 hash of the specific section content at decomposition |
| section_snapshot_ref | String | Reference to snapshot file for generating diffs (e.g., "spec_v1_decomposed.md") |
| out_of_spec | Boolean | Task not aligned with spec (user chose "proceed anyway") |

## Owner Values

The `owner` field determines who is responsible and where tasks appear in the dashboard:

| Value | Emoji | Dashboard Section | When to Use |
|-------|-------|-------------------|-------------|
| `claude` | 🤖 | Claude Status | Tasks Claude can do autonomously (default) |
| `human` | ❗ | Your Actions | Requires human action (config, decisions, external) |
| `both` | 👥 | Both sections | Collaborative work (appears in BOTH dashboard sections) |

### Examples by Owner

**`claude`** (default - omit field if this):
- Write code, implement features
- Create tests, documentation
- Refactor, fix bugs
- Research and analysis

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

## Milestones

Milestones are lightweight date markers for project phases:

```json
{
  "id": "M1",
  "title": "MVP Complete",
  "type": "milestone",
  "target_date": "2026-02-01",
  "status": "Pending",
  "description": "Core functionality complete and working"
}
```

Save as `milestone-M1.json` in `.claude/tasks/`. Tasks reference via `"milestone": "M1"`.

### Milestone Status Values

| Status | Icon | Meaning | Auto-determined by |
|--------|------|---------|-------------------|
| Pending | ⏳ | Not started | No tasks finished |
| In Progress | 🔄 | Work underway | Some tasks finished, not all |
| Complete | ✅ | Done | All linked tasks finished |
| At Risk | ⚠️ | May miss target | Past target date, not complete |
| Overdue | 🔴 | Missed target | Significantly past target |

Milestone status is calculated automatically based on:
1. Count of tasks with `"milestone": "M1"` that are "Finished"
2. Comparison of current date to `target_date`

### Dashboard Integration

Milestones appear in two dashboard sections:
- **🎯 Milestones** - Dedicated section showing all milestones with progress
- **⏰ Timeline** - Milestones shown in **bold** alongside task due dates

## Status Rules

1. Only work on tasks with status "Pending" or "In Progress"
2. Never work directly on "Broken Down" tasks - work on subtasks
3. "Broken Down" tasks auto-complete when all subtasks are "Finished"
4. Document blockers when setting status to "Blocked"

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
