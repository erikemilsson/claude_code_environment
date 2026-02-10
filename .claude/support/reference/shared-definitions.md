# Shared Definitions

Single source of truth for task management definitions.

## Difficulty Scale (1-10)

| Level | Category | Action | Examples |
|-------|----------|--------|----------|
| 1-2 | Routine | Just do it | Fix typo, add field, update config |
| 3-4 | Standard | May take multiple steps | CRUD for entity, API endpoint, OAuth integration |
| 5-6 | Substantial | Design decisions needed | New module, real-time features, RBAC |
| 7-8 | Large scope | **MUST break down first** | Microservice migration, replace database |
| 9-10 | Multi-phase | **MUST break down into phases** | Architecture redesign, security overhaul |

### When to Break Down

Ask: "Can this be completed in one focused session?"
- **Yes** → Difficulty 1-6, just do it
- **No, too much scope** → Difficulty 7-8, break into chunks
- **No, need discovery** → Difficulty 9-10, break into phases

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
- No stage gate blocks any task in the batch
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

**Human tasks** - Configure secrets, make decisions, external actions, review/approve
**Claude tasks** - Write code, implement features, tests, docs, research
**Both tasks** - Human provides direction, Claude implements (appears in BOTH dashboard sections with 👥)

## Task ID Conventions

| Pattern | Meaning | Example |
|---------|---------|---------|
| `N` | Top-level task | `1`, `2`, `3` |
| `N_M` | Sequential subtask | `1_1`, `1_2` (must do in order) |
| `N_Ma` | Parallel subtask | `1_1a`, `1_1b` (can do simultaneously) |

Use underscores for sequential dependencies, letters for parallel work within a sequence. Tasks using the `N_Ma` convention are natural candidates for parallel dispatch — they were designed to run concurrently. `/work` checks these alongside all other eligible tasks when building parallel batches.
