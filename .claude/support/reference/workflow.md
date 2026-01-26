# Workflow Guide

The Spec → Execute → Verify workflow for autonomous multi-phase projects.

## Overview

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│   Spec   │ → │ Execute  │ → │  Verify  │
│          │    │          │    │          │
│ Define   │    │ Build    │    │ Validate │
│ what     │    │ it       │    │ it works │
└──────────┘    └──────────┘    └──────────┘
     ↑                               │
     └───── (if issues found) ──────┘
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

**Process:** Manual (human-guided via specification_creator)

To create or revise the spec, start a Claude Code session from `.claude/specification_creator/`. Claude will guide you through iterative Q&A but you edit the spec directly.

### Execute Phase

**Goal:** Build the implementation

**Activities:**
- Decompose spec into tasks (handled by /work if no tasks exist)
- Work through tasks in dependency order
- Write code and create files
- Self-review changes
- Document completion notes
- Flag discovered issues

**Exit Criteria:**
- All tasks marked Finished
- No blocked tasks remain
- Code follows project conventions
- Ready for verification

**Agent:** implement-agent

### Verify Phase

**Goal:** Confirm it works correctly

**Activities:**
- Run test suite
- Validate acceptance criteria
- Check non-functional requirements
- Identify issues
- Create report

**Exit Criteria:**
- Tests pass
- Acceptance criteria validated
- No critical issues remain
- Human approved final state

**Agent:** verify-agent

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
1. `/work` invokes implement-agent for pending tasks
2. implement-agent builds and marks tasks finished
3. When all tasks are done, `/work` invokes verify-agent
4. verify-agent tests against spec acceptance criteria
5. Issues found become new tasks, back to implement-agent

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

When invoking a specialist, /work provides:

```markdown
## Context
- Current phase: [phase]
- Spec summary: [key requirements]
- Recent activity: [what happened]

## Task
[What the specialist should do]

## Constraints
- Questions to avoid: [already asked]
- Scope limits: [if any]
```

### Specialist → /work

When completing work, agents return:

```markdown
## Completed
- [What was accomplished]

## Output
- [Files created/modified]
- [Status updates made]

## Questions Generated
- [New questions for human]

## Recommendations
- [Suggested next steps]

## Issues
- [Problems encountered]
```

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
- Decompose spec into tasks (if no tasks exist)
- Present checkpoint to human
- Invoke implement-agent with first available task

### Execute → Verify

**Trigger:** All execute tasks finished

**Handoff includes:**
- List of completed tasks
- Files modified
- Any discovered issues
- Self-review notes

**What /work does:**
- Present checkpoint to human
- Invoke verify-agent with implementation summary

### Verify → Complete

**Trigger:** Verify agent reports verification passed

**Handoff includes:**
- Test results
- Acceptance criteria validation
- Issues found (if any)
- Recommendations

**What /work does:**
- Present final checkpoint to human
- Project complete (or loop back if issues)

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

Questions accumulate during work in `.claude/support/questions.md`:

```markdown
## Requirements
- Should login require email verification?

## Technical
- [BLOCKING] What caching solution to use?
- Should we add rate limiting?

## Scope
- Is mobile support in v1?
```

**Categories:**
- **Requirements:** What the system should do
- **Technical:** How things should work
- **Scope:** What's in/out
- **Dependencies:** External systems/blockers

### Blocking vs Non-Blocking

**Blocking:** Cannot proceed without answer
- Mark with `[BLOCKING]` prefix
- Triggers immediate checkpoint

**Non-Blocking:** Can proceed with assumption
- Note assumption made
- Present at next phase boundary

### At Checkpoints

/work presents accumulated questions:

1. Group by category
2. Prioritize blocking questions
3. Present to human
4. Wait for answers
5. Clear answered questions
6. Continue work

**When presented:**
- At phase boundaries
- At quality gate failures
- When explicitly blocking

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
