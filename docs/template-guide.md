# Template Usage Guide

## Overview
This repository contains copyable templates for bootstrapping Claude Code project environments. Each template provides a complete `.claude/` folder structure with task management, commands, and technology-specific standards.

## Available Templates

### 1. Base Template
**Location**: `templates/base/`
**Use for**: Any project type, minimal setup

**Includes**:
- Task management system (JSON-based with auto-generated overview)
- Core commands (breakdown, complete-task, sync-tasks, update-tasks)
- Reference files (difficulty guide, validation rules, breakdown workflow)
- Example tasks and context structure

**Best for**:
- Small to medium projects (<10 tasks initially)
- General-purpose development
- When you don't need technology-specific standards
- Quick project setup

### 2. Data Engineering Template
**Location**: `templates/data-engineering/`
**Use for**: ETL pipelines, data processing, analytics engineering

**Includes**: Everything from Base, plus:
- Python/Polars coding standards
- SQL conventions and patterns
- Testing standards (unit, integration, data quality)
- Data validation patterns

**Best for**:
- Data pipeline projects
- ETL/ELT workflows
- Data transformation with Python and SQL
- Analytics engineering projects

### 3. BI/Dashboard Template
**Location**: `templates/bi-dashboard/`
**Use for**: Power BI, reporting, visualization projects

**Includes**: Everything from Base, plus:
- DAX coding standards
- Power Query M standards
- Power BI best practices (data model, reports, performance)
- Visual design guidelines

**Best for**:
- Power BI dashboard development
- Reporting projects
- Data visualization work
- Business intelligence solutions

### 4. Hybrid Template
**Location**: `templates/hybrid/`
**Use for**: Projects combining data engineering and BI/dashboards

**Includes**: Everything from Base, plus:
- All Data Engineering standards (Python, SQL, Testing)
- All BI standards (DAX, M, Power BI)
- Full stack data solution patterns

**Best for**:
- End-to-end data solutions (pipeline + dashboard)
- Projects requiring both ETL and reporting
- Full-stack data team projects
- Complex analytics platforms

## How to Use Templates

### Method 1: Manual Copy
```bash
# Navigate to your new project directory
cd /path/to/new-project

# Copy template files
cp -r /path/to/claude_code_environment/templates/base/* .

# Customize CLAUDE.md with your project details
# Customize task files in .claude/tasks/
# Start working!
```

### Method 2: Copy Script (Recommended)
```bash
# Use the copy script (if available)
./scripts/copy-template.sh --template base --destination /path/to/new-project
```

### Method 3: Reference in Claude Code
When working with Claude Code:
1. Navigate to your new project directory
2. Reference this repository: `@/path/to/claude_code_environment/templates/[template-type]/`
3. Ask Claude to copy and customize the template for your project

## Customization Checklist

After copying a template:

### 1. Update CLAUDE.md
- [ ] Replace `[Your Project Name]` with actual project name
- [ ] Fill in "What I'm Building" section
- [ ] Update "Current Focus" with initial task
- [ ] Customize "Next task" field

### 2. Update README.md
- [ ] Add project description
- [ ] List key features
- [ ] Add installation instructions
- [ ] Update project structure if needed

### 3. Customize Tasks
- [ ] Review `.claude/tasks/task-overview.md`
- [ ] Edit or replace example tasks in `.claude/tasks/task-*.json`
- [ ] Run `@.claude/commands/sync-tasks.md` to update overview
- [ ] Identify any difficulty ≥7 tasks for breakdown

### 4. Update Context
- [ ] Fill in `.claude/context/overview.md` with project details
- [ ] Add any project-specific context files
- [ ] Review standards files and customize if needed

### 5. Validate Setup
- [ ] Run `@.claude/commands/update-tasks.md` to check system health
- [ ] Verify all task references are valid
- [ ] Confirm no validation errors

## Template Structure Explanation

```
template/
├── CLAUDE.md                   # AI context router (keep <100 lines)
├── README.md                   # Human documentation
└── .claude/
    ├── commands/               # Reusable workflow patterns
    │   ├── complete-task.md    # Start/finish tasks with tracking
    │   ├── breakdown.md        # Split difficult tasks
    │   ├── sync-tasks.md       # Update task overview
    │   └── update-tasks.md     # Validate system health
    ├── context/                # Project understanding
    │   ├── overview.md         # Project goals, scope, decisions
    │   └── standards/          # Technology-specific conventions
    ├── tasks/                  # Work tracking
    │   ├── task-overview.md    # Auto-generated summary table
    │   └── task-*.json         # Individual task files
    └── reference/              # Supporting information
        ├── difficulty-guide.md     # Task scoring criteria
        ├── validation-rules.md     # Task validation rules
        └── breakdown-workflow.md   # Hierarchy management
```

## Workflow After Setup

### Starting Work
1. Review `.claude/tasks/task-overview.md`
2. Identify next task (check dependencies)
3. Check for 🔴 markers (difficulty ≥7) - break these down first
4. Use `@.claude/commands/complete-task.md <task_id>` to start work

### During Development
1. Work on tasks following proper workflow
2. Update task status as you progress
3. Add notes to task JSON files
4. Create new tasks as needed

### Task Management
- Use `breakdown.md` for complex tasks (difficulty ≥7)
- Use `sync-tasks.md` after modifying task JSON files
- Use `update-tasks.md` to check system health
- Tasks marked "Broken Down" auto-complete when subtasks finish

## Common Scenarios

### Scenario 1: Simple Project
**Template**: Base
**Customize**: Minimal - just update project name and create 3-5 initial tasks

### Scenario 2: Data Pipeline
**Template**: Data Engineering
**Customize**:
- Add specific data sources to context/overview.md
- Create tasks for extract, transform, load phases
- Reference Python and SQL standards as you work

### Scenario 3: Dashboard Project
**Template**: BI/Dashboard
**Customize**:
- Document data model in context/overview.md
- Create tasks for data prep, model, and visual phases
- Reference DAX, M, and Power BI standards

### Scenario 4: Full Stack Data Solution
**Template**: Hybrid
**Customize**:
- Document both pipeline and dashboard architecture
- Organize tasks by layer (ETL vs BI)
- Use appropriate standards for each component

## Tips for Success

1. **Start with overview**: Fill in context/overview.md thoroughly before coding
2. **Break down early**: Don't start difficult tasks without breaking them down
3. **Keep tasks atomic**: Each task should be independently completable
4. **Use standards**: Reference the standards files frequently
5. **Update as you go**: Keep task status current and add notes
6. **Leverage commands**: Use the command files - they automate tedious tracking

## Upgrading Templates

If you started with a minimal setup and need to upgrade:

1. Copy additional folders from appropriate template
2. Add standards files to `.claude/context/standards/`
3. Add new commands to `.claude/commands/`
4. Update CLAUDE.md to reference new files
5. Run `update-tasks.md` to ensure compatibility

## Getting Help

- **Template structure questions**: See `docs/template-overview10.md`
- **Task management details**: See `.claude/reference/breakdown-workflow.md` in any template
- **Development tasks**: See `docs/todo.md` for this repository's roadmap
- **Repository setup**: See root `CLAUDE.md` and `README.md`
