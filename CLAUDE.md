# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **template repository** for bootstrapping new Claude Code project environments. It contains:

1. **Environment templates** - Versioned patterns for different project types (Base, Data Engineering, BI/Dashboard, Hybrid, Power Query)
2. **Task management system** - Hierarchical task breakdown with JSON-based tracking
3. **Command patterns** - Reusable workflow instructions for common operations
4. **Documentation** - Comprehensive guides for creating and using project environments

## Core Workflow: Creating New Projects

### Simplified Workflow (Recommended)

1. **In Claude Desktop**: User discusses project idea, iterates on specification, exports to single Markdown file
2. **In VS Code with Claude Code**: User navigates to new project directory and says:
   ```
   "Create the environment from claude_code_environment repo using spec: [path/to/spec.md]"
   ```
3. **Claude Code automatically**:
   - Reads and analyzes the specification
   - Detects the appropriate template (Power Query, Research, Life Projects, Documentation, or Base)
   - Asks only necessary clarifying questions (if template is ambiguous)
   - Generates complete `.claude/` environment structure
   - Populates files with content extracted from specification

**Key Benefits**:
- No need to manually choose template type
- No need to answer extensive setup questions
- Specification content automatically populates environment files
- Smart detection with transparent reasoning

### Advanced Workflow (More Control)

Use `.claude/commands/bootstrap.md` for interactive template selection with step-by-step customization.

### This Repository's Role

- **Version control** for environment templates
- **Iteration space** for improving template patterns
- **Reference documentation** for the `.claude/` folder structure and conventions
- **Smart bootstrap system** for automatic template detection

## Key Files

### legacy-template-reference.md
**Legacy comprehensive template documentation** (52KB, frozen snapshot) containing:

- Quick start minimal setup (5 minutes)
- Full environment patterns for different project types
- Task management system details (JSON schema, difficulty scoring, status values)
- Command file examples (breakdown.md, complete-task.md, sync-tasks.md, update-tasks.md)
- Context file templates
- Tool integration guidance (Gemini API for research/analysis, Claude for implementation)
- Hierarchical task breakdown workflow

**When to reference**:
- User asks how to create a new environment
- User asks about task management conventions
- User asks about command patterns or `.claude/` folder structure
- Explaining how different project types should be set up

### .claude/tasks/task-overview.md
Current and completed development tasks for this repository

### .vscode/settings.json
Power Query configuration for this workspace

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
1. Create new template in `templates/[name]/` directory with README.md and components.json
2. Include folder structure, typical commands, and context files in customizations/
3. Explain when to use this template type in the README
4. Add to main README.md under "Available Templates"

### Updating Task Management System
1. Changes to task schema must update:
   - Component documentation in `components/task-management/README.md`
   - Example JSON schemas in `components/task-management/schema.json`
   - Command file examples in `components/task-management/commands/`
   - Validation rules in `components/task-management/reference/validation-rules.md`

### Testing Templates
When user requests to test a template:
1. Create temporary directory structure
2. Generate files based on template pattern
3. Validate structure matches documentation
4. Test command patterns with sample tasks
5. Confirm task lifecycle (Pending → In Progress → Finished, including breakdown/auto-completion)

## README.md Requirements

Based on user's requirements, the README.md should explain:

1. **Purpose**: This is a template repository for bootstrapping Claude Code environments with version control
2. **Simplified Workflow** (one-command setup):
   - Create project specification in Claude Desktop (export to single .md file)
   - Open VS Code in new project directory with Claude Code
   - Say: "Create the environment from claude_code_environment repo using spec: [path]"
   - Claude Code automatically detects template type and generates structure
3. **Smart Bootstrap Features**:
   - Automatic template detection from specification content
   - Pattern matching for Power Query, Research, Life Projects, Documentation, and Base templates
   - Asks only necessary clarifying questions
   - Populates files with content extracted from specification
4. **Template Types Available**: See `templates/` directory and README.md
5. **Benefits**:
   - Version-controlled environment patterns
   - One-command project setup (no manual template selection)
   - Consistent project setup across multiple projects
   - Hierarchical task management with automatic parent completion
   - Reusable command patterns
   - Technology-specific standards
6. **Getting Started**: Simple instructions for one-command bootstrap

## Commands to Run

Since this is a documentation/template repository, there are no build, lint, or test commands. The primary operations are:

- **Read template documentation**: See `templates/[name]/README.md` or `legacy-template-reference.md`
- **Create new project environment**: Use `.claude/commands/bootstrap.md` or apply template patterns
- **Update templates**: Modify files in `templates/` and `components/` directories
- **Version control**: Standard git operations for tracking template evolution

## Repository Conventions

- **No emojis in documentation** unless explicitly requested by user
- **Component-based architecture** for reusable template elements
- **Markdown format** for all documentation
- **JSON format** for task schemas
- **Command files** use `.md` extension with structured format (Purpose, Context Required, Process, Output Location)
- **Keep CLAUDE.md minimal** in generated projects (<100 lines, router pattern)
- **Separation of concerns**: `.claude/` for AI context, README.md/docs for humans

## Navigation Rules

- **Creating new environment?** → Use `.claude/commands/smart-bootstrap.md` (recommended) or `.claude/commands/bootstrap.md` (interactive)
- **Understanding template detection?** → See `.claude/reference/template-selection-rules.md`
- **Power Query projects?** → See `templates/power-query/README.md` for Phase 0 workflow, LLM pitfalls checklist, and 5-dimension difficulty scoring
- **Task management questions?** → See "Task Management System" section in `legacy-template-reference.md`
- **Command pattern examples?** → See "Command File Examples" section (breakdown.md, complete-task.md, sync-tasks.md)
- **Understanding hierarchy?** → See `reference/breakdown-workflow.md` template
- **Tool integration?** → See "Tool Routing & Model Selection" section
- **Repository development tasks?** → Check `.claude/tasks/task-overview.md`

## Current Focus

Maintaining and improving environment templates for efficient Claude Code project bootstrapping. Recent additions include hierarchical task breakdown with automatic parent completion and Gemini API integration patterns.
