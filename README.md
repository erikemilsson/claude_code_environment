# Claude Code Environment Templates

A version-controlled repository of environment templates for bootstrapping new Claude Code projects.

## Purpose

This repository contains refined, iterable templates that work alongside project specifications to quickly set up new development environments with Claude Code. Instead of recreating project structure and conventions from scratch, you can leverage these battle-tested patterns to start productive work immediately.

## The Problem This Solves

When starting a new project with Claude Code, you need:
- Consistent file structure for AI context management
- Task tracking system with proper breakdown strategies
- Reusable command patterns for common workflows
- Technology-specific coding standards
- Clear separation between AI context and human documentation

Creating these from scratch every time is inefficient. This repository provides version-controlled templates you can iterate on and reuse across multiple projects.

## Typical Workflow

### 1. Create Project Specification (Claude Desktop)
- Discuss your project idea with Claude Desktop
- Iterate on requirements, goals, and constraints
- Export the specification to a single Markdown file

### 2. Bootstrap Environment (VS Code with Claude Code)
- Open VS Code in your new project directory
- Reference this repository's templates
- Provide your specification document to Claude Code
- Claude Code generates the complete `.claude/` environment structure

### 3. Start Working
- Review generated tasks and context files
- Break down high-difficulty tasks (≥7) into manageable subtasks
- Begin work using standardized commands
- Track progress with automatic status updates

## What's Inside

### template_overview10.md
Comprehensive 52KB documentation containing:
- **Quick Start**: Minimal 5-minute setup for simple projects
- **Environment Types**: Base, Data Engineering, BI/Dashboard, Hybrid templates
- **Task Management System**: JSON-based hierarchical task tracking with automatic parent completion
- **Command Patterns**: Reusable workflow instructions (breakdown, complete-task, sync-tasks, update-tasks)
- **Context File Templates**: Standards, reference docs, validation rules
- **Tool Integration**: When to use Gemini API vs Claude native capabilities

### Template Types

#### 1. Base Template
For general planning, research, and non-technical projects. Includes essential task management and command structure.

#### 2. Data Engineering Template
For ETL pipelines, data processing, and analytics engineering. Adds Python/Polars standards, SQL conventions, performance optimization patterns.

#### 3. BI/Dashboard Template
For Power BI, reporting, and visualization projects. Includes DAX patterns, naming conventions, KPI documentation, data source management.

#### 4. Hybrid Template
Combines elements from multiple templates based on project needs.

### .claude/ Folder Structure

Every generated environment follows this pattern:

```
project/
├── CLAUDE.md              # Router file (<100 lines, points to context)
├── README.md              # Human-readable documentation
└── .claude/               # Claude-specific context
    ├── commands/          # Reusable task patterns
    │   ├── complete-task.md    # Start/finish tasks with status tracking
    │   ├── breakdown.md        # Split complex tasks into subtasks
    │   ├── sync-tasks.md       # Update task overview
    │   └── update-tasks.md     # Validate task system health
    ├── context/           # Project understanding
    │   ├── overview.md         # Goals, scope, decisions
    │   ├── standards/          # Tech-specific conventions
    │   └── validation-rules.md # Task validation rules
    ├── tasks/             # Work tracking
    │   ├── task-overview.md    # Auto-generated summary table
    │   └── task-*.json         # Individual task files
    └── reference/         # Supporting information
        ├── difficulty-guide.md      # Task scoring criteria
        └── breakdown-workflow.md    # Hierarchical task guide
```

## Key Features

### Hierarchical Task Management
- **Difficulty Scoring**: Tasks rated 1-10 based on LLM error probability
- **Automatic Breakdown**: Tasks ≥7 difficulty must be split into subtasks ≤6
- **Parent Auto-Completion**: "Broken Down" parent tasks automatically finish when all subtasks complete
- **Progress Tracking**: Clear visibility with "Broken Down (X/Y done)" status indicators
- **Status Validation**: Consistent state management prevents manual tracking errors

### Reusable Command Patterns
- **complete-task.md**: Standard workflow for starting and finishing work (ensures proper status tracking)
- **breakdown.md**: Split high-difficulty tasks with automatic parent status transition
- **sync-tasks.md**: Update task-overview.md from JSON files
- **update-tasks.md**: Validate task structure and flag inconsistencies

### Tool Integration Strategy
- **Gemini API**: Research, domain analysis, content generation, image analysis, code review
- **Claude Native**: Code implementation, system design, file operations, project management
- **Hybrid Workflows**: Gemini researches/analyzes, Claude implements/refactors

## Benefits

1. **Version Control**: Track template evolution over time with Git
2. **Consistency**: Same proven structure across all your projects
3. **Efficiency**: Bootstrap new environments in minutes, not hours
4. **Reduced Errors**: Task breakdown system prevents high-complexity failures
5. **Context Management**: Lazy-load only relevant files, minimize token usage
6. **Reusability**: Technology-specific templates for common project types
7. **Automation**: Parent task completion, status synchronization, validation checks

## How to Use This Repository

### For Starting a New Project

1. **Clone this repository** (or keep it accessible for reference)
2. **Create project specification** in Claude Desktop and export to Markdown
3. **In VS Code**, navigate to your new project directory
4. **Ask Claude Code** to create an environment based on this repository's templates:
   ```
   "Create a [Data Engineering/BI/Base/Hybrid] environment based on the
   claude_code_environment templates. Here's my specification: [paste/attach]"
   ```
5. **Claude Code will**:
   - Read the appropriate template from `template_overview10.md`
   - Generate `.claude/` folder structure
   - Create initial tasks with difficulty scoring
   - Set up command files and context documents
   - Provide next steps for validation and task breakdown

### For Maintaining This Repository

1. **Iterate on templates**: Edit `template_overview10.md` based on lessons learned from real projects
2. **Version incrementally**: When making major changes, save as `template_overview11.md` etc.
3. **Test templates**: Create sample environments to validate structure and commands
4. **Document patterns**: Add new template types or command patterns as you discover useful workflows
5. **Track improvements**: Use `todo.md` for planned enhancements

## Task Management Quick Reference

### Difficulty Scale (LLM Error Risk)
- **1-2**: Trivial (fix typo, update text)
- **3-4**: Low (basic CRUD, simple UI)
- **5-6**: Moderate (form validation, API integration)
- **7-8**: High (**requires breakdown** - auth setup, migration)
- **9-10**: Extreme (**requires breakdown** - architecture changes)

### Task Status Values
- **Pending**: Defined but not started
- **In Progress**: Currently being worked on
- **Blocked**: Cannot proceed due to blockers
- **Broken Down**: Decomposed into subtasks (auto-completes when subtasks finish)
- **Finished**: Complete

### Critical Workflow Rules
1. Tasks ≥7 difficulty **must** be broken down before starting work
2. "Broken Down" tasks **cannot** be worked on directly (work on subtasks instead)
3. Always use `complete-task.md` command to start work (ensures status tracking)
4. Parent tasks **automatically** transition to "Finished" when last subtask completes
5. Run `update-tasks.md` regularly to validate task system health

## Example: From Idea to Working Environment

**User's Initial Request:**
> "I need to build an ETL pipeline that pulls carbon emissions data from various APIs,
> processes it with Polars, and loads it into Azure SQL Database for a Power BI dashboard."

**After Specification in Claude Desktop:**
- Export detailed requirements document
- Include API sources, data volume, error handling needs, authentication details

**In VS Code with Claude Code:**
```
User: "Create a Data Engineering environment for this carbon emissions ETL project.
       [attaches specification.md]"

Claude Code:
1. Reads Data Engineering template from template_overview10.md
2. Generates .claude/ structure with:
   - Task 1: "Setup project structure" (difficulty: 3)
   - Task 2: "Configure API connections" (difficulty: 8) ← flagged for breakdown
   - Task 3: "Build Polars pipeline" (difficulty: 7) ← flagged for breakdown
   - Task 4: "Implement Azure SQL loader" (difficulty: 7) ← flagged for breakdown
   - Task 5: "Create scheduling system" (difficulty: 5)
3. Creates command files (breakdown.md, complete-task.md, etc.)
4. Sets up context files with Python/Polars standards
5. Provides next steps: validate with update-tasks.md, break down tasks 2-4

User: "@.claude/commands/breakdown.md 2"

Claude Code:
- Splits Task 2 into 5 subtasks (difficulty 3-5 each)
- Sets parent to "Broken Down (0/5 done)" status
- Updates task-overview.md
- Suggests starting with first subtask

User: "@.claude/commands/complete-task.md 6" (first subtask)

Claude Code:
- Confirms task details
- Updates status: Pending → In Progress
- Performs work (creates API client base class)
- Updates status: In Progress → Finished
- Updates parent progress: "Broken Down (1/5 done)"
- Suggests next subtask
```

**Result:**
- Clear task hierarchy with manageable complexity
- Automatic progress tracking
- Reduced error risk through subtask breakdown
- Complete environment ready for productive work

## Resources

- **Main Template Documentation**: `template_overview10.md`
- **Current Development Tasks**: `todo.md`
- **AI Context Guide**: `CLAUDE.md` (for Claude Code to understand this repo)

## Contributing

This is a personal template repository, but the patterns are designed to be adaptable. Feel free to fork and customize for your own workflow.

## Version History

- **v10** (Current): Hierarchical task management with automatic parent completion, Gemini API integration
- Earlier versions focused on basic task tracking and command patterns

## License

Templates and documentation in this repository are provided as-is for personal use.
