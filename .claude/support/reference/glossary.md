# Glossary

Canonical definitions for all terms used in this environment. This is the single source of truth for terminology — other files should reference definitions here rather than restating them.

---

## Core Workflow

### Spec (Specification)

The project specification, living at `.claude/spec_v{N}.md`. The single source of truth for what gets built. All work aligns with it, or the spec is updated intentionally. Has a `status` field in its YAML frontmatter: `draft` (being written), `active` (being implemented), or `complete` (all work done and verified).

### Spec Phase

The first workflow phase. Goal: define what needs to be built. Human-guided via `/iterate`. Produces a specification with testable acceptance criteria. Exit criteria: all blocking questions answered, acceptance criteria are testable, key decisions documented, scope is clear, human approved.

### Execute Phase

The second workflow phase. Goal: build the implementation. The spec is decomposed into tasks, which are worked through in dependency order by the implement-agent. Each completed task goes through per-task verification before being marked Finished. Exit criteria: all tasks Finished with passing verification.

### Verify Phase

The third workflow phase. Operates in two tiers:

- **Tier 1 (Per-Task):** Runs during Execute, immediately after each task is implemented. Checks file artifacts, spec alignment, code quality, and integration boundaries. Automatic — part of the implement → verify atomic cycle.
- **Tier 2 (Phase-Level):** Runs once when all tasks are Finished. Validates the full implementation against spec acceptance criteria. Produces a structured report with pass/fail per criterion. Result written to `.claude/verification-result.json`.

### Implementation Stage

Organizational groupings for tasks within the Execute phase. Not workflow phases. Four stages: **Foundation** (setup, scaffolding), **Core Features** (main functionality), **Polish** (edge cases, error handling), **Validation** (testing, documentation).

---

## Task System

### Task

A unit of work tracked as a JSON file in `.claude/tasks/task-*.json`. Has required fields (`id`, `title`, `status`, `difficulty`) and optional fields (see `task-schema.md` for the full schema).

### Task Status

The lifecycle state of a task. Values:

| Status | Meaning |
|--------|---------|
| **Pending** | Not started, ready to work on |
| **In Progress** | Currently being worked on |
| **Awaiting Verification** | Implementation done, must proceed to verify-agent immediately |
| **Blocked** | Cannot proceed; blocker documented in notes |
| **Broken Down** | Split into subtasks; work on subtasks, not this task |
| **Finished** | Complete and verified (requires `task_verification.result` of "pass" or "pass_with_issues") |

Flow: `Pending → In Progress → Awaiting Verification → Finished` (or back to In Progress on verification failure).

### Task Difficulty

A 1–10 scale calibrated for Claude Opus 4.6:

| Level | Category | Action |
|-------|----------|--------|
| 1–2 | Routine | Just do it |
| 3–4 | Standard | May take multiple steps |
| 5–6 | Substantial | Design decisions needed |
| 7–8 | Large scope | **Must break down first** |
| 9–10 | Multi-phase | **Must break into phases** |

The key question: "Can Opus 4.6 complete this reliably in one focused session, with changes that are reviewable and verifiable as a unit?" If not, break it down.

### Task Priority

Affects sorting in dashboard Ready sections. Values:

| Value | Emoji | Meaning |
|-------|-------|---------|
| **critical** | Red circle | Blocking other work, immediate attention |
| **high** | Orange circle | Important, should be done soon |
| **medium** | — | Normal priority (default) |
| **low** | — | Nice to have |

### Task Owner

Determines responsibility and dashboard placement. Values:

| Value | Emoji | Meaning |
|-------|-------|---------|
| **claude** | Robot | Autonomous work (default) |
| **human** | Exclamation | Requires human action |
| **both** | People | Collaborative work (appears in both dashboard sections) |

### Human Task

A task only the user can do — external actions like configuring secrets, setting up accounts, or providing credentials. Tracked with `owner: human`. Not to be confused with decisions, which have their own mechanism (checkbox in decision doc).

### Subtask

A child task created when a parent task is broken down. Uses ID conventions: `N_M` for sequential subtasks (must do in order), `N_Ma` for parallel subtasks (can do simultaneously). Parent tasks auto-complete when all subtasks finish.

### Out-of-Spec Task

A task not aligned with the specification, created when the user selects "proceed anyway" on a spec misalignment, or when verify-agent creates recommendation tasks for improvements beyond acceptance criteria. Marked with `out_of_spec: true`. Shown with a warning prefix in the dashboard. Excluded from phase routing and completion conditions.

### Parallel Execution

The default dispatch mode. When `/work` finds multiple pending tasks with no mutual dependencies, no file conflicts, all in the current phase, each with difficulty < 7, and batch size within `max_parallel_tasks` (default: 3) — it dispatches them concurrently. Each task still runs the full implement → verify cycle independently. Falls back to sequential when conditions aren't met.

### Parallel-Safe Task

A task with `parallel_safe: true` that is eligible for parallel execution even with an empty `files_affected` array. Used for research/analysis tasks with no file side effects.

---

## Decision System

### Decision

A choice with multiple viable options, tracked as a decision record at `.claude/support/decisions/decision-*.md`. Contains a comparison matrix, option details, optional weighted scoring, and a checkbox for the user to mark their selection. Dependent tasks are blocked until the decision is resolved.

### Decision Status

The lifecycle state of a decision:

| Status | Meaning |
|--------|---------|
| **draft** | Being researched, not ready for review |
| **proposed** | Options documented, ready for stakeholder input |
| **approved** | Decision finalized, may await implementation |
| **implemented** | Decision reflected in codebase |
| **superseded** | Replaced by a newer decision |

### Decision Category

Classification for decision records: `architecture`, `technology`, `process`, `scope`, `methodology`, or `vendor`.

### Pick-and-Go Decision

A decision where, after resolution, blocked tasks simply unblock and `/work` continues normally. The default — any decision without `inflection_point: true`. Contrast with inflection point.

### Inflection Point

A decision where the outcome changes *what gets built*, not just how. Flagged with `inflection_point: true` in decision frontmatter. After resolution, `/work` pauses and suggests running `/iterate` to revisit the spec before dependent work continues. Example: "supervised vs unsupervised analysis" changes what data you collect and what pipeline you build.

### Comparison Matrix

The core of a decision record. A criteria-vs-options table that forces structured evaluation. Common criteria: Performance, Complexity, Cost, Ecosystem, Fit, Risk.

### Weighted Scoring

Optional addition for high-stakes decisions. Each criterion gets a percentage weight and each option gets a score (1–5). Weighted totals make evaluation explicit. Use when decisions affect architecture, have multiple strong alternatives, or need communicable rationale.

### Implementation Anchor

A reference linking a decision to where it's realized in code. Added when a decision reaches `implemented` status. Fields: `file` (path), `line` (optional), `description`. Validated by `/health-check`.

### Spec-Level Choice

A choice that defines requirements, scope, or user-visible behavior (the "what"). Affects user-facing behavior or system architecture. Should be decided before implementation begins. Changes require spec revision. Examples: which features to include in MVP, authentication strategy, data model structure.

### Implementation-Level Choice

A choice that defines tools, libraries, or technical details (the "how"). Affects developer experience, not user-visible behavior. Can be decided during implementation. Changes don't require spec revision. Examples: which OAuth library, database engine, testing framework.

---

## Spec Drift & Reconciliation

### Spec Drift

When the specification changes after tasks have been decomposed from it. Detected by comparing the current spec's hash against task fingerprints. Reconciliation identifies which specific sections changed and offers targeted updates.

### Spec Fingerprint

SHA-256 hash of the full spec file content at decomposition time. Stored in each task as `spec_fingerprint`. Used for coarse drift detection — if the current spec hash differs, *something* changed.

### Section Fingerprint

SHA-256 hash of a specific spec section's content at decomposition time. Stored in each task as `section_fingerprint`. Enables granular drift detection — only tasks from changed sections are flagged for review.

### Drift Deferral

When a user selects "Skip section" during reconciliation, the skipped section is recorded in `.claude/drift-deferrals.json` with a timestamp. Deferrals accumulate and are tracked in the dashboard.

### Drift Budget

A limit on how much unreconciled drift can accumulate before work is blocked. Configured in spec frontmatter via `drift_policy`: `max_deferred_sections` (default: 3) and `max_deferral_age_days` (default: 14). Enforced by both `/work` and `/health-check`. When exceeded, reconciliation is required before work can continue.

### Reconciliation

The process of updating tasks to match a changed spec. Options per section: **Apply suggestions** (auto-update), **Review individually** (step through each task), **Skip section** (creates a deferral), **Mark out-of-spec** (flag task as no longer aligned).

---

## Verification

### Per-Task Verification (Tier 1)

Verification that runs immediately after each task is implemented, as part of the atomic implement → verify cycle. Checks: files exist, spec alignment, code quality, integration readiness. Result written to the task's `task_verification` field. Pass → Finished. Fail → back to In Progress (max 2 retries before escalating to human).

### Phase-Level Verification (Tier 2)

Verification that runs once when all tasks are Finished with passing per-task verification. Validates the full implementation against spec acceptance criteria. Creates fix tasks for issues found. Result: `pass`, `fail`, or `pass_with_issues`. Written to `.claude/verification-result.json`.

### Verification Debt

Tasks that have bypassed or failed verification. Three conditions: (1) status "Awaiting Verification", (2) status "Finished" without a `task_verification` field, (3) `task_verification.result` is "fail". Tracked in the dashboard and blocks project completion. Out-of-spec tasks are excluded from the count.

---

## Agents

### Implement-Agent

The builder agent. Executes tasks, writes code, self-reviews, and marks tasks "Awaiting Verification". Focuses purely on building — no self-validation bias. Workflow defined in `.claude/agents/implement-agent.md`.

### Verify-Agent

The validator agent. Tests against spec, finds issues, ensures quality. Validates with fresh perspective (not the same agent that built it). Handles both per-task (Tier 1) and phase-level (Tier 2) verification. Workflow defined in `.claude/agents/verify-agent.md`.

---

## Dashboard

### Dashboard

The project dashboard at `.claude/dashboard.md`. The primary communication channel between Claude and the user during the build phase. Regenerated automatically after task changes. Contains canonical sections in a fixed order (see `dashboard-patterns.md`).

### Needs Your Attention

The dashboard's primary action hub. Everything Claude needs from the user: pending decisions, human tasks, reviews, verification debt. Each item must be actionable — with links to relevant files and ways to respond. Sub-sections: Verification Debt, Decisions Pending, Tasks Ready for You, Reviews & Approvals.

### Dashboard Freshness

Whether the dashboard reflects current task state. Detected by comparing a `task_hash` (SHA-256 of sorted task_id:status pairs) in the dashboard metadata against the current computed hash. Stale dashboards are regenerated before use.

---

## Project Structure

### Phase (Project Phase)

A logical stage of the project (e.g., "Data Pipeline", "Visualization"). Phase N+1 can't begin until all Phase N tasks are complete. Implicit from spec structure — sections in the spec naturally group into phases. Tasks get a `phase` field during decomposition. Dashboard groups tasks by phase with per-phase progress.

### Workspace

Temporary documents directory at `.claude/support/workspace/`. For scratch work, research, and drafts. Never create working documents in the project root.

### Vision Document

An ideation document saved to `.claude/vision/`. Captures intent and philosophy from brainstorming sessions (e.g., Claude Desktop). Run `/iterate distill` to extract a buildable spec from vision docs. Vision docs are preserved alongside specs.

---

## Cross-Reference

Where each term was previously defined (for migration reference):

| Term | Previously Defined In |
|------|----------------------|
| Phase, Decision, Inflection Point, Human Task | `shared-definitions.md` (Vocabulary), `extension-patterns.md`, `CLAUDE.md` |
| Task Status, Priority, Owner, Difficulty | `shared-definitions.md`, `task-schema.md` |
| Pick-and-Go | `extension-patterns.md` |
| Spec-Level / Implementation-Level Choice | `choice-classification.md` |
| Decision Status, Category | `decision-template.md`, `decision-guide.md` |
| Verification Debt | `dashboard-patterns.md`, `task-schema.md` |
| Spec Drift, Drift Budget | `work.md`, `health-check.md` |
| Per-Task / Phase-Level Verification | `workflow.md` |
| Dashboard Freshness | `work.md`, `dashboard-patterns.md` |
| Implementation Stage | `workflow.md` |
