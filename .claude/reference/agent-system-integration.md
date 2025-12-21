# Agent System Integration Guide

*Created: 2025-12-17*

## Status

**EXPERIMENTAL / ASPIRATIONAL**

The agent system is a well-designed architectural pattern for organizing Claude Code workflows into three specialized agents. However, as of 2025-12-17, this system is:

- ✅ **Fully Documented**: Comprehensive documentation exists
- ✅ **Well Architected**: Clear boundaries and handoff protocols defined
- ⚠️ **Partially Implemented**: Some supporting scripts exist (Python scripts from Task 79)
- ❌ **Not Integrated**: No automatic agent invocation in Claude Code
- ❌ **Not Tested**: No integration tests or validation

## Purpose

This guide explains:
1. What the agent system is designed to do
2. Current implementation status
3. How to use it (when fully implemented)
4. How to integrate it with existing workflows
5. Roadmap to full implementation

## The Agent System Vision

### Three Specialized Agents

#### 1. Environment Architect
- **Purpose**: Project initialization and template selection
- **Phase**: Before project structure exists
- **Files**:
  - Definition: `.claude/agents/environment-architect.md`
  - Scripts: `scripts/bootstrap.py`, `scripts/pattern-matcher.py`
  - Commands: `.claude/commands/smart-bootstrap.md`, `.claude/commands/bootstrap.md`

#### 2. Task Orchestrator
- **Purpose**: Task hierarchy and breakdown management
- **Phase**: Task planning and organization
- **Files**:
  - Definition: `.claude/agents/task-orchestrator.md`
  - Scripts: `scripts/task-manager.py`, `scripts/dependency-analyzer.py`
  - Commands: `.claude/commands/breakdown.md`, `.claude/commands/sync-tasks.md`

#### 3. Execution Guardian
- **Purpose**: Task execution with validation gates
- **Phase**: Active task execution
- **Files**:
  - Definition: `.claude/agents/execution-guardian.md`
  - Scripts: `scripts/validation-gates.py`, `scripts/checkpoint-manager.py`
  - Commands: `.claude/commands/complete-task.md`, `.claude/commands/check-risks.md`

### Key Design Principles

1. **Lifecycle-Based Separation**: Each agent owns one phase (init → plan → execute)
2. **Exclusive Ownership**: Each script/command belongs to exactly one agent
3. **State-Based Exclusivity**: Task status determines which agent can act
4. **Automatic Handoffs**: Agents pass control based on defined triggers

## Current Implementation Status

### What Exists

#### Documentation (Complete)
- [x] Agent definitions: `.claude/agents/environment-architect.md`, `task-orchestrator.md`, `execution-guardian.md`
- [x] Agent README: `.claude/agents/README.md`
- [x] Architecture doc: `.claude/agent-docs/architecture.md`
- [x] Handoff protocol: `.claude/agent-docs/handoff-protocol.md`
- [x] Agent config: `.claude/agent-config.json`
- [x] Use-agent command: `.claude/commands/use-agent.md`

#### Scripts (Partial)
Created as part of Task 79 (Implement Scripting Automation):
- [x] `scripts/bootstrap.py` - Environment initialization (Environment Architect)
- [x] `scripts/task-manager.py` - Task operations (Task Orchestrator)
- [x] `scripts/validation-gates.py` - Validation gates (Execution Guardian)
- [x] `scripts/checkpoint-manager.py` - Checkpoints (Execution Guardian)
- [x] `scripts/dependency-analyzer.py` - Dependencies (Task Orchestrator)
- [x] `scripts/breakdown-suggester.py` - Breakdown (Task Orchestrator)
- [x] `scripts/pattern-matcher.py` - Template detection (Environment Architect)

### What's Missing

#### Integration Layer
- [ ] Automatic agent selection logic
- [ ] Agent invocation mechanism
- [ ] Handoff execution system
- [ ] Conflict detection and prevention
- [ ] Performance metrics tracking

#### Command Integration
- [ ] Commands don't automatically invoke agents
- [ ] No agent boundary enforcement
- [ ] Handoff triggers not implemented
- [ ] State-based exclusivity not enforced

#### Testing
- [ ] No integration tests
- [ ] No agent workflow tests
- [ ] No handoff scenario tests
- [ ] No boundary violation detection

## How to Use (Current State)

### Without Agent System (Current Workflow)

Currently, you use commands directly:

```bash
# Create environment
"Create environment from spec: requirements.md"
→ Uses smart-bootstrap.md directly

# Break down task
"Break down task 42"
→ Uses breakdown.md directly

# Complete task
"Complete task 42_1"
→ Uses complete-task.md directly
```

### With Agent System (Intended Workflow)

When fully implemented, you would:

```bash
# System automatically selects agent
"Create environment from spec: requirements.md"
→ Analyzes context (empty dir)
→ Selects Environment Architect
→ Invokes smart-bootstrap.md
→ Handoff to Task Orchestrator if needed

# Task breakdown
"Break down task 42"
→ Analyzes task (difficulty 8, status Pending)
→ Selects Task Orchestrator
→ Invokes breakdown.md
→ Handoff to Execution Guardian when ready

# Task execution
"Complete task 42_1"
→ Analyzes task (status changes to In Progress)
→ Selects Execution Guardian
→ Runs validation gates
→ Invokes complete-task.md
→ Handoff to Task Orchestrator if parent complete
```

## Integration with Existing System

### Current Command Workflow

Existing commands work independently:
1. User invokes command directly (e.g., `/breakdown 42`)
2. Command reads task file
3. Command performs operation
4. Command updates task file
5. Command may call other commands (e.g., sync-tasks)

### Agent-Enhanced Workflow

Agent system would add coordination layer:
1. **Context Analysis**: Determine current state and requirements
2. **Agent Selection**: Choose appropriate agent based on state
3. **Boundary Check**: Verify agent can act on current state
4. **Command Invocation**: Agent executes appropriate command
5. **Handoff Detection**: Check if another agent should take over
6. **Handoff Execution**: Transfer control if needed

### Relationship to Scripts

Scripts (from Task 79) provide deterministic operations:
- **Without Agents**: Commands call scripts directly
- **With Agents**: Agents orchestrate script usage and ensure proper sequencing

Example:
```
Without Agents:
User → breakdown.md → task-manager.py (create subtasks) → sync-tasks

With Agents:
User Request → Agent Selector → Task Orchestrator → breakdown.md → task-manager.py → Handoff to Execution Guardian
```

## Implementation Roadmap

### Phase 1: Script Integration (Completed in Task 79)
- [x] Create Python scripts for deterministic operations
- [x] Ensure scripts handle task operations correctly
- [x] Test scripts independently

### Phase 2: Agent Layer (Current Gap)
- [ ] Implement agent selection logic (in Python or as Claude prompt)
- [ ] Create agent invocation mechanism
- [ ] Add state-based exclusivity checks
- [ ] Implement handoff trigger detection

### Phase 3: Command Integration
- [ ] Update commands to work with agent system
- [ ] Add agent boundary checks to commands
- [ ] Implement handoff calls in commands
- [ ] Test agent-command interaction

### Phase 4: Testing & Validation
- [ ] Create integration tests
- [ ] Test all handoff scenarios
- [ ] Validate boundary enforcement
- [ ] Measure performance impact

### Phase 5: Documentation & Rollout
- [ ] Update this guide with implementation details
- [ ] Create user guide for agent system
- [ ] Update CLAUDE.md with agent information
- [ ] Train users on agent-based workflow

## Design Decisions

### Why Three Agents?

**Separation of Concerns**:
- **Environment Architect**: One-time initialization, doesn't touch execution
- **Task Orchestrator**: Structure and organization, doesn't execute work
- **Execution Guardian**: Implementation and validation, doesn't modify structure

**Clear Handoffs**:
- EA → TO: When high-difficulty tasks created
- TO → EG: When subtasks ready for execution
- EG → TO: When subtask complete (check parent)

**Minimal Overlap**:
- Each agent has exclusive script/command ownership
- No shared responsibilities
- State-based exclusivity prevents conflicts

### Alternative Approaches Considered

#### Single Agent (Rejected)
- **Pros**: Simpler, no handoffs
- **Cons**: Unclear boundaries, risk of conflicts, harder to maintain

#### Many Agents (Rejected)
- **Pros**: More specialized roles
- **Cons**: Complex handoffs, more overhead, harder mental model

#### Two Agents (Considered)
- **Option**: Planning Agent + Execution Agent
- **Issue**: Initialization still needs separate handling
- **Decision**: Three agents provide clearer separation

### Agent vs. Direct Command Usage

**Agents Add Value When**:
- Multiple commands might apply (agent selects correct one)
- Handoffs needed between operations
- State validation required
- Consistency enforcement needed

**Direct Commands Better When**:
- User knows exactly which command to use
- No handoff needed
- Simple, isolated operation
- Learning/debugging the system

**Strategy**: Support both patterns
- Default: Agent-based for automated workflows
- Override: Direct command invocation for advanced users

## Configuration

### Agent Config File: `.claude/agent-config.json`

Defines:
- Agent ownership matrix (scripts, commands)
- Trigger conditions (when each agent activates)
- Boundary rules (what each agent can/cannot do)
- Handoff protocol (when to transfer control)
- Performance metrics (tracking agent effectiveness)

### Customization Points

**Modify Triggers**:
Edit `agent-config.json` → `agents.{agent-name}.triggers`

**Change Ownership**:
Update `agent-config.json` → `agents.{agent-name}.scripts/commands`

**Adjust Boundaries**:
Modify `agent-config.json` → `agents.{agent-name}.boundaries`

**Add Handoffs**:
Extend `agent-config.json` → `agents.{agent-name}.handoff_triggers`

## Using Agent System Today

### Conceptual Framework

Even without full implementation, you can use agent mental model:

1. **Think in Phases**:
   - Am I creating a new environment? (Environment Architect mindset)
   - Am I organizing tasks? (Task Orchestrator mindset)
   - Am I executing work? (Execution Guardian mindset)

2. **Respect Boundaries**:
   - Don't mix initialization and execution
   - Complete task breakdown before starting work
   - Validate before and after execution

3. **Follow Handoffs**:
   - After environment creation, review tasks for breakdown
   - After breakdown, prepare for execution
   - After execution, check parent task status

### Manual Agent Workflow

Simulate agents by following command sequences:

**Environment Creation**:
```
1. smart-bootstrap.md (or bootstrap.md)
2. Review created tasks
3. If difficulty ≥7 → proceed to Task Orchestrator
```

**Task Breakdown**:
```
1. breakdown.md for high-difficulty tasks
2. sync-tasks.md to update overview
3. Review subtasks → proceed to Execution Guardian
```

**Task Execution**:
```
1. complete-task.md to start work
2. validate-assumptions.md during work
3. complete-task.md to finish
4. If subtask complete → check parent (Task Orchestrator)
```

## Future Enhancements

### Pattern Learning
- Track successful workflows across projects
- Suggest breakdown patterns based on history
- Predict likely handoff points

### Proactive Assistance
- Automatically detect when breakdown needed
- Suggest next steps after completion
- Flag potential issues before execution

### Cross-Project Intelligence
- Learn from multiple project patterns
- Improve template detection
- Optimize task breakdown strategies

## Troubleshooting

### "Which agent should I use?"

Check current context:
- Empty directory? → Environment Architect
- Task needs breakdown? → Task Orchestrator
- Ready to work on task? → Execution Guardian

### "Can I skip the agent system?"

Yes! Agents are organizational framework. You can:
- Use commands directly
- Follow command patterns manually
- Implement your own workflow

### "How do I know if agents are working?"

When fully implemented:
- Agent selection messages appear
- Handoff notifications shown
- Logs in `.claude/agent-logs/`
- Metrics in `.claude/agent-metrics.json`

Currently: Not implemented, so you won't see these

## Related Documentation

- **Agent Definitions**: `.claude/agents/environment-architect.md`, `task-orchestrator.md`, `execution-guardian.md`
- **Architecture**: `.claude/agent-docs/architecture.md`
- **Handoff Protocol**: `.claude/agent-docs/handoff-protocol.md`
- **Agent Command**: `.claude/commands/use-agent.md`
- **Script Documentation**: `scripts/README.md`

## Contributing to Agent System

If you want to help implement the agent system:

1. Review existing documentation
2. Understand script layer (Task 79 implementation)
3. Implement agent selection logic
4. Create integration tests
5. Update this document with implementation details

## Summary

The agent system is a well-designed architectural pattern that:
- **Provides clear separation** of initialization, planning, and execution
- **Prevents conflicts** through exclusive ownership and state-based rules
- **Enables automation** of workflow transitions
- **Is currently aspirational** but has foundation in place (scripts, docs, config)

**Current Recommendation**:
- Use agent mental model for organizing work
- Follow command patterns directly
- Prepare for future agent integration by respecting boundaries

**Future State**:
- Agents automatically selected based on context
- Seamless handoffs between phases
- Enforced boundaries and validation
- Performance tracking and optimization
