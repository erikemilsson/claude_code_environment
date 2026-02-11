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
| 1-2 | Routine | Just do it | Fix typo, add field, update config, simple CRUD, single vendor lookup, update a contact list |
| 3-4 | Standard | May take multiple steps | OAuth integration, REST API with auth, compare 5+ vendor quotes and produce shortlist, research and summarize 3 options with pros/cons |
| 5-6 | Substantial | Design decisions needed | Full auth system (JWT + sessions + RBAC), payment integration, full vendor evaluation with site visits and scoring matrix, project timeline with dependencies and resource allocation |
| 7-8 | Large scope | **MUST break down first** | Microservice extraction from monolith, full DB migration (schema + data + rollback), complete procurement process (research + quotes + negotiation + contracts) |
| 9-10 | Multi-phase | **MUST break down into phases** | Platform migration (e.g., Rails → Next.js), architecture redesign, full project delivery (research → planning → procurement → execution → validation) |

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

Spec files are parsed into sections for fingerprinting: each `##` heading starts a new section that includes all content until the next `##` or EOF (including `###` subsections). YAML frontmatter is stripped first, and H1 headings are ignored. Fingerprint: `sha256(heading + "\n" + content)`.

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

| Value | Emoji | Dashboard Location | When to Use |
|-------|-------|-------------------|-------------|
| `claude` | 🤖 | Claude section | Autonomous work (default when omitted) |
| `human` | ❗ | Action Required → Your Tasks | Requires human action |
| `both` | 👥 | Both sections | Collaborative work |

**Human tasks** - Configure secrets, external actions (phone calls, site visits), review/approve
**Claude tasks** - Execute tasks, create deliverables, research, analysis, documentation
**Both tasks** - Human provides direction or external input, Claude produces deliverables (appears in BOTH dashboard sections with 👥)

## Task ID Conventions

| Pattern | Meaning | Example |
|---------|---------|---------|
| `N` | Top-level task | `1`, `2`, `3` |
| `N_M` | Sequential subtask | `1_1`, `1_2` (must do in order) |
| `N_Ma` | Parallel subtask | `1_1a`, `1_1b` (can do simultaneously) |

Use underscores for sequential dependencies, letters for parallel work within a sequence. Tasks using the `N_Ma` convention are natural candidates for parallel dispatch — they were designed to run concurrently. `/work` checks these alongside all other eligible tasks when building parallel batches.

---

## Glossary

Canonical definitions for terms used across the environment. Terms already defined in the tables above are not repeated.

### Workflow Phases

| Term | Definition |
|------|------------|
| **Spec** | The project specification at `.claude/spec_v{N}.md`. Single source of truth for what gets built. Frontmatter status: `draft`, `active`, or `complete`. |
| **Spec Phase** | First workflow phase. Define what needs to be built via `/iterate`. Exit: all blocking questions answered, acceptance criteria testable, human approved. |
| **Execute Phase** | Second workflow phase. Spec decomposed into tasks, worked in dependency order by implement-agent. Each task goes through per-task verification. Exit: all tasks Finished. |
| **Verify Phase** | Third workflow phase. Two tiers: **Tier 1** (per-task, runs during Execute after each implementation) and **Tier 2** (phase-level, runs once when all tasks Finished, validates full implementation against spec). |
| **Implementation Stage** | Organizational groupings within Execute: Foundation (setup), Core Features (main functionality), Polish (edge cases), Validation (testing). Not workflow phases. |

### Task Concepts

| Term | Definition |
|------|------------|
| **Subtask** | Child task from breakdown. ID `N_M` = sequential (do in order), `N_Ma` = parallel (do simultaneously). Parent auto-completes when all subtasks finish. |
| **Out-of-Spec Task** | Task not aligned with spec, created when user proceeds despite misalignment or verify-agent suggests improvements beyond acceptance criteria. Marked `out_of_spec: true`. Excluded from phase routing and completion conditions. |
| **Parallel-Safe Task** | Task with `parallel_safe: true`, eligible for parallel execution even with empty `files_affected`. Used for research/analysis with no file side effects. |

### Decision Concepts

| Term | Definition |
|------|------------|
| **Pick-and-Go Decision** | Default decision type. After resolution, blocked tasks simply unblock and `/work` continues. Any decision without `inflection_point: true`. |
| **Comparison Matrix** | Core of a decision record. Criteria-vs-options table forcing structured evaluation. Common criteria: Performance, Complexity, Cost, Ecosystem, Fit, Risk. |
| **Weighted Scoring** | Optional addition for high-stakes decisions. Each criterion gets a percentage weight, options scored 1–5. Makes evaluation explicit. |
| **Implementation Anchor** | Reference linking a decision to where it was realized. Added at `implemented` status. Fields: `file`, `line` (optional), `description`. Validated by `/health-check`. |
| **Spec-Level Choice** | Choice defining requirements or user-visible behavior (the "what"). Changes require spec revision. |
| **Implementation-Level Choice** | Choice defining tools or technical details (the "how"). Changes don't require spec revision. |

### Spec Drift

| Term | Definition |
|------|------------|
| **Spec Drift** | When spec changes after tasks were decomposed from it. Detected by comparing current spec hash against task fingerprints. |
| **Drift Deferral** | When user selects "Skip section" during reconciliation. Recorded in `.claude/drift-deferrals.json` with timestamp. |
| **Drift Budget** | Limit on unreconciled drift. Configured via `drift_policy` in spec frontmatter: `max_deferred_sections` (default: 3), `max_deferral_age_days` (default: 14). Enforced by `/work` and `/health-check`. |
| **Reconciliation** | Updating tasks to match a changed spec. Options per section: apply suggestions, review individually, skip (creates deferral), mark out-of-spec. |

### Verification

| Term | Definition |
|------|------------|
| **Per-Task Verification (Tier 1)** | Runs after each task implementation. Checks: files exist, spec alignment, output quality, integration readiness. Pass → Finished. Fail → back to In Progress (max 2 retries). |
| **Phase-Level Verification (Tier 2)** | Runs once when all tasks Finished. Validates full implementation against spec acceptance criteria. Result: `pass`, `fail`, or `pass_with_issues`. Written to `.claude/verification-result.json`. |
| **Verification Debt** | Tasks that bypassed or failed verification: status "Awaiting Verification", "Finished" without `task_verification`, or `task_verification.result` is "fail". Blocks project completion. |

### Agents & Infrastructure

| Term | Definition |
|------|------------|
| **Implement-Agent** | Builder agent. Executes tasks, produces deliverables, self-reviews, marks "Awaiting Verification". Defined in `.claude/agents/implement-agent.md`. |
| **Verify-Agent** | Validator agent. Tests against spec, finds issues, handles both Tier 1 and Tier 2 verification. Defined in `.claude/agents/verify-agent.md`. |
| **Dashboard** | Project dashboard at `.claude/dashboard.md`. Primary communication channel during build phase. Regenerated after task changes. |
| **Dashboard Freshness** | Whether dashboard reflects current state. Detected by comparing `task_hash` (SHA-256 of sorted task_id:status pairs) against current computed hash. |
| **Workspace** | Temporary documents at `.claude/support/workspace/`. Subdirs: scratch, research, drafts. May be deleted between sessions. |
| **Vision Document** | Ideation document in `.claude/vision/`. Captures intent and philosophy. Run `/iterate distill` to extract a buildable spec. |
