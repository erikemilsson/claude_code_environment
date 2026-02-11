# Shared Definitions

Single source of truth for task management definitions.

## Vocabulary

Canonical terminology used across the system.

| Term | Definition |
|------|------------|
| **Phase** | A logical stage of the project (e.g., Data Pipeline, Visualization). Phase N+1 can't begin until all Phase N tasks are complete. Implicit from spec structure; tasks get a `phase` field; dashboard groups by phase. |
| **Decision** | A choice with multiple viable options, tracked as a decision record (`.claude/support/decisions/decision-*.md`). Has comparison matrix, option details, optional weighted scoring, and a checkbox for the user to mark their selection. Dependent tasks are blocked until resolved. |
| **Inflection Point** | A decision where the outcome changes what gets built, not just how. After an inflection point is resolved, `/work` pauses and suggests running `/iterate` to revisit the spec before dependent work continues. Contrast with "pick-and-go" decisions where tasks simply unblock. Flagged with `inflection_point: true` in decision frontmatter. |
| **Human Task** | A task only the user can do — external actions like configuring secrets, setting up accounts, or providing credentials. Tracked with `owner: human` in task JSON. Decisions have their own mechanism (checkbox in decision doc) and are not human tasks. |

## Difficulty Scale (1-10)

> **Calibrated for Claude Opus 4.6.** These difficulty ratings and breakdown thresholds assume Opus-level reasoning capability. Tasks rated 5-6 ("Substantial") are at the upper limit of what should be attempted without breakdown — Opus can handle the design decisions involved. Tasks at 7+ **must** be broken down regardless of model confidence.

| Level | Category | Action | Examples |
|-------|----------|--------|----------|
| 1-2 | Routine | Just do it | Fix typo, add field, update config, simple CRUD, add validation rules |
| 3-4 | Standard | May take multiple steps | OAuth integration, REST API with auth, DB schema + migrations, component library setup |
| 5-6 | Substantial | Design decisions needed | Full auth system (JWT + sessions + RBAC), real-time WebSocket features, payment integration, new service with API + tests |
| 7-8 | Large scope | **MUST break down first** | Microservice extraction from monolith, full DB migration (schema + data + rollback), multi-tenant architecture |
| 9-10 | Multi-phase | **MUST break down into phases** | Platform migration (e.g., Rails → Next.js), architecture redesign, security overhaul across all services |

### When to Break Down

Ask: "Can Opus 4.6 complete this reliably in one focused session, with changes that are reviewable and verifiable as a unit?"
- **Yes** → Difficulty 1-6, execute directly
- **No, too many interacting parts** → Difficulty 7-8, break into chunks
- **No, requires discovery or affects the whole system** → Difficulty 9-10, break into phases

## Status Values

| Status | Meaning | Rules |
|--------|---------|-------|
| Pending | Not started | Ready to work on |
| In Progress | Currently working | Multiple allowed when parallel-eligible (see below) |
| Awaiting Verification | Implementation done, needs verification | Must proceed to verify-agent immediately |
| Blocked | Cannot proceed | Document blocker in notes |
| Broken Down | Split into subtasks | Work on subtasks, not this |
| Finished | Complete and verified | Requires `task_verification.result` of "pass" or "pass_with_issues" |

## Priority Values

See `task-schema.md` for full priority definitions. Summary:

| Value | Emoji | Meaning |
|-------|-------|---------|
| critical | 🔴 | Blocking other work, immediate attention |
| high | 🟠 | Important, should be done soon |
| medium | (none) | Normal priority (default) |
| low | (none) | Nice to have, do when time permits |

Priority affects sorting in Ready sections (critical → high → medium → low).
Only critical and high show emoji prefixes in the dashboard.

## Task JSON Structure

See `task-schema.md` for complete field definitions including timeline fields (priority, due_date, external_dependency).

### Minimal Task
```json
{
  "id": "1",
  "title": "Brief description",
  "status": "Pending",
  "difficulty": 3
}
```

## Drift Prevention Fields

Optional fields that track spec-to-task alignment:

| Field | Type | Description |
|-------|------|-------------|
| `spec_fingerprint` | String | SHA-256 hash of full spec at decomposition |
| `spec_version` | String | Spec filename (e.g., "spec_v1") |
| `spec_section` | String | Originating section heading |
| `section_fingerprint` | String | SHA-256 hash of specific section at decomposition |
| `section_snapshot_ref` | String | Reference to snapshot file for diffs |
| `phase` | String | Phase this task belongs to (e.g., "1" or "Data Pipeline") |
| `decision_dependencies` | Array | Decision IDs that block this task (e.g., ["DEC-002"]) |
| `out_of_spec` | Boolean | Task not aligned with spec |
| `task_verification` | Object | Per-task verification result from verify-agent (see task-schema.md) |

These fields enable:
- **Spec drift detection**: Warning when spec changes after tasks are created
- **Granular section tracking**: Detecting which specific sections changed
- **Out-of-spec tracking**: Identifying tasks created outside spec scope
- **Spec provenance**: Tracing which tasks came from which spec sections
- **Diff generation**: Showing exactly what changed via snapshot comparison
- **Per-task verification**: Recording verify-agent results for each completed task

See `task-schema.md` for detailed field documentation.

## Section Parsing Algorithm

How spec files are parsed into sections for fingerprinting:

### Definition

```
Section = ## heading + all content until next ## or EOF
```

### Parsing Rules

1. **Strip YAML frontmatter** - Remove `---` delimited frontmatter before parsing
2. **Extract ## level headings** - Each `## Title` starts a new section
3. **Include ### subsections** - Subsections belong to their parent ## section
4. **Normalize heading text** - Trim whitespace from heading
5. **Compute fingerprint** - `sha256(heading + "\n" + content)`

### Example

Given spec:
```markdown
---
version: 1
---

# Project Spec

## Authentication

Users can log in with email and password.

### Password Requirements

- Minimum 8 characters
- Must include number

## API Endpoints

RESTful API with JSON responses.
```

Produces sections:
| Section | Content |
|---------|---------|
| `## Authentication` | "Users can log in...\n\n### Password Requirements\n\n- Minimum 8 characters..." |
| `## API Endpoints` | "RESTful API with JSON responses." |

Note: `# Project Spec` (H1) is not a section - only H2 (`##`) headings define sections.

### Edge Cases

| Scenario | Handling |
|----------|----------|
| No ## headings | Entire spec content (after frontmatter) is one "section" |
| Empty section | Section with heading but no content - fingerprint is hash of heading only |
| Consecutive ## | Creates sections with empty content between them |
| Content before first ## | Ignored for section purposes (preamble) |

## Mandatory Rules

**ALWAYS:**
1. Break down tasks with difficulty >= 7 before starting
2. Dashboard regenerates automatically after task changes
3. Parent tasks auto-complete when all subtasks finish

**Parallel Execution Rules:**
Multiple "In Progress" tasks are allowed when ALL of these conditions are met:
- All dependencies for each task are "Finished"
- `files_affected` arrays do not overlap between any tasks in the batch
- All tasks in the batch belong to the current active phase (no phase dependency blocks any task)
- Batch size does not exceed `max_parallel_tasks` (default: 3)
- Each task has difficulty < 7

When conditions are not met, fall back to sequential execution (one "In Progress" at a time).

**NEVER:**
- Work on "Broken Down" tasks directly (work on subtasks instead)
- Skip status updates
- Dispatch parallel tasks without checking file conflicts

## Owner Field

Tasks have an `owner` field that determines responsibility and dashboard placement:

| Value | Emoji | Dashboard Section | When to Use |
|-------|-------|-------------------|-------------|
| `claude` | 🤖 | Claude Status | Autonomous work (default when omitted) |
| `human` | ❗ | Your Actions | Requires human action |
| `both` | 👥 | Both sections | Collaborative work |

**Human tasks** - Configure secrets, external actions, review/approve
**Claude tasks** - Write code, implement features, tests, docs, research
**Both tasks** - Human provides direction, Claude implements (appears in BOTH dashboard sections with 👥)

## Task ID Conventions

| Pattern | Meaning | Example |
|---------|---------|---------|
| `N` | Top-level task | `1`, `2`, `3` |
| `N_M` | Sequential subtask | `1_1`, `1_2` (must do in order) |
| `N_Ma` | Parallel subtask | `1_1a`, `1_1b` (can do simultaneously) |

Use underscores for sequential dependencies, letters for parallel work within a sequence. Tasks using the `N_Ma` convention are natural candidates for parallel dispatch — they were designed to run concurrently. `/work` checks these alongside all other eligible tasks when building parallel batches.
