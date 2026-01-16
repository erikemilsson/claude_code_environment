# Simple Todo App Example

This example demonstrates how the **Base template** is used for a straightforward web application project.

## What This Example Shows

### Template Detection
When the specification was provided to Claude Code's smart-bootstrap system, it automatically selected the **Base template** because:
- No domain-specific keywords (Power Query, research, life project)
- General software development project
- Standard web application requirements

### Generated Structure
The `.claude/` environment was automatically generated with:

1. **Commands** - Task management and workflow patterns
2. **Context** - Project understanding extracted from spec
3. **Tasks** - Initial tasks created from requirements
4. **Reference** - Supporting documentation

### Key Benefits Demonstrated

#### 1. Automatic Content Population
The specification content was automatically extracted and organized into:
- `context/overview.md` - Project summary
- `context/requirements.md` - Functional and technical requirements
- `tasks/` - Initial task breakdown from implementation plan

#### 2. Task Management Setup
Tasks were created with:
- Appropriate difficulty scores (based on complexity)
- Dependencies mapped from phases
- Status tracking ready to use

#### 3. Ready-to-Use Commands
Pre-configured commands for:
- `complete-task.md` - Start and finish tasks
- `breakdown.md` - Split complex tasks
- `sync-tasks.md` - Update task overview
- `update-tasks.md` - Validate system health

## How It Was Created

### 1. User Provided Specification
```bash
# User created original-spec.md with project requirements
```

### 2. Bootstrap Command
```
"Create environment from claude_code_environment repo using spec: original-spec.md"
```

### 3. Automatic Processing
Claude Code:
1. Read the specification
2. Detected Base template (no special domain markers)
3. Generated complete `.claude/` structure
4. Populated files with spec content
5. Created initial tasks from requirements

### 4. Ready to Work
The project is now ready with:
- Clear task breakdown
- Tracking system in place
- Workflow commands available
- Context documented

## Compare With Other Templates

This uses the **Base template** which provides:
- General task management
- Standard workflow commands
- Basic validation rules

Other examples in this directory show domain-specific templates:
- **pension-calculator/** - Power Query template with Phase 0 workflow
- **research-project/** - Research template with literature review

## Files in This Example

```
simple-todo-app/
├── original-spec.md           # The input specification
├── generated-environment/     # What was generated
│   └── .claude/
│       ├── commands/         # Workflow patterns
│       ├── context/          # Extracted understanding
│       ├── tasks/           # Created task files
│       └── reference/       # Support docs
└── README.md                # This explanation
```

## Using This Pattern

To create your own project using this pattern:

1. Write a specification document
2. Open VS Code in new project directory
3. Tell Claude Code: "Create environment using spec: [path]"
4. Start working with generated tasks

The Base template works well for:
- Web applications
- CLI tools
- APIs and services
- General software projects
- Any project without special domain needs