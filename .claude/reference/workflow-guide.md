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

## The `/work` Command

Primary entry point for the workflow:

```
/work              # Start or continue work
/work 5            # Continue work on specific task
/work "request"    # Handle ad-hoc request (gets spec-checked)
```

What it does:
1. Checks request against spec (if request provided)
2. Analyzes project state
3. Determines current phase
4. Decomposes spec into tasks (if needed)
5. Routes to appropriate agent
6. Accumulates questions during work
7. Presents questions at checkpoints

## Spec-First Philosophy

All work flows from the specification:

```
Spec (source of truth)
  ↓
Tasks (decomposed from spec, or ad-hoc with spec check)
  ↓
Implementation (by implement-agent)
  ↓
Verification (against spec, by verify-agent)
```

**For ad-hoc requests:**
- /work checks against spec
- Significant additions prompt spec update discussion
- Minor fixes proceed without spec change
- This keeps the spec as a living, accurate document

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

### Respect the Spec
- Check requests against spec
- Update spec intentionally, not accidentally
- Key decisions belong in spec, not just in code

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
