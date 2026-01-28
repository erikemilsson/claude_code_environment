# Workflow Guide

The Spec → Execute → Verify workflow for autonomous multi-phase projects.

## Overview

```
┌──────────┐    ┌───────────────────────────────────────┐    ┌──────────┐
│   Spec   │ -> │              Execute                   │ -> │  Verify  │
│          │    │  ┌────────────┐   ┌────────────────┐  │    │ (phase)  │
│ Define   │    │  │ Implement  │ -> │ Verify (task)  │  │    │          │
│ what     │    │  │ task N     │   │ task N         │  │    │ Validate │
│          │    │  └────────────┘   └────────────────┘  │    │ all ACs  │
│          │    │       ^                │               │    │          │
│          │    │       └── (if fail) ───┘               │    │          │
│          │    │       v (if pass)                      │    │          │
│          │    │  next task...                          │    │          │
└──────────┘    └───────────────────────────────────────┘    └──────────┘
     ^                                                            │
     └──────────── (if issues found) ────────────────────────────┘
```

**Core principle:** The spec is the living source of truth. All work should align with it, or the spec should be updated intentionally.

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
- Write code and create files
- Self-review changes
- Per-task verification after each task completion
- Document completion notes
- Flag discovered issues

**Exit Criteria:**
- All tasks have status "Finished" with passing per-task verification
- No blocked tasks remain
- Code follows project conventions
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
- Validate code quality (no TODOs, follows patterns)
- Check integration boundaries (dependencies consumed correctly, outputs match downstream expectations)

**Output:** `task_verification` field written to task JSON with per-check pass/fail

**What happens after per-task verification:**
- **Pass:** Task status set to "Finished" (from "Awaiting Verification"). `/work` proceeds to next pending task.
- **Fail:** Task set back to "In Progress". implement-agent fixes, then re-verification. Maximum 2 re-verification attempts before escalation to human.

#### Tier 2: Phase-Level Verification

**Goal:** Confirm the full implementation matches the spec's acceptance criteria

**When it triggers:** Automatically when `/work` detects all spec tasks are finished AND all have passing per-task verification (auto-detect mode), or manually when the user runs `/work` after completing all tasks.

**Activities:**
- Run existing test suite (if available)
- Validate each spec acceptance criterion individually
- Check code quality, security, and integration
- Identify and categorize issues (critical/major/minor)
- Create fix tasks for issues found (in-spec bugs as regular tasks; recommendations as `out_of_spec: true`)
- Write verification result to `.claude/verification-result.json`
- Generate verification report for the user
- Reference per-task verification results as evidence for individual checks

**Output:** A structured report showing:
- Pass/fail status for each acceptance criterion
- Issues found, categorized by severity
- Tasks created for fixes (if any)
- Overall result: `pass`, `fail`, or `pass_with_issues`

**What happens after phase-level verification:**
- **Pass:** `/work` transitions to Complete phase. Spec status updates to `complete`.
- **Pass with issues:** Minor issues noted but no critical/major blockers. Same as pass — project completes, issues logged for future work.
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
3. Verification result can still be `"pass_with_issues"` (spec criteria met)
4. `/work` presents recommendations to user for Accept/Reject/Defer
5. Accepted tasks are executed independently; they don't block project completion

**Exit Criteria:**
- All acceptance criteria pass (or failures are documented and accepted)
- No critical issues remain
- Verification result persisted to `.claude/verification-result.json`
- Human approved final state

**Agent:** verify-agent (see `.claude/agents/verify-agent.md` for detailed workflow)

---

## Agent Synergy: Implement + Verify

This project uses two specialist agents that check each other's work:

| Agent | Role | Focus |
|-------|------|-------|
| **implement-agent** | Builder | Executes tasks, writes code, marks tasks finished |
| **verify-agent** | Validator | Tests against spec, finds issues, ensures quality |

**Why two agents?**
A single agent implementing and validating its own work has blind spots.
By separating concerns:
- implement-agent focuses purely on building (no self-validation bias)
- verify-agent validates against the spec with fresh perspective
- Issues caught by verify-agent become new tasks for implement-agent

**The workflow:**
1. `/work` reads and follows implement-agent workflow for the next pending task
2. implement-agent: build, self-review, update status to "Awaiting Verification"
3. implement-agent Step 6b: trigger verify-agent per-task workflow (atomic with step 2)
4. verify-agent: verify files, spec alignment, quality, integration boundaries
5. If verification passes: status → "Finished", regenerate dashboard, back to step 1 for next task
6. If verification fails: status → "In Progress", back to step 1 (implement-agent fixes)
7. When all tasks have "Finished" status with passing verification, `/work` reads verify-agent phase-level workflow
8. verify-agent: test against spec acceptance criteria
9. Issues found become new tasks, back to implement-agent

This separation produces higher quality output than a single agent could achieve alone.

---

## Implementation Stages

When decomposing the spec into execute-phase tasks, organize them into logical stages:

| Stage | Focus | Examples |
|-------|-------|----------|
| **Foundation** | Setup, core infrastructure, basic scaffolding | Project structure, database schema, auth setup |
| **Core Features** | Main functionality from spec | Primary user flows, API endpoints, business logic |
| **Polish** | Edge cases, error handling, UX | Validation, error messages, loading states |
| **Validation** | Testing, documentation, verification | Unit tests, integration tests, API docs |

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

**Verification result validity:** The result is valid when `result` is `"pass"` or `"pass_with_issues"`, `spec_fingerprint` matches the current spec, and no tasks changed since the verification `timestamp`. If the spec changes or new tasks appear, the result is automatically invalidated and `/work` re-routes to verification.

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
- Execute → Verify: "Implementation complete. Ready to verify?"
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

Questions accumulate in `.claude/support/questions.md` under categories: Requirements, Technical, Scope, Dependencies.

**Blocking vs Non-Blocking:**
- `[BLOCKING]` prefix → cannot proceed, triggers immediate checkpoint
- Non-blocking → note assumption, present at next phase boundary

**At checkpoints:** Group by category, prioritize blocking, present to human, clear when answered.

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
3. **`/work` detects drift** — Compares spec fingerprint against task fingerprints (see Step 1b in work.md)
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

- Spec files follow `spec_v{N}.md` naming
- Increment version number for major scope changes (new spec_v2.md)
- Minor edits stay in the same version
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

Out-of-spec tasks appear in the All Tasks table with a ⚠️ prefix:

```
| ID | Title | Status | Owner |
|----|-------|--------|-------|
| 13 | ⚠️ Add unit tests for CI | Pending | claude |
```

Unapproved out-of-spec tasks also appear in the "Needs Your Attention" section under "Reviews & Approvals" to prompt user action.

---

## Best Practices

### Keep Phases Clean
- Don't code during Spec phase
- Don't change scope during Execute phase
- Don't skip Verify phase

### Respect the Spec
- Check requests against spec
- Update spec intentionally, not accidentally
- Key decisions belong in spec, not just in code

### Respect Boundaries
- Complete current phase before moving on
- Get human approval at transitions
- Don't gold-plate

### For Specialists
- Stay focused on your phase
- Don't do work outside your responsibility
- Document everything for handoff
- Flag issues early
- Report spec misalignments back to /work

### Document Everything
- Log decisions as they're made
- Update phase status
- Note questions as they arise

### Handle Issues Gracefully
- Create tasks for discovered work
- Don't derail current task
- Flag blocking issues immediately
