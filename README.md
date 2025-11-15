# Claude Code Environment Templates

A version-controlled repository of copyable environment templates for bootstrapping new Claude Code projects with task management, standards, and workflow automation.

## Purpose

This repository provides production-ready templates to quickly set up new development environments with Claude Code. Each template includes:
- Complete `.claude/` folder structure
- Task management system with hierarchical breakdown
- Reusable command patterns for workflows
- Technology-specific coding standards
- Automatic progress tracking and validation

## Quick Start

### 1. Choose Your Template

```bash
# For any project type (minimal setup)
cp -r templates/base/* /path/to/new-project/

# For data engineering (Python, SQL, ETL)
cp -r templates/data-engineering/* /path/to/new-project/

# For Power BI dashboards
cp -r templates/bi-dashboard/* /path/to/new-project/

# For combined data + BI projects
cp -r templates/hybrid/* /path/to/new-project/
```

### 2. Customize

1. Update `CLAUDE.md` with your project name and description
2. Edit tasks in `.claude/tasks/` to match your work
3. Fill in `.claude/context/overview.md` with project details
4. Run `@.claude/commands/update-tasks.md` to validate setup

### 3. Start Working

- Review `.claude/tasks/task-overview.md` for your task list
- Use `@.claude/commands/complete-task.md <id>` to start work
- Break down complex tasks with `@.claude/commands/breakdown.md <id>`

## Repository Structure

```
claude_code_environment/
├── templates/              # Copyable project templates
│   ├── base/               # Minimal, any project type
│   ├── data-engineering/   # ETL pipelines, data processing
│   ├── bi-dashboard/       # Power BI, reporting
│   ├── hybrid/             # Combined data + BI
│   └── experimental/       # Work-in-progress templates
├── docs/                   # Documentation
│   ├── template-guide.md       # How to use templates
│   ├── template-overview10.md  # Comprehensive reference
│   ├── development.md          # Contributing guide
│   └── todo.md                 # Development tasks
├── CLAUDE.md               # AI context for this repo
└── README.md               # This file
```

## Available Templates

### Base Template
**Path**: `templates/base/`
**Use for**: Any project type, minimal setup

**Includes**:
- Task management (JSON + auto-generated overview)
- Core commands (breakdown, complete, sync, update)
- Reference files (difficulty guide, validation rules)
- Example tasks and context structure

**Best for**: Small projects, general development, quick setup

### Data Engineering Template
**Path**: `templates/data-engineering/`
**Use for**: ETL pipelines, data processing, analytics engineering

**Includes**: Everything in Base, plus:
- Python/Polars coding standards
- SQL conventions and patterns
- Testing standards (unit, integration, data quality)

**Best for**: Data pipelines, ETL/ELT, analytics engineering

### BI/Dashboard Template
**Path**: `templates/bi-dashboard/`
**Use for**: Power BI, reporting, visualization

**Includes**: Everything in Base, plus:
- DAX coding standards and patterns
- Power Query M standards
- Power BI best practices (modeling, performance, design)

**Best for**: Power BI dashboards, reporting projects, BI solutions

### Hybrid Template
**Path**: `templates/hybrid/`
**Use for**: End-to-end data solutions

**Includes**: Everything in Base, plus:
- All Data Engineering standards (Python, SQL, Testing)
- All BI standards (DAX, M, Power BI)

**Best for**: Full-stack data projects (pipeline + dashboard)

## Template Structure

Each template contains:

```
template/
├── CLAUDE.md                   # AI context router
├── README.md                   # Human documentation
└── .claude/
    ├── commands/               # Workflow automation
    │   ├── complete-task.md    # Start/finish tasks
    │   ├── breakdown.md        # Split difficult tasks
    │   ├── sync-tasks.md       # Update overview
    │   └── update-tasks.md     # Validate system
    ├── context/                # Project understanding
    │   ├── overview.md         # Goals, scope, decisions
    │   └── standards/          # Tech-specific conventions
    ├── tasks/                  # Work tracking
    │   ├── task-overview.md    # Summary table (auto-generated)
    │   └── task-*.json         # Individual tasks
    └── reference/              # Supporting info
        ├── difficulty-guide.md
        ├── validation-rules.md
        └── breakdown-workflow.md
```

## Key Features

### Hierarchical Task Management
- **Difficulty Scoring**: 1-10 scale based on LLM error risk
- **Automatic Breakdown**: Tasks ≥7 must be split into subtasks ≤6
- **Parent Auto-Completion**: Parents auto-finish when all subtasks complete
- **Progress Tracking**: "Broken Down (X/Y done)" status
- **Status Validation**: Prevents manual tracking errors

### Workflow Commands
- **complete-task.md**: Standard workflow with status tracking
- **breakdown.md**: Split complex tasks automatically
- **sync-tasks.md**: Update overview from JSON files
- **update-tasks.md**: Validate task structure

### Technology Standards
- **Data Engineering**: Python, SQL, Polars, testing patterns
- **BI/Dashboard**: DAX, M, Power BI best practices
- **Hybrid**: All of the above

## Usage Examples

### Scenario 1: Simple Project
```bash
cp -r templates/base/* my-new-project/
cd my-new-project
# Edit CLAUDE.md and tasks, start working
```

### Scenario 2: Data Pipeline
```bash
cp -r templates/data-engineering/* carbon-emissions-etl/
cd carbon-emissions-etl
# Customize tasks for ETL phases
# Reference Python and SQL standards as you work
```

### Scenario 3: Power BI Dashboard
```bash
cp -r templates/bi-dashboard/* sales-dashboard/
cd sales-dashboard
# Document data model in context/overview.md
# Reference DAX and M standards while building
```

### Scenario 4: Full Stack Data Solution
```bash
cp -r templates/hybrid/* analytics-platform/
cd analytics-platform
# Organize tasks by layer (ETL vs BI)
# Use appropriate standards for each component
```

## Task Management Quick Reference

### Difficulty Scale
- **1-2**: Trivial (typo fix, text update)
- **3-4**: Low (basic CRUD, simple UI)
- **5-6**: Moderate (validation, API integration)
- **7-8**: High (**must break down** - auth, migration)
- **9-10**: Extreme (**must break down** - architecture)

### Task Status
- **Pending**: Not started
- **In Progress**: Currently working
- **Blocked**: Cannot proceed
- **Broken Down**: Split into subtasks (auto-completes)
- **Finished**: Complete

### Workflow Rules
1. Tasks ≥7 **must** be broken down first
2. "Broken Down" tasks **cannot** be worked directly
3. Always use `complete-task.md` to start work
4. Parents auto-complete when subtasks finish
5. Run `update-tasks.md` to check system health

## Documentation

- **Getting Started**: See `docs/template-guide.md`
- **Comprehensive Reference**: See `docs/template-overview10.md`
- **Contributing**: See `docs/development.md`
- **Development Tasks**: See `docs/todo.md`

## Benefits

1. **Version Control**: Track template evolution with Git
2. **Consistency**: Same structure across all projects
3. **Efficiency**: Bootstrap environments in minutes
4. **Reduced Errors**: Task breakdown prevents high-complexity failures
5. **Standards**: Technology-specific best practices included
6. **Automation**: Auto-completion, validation, status tracking

## Typical Workflow

### 1. Create Specification (Claude Desktop)
- Discuss project idea with Claude
- Iterate on requirements and constraints
- Export specification to Markdown file

### 2. Bootstrap Environment (VS Code)
- Copy appropriate template to project directory
- Customize CLAUDE.md, tasks, and context files
- Validate with `update-tasks.md`

### 3. Work on Tasks
- Review `task-overview.md` for task list
- Break down difficulty ≥7 tasks first
- Use `complete-task.md` for work tracking
- Tasks auto-sync and validate

## Example: From Idea to Working Environment

**User Request:**
> "Build an ETL pipeline for carbon emissions data from APIs, process with Polars, load to Azure SQL for Power BI."

**Steps:**
1. Copy hybrid template: `cp -r templates/hybrid/* carbon-emissions-platform/`
2. Update CLAUDE.md with project description
3. Create tasks:
   - Task 1: Setup project (difficulty: 3)
   - Task 2: API connections (difficulty: 8) ← needs breakdown
   - Task 3: Polars pipeline (difficulty: 7) ← needs breakdown
   - Task 4: Azure SQL loader (difficulty: 7) ← needs breakdown
   - Task 5: Power BI model (difficulty: 6)
4. Run `@.claude/commands/breakdown.md 2` to split Task 2
5. Start work: `@.claude/commands/complete-task.md 6` (first subtask)
6. Reference Python, SQL, and DAX standards as needed

**Result:**
- Manageable task hierarchy
- Automatic progress tracking
- Clear standards to follow
- Reduced error risk

## Contributing

This is a template repository for bootstrapping Claude Code projects. To contribute:
1. See `docs/development.md` for guidelines
2. Test changes in real projects
3. Update documentation
4. Track ideas in `docs/todo.md`

## Version History

- **Current**: Reorganized with copyable template folders, comprehensive standards
- **v10**: Added hierarchical task management with auto-completion
- Earlier: Basic task tracking and command patterns

## License

Templates and documentation provided as-is for personal use.
