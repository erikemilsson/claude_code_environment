# Agent Integration Template

*Standard pattern for agent-invoked commands.*

## Agent Invocation Pattern

When a command invokes an agent:

```markdown
AGENT: [Agent Name]
PHASE: [Task Execution | Planning | Validation | etc.]
OWNERSHIP: [What the agent controls/validates]
```

## Standard Agent Responsibilities

### Execution Guardian
- Pre-execution validation gates
- Progress monitoring and checkpoints
- Confidence tracking
- Error recovery coordination
- Completion validation

### Task Orchestrator
- Subtask coordination
- Parent task status management
- Dependency tracking
- Task hand-off management

## Handoff Protocol

### Agent-to-Agent Handoff
```markdown
1. Source agent completes owned phase
2. Source documents state and findings
3. Source explicitly hands off: "Handing off to [Agent] for [Phase]"
4. Target agent receives context and continues
```

### Handoff Information Required
- Current state/progress
- Key findings or decisions
- Open items or concerns
- Recommended next steps

## Validation Gates by Agent

| Agent | Pre-Execution | During | Post-Execution |
|-------|---------------|--------|----------------|
| Execution Guardian | Task status, dependencies | Progress checkpoints | Completion criteria |
| Task Orchestrator | Breakdown feasibility | Subtask progress | Parent completion |

## State Transitions

```
pending → ignition → building → cruising → coasting/completed
                 ↓                    ↓
              stalling ←──────────────┘
                 ↓
              stopped
```

## Agent Scripts (When Available)

```bash
# Pre-execution validation
python scripts/validation-gates.py pre --task-id {ID}

# Progress checkpoints
python scripts/checkpoint-manager.py create --task-id {ID}

# Post-execution validation
python scripts/validation-gates.py post --task-id {ID}
```

## Manual Process (Fallback)

When scripts unavailable, agents follow their documented protocols manually:
1. Execute validation checks as listed
2. Document results in task notes
3. Make go/no-go decisions based on criteria
4. Log handoffs explicitly

## Related Documentation
- Agent definitions: `.claude/agents/`
- Agent config: `.claude/agent-config.json`
- Validation gates: `validation-gates.md`
