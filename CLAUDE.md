# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **template repository** for bootstrapping new Claude Code project environments. It contains:

1. **Environment templates** - Versioned patterns for different project types (Base, Data Engineering, BI/Dashboard, Hybrid)
2. **Task management system** - Hierarchical task breakdown with JSON-based tracking
3. **Command patterns** - Reusable workflow instructions for common operations
4. **Documentation** - Comprehensive guides for creating and using project environments

## Core Workflow: Creating New Projects

### User's Typical Usage Pattern

1. **In Claude Desktop**: User discusses project idea, iterates on specification, exports to single Markdown file
2. **In VS Code with Claude Code**: User navigates to new project directory, references this repo's templates, provides specification
3. **Claude Code creates**: Full `.claude/` environment structure with tasks, commands, and context based on project needs

### This Repository's Role

- **Version control** for environment templates
- **Iteration space** for improving template patterns
- **Reference documentation** for the `.claude/` folder structure and conventions

## Repository Structure

```
claude_code_environment/
├── templates/              # Copyable project templates
│   ├── base/               # Minimal, any project type
│   ├── data-engineering/   # ETL pipelines, data processing
│   ├── bi-dashboard/       # Power BI, reporting, visualization
│   ├── hybrid/             # Combined data + BI
│   └── experimental/       # Work-in-progress templates
├── docs/                   # Documentation
│   ├── template-guide.md       # How to use templates
│   ├── template-overview10.md  # Comprehensive reference
│   ├── development.md          # Contributing guide
│   └── todo.md                 # Development tasks
├── CLAUDE.md               # This file
└── README.md               # User documentation
```

## Key Files

### templates/
**Copyable template folders** - Each contains complete `.claude/` structure:
- **base/**: Minimal setup for any project type
- **data-engineering/**: Python, SQL, testing standards for data pipelines
- **bi-dashboard/**: DAX, M, Power BI best practices for dashboards
- **hybrid/**: All standards from both data-engineering and bi-dashboard
- **experimental/**: New templates under development

### docs/template-guide.md
**User-facing guide** for choosing and using templates:
- Template selection criteria
- Customization checklist
- Usage workflows
- Common scenarios

### docs/template-overview10.md
**Comprehensive reference** (52KB) containing:
- Quick start minimal setup
- Full environment patterns for all template types
- Task management system details
- Command file examples
- Context file templates
- Tool integration guidance

### docs/development.md
**Contributor guide** for maintaining this repository:
- Adding new templates
- Updating existing templates
- Testing procedures
- Standards file guidelines

### docs/todo.md
Current development tasks for this repository

## Environment Template Pattern

All templates follow this base structure:

```
project/
├── CLAUDE.md              # Router file (<100 lines, points to context)
├── README.md              # Human documentation
└── .claude/
    ├── commands/          # Reusable workflow patterns
    │   ├── complete-task.md    # Start/finish tasks with status tracking
    │   ├── breakdown.md        # Split difficulty ≥7 tasks into subtasks
    │   ├── sync-tasks.md       # Update task-overview.md from JSON
    │   └── update-tasks.md     # Validate task system health
    ├── context/           # Project understanding
    │   ├── overview.md
    │   ├── standards/     # Technology-specific conventions
    │   └── validation-rules.md
    ├── tasks/             # Work tracking
    │   ├── task-overview.md    # Auto-generated summary table
    │   └── task-*.json         # Individual task files
    └── reference/         # Supporting information
        ├── difficulty-guide.md
        └── breakdown-workflow.md
```

## Task Management Key Concepts

### Task Difficulty Scoring (LLM Error Risk)
- **1-2**: Trivial (fix typo, update text)
- **3-4**: Low (basic CRUD, simple UI)
- **5-6**: Moderate (form validation, API integration)
- **7-8**: High (**must break down** - auth setup, database migration)
- **9-10**: Extreme (**must break down** - architecture changes, distributed systems)

### Task Status Values
- **Pending**: Defined but not started
- **In Progress**: Currently being worked on
- **Blocked**: Cannot proceed due to blockers
- **Broken Down**: Decomposed into subtasks (container, not workable directly)
- **Finished**: Complete

### Critical Workflow Rules
1. Tasks with difficulty ≥7 **must** be broken down using `breakdown.md` before starting work
2. "Broken Down" tasks become **containers** that:
   - Cannot be worked on directly
   - Auto-complete when all subtasks finish
   - Show progress as "Broken Down (X/Y done)"
3. Always use `complete-task.md` to start work (ensures proper status tracking)
4. Parent tasks automatically transition to "Finished" when last subtask completes

## Tool Integration Strategy

### When to Use Gemini API (via MCP)
- **Research**: Current regulations, market trends, up-to-date information (use `grounding: true`)
- **Domain Analysis**: Industry expertise, compliance interpretation, business domain knowledge
- **Content Generation**: Documentation, summaries, blog posts
- **Image Analysis**: Chart interpretation, dashboard reviews
- **Code Review**: Architecture patterns, best practices validation

**Model Selection:**
- `gemini-2.5-pro` with `grounding: true` - Factual/current information, complex analysis
- `gemini-2.5-flash` - Speed-critical tasks, simple queries, image analysis

### When to Use Claude Native Capabilities
- **Code Implementation**: Writing, editing, refactoring, debugging (Python, SQL, DAX, M, JavaScript)
- **System Design**: ETL pipelines, database schemas, architecture
- **Project Management**: Task breakdown, file operations, status tracking
- **File System Operations**: Read, Write, Edit tools

### Hybrid Workflows
1. **Analysis → Implementation**: Gemini researches/reviews, Claude implements
2. **Review → Refactor**: Gemini provides feedback, Claude applies changes
3. **Research → Design**: Gemini gathers information, Claude designs solution

## Working in This Repository

### Adding New Templates
1. Copy `templates/base/` to `templates/experimental/[new-name]/`
2. Add technology-specific standards to `.claude/context/standards/`
3. Create example tasks relevant to template type
4. Update template's CLAUDE.md and README.md
5. Document in `docs/template-guide.md`
6. After testing, promote to `templates/[new-name]/`

See `docs/development.md` for detailed guide.

### Updating Task Management System
1. Changes to task schema must update:
   - All template reference files (`validation-rules.md`, `difficulty-guide.md`)
   - All command files (`breakdown.md`, `complete-task.md`, etc.)
   - Example tasks in all templates
   - Documentation in `docs/template-overview10.md`

### Testing Templates
When user requests to test a template:
1. Copy template to temporary directory
2. Run `@.claude/commands/update-tasks.md` to check health
3. Test task workflow (breakdown, complete, sync)
4. Verify all file references work
5. Use in real project if possible

## README.md Requirements

Based on user's requirements, the README.md should explain:

1. **Purpose**: This is a template repository for bootstrapping Claude Code environments with version control
2. **Typical Workflow**:
   - Create project specification in Claude Desktop (export to single .md file)
   - Open VS Code in new project directory with Claude Code
   - Reference this repo's templates
   - Provide specification document
   - Claude Code generates `.claude/` environment structure
3. **Template Types Available**: Link to template_overview10.md sections
4. **Benefits**:
   - Version-controlled environment patterns
   - Consistent project setup across multiple projects
   - Hierarchical task management with automatic parent completion
   - Reusable command patterns
   - Technology-specific standards
5. **Getting Started**: Instructions for using templates to bootstrap new projects

## Commands to Run

Since this is a documentation/template repository, there are no build, lint, or test commands. The primary operations are:

- **Copy template**: `cp -r templates/[type]/* /path/to/new-project/`
- **Read template guide**: `@docs/template-guide.md`
- **Read comprehensive reference**: `@docs/template-overview10.md`
- **Update templates**: Edit files in `templates/`, test, and document
- **Version control**: Standard git operations for tracking template evolution

## Repository Conventions

- **No emojis in documentation** unless explicitly requested by user
- **Sequential versioning** of template overview (currently v10: `template_overview10.md`)
- **Markdown format** for all documentation
- **JSON format** for task schemas
- **Command files** use `.md` extension with structured format (Purpose, Context Required, Process, Output Location)
- **Keep CLAUDE.md minimal** in generated projects (<100 lines, router pattern)
- **Separation of concerns**: `.claude/` for AI context, README.md/docs for humans

## Navigation Rules

- **Which template to use?** → `@docs/template-guide.md`
- **Creating new environment?** → Copy from `templates/[type]/` then customize
- **Task management questions?** → `@docs/template-overview10.md` (Task Management System section)
- **Command pattern examples?** → Any template's `.claude/commands/` folder
- **Understanding hierarchy?** → Any template's `.claude/reference/breakdown-workflow.md`
- **Contributing to repo?** → `@docs/development.md`
- **Repository development tasks?** → `@docs/todo.md`

## Current Focus

Recently reorganized repository structure:
- Created `templates/` folder with 4 production-ready templates (base, data-engineering, bi-dashboard, hybrid)
- Moved documentation to `docs/` folder
- Added comprehensive standards files (Python, SQL, DAX, M, Power BI, Testing)
- Created template-guide.md and development.md for better usability

Maintaining and improving environment templates for efficient Claude Code project bootstrapping.
