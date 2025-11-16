# Claude Code Environment Templates

A version-controlled repository of modular components and templates for bootstrapping new Claude Code projects.

## Purpose

This repository provides a component-based architecture for creating Claude Code environments. Instead of monolithic template files, it uses:

- **Reusable components** (task-management, data-pipelines, etc.) that can be mixed and matched
- **Project-type templates** (research-analysis, documentation-content, life-projects) that compose components with domain-specific customizations
- **Version control** for both components and templates independently
- **Clear composition patterns** via `components.json` manifests

## The Problem This Solves

When starting a new project with Claude Code, you need:
- Consistent file structure for AI context management
- Task tracking system with proper breakdown strategies
- Reusable command patterns for common workflows
- Technology-specific coding standards
- Clear separation between AI context and human documentation

Creating these from scratch every time is inefficient. This repository provides modular, version-controlled building blocks you can compose and reuse across multiple projects.

## Architecture Overview

### Components vs Templates

```
components/                    # Reusable, versioned modules
├── task-management/          # Core task tracking (v1.0.0)
│   ├── README.md             # Component docs + versioning
│   ├── schema.json           # Task structure definition
│   ├── commands/             # Reusable workflows
│   └── reference/            # Supporting documentation

templates/                     # Project-type environments
├── research-analysis/        # For research projects
│   ├── README.md             # When to use, what's included
│   ├── components.json       # Component dependencies + customizations
│   └── customizations/       # Template-specific files
├── documentation-content/    # For docs/writing projects
└── life-projects/            # For non-tech projects
```

### How Components and Templates Work Together

1. **Components** = Reusable modules with generic functionality
   - Versioned independently (semantic versioning)
   - Can be used by multiple templates
   - Example: task-management component (v1.0.0)

2. **Templates** = Project-type-specific environments
   - Declare which components they use (via `components.json`)
   - Add domain-specific customizations (standards, workflows, commands)
   - Example: research-analysis template uses task-management + adds hypothesis tracking, literature review workflows, citation standards

3. **Composition** happens at project initialization:
   ```
   User requests: "Create research-analysis environment"

   Claude Code:
   1. Reads templates/research-analysis/components.json
   2. Includes task-management component (commands + reference docs)
   3. Adds research-specific customizations (lit review, hypothesis tracking)
   4. Generates .claude/ structure in target project
   5. Creates initial tasks based on user's specification
   ```

## Available Templates

### 1. Research/Analysis Template
**Path:** `templates/research-analysis/`

For academic research, data science projects, experimental work, and market research.

**Includes:**
- Task management component (v1.0.0)
- Literature review structure and workflows
- Hypothesis tracking framework
- Experiment design patterns
- Data analysis workflows (exploration, cleaning, validation)
- Citation management standards
- Statistical methods reference guide

**When to use:**
- Graduate research and dissertations
- Data science and statistical modeling
- Experimental research and A/B testing
- Market and competitive analysis

### 2. Documentation/Content Template
**Path:** `templates/documentation-content/`

For technical documentation, API docs, content creation, and writing projects.

**Includes:**
- Task management component (v1.0.0)
- Writing style guides
- Documentation structure patterns
- API documentation standards
- Content review workflows
- Publishing command patterns
- Content review checklists

**When to use:**
- Technical documentation projects
- API documentation
- User guides and tutorials
- Content creation and editing

### 3. Life Projects Template
**Path:** `templates/life-projects/`

For everyday non-technical projects like home improvement, event planning, moving, etc.

**Includes:**
- Task management component (v1.0.0)
- Project planning standards
- Budget management guidelines
- Timeline planning patterns
- Progress tracking workflows
- Decision-making processes
- Vendor evaluation workflows
- Project brief, budget, and decision log templates

**When to use:**
- Home renovation or improvement
- Event planning (weddings, parties)
- Moving and relocation
- Personal goal projects
- Family projects and coordination

### 4. Power Query Template
**Path:** `templates/power-query/`

For Excel Power Query projects, regulatory/compliance calculations, and complex data transformations.

**Key Features:**
- **Phase 0 Workflow**: Front-load all ambiguity resolution before coding begins
  - Initialize project: Analyze calculation documents, extract ambiguities
  - Resolve ambiguities: Interactive batch resolution (5 at a time)
  - Generate artifacts: Create glossary, data contracts, initial tasks
  - Extract queries: Extract .m files from Excel, enable watch mode
- **Phase 0 Outputs**: Glossary, assumptions, data contracts, query manifest, dependency graph
- **LLM Pitfalls Checklist**: Pre-populated common mistakes when interpreting regulatory documents
- **5-Dimension Difficulty Scoring**:
  - Query Dependency Depth (1-10)
  - Formula Complexity (1-10)
  - Error Surface (1-10)
  - Regulatory Precision (1-10)
  - Performance Impact (1-10)
  - Final Score = Average of 5 dimensions, rounded to nearest integer
- **Excel Integration**: .m file version control, watch mode auto-sync, git-friendly workflow

**Includes:**
- Task management component (with PQ-specific difficulty scoring)
- Phase 0 commands (initialize, resolve-ambiguities, generate-artifacts, extract-queries)
- Power Query standards (M-code conventions, naming rules, error handling)
- Data architecture guide (Bronze-Silver-Gold medallion pattern)
- Validation commands (validate-query for schema checking)
- Reference documentation (ambiguity reports, data contracts, query manifests)

**When to use (Comprehensive Approach):**
- Implementing regulatory/compliance calculations (EU Battery Regulation, ISO standards, etc.)
- Source documents have ambiguous legal language
- Multiple calculation methods need reconciliation
- Audit trail required for compliance
- Zero error tolerance projects
- Team needs shared variable definitions

**When to use (Minimal Approach):**
- Existing PQ project needs documentation
- Simple data transformations
- No regulatory requirements
- Solo developer, no shared context needed
- Quick prototyping

**Link to detailed documentation**: See "Power Query Template" section in `template_overview10.md`

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

## Generated Project Structure

When you use a template, Claude Code generates this structure in your project:

```
your-project/
├── CLAUDE.md                    # Router file (<100 lines, points to context)
├── README.md                    # Human-readable documentation
└── .claude/                     # Claude-specific context
    ├── commands/                # Workflow patterns
    │   ├── complete-task.md     # From task-management component
    │   ├── breakdown.md         # From task-management component
    │   ├── sync-tasks.md        # From task-management component
    │   ├── update-tasks.md      # From task-management component
    │   └── [template-specific]  # From template customizations
    ├── context/                 # Project understanding
    │   ├── overview.md          # Generated during initialization
    │   ├── standards/           # From template customizations
    │   └── validation-rules.md  # Generated during initialization
    ├── tasks/                   # Work tracking
    │   ├── task-overview.md     # Auto-generated summary table
    │   └── task-*.json          # Individual task files
    └── reference/               # Supporting information
        ├── difficulty-guide.md       # From task-management component
        ├── breakdown-workflow.md     # From task-management component
        └── [template-specific]       # From template customizations
```

## Component Composition Pattern

Templates use `components.json` to declare dependencies and customizations:

```json
{
  "template_name": "research-analysis",
  "version": "1.0.0",
  "included_components": [
    {
      "name": "task-management",
      "path": "../../components/task-management",
      "version": "1.0.0",
      "required": true
    }
  ],
  "customizations": [
    {
      "category": "standards",
      "files": [
        {
          "name": "literature-review-structure.md",
          "path": "customizations/standards/literature-review-structure.md",
          "destination": ".claude/context/standards/literature-review.md"
        }
      ]
    }
  ]
}
```

This pattern allows:
- **Independent versioning** of components and templates
- **Selective updates** (update component without changing template)
- **Composition flexibility** (mix components as needed)
- **Clear provenance** (know where each file comes from)

## Key Features

### Hierarchical Task Management
- **Difficulty Scoring**: Tasks rated 1-10 based on LLM error probability
- **Automatic Breakdown**: Tasks ≥7 difficulty must be split into subtasks ≤6
- **Parent Auto-Completion**: "Broken Down" parent tasks automatically finish when all subtasks complete
- **Progress Tracking**: Clear visibility with "Broken Down (X/Y done)" status indicators
- **Status Validation**: Consistent state management prevents manual tracking errors

### Reusable Command Patterns
- **complete-task.md**: Standard workflow for starting and finishing work
- **breakdown.md**: Split high-difficulty tasks with automatic parent status transition
- **sync-tasks.md**: Update task-overview.md from JSON files
- **update-tasks.md**: Validate task structure and flag inconsistencies
- **Template-specific commands**: Domain-specific workflows (e.g., review-literature.md)

### Version Control
- **Component versions**: Independent semantic versioning (e.g., task-management v1.0.0)
- **Template versions**: Track template evolution separately
- **Backwards compatibility**: MINOR updates don't break existing projects
- **Migration paths**: MAJOR updates include migration scripts

## Benefits

1. **Modularity**: Components can be updated independently from templates
2. **Consistency**: Same proven patterns across all your projects
3. **Efficiency**: Bootstrap new environments in minutes, not hours
4. **Reduced Errors**: Task breakdown system prevents high-complexity failures
5. **Context Management**: Lazy-load only relevant files, minimize token usage
6. **Reusability**: Mix and match components for custom project needs
7. **Automation**: Parent task completion, status synchronization, validation checks

## How to Use This Repository

### For Starting a New Project

1. **Clone this repository** (or keep it accessible for reference)
2. **Create project specification** in Claude Desktop and export to Markdown
3. **In VS Code**, navigate to your new project directory
4. **Ask Claude Code** to create an environment based on a template:
   ```
   "Create a [research-analysis/documentation-content/life-projects/power-query] environment
   based on the claude_code_environment repository. Here's my specification:
   [paste/attach specification.md]"
   ```
5. **Claude Code will**:
   - Read the template's components.json
   - Include required components (task-management, etc.)
   - Add template-specific customizations
   - Generate `.claude/` folder structure
   - Create initial tasks with difficulty scoring
   - Provide next steps for validation and task breakdown

### For Maintaining This Repository

#### Adding New Components
1. Create `components/[name]/` directory
2. Add README.md with versioning info
3. Include schema (if applicable), commands/, reference/
4. Document integration in component README
5. Use semantic versioning

#### Adding New Templates
1. Create `templates/[name]/` directory
2. Add README.md explaining when to use
3. Create components.json listing dependencies
4. Add customizations/ folder with domain-specific files
5. Document typical tasks and initialization questions

#### Updating Existing Components
1. Follow semantic versioning (MAJOR.MINOR.PATCH)
2. Update version in component README
3. Add version history entry
4. If breaking changes, provide migration script
5. Test with existing templates

## Migration from template_overview10.md

This repository previously used a monolithic `template_overview10.md` file (52KB) containing all templates and patterns. The new component-based architecture provides:

**Before (Monolithic):**
- Single large file with all templates
- Difficult to version different parts independently
- No clear reuse mechanism across templates
- Manual copy-paste for common patterns

**After (Component-Based):**
- Components versioned independently
- Templates compose components + customizations
- Clear reuse via components.json
- Automatic composition at project initialization

**Migration Path:**
- `template_overview10.md` remains available for reference
- New projects should use component-based templates
- Existing content extracted into:
  - Task management → `components/task-management/`
  - Project types → `templates/[type]/`
  - Domain patterns → `templates/[type]/customizations/`

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
> "I need to conduct a literature review and statistical analysis for my graduate
> research on carbon emissions forecasting models."

**After Specification in Claude Desktop:**
- Export detailed requirements document
- Include research questions, methodology, data sources, analysis approach

**In VS Code with Claude Code:**
```
User: "Create a research-analysis environment based on claude_code_environment
       repository. [attaches specification.md]"

Claude Code:
1. Reads templates/research-analysis/components.json
2. Includes task-management component (v1.0.0)
   - Commands: complete-task, breakdown, sync-tasks, update-tasks
   - Reference: difficulty-guide, breakdown-workflow, validation-rules
3. Adds research-specific customizations:
   - Standards: literature-review, hypothesis-tracking, citation-format
   - Commands: review-literature, conduct-analysis
   - Reference: data-analysis-checklist, statistical-methods-guide
4. Generates .claude/ structure with:
   - Task 1: "Conduct systematic literature review" (difficulty: 8) ← breakdown required
   - Task 2: "Formulate research hypotheses" (difficulty: 5)
   - Task 3: "Collect and clean dataset" (difficulty: 6)
   - Task 4: "Build forecasting models" (difficulty: 8) ← breakdown required
   - Task 5: "Validate model performance" (difficulty: 6)
   - Task 6: "Write research paper" (difficulty: 7) ← breakdown required
5. Creates context files with research standards
6. Provides next steps: validate with update-tasks.md, break down tasks 1, 4, 6

User: "@.claude/commands/breakdown.md 1"

Claude Code:
- Splits Task 1 into 6 subtasks:
  1.1: Define search strategy and keywords (difficulty: 4)
  1.2: Search academic databases (difficulty: 3)
  1.3: Screen and filter results (difficulty: 5)
  1.4: Extract key information (difficulty: 5)
  1.5: Synthesize findings (difficulty: 6)
  1.6: Document literature gaps (difficulty: 4)
- Sets parent to "Broken Down (0/6 done)" status
- Updates task-overview.md
- Suggests starting with Task 1.1

User: "@.claude/commands/complete-task.md 7" (Task 1.1)

Claude Code:
- Confirms task details and dependencies
- Updates status: Pending → In Progress
- Performs work (creates search strategy document)
- Updates status: In Progress → Finished
- Updates parent progress: "Broken Down (1/6 done)"
- Suggests next subtask (Task 1.2)
```

**Result:**
- Complete research environment with domain-specific standards
- Clear task hierarchy with manageable complexity
- Automatic progress tracking
- Literature review workflows and citation standards
- Data analysis checklist and statistical methods guide
- Ready for productive research work

## Resources

- **Component Documentation**: See individual READMEs in `components/[name]/`
- **Template Documentation**: See individual READMEs in `templates/[name]/`
- **Legacy Reference**: `template_overview10.md` (monolithic version)
- **Current Development Tasks**: `todo.md`
- **AI Context Guide**: `CLAUDE.md` (for Claude Code to understand this repo)

## Contributing

This is a personal template repository, but the patterns are designed to be adaptable. Feel free to fork and customize for your own workflow.

## Version History

### Component-Based Architecture (Current)
- **Components**: task-management v1.0.0
- **Templates**: research-analysis v1.0.0, documentation-content v1.0.0, life-projects v1.0.0
- **Architecture**: Modular composition via components.json

### Monolithic Architecture (Legacy)
- **v10**: Hierarchical task management, Gemini API integration
- Earlier versions: Basic task tracking and command patterns
- Migrated to component-based architecture (November 2025)

## License

Templates and documentation in this repository are provided as-is for personal use.
