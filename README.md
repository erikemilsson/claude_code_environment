# Claude Code Environment Templates

**Version-controlled templates for bootstrapping Claude Code projects with structured task management and reusable workflows.**

## Quick Start

**In your new project directory:**

```bash
# In Claude Code (VS Code)
"Create a [template-name] environment from claude_code_environment repo"
```

Claude Code generates a complete `.claude/` structure with:
- Task management system with automatic breakdown
- Project-type-specific commands and standards
- Context files for AI understanding
- Initial tasks from your specification

**Choose your template:** research-analysis, documentation-content, life-projects, power-query

## How It Works

**Components** (e.g., task-management) provide reusable, versioned functionality.
**Templates** (e.g., research-analysis) combine components + domain-specific customizations.

At initialization, Claude Code:
1. Reads template's `components.json`
2. Includes required components
3. Adds template customizations
4. Generates `.claude/` folder in your project
5. Creates initial tasks from your spec

## Available Templates

| Template | Use Case | Key Features |
|----------|----------|--------------|
| **research-analysis** | Academic research, data science, experiments | Literature review workflows, hypothesis tracking, statistical methods, citation standards |
| **documentation-content** | Technical docs, API docs, content writing | Writing standards, doc structure patterns, review workflows, publishing commands |
| **life-projects** | Home improvement, event planning, personal goals | Budget management, timeline planning, decision logs, vendor evaluation |
| **power-query** | Excel Power Query, regulatory calculations | Phase 0 ambiguity resolution, 5-dimension difficulty scoring, M-code standards, Excel integration |

**Detailed docs:** See `templates/[name]/README.md` or `template_overview10.md`

## Workflow

1. **Create spec** (Claude Desktop): Discuss project, export to .md file
2. **Bootstrap** (Claude Code): `"Create [template] environment..."` → generates `.claude/` structure
3. **Work**: Break down tasks ≥7 difficulty, use commands (`complete-task`, `breakdown`, etc.), auto-tracked progress

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

**Starting a new project:**
```
"Create a [template-name] environment from claude_code_environment repo.
Here's my specification: [paste/attach spec.md]"
```

**Maintaining this repo:**
- **Add component:** Create `components/[name]/` with README, schema, commands/, reference/
- **Add template:** Create `templates/[name]/` with README, components.json, customizations/
- **Update component:** Follow semver, update README, test with templates

## Task Management Quick Reference

**Difficulty (LLM error risk):** 1-2 (trivial), 3-4 (low), 5-6 (moderate), 7-8 (high, **breakdown required**), 9-10 (extreme, **breakdown required**)

**Status:** Pending → In Progress → Finished | Blocked | Broken Down (auto-completes when subtasks done)

**Rules:** Tasks ≥7 must break down before starting. Use `complete-task.md` to start work. Parents auto-finish when subtasks complete.

## Resources

- **Templates:** `templates/[name]/README.md` for detailed docs
- **Components:** `components/[name]/README.md` for component docs
- **Legacy reference:** `template_overview10.md` (52KB monolithic version)
- **Development:** See `todo.md`

---

**License:** Provided as-is for personal use. Fork and customize as needed.
