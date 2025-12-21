# Show Commands - Command Browser Utility

## Purpose
Discover all available commands in the current project, grouped by category with brief descriptions. Helps with workflow discovery without needing to explore directories or read documentation.

## Context Required
- Access to `.claude/commands/` directory
- Understanding of command categorization patterns

## Process

### Step 1: Scan Available Commands

List all command files in `.claude/commands/` and categorize them:

**Project Initialization**
- `smart-bootstrap.md` - Auto-detect template from specification and create environment
- `bootstrap.md` - Interactive template selection with guided setup
- `tutorial-bootstrap.md` - Step-by-step tutorial for first-time setup
- `undo-bootstrap.md` - Remove generated environment files
- `validate-spec.md` - Validate specification quality before bootstrap

**Task Management**
- `complete-task.md` - Start and finish tasks with status tracking
- `breakdown.md` - Split high-difficulty tasks (≥7) into manageable subtasks
- `sync-tasks.md` - Update task-overview.md from JSON task files
- `update-tasks.md` - Validate task system health and fix issues

**Agent Orchestration**
- `use-agent.md` - Intelligently invoke appropriate agent based on context

**Validation & Analysis**
- `validate-assumptions.md` - Systematically validate pending assumptions
- `check-risks.md` - Analyze and document task risks
- `analyze-patterns.md` - Identify patterns across tasks and decisions

**Decision Tracking**
- `log-decision.md` - Document significant decisions with rationale

**Project Monitoring**
- `show-dashboard.md` - Display project health dashboard with real-time metrics

### Step 2: Display Command Catalog

Show organized list with:
- Category headers
- Command names (without .md extension)
- Brief one-line descriptions
- Usage hint (e.g., `/command-name`)

### Step 3: Provide Command Details (Optional)

If user requests details about specific command:
1. Read the command file
2. Extract Purpose, Context Required, and Process sections
3. Display formatted output

If user wants to run a command:
1. Confirm command name
2. Ask for required arguments (if any)
3. Execute the command pattern

## Output Format

```
📋 Available Commands

PROJECT INITIALIZATION
  smart-bootstrap      Auto-detect template from specification
  bootstrap            Interactive template selection
  tutorial-bootstrap   Step-by-step setup tutorial
  undo-bootstrap       Remove generated environment
  validate-spec        Validate specification quality

TASK MANAGEMENT
  complete-task        Start/finish tasks with tracking
  breakdown            Split high-difficulty tasks
  sync-tasks           Update task overview
  update-tasks         Validate task system health

AGENT ORCHESTRATION
  use-agent            Invoke appropriate agent

VALIDATION & ANALYSIS
  validate-assumptions Validate pending assumptions
  check-risks          Analyze task risks
  analyze-patterns     Identify cross-task patterns

DECISION TRACKING
  log-decision         Document decisions

PROJECT MONITORING
  show-dashboard       Display health dashboard

💡 Usage: /command-name [args]
💡 Details: /show-commands <command-name>
```

## Examples

**Browse all commands:**
```
User: /show-commands
Claude: [Displays categorized list above]
```

**Get command details:**
```
User: /show-commands complete-task
Claude: [Shows Purpose, Context Required, Process sections]
```

**Run a command:**
```
User: /show-commands run breakdown 78
Claude: [Executes breakdown.md for task 78]
```

## Output Location
- Terminal display (no files modified)

## Notes
- Command categories are inferred from command purposes
- New commands added to `.claude/commands/` will appear automatically
- Template-specific commands (e.g., Phase 0 commands in Power Query) are not included in base catalog
