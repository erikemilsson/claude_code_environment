# Work Command

Context-aware entry point for the Spec→Plan→Execute→Verify workflow.

## Usage
```
/work [task-id]
```

## What It Does

1. **Analyzes project state** - Reads phases.md, tasks, and recent activity
2. **Determines current phase** - Spec, Plan, Execute, or Verify
3. **Routes to appropriate agent** - Invokes the specialist for that phase
4. **Accumulates questions** - Collects questions during work for batch presentation
5. **Triggers checkpoints** - Presents questions at phase boundaries or quality gate failures

## Phase Detection Logic

```
IF no spec exists OR spec incomplete:
  → Stop and prompt user to create spec via specification_creator

ELSE IF no plan exists OR plan incomplete:
  → Route to plan-agent

ELSE IF tasks exist AND work remains:
  → Route to implement-agent

ELSE IF implementation complete:
  → Route to verify-agent
```

**Note:** The Spec phase is manual. If no spec exists at `.claude/spec_v{N}.md`, direct the user to create one by starting a Claude Code session from `.claude/specification_creator/`.

## Process

### 1. State Analysis

Read and analyze:
- `.claude/context/phases.md` - Current phase status
- `.claude/context/overview.md` - Project context
- `.claude/tasks/task-overview.md` - Task status
- `.claude/context/questions.md` - Pending questions

### 2. Phase Determination

Determine which phase needs work:

| Condition | Phase | Agent |
|-----------|-------|-------|
| Missing or incomplete specification | Spec | (manual - specification_creator) |
| Missing or incomplete plan | Plan | plan-agent |
| Tasks pending | Execute | implement-agent |
| Work complete, needs validation | Verify | verify-agent |

### 3. Agent Invocation

Invoke the appropriate agent via Task tool with the orchestrator:
- Pass current context
- Let agent do focused work
- Collect questions during work

### 4. Question Handling

Questions accumulate in `.claude/context/questions.md` during work.

**Present questions when:**
- Phase boundary reached (transitioning to next phase)
- Quality gate failure (tests fail, spec violation)
- Agent explicitly requests human input

**Question format in questions.md:**
```markdown
## Requirements
- [Question about scope or features]

## Technical
- [Question about implementation approach]

## Scope
- [Question about boundaries or priorities]

## Dependencies
- [Question about external systems or blockers]
```

## Examples

```
# Start working (auto-detects what to do)
/work

# Continue work on specific task
/work 5

# After human answers questions, continue
/work
```

## Output

Reports:
- Current phase and what was done
- Any questions requiring human input
- Next steps or what's blocking progress
