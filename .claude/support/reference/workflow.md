# Workflow Guide

The Spec → Execute → Verify workflow for autonomous multi-phase projects.

## Overview

```
┌──────────┐    ┌──────────────────────────────────────────────────┐    ┌──────────┐
│   Spec   │ -> │                    Execute                        │ -> │  Verify  │
│          │    │                                                    │    │ (phase)  │
│ Define   │    │  ┌─ Parallel batch (when eligible) ─────────────┐ │    │          │
│ what     │    │  │ ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │    │ Validate │
│          │    │  │ │impl → vfy│  │impl → vfy│  │impl → vfy│    │ │    │ all ACs  │
│          │    │  │ │ task A   │  │ task B   │  │ task C   │    │ │    │          │
│          │    │  │ └──────────┘  └──────────┘  └──────────┘    │ │    │          │
│          │    │  └──────────────────────────────────────────────┘ │    │          │
│          │    │       v (collect results, single dashboard regen)  │    │          │
│          │    │  next batch or sequential task...                  │    │          │
└──────────┘    └──────────────────────────────────────────────────┘    └──────────┘
     ^                                                                        │
     └──────────── (if issues found) ────────────────────────────────────────┘
```

Each parallel lane runs the full implement → verify cycle independently. The `/work` coordinator manages batching, result collection, and a single dashboard regeneration. When tasks are not parallel-eligible, execution falls back to the sequential one-at-a-time model shown below:

```
  ┌────────────┐   ┌────────────────┐
  │ Implement  │ -> │ Verify (task)  │
  │ task N     │   │ task N         │
  └────────────┘   └────────────────┘
       ^                │
       └── (if fail) ───┘
       v (if pass)
  next task...
```

---

## Phase Details

### Spec Phase

**Goal:** Define what needs to be built

**Activities:**
- Document problem statement
- Define goals and non-goals
- List requirements (functional and non-functional)
- Create testable acceptance criteria
- Identify constraints
- Make key architecture decisions

**Exit Criteria:**
- All blocking questions answered
- Acceptance criteria are testable
- Key decisions documented
- Scope is clear
- Human approved specification

**Process:** Manual (human-guided via `/iterate`)

To create or revise the spec, run `/iterate`. Claude will guide you through iterative Q&A but you edit the spec directly.

### Execute Phase

**Goal:** Build the implementation

**Activities:**
- Decompose spec into tasks (handled by /work if no tasks exist)
- Work through tasks in dependency order
- Create deliverables and files
- Self-review changes
- Per-task verification after each task completion
- Document completion notes
- Flag discovered issues

**Exit Criteria:**
- All tasks have status "Finished" with passing per-task verification (Absorbed tasks are excluded — they don't count as incomplete)
- No blocked tasks remain
- No "On Hold" tasks remain (user must resume, absorb, or remove them before phase exit)
- Deliverables follow project conventions
- Ready for phase-level verification

**Agent:** implement-agent

### Verify Phase

Verification operates in two tiers:

#### Tier 1: Per-Task Verification (during Execute phase)

**Goal:** Catch issues in each task immediately after completion

**When it triggers:** After implement-agent sets a task to "Awaiting Verification" status. Verification is triggered automatically as part of Step 6 in implement-agent, making implementation and verification atomic.

**Activities:**
- Verify file artifacts exist and match task description
- Check spec alignment against task description and spec section
- Validate output quality (no incomplete items, follows patterns)
- Check integration boundaries (dependencies consumed correctly, outputs match downstream expectations)

**Output:** `task_verification` field written to task JSON with per-check pass/fail

**What happens after per-task verification:**
- **Pass:** Task status set to "Finished" (from "Awaiting Verification"). `/work` proceeds to next pending task.
- **Fail:** Task set back to "In Progress". implement-agent fixes, then re-verification. The `verification_attempts` counter tracks attempts; after 3 total (initial + 2 retries), the task is escalated to human review as "Blocked".

#### Tier 2: Phase-Level Verification

**Goal:** Confirm the full implementation matches the spec's acceptance criteria

**When it triggers:** Automatically when `/work` detects all spec tasks are finished AND all have passing per-task verification (auto-detect mode), or manually when the user runs `/work` after completing all tasks.

**Activities:**
- Run existing test suite (if available)
- Validate each spec acceptance criterion individually
- Check quality, completeness, and integration
- Identify and categorize issues (critical/major/minor)
- Create fix tasks for issues found (in-spec bugs as regular tasks; recommendations as `out_of_spec: true`)
- Write verification result to `.claude/verification-result.json`
- Generate verification report for the user
- Reference per-task verification results as evidence for individual checks

**Output:** A structured report showing:
- Pass/fail status for each acceptance criterion
- Issues found, categorized by severity
- Tasks created for fixes (if any)
- Overall result: `pass` or `fail`

**What happens after phase-level verification:**
- **Pass:** `/work` transitions to Complete phase. Spec status updates to `complete`. Any out-of-spec recommendation tasks are presented to the user for approval at the phase boundary.
- **Fail:** Critical/major issues found where spec requirements aren't met. In-spec fix tasks are created (regular tasks, not out-of-spec). `/work` automatically routes them to implement-agent. Once fixes are done and all spec tasks pass per-task verification again, phase-level verification re-runs.

**Feedback loop — bug fixes (in-spec):**
1. verify-agent identifies issues where spec requirements aren't met
2. Fix tasks are created as **regular tasks** (not out-of-spec)
3. Verification result is set to `"fail"`
4. `/work` routes fix tasks to implement-agent automatically
5. When all spec tasks are finished again, phase-level verification re-runs

**Feedback loop — recommendations (out-of-spec):**
1. verify-agent identifies improvements beyond spec acceptance criteria
2. Recommendation tasks are created with `out_of_spec: true`
3. Verification result is `"pass"` (spec criteria met)
4. `/work` presents recommendations to user for Accept/Reject/Defer
5. Accepted tasks are executed independently; they don't block project completion

**Exit Criteria:**
- All acceptance criteria pass (or failures are documented and accepted)
- No critical issues remain
- Verification result persisted to `.claude/verification-result.json`
- Human approved final state

**Agent:** verify-agent (see `.claude/agents/verify-agent.md` for detailed workflow)

---

## Agent Synergy: Implement + Verify + Research

This project uses three specialist agents:

| Agent | Role | Focus |
|-------|------|-------|
| **implement-agent** | Builder | Executes tasks, produces deliverables, marks tasks finished |
| **verify-agent** | Validator | Tests against spec, finds issues, ensures quality |
| **research-agent** | Investigator | Gathers evidence for decisions, populates comparison matrices |

**Why three agents?**
A single agent implementing and validating its own work has blind spots.
By separating concerns:
- implement-agent focuses purely on building (no self-validation bias)
- verify-agent validates against the spec with fresh perspective
- research-agent investigates options without implementation or compliance bias
- Issues caught by verify-agent become new tasks for implement-agent
- Evidence gathered by research-agent feeds into decision records for human selection

**Architectural separation:** verify-agent and research-agent always run as **separate `Task` agents** (spawned via the Task tool), never inline in the implementation context. This ensures genuine independence — the verifier has no memory of implementation decisions, only the artifacts (task JSON, spec section, and files); the researcher has no implementation or compliance bias, only the decision record and project context. This applies to both sequential and parallel execution modes.

**The build workflow:**
1. `/work` reads and follows implement-agent workflow for the next pending task
2. implement-agent: build, self-review, update status to "Awaiting Verification"
3. implement-agent Step 6b: **spawn** verify-agent as a separate Task agent (fresh context)
4. verify-agent (separate context): verify files, spec alignment, quality, integration boundaries
5. If verification passes: status → "Finished", regenerate dashboard, back to step 1 for next task
6. If verification fails: status → "In Progress", back to step 1 (implement-agent fixes)
7. When all tasks have "Finished" status with passing verification, `/work` spawns verify-agent for phase-level workflow
8. verify-agent: test against spec acceptance criteria
9. Issues found become new tasks, back to implement-agent

**The research workflow:**
1. `/work` encounters an unresolved decision blocking a task (or `/research` is invoked directly)
2. research-agent is spawned with decision record and project context
3. research-agent: gathers options, evaluates against criteria, checks compatibility with existing decisions
4. research-agent: populates decision record comparison matrix and option details, writes research archive
5. research-agent: updates decision status to `proposed` (ready for user selection)
6. User selects option via checkbox → `/work` auto-updates status to `approved` → dependent tasks unblock

**The review workflow** (via `/iterate review`):
1. `/iterate` detects active spec with completed tasks (or user explicitly requests review)
2. Reviews implementation artifacts across completed tasks for quality patterns
3. Assesses: architecture coherence, integration quality, pattern consistency, cross-cutting concerns, technical debt, decision alignment
4. Presents findings and suggestions — purely advisory, no state changes
5. User applies suggestions manually, then continues with `/work`

This separation — both logical and contextual — produces higher quality output than a single agent could achieve alone.

---

## Parallel Execution

By default, `/work` dispatches multiple tasks concurrently when they are independent. Each parallel task still runs the full atomic implement → verify cycle. The coordinator manages batching, result collection, and a single dashboard regeneration.

### Eligibility Criteria

A task is eligible for parallel dispatch when ALL conditions are met:

| Condition | Rationale |
|-----------|-----------|
| Status is "Pending" | Only unstarted tasks can be batched |
| Owner is not "human" | Human tasks require manual action |
| All dependencies are "Finished" | No unresolved blockers |
| Task belongs to current active phase | Phase N+1 blocked until Phase N complete |
| All decision dependencies are resolved | Pending decisions block dependent tasks |
| Difficulty < 7 | Complex tasks need breakdown first |
| `files_affected` don't overlap with other batch tasks | Prevents file conflicts |

Tasks with empty `files_affected` and no `parallel_safe: true` are excluded from parallel batches (unknown file impact). Set `parallel_safe: true` on research/analysis tasks that have no file side effects.

### How It Works

1. **Gather candidates** — `/work` collects all eligible tasks
2. **Build conflict-free batch** — Pairwise comparison of `files_affected` using the file conflict detection algorithm (see `.claude/support/reference/parallel-execution.md` § "File Conflict Detection Algorithm"). Two paths conflict if they are an exact match OR one is a directory containing the other (e.g., `src/` conflicts with `src/auth.py`). Paths are normalized before comparison. Tasks with conflicts are tracked in a `held_back` list with the specific conflict reason (task ID and shared files)
3. **Annotate held-back tasks** — Add `conflict_note` to held-back task JSONs (surfaced in the dashboard's Status column); cap batch at `max_parallel_tasks`
4. **Dispatch** — If batch size >= 2, set all to "In Progress" and spawn parallel agents (using `run_in_background: true`) via Claude Code's `Task` tool. Each agent reads `implement-agent.md` and runs Steps 2/4/5/6a/6b independently
5. **Incremental re-dispatch** — Poll for agent completion. When an agent finishes, re-run eligibility assessment: tasks whose file conflicts are now resolved become eligible and can be dispatched immediately (even while other agents are still running). Clear `conflict_note` from newly-dispatched tasks
6. **Post-parallel cleanup** — After all agents finish: final parent auto-completion check, single dashboard regeneration (clears remaining `conflict_note` fields), operational checks (see `/work` Step 6)

### Constraints

- **Verification is still per-task** — Each agent runs its own implement → verify cycle
- **Dashboard regeneration is coordinator-only** — Parallel agents do NOT regenerate the dashboard; the `/work` coordinator does it once after all agents finish
- **Parent auto-completion is deferred** — The coordinator checks parent completion after collecting all results, preventing races when siblings finish simultaneously
- **Phase-level verification remains sequential** — Runs once when ALL tasks are done
- **Conflict notes are transient** — `conflict_note` fields are cleaned up during post-parallel dashboard regeneration

### Configuration

In spec frontmatter (optional — defaults apply if absent):

```yaml
parallel_execution:
  max_parallel_tasks: 3    # default: 3
  enabled: true            # default: true
```

Set `enabled: false` to force sequential execution for the entire project.

### Fallback to Sequential

Parallel execution falls back to sequential (one task at a time) when:
- Only one eligible task exists
- All eligible tasks have file conflicts with each other
- `parallel_execution.enabled` is `false`
- A single task is specified via `/work {task-id}`

---

## Implementation Stages

When decomposing the spec into execute-phase tasks, organize them into logical stages:

| Stage | Focus | Examples |
|-------|-------|----------|
| **Foundation** | Setup, core infrastructure, initial research | Project structure, database schema, vendor research, requirements gathering |
| **Core Features** | Main functionality from spec | Primary user flows, API endpoints, procurement, key deliverables |
| **Polish** | Edge cases, error handling, refinement | Validation, error messages, budget reconciliation, final reviews |
| **Validation** | Testing, documentation, verification | Unit tests, integration tests, documentation, acceptance checks |

**Note:** These are organizational stages for tasks within the Execute phase, not to be confused with workflow phases (Spec → Execute → Verify).

---

## The `/work` Command as Coordinator

The `/work` command handles coordination (no separate orchestrator agent):

```
User → /work → Specialist Agent → /work → User
         ↓            ↓              ↓
    Analyze state  Do focused    Report results
    Check spec     work
```

**What `/work` handles:**
- Analyze current state
- Check requests against spec
- Decompose spec into tasks (when needed)
- Complete tasks (`/work complete`)
- Select appropriate agent
- Pass context to agent
- Collect questions
- Trigger checkpoints
- Report progress
- Auto-sync dashboard after changes

---

## Handoff Protocol

### /work → Specialist

Provides: current phase, spec summary, recent activity, task to do, constraints (already-asked questions, scope limits).

### Specialist → /work

Returns: what was completed, files modified, status updates, questions generated, recommendations, issues encountered.

---

## Phase Transitions

### Spec → Execute

**Trigger:** Spec exists at `.claude/spec_v{N}.md` and is complete

**Handoff includes:**
- Specification document
- Acceptance criteria
- Constraints and requirements

**What /work does:**
- Verify spec exists and has content
- Update spec `status` from `draft` to `active`
- Decompose spec into tasks (if no tasks exist)
- Present checkpoint to human
- Read and follow implement-agent workflow for first available task

### Execute → Verify (Phase-Level)

**Trigger:** All execute tasks finished AND all passed per-task verification

**Handoff includes:**
- List of completed tasks with per-task verification results
- Files modified
- Any discovered issues
- Self-review notes and verification notes

**What /work does:**
- Present checkpoint to human
- Read and follow verify-agent phase-level workflow with implementation summary

### Verify → Complete

**Trigger:** Verify agent reports verification passed and writes a valid result to `.claude/verification-result.json`

**Handoff includes:**
- Test results
- Acceptance criteria validation
- Issues found (if any)
- Recommendations
- Persisted verification result (`.claude/verification-result.json`)

**What /work does:**
- Check `.claude/verification-result.json` for a valid passing result
- Update spec `status` from `active` to `complete`
- Update dashboard with completion summary
- Present final checkpoint to human
- Project complete (or loop back if issues)

**Verification result validity:** The result is valid when `result` is `"pass"`, `spec_fingerprint` matches the current spec, and no tasks changed since the verification `timestamp`. If the spec changes or new tasks appear, the result is automatically invalidated and `/work` re-routes to verification.

---

## Spec Status Transitions

The spec metadata `status` field tracks the project lifecycle:

| Status | Meaning | Trigger |
|--------|---------|---------|
| `draft` | Spec is being written | Initial creation |
| `active` | Spec is being implemented | Decomposition begins (Spec → Execute) |
| `complete` | All work done and verified | Verification passes (Verify → Complete) |

**Rules:**
- Only `/work` updates the spec status (not manual edits)
- Transitioning back from `complete` to `active` happens automatically when the spec is modified and new tasks are created
- The status is in the YAML frontmatter of `.claude/spec_v{N}.md`

---

## Human Checkpoints

Humans are involved at:

### Phase Boundaries
When transitioning between phases:
- Spec → Execute: "Specification complete. Ready to implement?"
- **Phase N → Phase N+1** (within Execute): Surfaced as a dashboard Action Required item with a checkbox in a `<!-- PHASE GATE:{N}→{N+1} -->` marker. `/work` blocks until the user checks the box and re-runs. Once approved, the marker becomes `<!-- PHASE GATE:{N}→{N+1} APPROVED -->` so it won't re-trigger on subsequent runs.
- **Execute → Verify**: When all tasks are complete, the dashboard shows a "Verification Pending" item in Action Required, and the critical path displays "🤖 Phase verification → Done" instead of "All tasks complete!". Phase-level verification runs automatically on the next `/work`.
- Verify → Complete: "Verification passed. Ready to ship?"

### Spec Misalignment
When requests don't align with spec:
- /work surfaces the misalignment
- Options: add to spec, proceed anyway, or skip
- Keeps spec as source of truth

### Spec Drift (Granular Reconciliation)
When spec changes after tasks were decomposed:
- /work detects which specific sections changed
- Shows diff of changed content
- Groups affected tasks by section
- Options per section: apply suggestions, review individually, or skip
- Enables targeted updates without re-decomposing all tasks

### Quality Gate Failures
When something goes wrong:
- Tests fail
- Specification violations found
- Critical issues discovered

### Question Batches
When questions accumulate:
- Non-trivial questions need human input
- Blocking questions prevent progress

---

## Questions System

During execution, when implement-agent or verify-agent encounter something they can't resolve autonomously — a spec ambiguity, a technical choice needing user input, a dependency question — they write it to `.claude/support/questions/questions.md` under categories: Requirements, Technical, Scope, Dependencies. Questions are surfaced to the user in the dashboard's Action Required section at natural checkpoints.

**Blocking vs Non-Blocking:**
- `[BLOCKING]` prefix → cannot proceed, triggers immediate checkpoint
- Non-blocking → note assumption, present at next phase boundary

**Checkpoints where questions are surfaced:**

| Checkpoint | Trigger Condition | Question Type Presented |
|------------|-------------------|-------------------------|
| **Immediate** | `[BLOCKING]` question added | Blocking only — work halts until answered |
| **After task completion** | Task transitions to "Finished" | All unanswered questions (blocking + non-blocking) |
| **Phase boundary (Execute → Verify phase-level)** | All tasks in phase finished | All unanswered questions |
| **Phase boundary (Verify phase-level → Complete)** | Phase-level verification passes | All unanswered questions |
| **Quality gate failure** | Tests fail, spec violation detected | All unanswered questions |
| **Manual checkpoint** | User runs `/work` after answering questions in questions.md | All unanswered questions (validation that answers were captured) |

**At checkpoints:** Group by category, prioritize blocking first, present to human, clear answered questions to "Answered Questions" table when resolved.

---

## Error Handling

### Agent Failure

If an agent fails:
1. /work logs error
2. Preserves partial progress
3. Presents error to human
4. Awaits human direction

### Conflicting State

If state is inconsistent:
1. Document the conflict
2. Ask human to clarify
3. Do not proceed until resolved

### Infinite Loops

If work isn't progressing:
1. After 3 iterations, checkpoint
2. Present situation to human
3. Get explicit direction

---

## Spec Change and Feature Addition Workflow

When you need to add features or change requirements after initial decomposition, follow this workflow:

### Steps

1. **User edits the spec** — Update `.claude/spec_v{N}.md` directly (add sections, modify requirements, change acceptance criteria)
2. **User runs `/work`** — Auto-detect mode picks up the change
3. **`/work` detects drift** — Compares spec fingerprint against task fingerprints (see `.claude/support/reference/drift-reconciliation.md` § "Spec Drift Detection")
4. **`/work` shows what changed** — Granular section diffs showing added, modified, and removed content
5. **User confirms** — Per-section options: apply suggestions, review individually, or skip
6. **Tasks are created/updated** — Only for changed sections (unchanged tasks are preserved)
7. **Implementation proceeds** — Execute phase runs on new/updated tasks
8. **Verification confirms** — Verify phase runs against updated acceptance criteria

### Key Principles

- **Transparency first:** The user always sees what Claude thinks changed before any action is taken
- **Incremental by default:** Only affected tasks are updated; completed work is preserved
- **Full re-decomposition is rare:** Only needed for major rewrites or architecture changes (see table below)
- **Spec stays as source of truth:** Tasks follow the spec, not the other way around

### Adding a New Feature

1. Add a new `##` section to the spec describing the feature
2. Run `/work` — it detects the new section
3. Confirm the new tasks to be created
4. Existing tasks remain untouched

### Modifying an Existing Feature

1. Edit the relevant `##` section in the spec
2. Run `/work` — it shows the diff and affected tasks
3. Choose how to update each affected task
4. Unaffected tasks remain untouched

### Removing a Feature

1. Delete the `##` section from the spec
2. Run `/work` — it flags tasks tied to the removed section
3. Choose to mark them out-of-spec or delete them

### Versioning Conventions

- **Single-spec invariant**: Exactly one `spec_v{N}.md` exists in `.claude/` at any time
- **Version discovery**: `/work` globs for `spec_v*.md` and uses the highest N
- **Direct edits are safe**: The decomposed snapshot preserves the pre-edit state; drift detection handles reconciliation. After editing, run `/work` to continue building (detects changes and reconciles affected tasks) or `/iterate` to keep refining
- **Version bumps** are for major transitions (phase completion, inflection points, major pivots) — not for routine edits
- **Substantial change detection**: `/work` evaluates change magnitude and suggests a version bump when edits are large enough
- **Version Transition Procedure**: Archive → Copy → Bump frontmatter → Remove old (see `iterate.md` § "Version Transition Procedure")
- **Task migration**: Finished tasks keep old provenance; pending/in-progress tasks are migrated (see `.claude/support/reference/drift-reconciliation.md` § "Task Migration on Version Transition")
- Each decomposition saves a snapshot to `.claude/support/previous_specifications/`

---

## Spec Drift and Reconciliation

When the specification evolves after tasks are decomposed, granular reconciliation helps keep tasks aligned without starting over.

### How It Works

1. **At decomposition time:**
   - Full spec is hashed and stored in each task (`spec_fingerprint`)
   - Each section is individually hashed (`section_fingerprint`)
   - A snapshot is saved for diff generation (`section_snapshot_ref`)

2. **When /work runs:**
   - Current spec hash is compared to task fingerprints
   - If different, section-level analysis identifies which parts changed
   - Only affected tasks are flagged for review

3. **Reconciliation UI:**
   - Shows diff of changed sections
   - Groups affected tasks by section
   - Offers targeted update options

### Reconciliation Options

| Option | Effect |
|--------|--------|
| **Apply suggestions** | Auto-update task descriptions based on spec changes |
| **Review individually** | Step through each affected task one by one |
| **Skip section** | Acknowledge change without updating tasks |
| **Mark out-of-spec** | Flag task as no longer aligned with spec |

### Benefits

- **Targeted updates**: Only tasks from changed sections need review
- **Visible diffs**: See exactly what changed in each section
- **Preserves work**: Unchanged sections and their tasks remain intact
- **Backward compatible**: Tasks without section fingerprints fall back to full-spec comparison

### When to Re-decompose vs Reconcile

| Scenario | Recommendation |
|----------|---------------|
| Minor clarifications | Reconcile - update affected tasks |
| New section added | Create new tasks for new section only |
| Section deleted | Mark affected tasks out-of-spec or delete |
| Major rewrite | Re-decompose from scratch |
| Architecture change | Re-decompose from scratch |

---

## Out-of-Spec Task Handling

Tasks can be marked `out_of_spec: true` in two ways:
1. **User request** — `/work` spec check offers "Proceed anyway" for requests not in spec
2. **Verify-agent recommendations** — verify-agent creates recommendation tasks for improvements beyond acceptance criteria

### Key Rules

- **Out-of-spec tasks are excluded from phase routing.** The auto-detect table in `/work` only considers spec tasks when determining phase (Execute vs Verify vs Complete). This prevents the verify → execute → verify infinite loop.
- **Out-of-spec tasks require user approval before execution.** `/work` presents pending out-of-spec tasks at phase boundaries with Accept/Reject/Defer options.
- **Accepted tasks** get `out_of_spec_approved: true` and can be executed by `/work`.
- **The completion condition** is "all spec tasks finished + verification passed," regardless of out-of-spec task status.

### Dashboard Display

Out-of-spec tasks appear in the Tasks section with a ⚠️ prefix:

```
| ID | Title | Status | Owner |
|----|-------|--------|-------|
| 13 | ⚠️ Add unit tests for CI | Pending | claude |
```

Unapproved out-of-spec tasks also appear in "Action Required" → "Reviews" to prompt user action.

---

## System Overview

Reference documentation for the environment builder system.

### Roles

**What you do:**
- Review the dashboard for your next action
- Click through to linked files when needed (review a document, configure something, test a feature)
- Signal completion back through the dashboard (checkboxes, feedback sections)
- Update the spec when requirements change
- Make decisions when Claude surfaces options

**What Claude does:**
- Tracks tasks and progress (in `.claude/tasks/`)
- Implements according to spec
- Surfaces everything user-facing through the dashboard — action items with links, not buried in internal files
- Validates work against acceptance criteria
- Regenerates the dashboard after every significant change

### Workspace

When you need to create temporary documents (research, analysis, drafts), use `.claude/support/workspace/`:

- **scratch/** - Throwaway notes, quick analysis, temporary thinking
- **research/** - Web search results, reference material, gathered context
- **drafts/** - Work-in-progress documents before they move to their final location

**Rules:**
- Never create working documents in the project root or other locations
- Use simple descriptive names (`api-comparison.md`, not `task-5-research.md`)
- When a draft is ready to become permanent, discuss where it should go

### Template Configuration Files

Two files control template behavior:

**sync-manifest.json** — Defines which files sync during `/health-check` template sync vs stay project-specific:

| Category | Purpose | Examples |
|----------|---------|----------|
| `sync` | Updated from template | Commands, agents, reference docs |
| `customize` | User-editable, template provides defaults | `.claude/CLAUDE.md`, README.md, questions/questions.md, documents/README.md |
| `ignore` | Project-specific data, never synced | Tasks, dashboard, decision records, learnings |

**settings.local.json** — Pre-approved permissions for consistent Claude Code behavior. Ensures the template works the same way for everyone using it.

### Project Structure

```
.claude/
├── CLAUDE.md                  # Instructions for Claude Code
├── dashboard.md               # Project Dashboard (auto-generated)
├── verification-result.json   # Latest verification outcome (written by verify-agent)
├── spec_v{N}.md               # Project specification (source of truth)
├── vision/                    # Vision documents from ideation
│   └── {project}-vision.md   # Design philosophy, future roadmap
├── tasks/                     # Task data
│   ├── task-*.json           # Individual task files
│   └── archive/              # Completed tasks (when count exceeds 100)
├── commands/                  # /work and task commands
├── agents/                    # Specialist agents
│   ├── implement-agent.md    # Task execution
│   ├── verify-agent.md       # Validation against spec
│   └── research-agent.md     # Decision investigation
├── support/                   # Supporting documentation
│   ├── reference/            # Schemas, guides, definitions
│   │   ├── README.md          # Index of all reference files
│   │   ├── shared-definitions.md
│   │   ├── task-schema.md
│   │   ├── workflow.md
│   │   ├── paths.md
│   │   ├── decisions.md
│   │   ├── spec-checklist.md
│   │   ├── extension-patterns.md
│   │   ├── dashboard-regeneration.md
│   │   ├── drift-reconciliation.md
│   │   ├── parallel-execution.md
│   │   └── desktop-project-prompt.md
│   ├── decisions/            # Decision documentation
│   │   ├── decision-*.md     # Individual decision records
│   │   └── .archive/         # Research documents
│   ├── learnings/            # Project-specific patterns (see README.md)
│   │   └── README.md         # Categories, format, maintenance guidelines
│   ├── previous_specifications/  # Spec snapshots at decomposition (for drift detection)
│   ├── workspace/            # Claude's working area (gitignored, see README.md)
│   │   ├── README.md         # Directory rules, file placement guide
│   │   ├── scratch/          # Temporary notes, quick analysis
│   │   ├── research/         # Web search results, reference material
│   │   └── drafts/           # WIP docs before final location
│   ├── questions/            # Questions for human input
│   │   ├── README.md         # Workflow and categories
│   │   └── questions.md      # Active questions and archive
│   └── documents/            # User-provided reference files (PDFs, contracts, etc.)
│       └── README.md         # Conventions and file placement
├── sync-manifest.json
├── settings.local.json
└── version.json
```
