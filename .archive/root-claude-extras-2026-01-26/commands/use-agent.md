<!-- Type: Agent Coordinator -->
<!-- This command selects and invokes the appropriate agent -->

# Use Agent Command

## Purpose
Intelligently invoke the appropriate agent based on current context and user request. This command serves as the primary interface for the 3-agent architecture, automatically selecting and activating the correct agent while preventing conflicts.

## Context Required
- Current directory state (empty vs initialized)
- Task specification (if applicable)
- User command or request
- Current task status (if task exists)

## Process

### 1. Analyze Context
```python
# Determine current state
context = {
    'has_claude_folder': exists('.claude/'),
    'is_empty_directory': is_dir_empty(),
    'user_request': parse_user_command(),
    'task_specified': extract_task_id(),
    'task_status': get_task_status() if task_exists else None
}
```

### 2. Apply Decision Tree
```python
def select_agent(context):
    # RULE 1: Empty directory always triggers Environment Architect
    if context['is_empty_directory'] or not context['has_claude_folder']:
        return 'environment-architect'

    # RULE 2: No task specified - no agent needed
    if not context['task_specified'] and not context['user_request']:
        return None

    # RULE 3: Bootstrap/environment requests
    if any(keyword in context['user_request'] for keyword in
           ['bootstrap', 'create environment', 'initialize', 'template']):
        if not context['has_claude_folder']:
            return 'environment-architect'
        else:
            return None  # Environment already exists

    # RULE 4: Task-specific operations
    if context['task_specified']:
        task = load_task(context['task_id'])

        # Breakdown operations
        if task.difficulty >= 7 and task.status == 'Pending':
            return 'task-orchestrator'
        if 'break down' in context['user_request']:
            return 'task-orchestrator'

        # Execution operations
        if 'complete' in context['user_request'] or 'start' in context['user_request']:
            return 'execution-guardian'
        if task.status == 'In Progress':
            return 'execution-guardian'

        # Sync operations
        if 'sync' in context['user_request']:
            return 'task-orchestrator'

    # RULE 5: Health and validation requests
    if any(keyword in context['user_request'] for keyword in
           ['validate', 'health', 'checkpoint', 'risk']):
        return 'execution-guardian'

    return None  # No agent needed
```

### 3. Invoke Selected Agent

#### Environment Architect Invocation
```markdown
INVOKING: Environment Architect
================================
Role: Project initialization and template selection
Trigger: [trigger_condition]

The Environment Architect will:
1. Analyze your specification/requirements
2. Detect the appropriate template
3. Generate the complete .claude/ structure
4. Create initial tasks from requirements
5. Hand off to Task Orchestrator if needed

Proceeding with environment creation...
```

#### Task Orchestrator Invocation
```markdown
INVOKING: Task Orchestrator
================================
Role: Task hierarchy and breakdown management
Trigger: [trigger_condition]
Task: [task_id] - [task_title]

The Task Orchestrator will:
1. Analyze task complexity
2. Create appropriate subtasks
3. Set up dependencies
4. Validate the hierarchy
5. Hand off to Execution Guardian when ready

Proceeding with task organization...
```

#### Execution Guardian Invocation
```markdown
INVOKING: Execution Guardian
================================
Role: Task execution with validation gates
Trigger: [trigger_condition]
Task: [task_id] - [task_title]

The Execution Guardian will:
1. Run pre-execution validation gates
2. Monitor execution progress
3. Create checkpoints as needed
4. Validate completion criteria
5. Update metrics and health

Proceeding with validated execution...
```

### 4. Execute Agent Workflow

Based on the selected agent, execute its specific workflow:

```python
if selected_agent == 'environment-architect':
    # Load and execute environment-architect.md workflow
    result = execute_environment_creation(context)

elif selected_agent == 'task-orchestrator':
    # Load and execute task-orchestrator.md workflow
    result = execute_task_organization(context)

elif selected_agent == 'execution-guardian':
    # Load and execute execution-guardian.md workflow
    result = execute_task_with_validation(context)

else:
    # No agent needed - proceed with default behavior
    result = execute_default_action(context)
```

### 5. Handle Handoffs

Monitor for handoff triggers and facilitate transitions:

```python
def check_for_handoff(agent_result):
    if agent_result.needs_handoff:
        handoff_data = prepare_handoff_data(agent_result)
        next_agent = determine_next_agent(handoff_data)

        print(f"HANDOFF: {agent_result.agent} → {next_agent}")
        print(f"Reason: {handoff_data.reason}")
        print(f"Data: {handoff_data.context}")

        # Invoke next agent
        return invoke_agent(next_agent, handoff_data)

    return agent_result
```

## Usage Examples

### Example 1: Empty Directory
```bash
User: "Create environment from spec: requirements.md"

System: use-agent.md invoked
System: Context: empty directory detected
System: Selected: Environment Architect
Environment Architect: Analyzing specification...
Environment Architect: Template detected, creating environment...
```

### Example 2: Task Breakdown
```bash
User: "Break down task 003"

System: use-agent.md invoked
System: Context: task 003, difficulty 8, status Pending
System: Selected: Task Orchestrator
Task Orchestrator: Analyzing complexity...
Task Orchestrator: Creating 4 subtasks...
```

### Example 3: Task Execution
```bash
User: "Complete task 001_2"

System: use-agent.md invoked
System: Context: task 001_2, status Pending
System: Selected: Execution Guardian
Execution Guardian: Running validation gates...
Execution Guardian: Beginning execution...
```

## Conflict Prevention

### Mutual Exclusion Rules
```python
EXCLUSION_RULES = {
    'empty_dir': ['environment-architect'],  # Only EA can act
    'task_pending': ['task-orchestrator'],    # Only TO can modify
    'task_in_progress': ['execution-guardian'], # Only EG can modify
    'task_broken_down': ['task-orchestrator'], # Only TO manages subtasks
    'task_finished': []  # No agent modifies finished tasks
}
```

### Conflict Detection
```python
def detect_conflict(requested_agent, context):
    current_state = determine_state(context)
    allowed_agents = EXCLUSION_RULES.get(current_state, [])

    if requested_agent not in allowed_agents:
        return True, f"Agent {requested_agent} not allowed in state {current_state}"

    return False, None
```

## Error Handling

### Agent Selection Errors
```python
try:
    agent = select_agent(context)
except AmbiguousContextError as e:
    # Ask for clarification
    print("Unable to determine appropriate agent.")
    print("Please specify: ", e.clarification_needed)
except NoAgentAvailableError:
    # Proceed without agent
    print("No specialized agent needed for this operation.")
```

### Invocation Failures
```python
try:
    result = invoke_agent(agent, context)
except AgentNotFoundError:
    print(f"Agent {agent} not found. Check agent definitions.")
except AgentExecutionError as e:
    print(f"Agent {agent} failed: {e.message}")
    print("Attempting recovery...")
    result = recover_from_failure(agent, context, e)
```

## Performance Monitoring

Track agent invocation metrics:

```json
{
  "invocation_stats": {
    "total_invocations": 156,
    "by_agent": {
      "environment-architect": 23,
      "task-orchestrator": 67,
      "execution-guardian": 89
    },
    "selection_accuracy": 0.94,
    "handoff_success_rate": 0.98,
    "avg_selection_time_ms": 12
  }
}
```

## Output Location
- Agent selection logged to: `.claude/agent-logs/selection.log`
- Invocation results stored in: `.claude/agent-logs/[agent-name]/`
- Handoff records saved to: `.claude/agent-logs/handoffs.json`
- Performance metrics in: `.claude/agent-metrics.json`

## Validation

After agent execution, validate:
- [ ] Correct agent was selected
- [ ] Agent completed its operation
- [ ] Handoffs executed if needed
- [ ] State is consistent
- [ ] No boundary violations occurred

## Best Practices

### DO:
- Let the command analyze context automatically
- Trust the agent selection logic
- Monitor handoff messages
- Review agent logs for issues
- Report unexpected behavior

### DON'T:
- Force a specific agent unless necessary
- Skip the selection process
- Ignore handoff messages
- Modify agent state directly
- Invoke multiple agents simultaneously

## Troubleshooting

### Issue: Wrong agent selected
**Solution**: Check context analysis, verify task status, review selection rules

### Issue: Handoff failed
**Solution**: Check handoff data completeness, verify receiving agent ready, review logs

### Issue: No agent selected
**Solution**: Verify request contains actionable command, check if agent needed

### Issue: Agent boundary violation
**Solution**: Review agent definitions, check ownership matrix, verify exclusion rules