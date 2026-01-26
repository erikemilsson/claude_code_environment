# Workflow Guide

The Spec → Plan → Execute → Verify workflow for autonomous multi-phase projects.

## Overview

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Spec   │ → │   Plan   │ → │ Execute  │ → │  Verify  │
│          │    │          │    │          │    │          │
│ Define   │    │ Design   │    │ Build    │    │ Validate │
│ what     │    │ how      │    │ it       │    │ it works │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     ↑                                               │
     └───────────── (if issues found) ──────────────┘
```

## Phase Details

### Spec Phase

**Goal:** Define what needs to be built

**Activities:**
- Document problem statement
- Define goals and non-goals
- List requirements (functional and non-functional)
- Create testable acceptance criteria
- Identify constraints

**Exit Criteria:**
- All blocking questions answered
- Acceptance criteria are testable
- Scope is clear
- Human approved specification

**Agent:** spec-agent

### Plan Phase

**Goal:** Design how to build it

**Activities:**
- Design architecture approach
- Define implementation phases
- Create tasks with dependencies
- Identify risks and mitigations
- Log significant decisions

**Exit Criteria:**
- All tasks created (difficulty <= 6)
- Dependencies mapped
- No architectural questions remain
- Human approved approach

**Agent:** plan-agent

### Execute Phase

**Goal:** Build the implementation

**Activities:**
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

## Human Checkpoints

Humans are involved at:

### Phase Boundaries
When transitioning between phases:
- Spec → Plan: "Specification complete. Ready to plan?"
- Plan → Execute: "Plan complete. Ready to implement?"
- Execute → Verify: "Implementation complete. Ready to verify?"
- Verify → Complete: "Verification passed. Ready to ship?"

### Quality Gate Failures
When something goes wrong:
- Tests fail
- Specification violations found
- Critical issues discovered

### Question Batches
When questions accumulate:
- Non-trivial questions need human input
- Blocking questions prevent progress

## The `/work` Command

Primary entry point for the workflow:

```
/work          # Start or continue work
/work 5        # Continue work on specific task
```

What it does:
1. Analyzes project state
2. Determines current phase
3. Routes to appropriate agent
4. Accumulates questions during work
5. Presents questions at checkpoints

## Questions System

Questions accumulate during work in `.claude/context/questions.md`:

```markdown
## Requirements
- Should login require email verification?

## Technical
- Preferred caching solution?

## Scope
- Is mobile support in v1?
```

**Categories:**
- **Requirements:** What the system should do
- **Technical:** How things should work
- **Scope:** What's in/out
- **Dependencies:** External systems/blockers

**When presented:**
- At phase boundaries
- At quality gate failures
- When explicitly blocking

## Best Practices

### Keep Phases Clean
- Don't code during Spec phase
- Don't change scope during Execute phase
- Don't skip Verify phase

### Respect Boundaries
- Complete current phase before moving on
- Get human approval at transitions
- Don't gold-plate

### Document Everything
- Log decisions as they're made
- Update phase status
- Note questions as they arise

### Handle Issues Gracefully
- Create tasks for discovered work
- Don't derail current task
- Flag blocking issues immediately
