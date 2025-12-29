# Universal Claude Code Template

A standardized, copy-paste-ready project template for Claude Code that provides robust task management, phase tracking, decision logging, and agent integration.

## What Is This?

This is a **universal project template** that works for any type of software project. Instead of choosing from multiple template types, you get one flexible structure that adapts to your needs.

**Key Features:**
- Hierarchical task management with automatic parent completion
- Phase/component tracking for project structure
- Architectural decision logging and traceability
- Optional planning phase for specification development
- Standardized agent integration
- Executive summaries that serve as single source of truth

## Quick Start

### Option 1: Direct to Building (Specification Already Clear)

```bash
# 1. Copy template to your project directory
cp -r universal-template/ /path/to/your-project/
cd /path/to/your-project/

# 2. Remove planning folder (not needed)
rm -rf planning/

# 3. Open in VS Code with Claude Code
code .

# 4. Define your project structure
# Edit: .claude/context/overview.md
# Edit: .claude/context/phases.md
# Edit: .claude/context/decisions.md

# 5. Create initial tasks and start building
```

### Option 2: Planning Phase First (Specification Development)

```bash
# 1. Copy template to your project directory
cp -r universal-template/ /path/to/your-project/
cd /path/to/your-project/

# 2. Open in VS Code with Claude Code
code .

# 3. Initialize specification development
# In Claude Code, run: /init-specification

# 4. Develop specification iteratively in planning/specification.md

# 5. When ready to validate
# In Claude Code, run: /test-specification

# 6. Complete generated tasks to refine specification

# 7. Pull finalized plan to main project
# In Claude Code, run: /sync-from-planning

# 8. Start building
```

## Folder Structure

```
your-project/
├── CLAUDE.md                    # Canonical reference - READ THIS FIRST
├── README.md                    # Human-facing documentation
├── planning/                    # OPTIONAL: For specification development
│   ├── specification.md         # Iteratively developed spec
│   ├── tests/                   # Specification validation tests
│   └── .claude/                 # Planning task management
│       ├── context/
│       │   ├── decisions.md     # Decisions during planning
│       │   └── phases.md        # Phase definitions
│       ├── tasks/               # Specification refinement tasks
│       └── commands/
└── .claude/                     # Main task management
    ├── context/
    │   ├── overview.md          # Project summary
    │   ├── phases.md            # Phase/component architecture
    │   └── decisions.md         # Architectural decisions
    ├── tasks/
    │   ├── task-overview.md     # Auto-generated summary
    │   └── task-*.json          # Individual tasks
    ├── commands/
    │   ├── init-specification.md
    │   ├── test-specification.md
    │   ├── update-executive-summary.md
    │   ├── complete-task.md
    │   ├── breakdown.md
    │   └── sync-tasks.md
    ├── agents/
    │   ├── specification-architect.md
    │   ├── implementation-architect.md
    │   └── test-generator.md
    └── reference/
        ├── task-schema.md
        ├── phase-schema.md
        ├── decision-schema.md
        └── test-schema.md
```

## Core Concepts

### Single Source of Truth Hierarchy

```
CLAUDE.md (standards and canonical reference)
    ↓
.claude/context/phases.md (project structure)
.claude/context/decisions.md (major decisions)
    ↓
.claude/tasks/*.json (implementation work)
```

**Executive summaries** (phases.md, decisions.md) require approval before changes.
**Tasks** derive from and reference phases/decisions.

### Task Management

- **Task Schema**: Standardized JSON structure for all tasks
- **Difficulty Scoring**: 1-10 scale (≥7 must be broken down)
- **Status Tracking**: pending → in_progress → finished (or broken_down)
- **Auto-Completion**: Parent tasks auto-complete when all subtasks finished
- **Validation**: Each task defines completion criteria

**Key Commands:**
- `/complete-task` - Start or finish a task
- `/breakdown` - Split high-difficulty tasks into subtasks
- `/sync-tasks` - Update task-overview.md from JSON files

### Phase Tracking

Phases represent major stages in your project:
- Clear inputs and outputs
- Defined components
- Links to tasks and decisions
- Status tracking (pending → active → completed)

**Defined in**: `.claude/context/phases.md` (executive summary)

### Decision Tracking

Track only **architectural and major decisions**:
- Custom categories (defined during initialization)
- Alternatives considered and rejected
- Reasoning and impacts
- Traceability to tasks and phases

**Defined in**: `.claude/context/decisions.md` (executive summary)

### Agent Integration

Specialized agents for complex tasks:
- **specification-architect**: Validate specifications
- **implementation-architect**: Design implementations
- **test-generator**: Create test tasks

**Configured in**: `.claude/agents/*.md`

## Key Commands

### /init-specification
Initialize planning phase with custom decision categories.

**Use When**: Starting a project that needs detailed specification development

**Process**:
1. Define decision categories (architecture, data, integration, security, etc.)
2. Creates planning folder structure
3. Sets up specification template

### /test-specification
Generate and execute specification validation tests.

**Use When**: Ready to validate specification for completeness and consistency

**Process**:
1. Generates test files in planning/tests/
2. Executes tests with specification-architect agent
3. Creates tasks for issues found
4. Produces test results summary

### /update-executive-summary
Refresh phases.md and decisions.md based on recent work.

**Use When**: After completing several tasks, or periodically to keep summaries current

**Process**:
1. Analyzes completed tasks
2. Proposes changes to executive summaries
3. **Requires approval** before applying changes
4. Updates change logs

### /complete-task
Start or finish a task with status tracking.

**Use When**: Beginning work on a task or marking it complete

**Usage**:
- `/complete-task task-042 start` - Mark task as in_progress
- `/complete-task task-042 finish` - Mark task as finished

### /breakdown
Split high-difficulty tasks (≥7) into subtasks.

**Use When**: Task difficulty is ≥7

**Process**:
1. Analyzes task complexity
2. Creates subtasks with lower difficulty
3. Updates parent task status to broken_down
4. Parent auto-completes when all subtasks finished

### /sync-tasks
Update task-overview.md from task JSON files.

**Use When**: After creating, updating, or completing tasks

**Output**: `.claude/tasks/task-overview.md` with formatted table

## Benefits

1. **Universal**: Works for any project type (no template selection needed)
2. **Flexible**: Planning phase is optional
3. **Traceable**: Phases, decisions, and tasks all linked
4. **Standardized**: Comprehensive documentation in CLAUDE.md
5. **Agent-Ready**: Clear integration points for specialized agents
6. **Evolvable**: Structure can change as project evolves
7. **Version-Controlled**: All project context in plain text files

## Getting Started Checklist

### If Skipping Planning Phase
- [ ] Copy universal-template/ to project directory
- [ ] Remove planning/ folder
- [ ] Edit .claude/context/overview.md (project purpose, goals, scope)
- [ ] Edit .claude/context/phases.md (define project phases)
- [ ] Edit .claude/context/decisions.md (add decision categories)
- [ ] Create initial tasks in .claude/tasks/
- [ ] Run /sync-tasks
- [ ] Start building!

### If Using Planning Phase
- [ ] Copy universal-template/ to project directory
- [ ] Run /init-specification (define decision categories)
- [ ] Develop planning/specification.md iteratively
- [ ] Define phases in planning/.claude/context/phases.md
- [ ] Document decisions in planning/.claude/context/decisions.md
- [ ] Run /test-specification when ready to validate
- [ ] Complete generated refinement tasks
- [ ] Run /sync-from-planning to pull plan to main .claude/
- [ ] Start building!

## Documentation

**Start Here**: `CLAUDE.md` - Canonical reference for all standards and workflows

**Schemas**:
- `.claude/reference/task-schema.md` - Task JSON structure
- `.claude/reference/phase-schema.md` - Phase tracking structure
- `.claude/reference/decision-schema.md` - Decision tracking structure
- `.claude/reference/test-schema.md` - Specification test structure

**Commands**:
- See `.claude/commands/*.md` for detailed command documentation

**Agents**:
- See `.claude/agents/*.md` for agent configurations and capabilities

## Example Projects

### Data Pipeline Project
- **Phases**: Ingestion → Transformation → Serving
- **Decision Categories**: architecture, data, integration
- **Planning Phase**: Optional (if requirements are clear)

### Web Application Project
- **Phases**: Backend → Frontend → Integration → Deployment
- **Decision Categories**: architecture, security, ux
- **Planning Phase**: Recommended (for UX flows and API design)

### Research/Analysis Project
- **Phases**: Data Collection → Analysis → Reporting
- **Decision Categories**: data, analysis
- **Planning Phase**: Recommended (for methodology specification)

## Customization

This is a **template** - customize it for your needs:

1. **Add project-specific standards** in `.claude/context/standards/`
2. **Modify decision categories** to match your domain
3. **Create custom commands** in `.claude/commands/`
4. **Add custom agents** in `.claude/agents/`
5. **Update CLAUDE.md** to document your customizations

**Philosophy**: The structure is standardized, but the content is yours.

## When Things Go Wrong

**Can't find where to document something?**
→ Check "Folder Structure Standard" in CLAUDE.md

**Not sure if a decision should be tracked?**
→ Check decision-schema.md - only track major/architectural decisions

**Phase structure doesn't match reality?**
→ Run /update-executive-summary and get approval for changes

**Task complexity is overwhelming?**
→ Check difficulty score, use /breakdown if ≥7

**Structure feels too rigid?**
→ Customize CLAUDE.md for your needs, but document deviations

## Contributing to Template

This template is designed to be improved over time:

1. Test the template on real projects
2. Document pain points and inefficiencies
3. Propose improvements to schemas and workflows
4. Update CLAUDE.md with best practices
5. Refine command patterns based on usage

## Version History

- **v2.0 (2025-12-29)**: Universal template with standardized schemas
- **v1.0**: Multi-template architecture (deprecated)

## License

[Your license here]

## Support

For questions or issues:
- Read CLAUDE.md for comprehensive documentation
- Check schema files in `.claude/reference/`
- Review command documentation in `.claude/commands/`
