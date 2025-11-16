# Repository Context

## What This Repository Is

This is a **meta-repository** for Claude Code environment templates. It serves three purposes:

1. **Version Control**: Track evolution of environment templates over time
2. **Component Library**: Reusable, composable components for different project types
3. **Iteration Space**: Refine patterns based on real-world project experience

## Repository Structure

```
claude_code_environment/
├── CLAUDE.md                    # Router file for Claude Code (main entry point)
├── README.md                    # Human-readable documentation
├── legacy-template-reference.md # Comprehensive template documentation (52KB, frozen snapshot)
├── components/                  # Reusable, composable components
│   └── task-management/         # Hierarchical task tracking system
│       ├── README.md            # Component documentation
│       ├── schema.json          # Task JSON schema definition
│       ├── commands/            # Reusable command patterns
│       │   ├── breakdown.md
│       │   ├── complete-task.md
│       │   ├── sync-tasks.md
│       │   └── update-tasks.md
│       └── reference/           # Supporting documentation
│           ├── breakdown-workflow.md
│           ├── difficulty-guide.md
│           └── validation-rules.md
└── .claude/                     # This repository's own Claude environment
    ├── commands/                # Commands for working on this repo
    ├── context/                 # This file and other context docs
    └── tasks/                   # Work tracking for this repo

```

## Key Concepts

### 1. Component Composition Pattern

Components are **self-contained, reusable units** that can be composed into complete project environments. Each component follows this structure:

```
component-name/
├── README.md           # Component overview, concepts, integration guide
├── schema.json         # (If applicable) Data structure definitions
├── commands/           # Reusable workflow patterns (.md files)
├── reference/          # Supporting documentation
└── examples/           # (Optional) Example usage

```

**Current Components:**
- **task-management**: Hierarchical task tracking with automatic parent completion

**Template Development:**
See `.claude/tasks/task-overview.md` for completed work on templates (documentation-content, research-analysis, life-projects, power-query)

### 2. Template Authoring

Templates in `legacy-template-reference.md` (historical) are **composition recipes** that combine components based on project needs:

- **Base Template**: Task management + minimal structure
- **Data Engineering Template**: Base + Python standards + SQL conventions
- **BI/Dashboard Template**: Base + DAX patterns + KPI documentation
- **Hybrid Template**: Custom component mix

### 3. Environment Generation Workflow

When a user creates a new project with Claude Code:

1. **User provides specification** (from Claude Desktop export or direct description)
2. **Claude Code selects template** based on project type
3. **Components are instantiated** into `.claude/` folder structure:
   - Copy command files from `components/*/commands/` to `.claude/commands/`
   - Copy reference docs from `components/*/reference/` to `.claude/reference/`
   - Create initial context files (overview.md, standards/)
   - Generate initial task JSON files
4. **CLAUDE.md is created** as a router (<100 lines, points to context files)
5. **User validates** with `update-tasks.md` and begins work

## Working in This Repository

### Common Tasks

#### Adding a New Component

1. Create `components/component-name/` directory
2. Write `README.md` with:
   - Overview and core concepts
   - File structure
   - Integration guide (how to use in projects)
   - Benefits and best practices
3. Create subdirectories (commands/, reference/, examples/)
4. Update `template_overview10.md` to reference the component
5. Update this file (`context/overview.md`) to list the new component

#### Updating Task Management Component

When changing task schema or workflow:

1. Update `components/task-management/schema.json`
2. Update command files in `components/task-management/commands/`
3. Update reference docs in `components/task-management/reference/`
4. Update `components/task-management/README.md`
5. Update relevant sections in `template_overview10.md`
6. Test with sample tasks in `.claude/tasks/`

#### Creating New Template Types

1. Create template in `templates/[name]/`:
   - README.md with template name, purpose, when to use it
   - components.json defining which components to include
   - customizations/ folder with domain-specific additions
2. Add to README.md under "Available Templates"
3. Test by generating a sample environment

#### Testing Templates

1. Create temporary directory: `mkdir /tmp/test-environment`
2. Generate `.claude/` structure based on template pattern
3. Validate:
   - All command files present and formatted correctly
   - Reference docs copied correctly
   - Task JSON files follow schema
   - CLAUDE.md router points to correct locations
4. Test workflow: create sample task → break down (if ≥7) → complete → verify parent completion
5. Clean up: `rm -rf /tmp/test-environment`

### Development Workflow for This Repo

1. **Check `.claude/tasks/task-overview.md`** for current focus areas and completed tasks
2. **Work on tasks** using `.claude/tasks/task-*.json` files
3. **Use commands** in `.claude/commands/` (complete-task.md, breakdown.md, etc.)
4. **Update documentation** as templates evolve
5. **Update templates/**: Modify template READMEs and customizations as needed
6. **Commit with clear messages**: Describe impact on template generation

## File Roles

### CLAUDE.md
**Purpose**: Main entry point for Claude Code when working on this repository

**Content**:
- Repository purpose and role
- Core workflow explanation
- Key files overview
- Task management concepts (references component)
- Tool integration strategy (Gemini vs Claude)
- Working in this repository guidelines
- Navigation rules

**Maintenance**: Keep under 200 lines; point to detailed docs rather than duplicating

### README.md
**Audience**: Human developers (GitHub visitors, future self)

**Content**:
- What problem this solves
- Typical workflow (Claude Desktop → VS Code)
- Template types available
- Benefits and features
- Getting started guide
- Example: idea to working environment

**Maintenance**: Update when adding new template types or major features

### legacy-template-reference.md
**Purpose**: Historical comprehensive template documentation (52KB, frozen snapshot)

**Content**:
- Quick start (5-minute minimal setup)
- Environment types (Base, Data Engineering, BI, Hybrid, Power Query)
- Task management system documentation
- Command file examples
- Context file templates
- Tool integration guidance

**Status**: Frozen historical reference
- Not actively maintained
- Preserved for understanding template evolution
- New templates use component-based architecture in templates/

### .claude/tasks/
**Purpose**: Structured task management for this repository

**Content**:
- task-overview.md: Summary of all tasks with progress tracking
- task-*.json: Individual task files with full details
- Completed tasks archived with notes and outcomes

**Maintenance**: Use commands (complete-task, breakdown, sync-tasks) to manage tasks

### components/*/README.md
**Purpose**: Component-specific documentation

**Content**:
- Component overview and concepts
- File structure and schema
- Command descriptions
- Integration guide
- Workflow examples
- Best practices and common pitfalls

**Maintenance**: Update when component changes; keep synchronized with command files

## Integration Patterns

### Lazy Loading Context

**Problem**: Large template files consume tokens unnecessarily

**Solution**: Router pattern in CLAUDE.md
- Keep CLAUDE.md minimal (<200 lines)
- Reference specific files by topic
- Let Claude Code read only what's needed

**Example**:
```markdown
## Navigation Rules

- **Creating new environment?** → Reference `templates/[name]/README.md` or use `.claude/commands/bootstrap.md`
- **Task management questions?** → See `components/task-management/README.md`
- **Command pattern examples?** → See `components/task-management/commands/`
```

### Component Composition

**Problem**: Different project types need different capabilities

**Solution**: Mix and match components
- Base: task-management only
- Data Engineering: task-management + python-standards + sql-conventions
- BI/Dashboard: task-management + dax-patterns + kpi-docs
- Hybrid: custom component selection

**Benefits**:
- Reusability across project types
- Independent component evolution
- Easier maintenance (update component once, affects all templates)

### Version Control Strategy

**Problem**: Template changes might break existing projects

**Solution**: Sequential versioning
- Current: `template_overview10.md`
- After breaking changes: `template_overview11.md`
- Keep previous versions available for reference
- Document migration path in README.md

## Tool Routing

### When to Use Gemini API (via MCP)

- **Research**: Current regulations, market trends, up-to-date information (use `grounding: true`)
- **Domain Analysis**: Industry expertise, compliance interpretation
- **Content Generation**: Documentation, summaries, blog posts
- **Image Analysis**: Chart interpretation, dashboard reviews
- **Code Review**: Architecture patterns, best practices validation

**Model Selection**:
- `gemini-2.5-pro` with `grounding: true`: Factual/current information, complex analysis
- `gemini-2.5-flash`: Speed-critical tasks, simple queries, image analysis

### When to Use Claude Native Capabilities

- **Code Implementation**: Writing, editing, refactoring, debugging
- **System Design**: ETL pipelines, database schemas, architecture
- **Project Management**: Task breakdown, file operations, status tracking
- **File System Operations**: Read, Write, Edit tools

### Hybrid Workflows

1. **Analysis → Implementation**: Gemini researches/reviews → Claude implements
2. **Review → Refactor**: Gemini provides feedback → Claude applies changes
3. **Research → Design**: Gemini gathers information → Claude designs solution

## Conventions

### Documentation Style

- **No emojis** unless explicitly requested by user
- **Markdown format** for all documentation
- **Active voice** in command descriptions
- **Clear hierarchy** with H2/H3/H4 headers
- **Code fences** with language hints
- **Examples** for complex concepts

### File Naming

- **Templates**: `template_overview{version}.md` (sequential versioning)
- **Tasks**: `task-{id}.json` (sequential IDs, no gaps)
- **Commands**: `{verb}-{noun}.md` (e.g., `complete-task.md`, `sync-tasks.md`)
- **Components**: `{domain-name}/` (lowercase with hyphens)

### JSON Schema

- Use JSON Schema Draft 7
- Include descriptions for all fields
- Mark required fields explicitly
- Provide examples in component README
- Validate with `update-tasks.md` command

### Command File Format

All command files follow this structure:

```markdown
# Command Name

## Purpose
One-sentence description of what this command does

## Context Required
- What information/files Claude Code needs to read
- What state validations are needed

## Process
1. Step-by-step workflow
2. Including validation checks
3. And error handling

## Output Location
Where results are written (files, status updates)

## Critical Rules
- Important constraints
- What NOT to do
- Edge cases to handle
```

## Current Focus

**Primary**: Extracting components from monolithic `template_overview10.md`

**In Progress**:
- Task 1: Task management component ✓ Finished
- Task 2: Documentation/content template component (Pending)

**Upcoming**:
- Testing/validation patterns component
- Technology-specific standards (Python, SQL, DAX, M)
- Gemini MCP integration patterns

See `.claude/tasks/task-overview.md` for detailed progress.

## Related Files

- **CLAUDE.md**: Main router for Claude Code (read this first when working on repo)
- **README.md**: Human documentation (for GitHub/reference)
- **legacy-template-reference.md**: Historical comprehensive template documentation (frozen snapshot)
- **templates/[name]/README.md**: Current template documentation
- **components/task-management/README.md**: Task system documentation
- **.claude/tasks/task-overview.md**: Current work tracking and completed tasks
