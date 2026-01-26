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
