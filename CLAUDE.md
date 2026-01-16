# CLAUDE.md

This file contains explicit instructions for Claude Code (claude.ai/code) when working in this repository. Follow these directives exactly.

> **Optimized for Claude Opus 4.5** - This system is calibrated for Opus 4.5's capabilities. Task difficulty, breakdown thresholds, and workflow design assume you're using Opus 4.5 with normal thinking settings. Earlier models may need more aggressive task breakdown.

## Repository Purpose

This is a **template repository** for bootstrapping new Claude Code project environments. It contains:

1. **Environment templates** - Versioned patterns for different project types (Base, Data Engineering, BI/Dashboard, Hybrid, Power Query)
2. **Task management system** - Hierarchical task breakdown with JSON-based tracking
3. **Command patterns** - Reusable workflow instructions for common operations
4. **Documentation** - Comprehensive guides for creating and using project environments

## Core Workflow: Creating New Projects

### ALWAYS Use This Workflow When User Requests Environment Creation

1. **IMMEDIATELY READ** the specification file when user provides path
2. **DETECT TEMPLATE TYPE** using these exact patterns:
   ```
   IF contains("power query" OR "dax" OR "power bi") → USE power-query template
   IF contains("research" OR "analysis" OR "study") → USE research template
   IF contains("life project" OR "personal") → USE life-projects template
   IF contains("documentation" OR "docs") → USE documentation template
   ELSE → USE base template
   ```
3. **EXECUTE THESE STEPS** without deviation:
   - Read the specification file completely
   - Extract all requirements and context
   - Generate the complete `.claude/` structure
   - Populate files with specification content
   - Create initial tasks from requirements
   - Run sync-tasks to generate overview

**Key Benefits**:
- No need to manually choose template type
- No need to answer extensive setup questions
- Specification content automatically populates environment files
- Smart detection with transparent reasoning

### Advanced Workflow (More Control)

Use `.claude/commands/bootstrap.md` (primary bootstrap command with auto-detection) or see `.archive/legacy-commands/bootstrap-interactive.md` for the legacy interactive version with manual template selection.

### This Repository's Role

- **Version control** for environment templates
- **Iteration space** for improving template patterns
- **Reference documentation** for the `.claude/` folder structure and conventions
- **Smart bootstrap system** for automatic template detection

## Key Files

### Task Schema Documentation
**Current authoritative schema**: `.claude/reference/task-schema-consolidated.md`
- Consolidated schema combining all previous versions
- Includes belief tracking, progress tracking, and momentum tracking
- Deprecated schemas archived in `.archive/deprecated-schemas/`

### Bootstrap Command
**Primary command**: `.claude/commands/bootstrap.md`
- Auto-detects template type from specification
- Agent-based (Environment Architect Agent)
- Minimal user interaction required
- Legacy interactive version: `.archive/legacy-commands/bootstrap-interactive.md`

### Reference Documentation
**Key reference files** in `.claude/reference/`:
- `task-schema-consolidated.md` - Authoritative task schema
- `claude-4-parallel-tools.md` - Parallel execution patterns (renamed from parallel-tool-patterns.md)
- `parallel-task-safety-checks.md` - Safety checks for parallel tasks (renamed from parallel-execution-gates.md)
- `validation-gates-reference.md` - Validation concepts (renamed from validation-gates.md)
- `claude-4-tool-usage.md` - Tool usage guidelines (renamed from coding-guidelines.md)

### Archive Directory
**Historical and deprecated files**: `.archive/`
- Deprecated schemas, legacy commands, historical documentation
- See `.archive/README.md` for guidance on when to reference archived files

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

### MANDATORY Task Management Rules

**ALWAYS:**
- Break down tasks with difficulty ≥7 before starting work
- Use `complete-task.md` to start ANY task work
- Update task status immediately when changing phases
- Run sync-tasks after completing any task
- Create checkpoints for tasks taking >10 steps

**NEVER:**
- Work on "Broken Down" status tasks directly
- Skip status updates
- Complete tasks without validation
- Modify parent task status manually (auto-completes)
- Work on multiple tasks simultaneously without updating status

## Tool Integration Strategy

**MCP Servers Available:** See `.claude/reference/mcp-servers.md` for full reference (Gemini, Playwright, Netlify)

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

## Claude Opus 4.5 Best Practices

### ALWAYS Execute Tools in Parallel When Possible

**PARALLEL EXECUTION RULES:**
1. Execute multiple Read operations in single message
2. Run independent Bash commands simultaneously
3. Perform multiple Grep/Glob searches concurrently
4. Update multiple task files in parallel
5. See `.claude/reference/parallel-tool-patterns.md` for patterns

**SEQUENTIAL EXECUTION ONLY WHEN:**
- Output of first operation needed for second
- Operations modify same resource
- Explicit ordering required for correctness

### Explicit Action Framework

**IMPLEMENT, Don't Suggest:**
- When user says "add" → CREATE the file/feature
- When user says "fix" → APPLY the fix immediately
- When user says "update" → MAKE the changes now
- When user says "check" → RUN the verification

**Ask for Clarification ONLY When:**
- Multiple valid interpretations exist
- Critical data is missing
- Destructive operation requested
- User explicitly requests options

### Context Management for Long Tasks

**FOR TASKS >10 STEPS:**
1. Create checkpoint after every 3 steps
2. Summarize completed work before step 5
3. Compress verbose outputs to key points
4. Track progress in structured JSON
5. See `.claude/reference/context-management.md` for patterns

### Tool Usage Priorities

**TOOL SELECTION HIERARCHY:**
```
File Operations:
1. Read (for reading files) - NEVER use cat via Bash
2. Write (for new files) - NEVER use echo > via Bash
3. Edit (for modifications) - NEVER use sed/awk via Bash

Search Operations:
1. Glob (for file patterns)
2. Grep (for content search)
3. NEVER use find/grep via Bash unless necessary

Execution:
1. Bash (for system commands ONLY)
2. Use && for sequential commands
3. Use parallel calls for independent commands
```

## Current Focus

Optimized for Claude Opus 4.5 (model ID: `claude-opus-4-5-20251101`). Key capabilities:
- 75-85% performance gains through parallel execution
- Explicit, imperative instruction patterns
- Proactive implementation approach
- Structured context management for long tasks
- Knowledge cutoff: May 2025
