# Agent Handoff Guide

How agents coordinate in the Spec → Execute → Verify workflow.

## Agent Responsibilities

| Agent | Phase | Primary Responsibility |
|-------|-------|------------------------|
| (manual) | Spec | Human creates spec via specification_creator |
| Implement Agent | Execute | Write code, complete tasks |
| Verify Agent | Verify | Test and validate |

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
- Select appropriate agent
- Pass context to agent
- Collect questions
- Trigger checkpoints
- Report progress

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
- Update phases.md (Spec: Complete, Execute: Active)
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
- Update phases.md (Execute: Complete, Verify: Active)
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
- Update phases.md (Verify: Complete)
- Present final checkpoint to human
- Project complete (or loop back if issues)

## Spec Alignment Checks

When a user request doesn't align with spec, /work handles the conversation:

```
User: /work "Add feature X"
        ↓
/work checks against spec
        ↓
Not in spec → Surface it:
  "This isn't covered in the spec. Options:
   1. Add to spec: [suggestion]
   2. Proceed anyway
   3. Skip"
```

This keeps the spec as the living source of truth.

## Question Handling

### During Agent Work

Agents add questions to questions.md:

```markdown
## Technical
- [BLOCKING] What caching solution to use?
- Should we add rate limiting?
```

### At Checkpoints

/work presents accumulated questions:

1. Group by category
2. Prioritize blocking questions
3. Present to human
4. Wait for answers
5. Clear answered questions
6. Continue work

### Blocking vs Non-Blocking

**Blocking:** Cannot proceed without answer
- Mark with [BLOCKING] prefix
- Triggers immediate checkpoint

**Non-Blocking:** Can proceed with assumption
- Note assumption made
- Present at next phase boundary

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

## Best Practices

### For Specialists

- Stay focused on your phase
- Don't do work outside your responsibility
- Document everything for handoff
- Flag issues early
- Report spec misalignments back to /work

### For Transitions

- Verify exit criteria before transitioning
- Don't rush past checkpoints
- Preserve all context for next phase
- Update all status documents
