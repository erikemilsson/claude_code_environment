# Agent Handoff Guide

How agents coordinate in the Spec → Plan → Execute → Verify workflow.

## Agent Responsibilities

| Agent | Phase | Primary Responsibility |
|-------|-------|------------------------|
| Orchestrator | All | Route work, manage transitions |
| Spec Agent | Spec | Create specifications |
| Plan Agent | Plan | Create implementation plans |
| Implement Agent | Execute | Write code, complete tasks |
| Verify Agent | Verify | Test and validate |

## Orchestrator Role

The orchestrator is the coordinator:

```
User → Orchestrator → Specialist Agent → Orchestrator → User
         ↓                    ↓                ↓
    Analyze state       Do focused work    Report results
```

**Responsibilities:**
- Determine current phase
- Select appropriate agent
- Pass context to agent
- Collect questions
- Trigger checkpoints
- Report progress

## Handoff Protocol

### Orchestrator → Specialist

When invoking a specialist, provide:

```markdown
## Context
- Current phase: [phase]
- Project overview: [summary]
- Recent activity: [what happened]

## Task
[What the specialist should do]

## Constraints
- Questions to avoid: [already asked]
- Time/scope limits: [if any]
```

### Specialist → Orchestrator

When completing work, return:

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

### Spec → Plan

**Trigger:** Spec agent reports specification complete

**Handoff includes:**
- Completed specification document
- Acceptance criteria
- Constraints and requirements
- Any remaining non-blocking questions

**Orchestrator action:**
- Update phases.md (Spec: Complete, Plan: Active)
- Present checkpoint to human
- Invoke plan-agent with spec context

### Plan → Execute

**Trigger:** Plan agent reports plan complete

**Handoff includes:**
- Architecture decisions
- Task list with dependencies
- Risk assessment
- Decisions log updates

**Orchestrator action:**
- Update phases.md (Plan: Complete, Execute: Active)
- Present checkpoint to human
- Invoke implement-agent with first available task

### Execute → Verify

**Trigger:** All execute tasks finished

**Handoff includes:**
- List of completed tasks
- Files modified
- Any discovered issues
- Self-review notes

**Orchestrator action:**
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

**Orchestrator action:**
- Update phases.md (Verify: Complete)
- Present final checkpoint to human
- Project complete (or loop back if issues)

## Question Handling

### During Agent Work

Agents add questions to questions.md:

```markdown
## Technical
- [BLOCKING] What caching solution to use?
- Should we add rate limiting?
```

### At Checkpoints

Orchestrator presents accumulated questions:

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
1. Orchestrator logs error
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

### For Orchestrator

- Always verify state before routing
- Don't skip checkpoints
- Present clear summaries
- Keep context flowing between agents

### For Transitions

- Verify exit criteria before transitioning
- Don't rush past checkpoints
- Preserve all context for next agent
- Update all status documents
