# Claude Code Environment Templates

**Version-controlled templates for bootstrapping Claude Code projects with structured task management and reusable workflows.**

## 5-Minute Quickstart

**Get from zero to working environment in 5 minutes:**

- [ ] **Step 1** (1 min): Clone this repo locally
  ```bash
  git clone https://github.com/yourusername/claude_code_environment.git
  ```

- [ ] **Step 2** (1 min): Write project spec in Claude Desktop → export as .md file
  - Describe what you're building
  - Include key technologies (Power BI, Python, etc.)
  - List main requirements/deliverables
  - See `examples/specifications/templates/` for examples

- [ ] **Step 3** (30 sec): Create new project directory
  ```bash
  mkdir ~/Projects/my-new-project
  cd ~/Projects/my-new-project
  ```

- [ ] **Step 4** (1 min): Open in VS Code with Claude Code, say:
  ```
  "Create the environment from claude_code_environment repo using spec: [path/to/spec.md]"
  ```

- [ ] **Step 5** (1-2 min): Verify environment created
  - Check `.claude/` directory exists with commands, context, tasks folders
  - Run `/sync-tasks` to see task overview
  - Start first task: `/complete-task 1`

**Total time: ~5 minutes**

**New to this system?** Try the interactive tutorial first:
```
/tutorial-bootstrap
```
Gets you familiar with the process using a safe example before using real projects.

**Video walkthrough:** [Coming soon - placeholder for future screencast]

---

## Quick Start

**Simplified workflow - just one command:**

```bash
# In Claude Code (VS Code), from your new project directory:
"Create the environment from claude_code_environment repo using spec: [path/to/spec.md]"
```

**That's it!** Claude Code will:
- Automatically detect the right template (Power Query, Research, Documentation, Life Projects, or Base)
- Extract content from your specification
- Generate complete `.claude/` structure with:
  - Task management system with automatic breakdown
  - Template-specific commands and standards
  - Context files populated from your spec
  - Optional: Initial tasks from detected deliverables

**No need to manually choose a template** - smart detection analyzes your specification and selects the best match.

## How It Works

### Smart Bootstrap (Recommended)

The **smart-bootstrap** command (`.claude/commands/smart-bootstrap.md`) automatically detects the right template:

1. **Reads** your project specification
2. **Analyzes** content for template signals (keywords, technologies, domain indicators)
3. **Scores** each template using pattern matching rules
4. **Selects** highest-scoring template (auto-select if score ≥ 70)
5. **Extracts** content from spec to populate files
6. **Generates** complete `.claude/` structure

**Detection confidence levels:**
- **90-100**: High confidence - auto-select without asking
- **70-89**: Medium-high - auto-select with explanation
- **50-69**: Medium - recommend with easy override
- **< 50**: Low - ask user to choose

### Component-Based Architecture

**Components** (e.g., task-management) provide reusable, versioned functionality.
**Templates** (e.g., research-analysis) combine components + domain-specific customizations.

At initialization, Claude Code:
1. Detects appropriate template from specification
2. Reads template's `components.json`
3. Includes required components
4. Adds template customizations
5. Generates `.claude/` folder in your project
6. Populates files with content from your spec

## Available Templates

| Template | Use Case | Key Features |
|----------|----------|--------------|
| **research-analysis** | Academic research, data science, experiments | Literature review workflows, hypothesis tracking, statistical methods, citation standards |
| **documentation-content** | Technical docs, API docs, content writing | Writing standards, doc structure patterns, review workflows, publishing commands |
| **life-projects** | Home improvement, event planning, personal goals | Budget management, timeline planning, decision logs, vendor evaluation |
| **power-query** | Excel Power Query, regulatory calculations | Phase 0 ambiguity resolution, 5-dimension difficulty scoring, M-code standards, Excel integration |

**Detailed docs:** See `templates/[name]/README.md` or `legacy-template-reference.md`

## Workflow

1. **Create spec** (Claude Desktop): Discuss project, export to .md file
2. **Bootstrap** (Claude Code): `"Create the environment from claude_code_environment repo using spec: [path]"`
   - Smart detection analyzes your spec
   - Automatically selects appropriate template
   - Populates files with extracted content
   - Asks only necessary clarifying questions (if ambiguous)
3. **Work**: Break down tasks ≥7 difficulty, use commands (`complete-task`, `breakdown`, etc.), auto-tracked progress

### Advanced: Manual Template Selection

If you prefer to choose the template yourself:
```
"Use bootstrap.md command to interactively set up [template-name] environment"
```

## Generated Structure

```
your-project/
├── CLAUDE.md              # Router file
├── README.md              # Human docs
└── .claude/
    ├── commands/          # Workflows (complete-task, breakdown, sync-tasks, etc.)
    ├── context/           # Project understanding (overview, standards, validation)
    ├── tasks/             # Work tracking (task-overview.md, task-*.json)
    └── reference/         # Supporting docs (difficulty guide, workflow patterns)
```

## Key Features

**Task Management:**
- Difficulty scoring (1-10) based on LLM error risk
- Auto-breakdown for tasks ≥7
- Parent tasks auto-complete when subtasks finish
- Progress tracking: "Broken Down (X/Y done)"

**Commands:** `complete-task`, `breakdown`, `sync-tasks`, `update-tasks`, plus template-specific workflows

**Versioning:** Components and templates versioned independently (semantic versioning)

## Usage

**Starting a new project (recommended):**
```
"Create the environment from claude_code_environment repo using spec: project-spec.md"
```

The smart bootstrap will:
1. Read your specification
2. Detect template type using pattern matching (see `.claude/reference/template-selection-rules.md`)
3. Generate environment with content from your spec
4. Explain detection reasoning

**See example specifications** in `examples/specifications/` to understand detection patterns.

**Maintaining this repo:**
- **Add component:** Create `components/[name]/` with README, schema, commands/, reference/
- **Add template:** Create `templates/[name]/` with README, components.json, customizations/
- **Update component:** Follow semver, update README, test with templates
- **Update detection:** Modify `.claude/reference/template-selection-rules.md` with new patterns

## Task Management Quick Reference

**Difficulty (LLM error risk):** 1-2 (trivial), 3-4 (low), 5-6 (moderate), 7-8 (high, **breakdown required**), 9-10 (extreme, **breakdown required**)

**Status:** Pending → In Progress → Finished | Blocked | Broken Down (auto-completes when subtasks done)

**Rules:** Tasks ≥7 must break down before starting. Use `complete-task.md` to start work. Parents auto-finish when subtasks complete.

## Resources

- **Templates:** `templates/[name]/README.md` for detailed docs
- **Components:** `components/[name]/README.md` for component docs
- **Development:** See `.claude/tasks/task-overview.md`

### Legacy Reference

`legacy-template-reference.md` is a **frozen historical snapshot** (52KB) of the original monolithic template documentation. It is:
- **Not actively maintained** - preserved as-is for historical context
- **Superseded by** the component-based architecture in `templates/` and `components/`
- **Useful for** understanding the evolution of template patterns
- **Not recommended** for new projects - use current templates instead

---

**License:** Provided as-is for personal use. Fork and customize as needed.
