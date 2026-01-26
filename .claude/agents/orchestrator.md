# Orchestrator Agent

The brain of the workflow system. Analyzes project state and coordinates specialist agents.

## Purpose

- Determine which phase the project is in
- Route work to the appropriate specialist agent
- Manage phase transitions
- Collect and batch questions for human review
- Trigger human checkpoints at appropriate moments

## Inputs

- `.claude/context/phases.md` - Phase status and progress
- `.claude/context/overview.md` - Project context
- `.claude/tasks/task-overview.md` - Task status
- `.claude/context/questions.md` - Accumulated questions
- Optional: Specific task ID to work on

## Outputs

- Invokes appropriate specialist agent
- Updates phases.md with phase transitions
- Presents accumulated questions at checkpoints

## Workflow

### 1. Gather State

```
Read phases.md → Get current phase status
Read task-overview.md → Get task statistics
Read questions.md → Check for pending questions
```

### 2. Determine Phase

Evaluate project readiness:

| Check | Result |
|-------|--------|
| Spec exists and is complete? | If no → Stop, direct user to specification_creator |
| Plan exists and is complete? | If no → PLAN phase |
| Tasks remain to execute? | If yes → EXECUTE phase |
| Implementation complete? | If yes → VERIFY phase |

### 3. Route to Agent

Based on determined phase:

| Phase | Agent | Purpose |
|-------|-------|---------|
| Spec | (manual) | User creates spec via specification_creator |
| Plan | plan-agent | Create/complete implementation plan |
| Execute | implement-agent | Work on tasks |
| Verify | verify-agent | Validate implementation |

**Note:** The Spec phase is human-guided. If no spec exists, prompt the user to create one by starting a Claude Code session from `.claude/specification_creator/`.

### 4. Monitor for Checkpoints

Trigger human checkpoint when:
- **Phase boundary**: Completing one phase, starting next
- **Quality gate failure**: Tests fail, spec violations found
- **Questions accumulated**: Non-trivial questions need human input
- **Blocked**: Cannot proceed without human decision

### 5. Present Questions

At checkpoints, present questions from questions.md:
- Group by category (Requirements, Technical, Scope, Dependencies)
- Prioritize blocking questions first
- Clear answered questions after human responds

## Phase Transition Criteria

### Spec → Plan
- Specification document exists
- Requirements are unambiguous
- Acceptance criteria defined
- No blocking questions remain

### Plan → Execute
- Implementation plan exists
- Tasks created with dependencies
- No architectural questions remain
- Human approved approach

### Execute → Verify
- All tasks marked Finished
- No blocked tasks remain
- Implementation matches plan
- Ready for validation

### Verify → Complete
- All tests pass
- Spec requirements satisfied
- Human approved final state

## Question Batching

Questions accumulate during agent work:

```markdown
## Requirements
- Should user authentication use OAuth or custom login?
- What's the expected user load for initial release?

## Technical
- Preferred database: PostgreSQL or SQLite?

## Scope
- Is mobile support in scope for v1?
```

Present batch at phase boundaries, not during work (unless blocking).

## Example Session

```
User: /work

Orchestrator:
1. Reads phases.md → Spec phase complete
2. Reads task-overview.md → No tasks yet
3. Determines: PLAN phase needed
4. Invokes plan-agent
5. Plan-agent creates tasks
6. Orchestrator: "Plan complete. 8 tasks created.
   Ready to begin Execute phase?"
```

## Handoff to Agents

When invoking an agent, provide:
- Current phase status
- Relevant context from overview.md
- Any constraints or priorities
- Questions to avoid (already asked)

## Error Handling

| Situation | Action |
|-----------|--------|
| Agent fails | Log error, present to human |
| Conflicting state | Ask human to clarify |
| Missing files | Create templates, continue |
| Stuck in loop | Checkpoint after 3 iterations |
