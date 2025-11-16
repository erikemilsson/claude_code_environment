# Power Query Project Starter Template

This is a reusable template for building Power Query projects with Claude Code assistance.

## Quick Setup

### 1. Copy Template for New Project
```bash
cp -r pq-project-starter/ my-new-project/
cd my-new-project/
```

### 2. Add Your Files

**Calculation Documents** (`calculation-docs/`)
- Place PDF, Word, or Markdown documents describing calculation methods
- Examples: Regulatory documents, technical specifications, formula references

**Excel Files** (`excel-files/`)
- Place Excel workbooks (.xlsx, .xlsm, .xlsb)
- Can include structure with headers but minimal/obfuscated data
- These are source files - Power Query will be extracted from them

### 3. Configure Project

Edit `.claude/context/overview.md`:
- Project name and description
- Goals and success criteria
- Any special requirements

### 4. Open in Claude Code
```bash
code .
```

Claude Code will automatically read `CLAUDE.md` and guide you through Phase 0 initialization.

## Phase 0: Initialization

Phase 0 resolves all ambiguities and sets up project context BEFORE any code is written.

**Commands to run in order:**
1. `@.claude/commands/initialize-project.md` - Analyzes documents
2. `@.claude/commands/resolve-ambiguities.md` - Interactive ambiguity resolution (run multiple times)
3. `@.claude/commands/generate-artifacts.md` - Creates glossary, tasks, schemas
4. `@.claude/commands/extract-queries.md` - Extracts .m files from Excel

**Output of Phase 0:**
- `.claude/context/glossary.md` - All variables defined
- `.claude/context/assumptions.md` - All interpretation decisions documented
- `.claude/reference/data-contracts.md` - Expected schemas
- `.claude/reference/query-manifest.md` - What each query does
- `.claude/reference/dependency-graph.md` - Query relationships
- `.claude/tasks/*.json` - Initial task breakdown

## Phase 1: Task Execution

After Phase 0, work on tasks:
- `@.claude/commands/complete-task.md [id]` - Execute a task
- `@.claude/commands/breakdown.md [id]` - Split complex tasks (difficulty ≥7)
- `@.claude/commands/validate-query.md [name]` - Check query schema

## Power Query Extension Setup

This template works with the **Excel Power Query Editor** VS Code extension:

1. Install extension: Search "Excel Power Query Editor" in VS Code
2. Settings to enable (in VS Code settings):
   - `excel-power-query-editor.watchAlways: true` (auto-watch extracted files)
   - `excel-power-query-editor.autoBackupBeforeSync: true` (safety)

## Data Privacy Notes

If working with sensitive data:
- Place only obfuscated/dummy data in Excel files within this project
- Keep real sensitive data in a separate environment
- Claude Code will work entirely with the obfuscated structure
- Deploy final queries to production environment separately

## Version Control

Recommended `.gitignore` is included:
- Excel files in `excel-files/` are gitignored (use Git LFS if needed)
- Backup files are gitignored
- `.m` files in `power-query/` are source of truth (tracked in git)

## Project Structure

```
project/
├── CLAUDE.md              # Router - start here
├── README.md              # This file
├── .gitignore             # Git exclusions
├── calculation-docs/      # Source documents (PDFs, etc.)
├── excel-files/           # Excel workbooks
├── power-query/           # Extracted .m files (git tracked)
├── .claude/
│   ├── commands/          # Reusable command templates
│   ├── context/           # Project understanding
│   ├── tasks/             # Work tracking
│   └── reference/         # Generated documentation
└── tests/
    ├── sample-data/       # Test inputs
    └── expected-outputs/  # Validation targets
```

## Troubleshooting

**Q: Claude doesn't see my calculation documents**
A: Make sure files are in `calculation-docs/` and you've run `initialize-project.md`

**Q: Power Query extraction fails**
A: Ensure Excel Power Query Editor extension is installed and Excel files are not open in Excel

**Q: Too many ambiguities to resolve**
A: Normal for complex regulatory documents. Batches of 5 keep it manageable. Can take 1-2 hours for complex projects.

**Q: Tasks are too difficult (>6)**
A: Use `@.claude/commands/breakdown.md [id]` to split them into subtasks

## Support

For Excel Power Query Editor extension issues:
- GitHub: https://github.com/ewc3labs/excel-power-query-editor

For Power Query M language reference:
- Microsoft Docs: https://learn.microsoft.com/en-us/powerquery-m/
