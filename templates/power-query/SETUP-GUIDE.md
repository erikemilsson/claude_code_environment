# How to Use This Template

## Quick Copy-Paste Setup

### 1. Copy Template to New Project

```bash
# Copy the entire template directory
cp -r /path/to/pq-project-starter /path/to/your-new-project

# Example:
cp -r ~/pq-project-starter ~/projects/battery-cff-calculation

# Navigate to new project
cd ~/projects/battery-cff-calculation
```

### 2. Add Your Project Files

```bash
# Add calculation method documents
cp ~/Documents/CFF-delegated-act.pdf calculation-docs/
cp ~/Documents/ISO-22628.pdf calculation-docs/

# Add Excel files (with obfuscated/dummy data)
cp ~/Documents/battery-template.xlsx excel-files/
cp ~/Documents/emission-factors.xlsx excel-files/
```

### 3. Edit Project Overview

```bash
# Open and edit the overview file
code .claude/context/overview.md

# Replace template content with your project description
# Include:
# - Project name and purpose
# - Key calculation methods being implemented
# - Data sources
# - Special requirements or constraints
```

### 4. Open in Claude Code

```bash
# Open in VS Code with Claude Code
code .

# Claude Code will automatically read CLAUDE.md
```

## Phase 0: Initialization Workflow

Once opened in Claude Code, run these commands **in order**:

### Step 1: Analyze Documents

```
@.claude/commands/initialize-project.md
```

**What happens**:
- Claude reads all documents in `calculation-docs/`
- Extracts variables, formulas, logic
- Identifies ambiguities
- Generates `ambiguity-report.md` in `.claude/reference/`

**Time**: 5-15 minutes depending on document complexity

---

### Step 2: Resolve Ambiguities (Interactive)

```
@.claude/commands/resolve-ambiguities.md
```

**What happens**:
- Claude presents first batch of 5 ambiguities
- You provide interpretation decisions
- Claude documents in `assumptions.md`
- Repeat until all ambiguities resolved

**Format of ambiguity presentation**:
```
Ambiguity Batch 1 of 5

1. [Description of ambiguity]
   Option A: [Interpretation 1]
   Option B: [Interpretation 2]
   Option C: [Interpretation 3]
   
   Your decision?

2. [Next ambiguity...]
```

**Your response format**:
```
1. B - [Brief rationale]
2. A - [Brief rationale]
3. C - [Brief rationale]
...
```

**Time**: 30 minutes - 2 hours depending on complexity

---

### Step 3: Generate Artifacts

```
@.claude/commands/generate-artifacts.md
```

**What happens**:
- Claude creates `glossary.md` with all variable definitions
- Creates `assumptions.md` with interpretation decisions
- Creates `data-contracts.md` with expected schemas
- Creates `query-manifest.md` with query descriptions
- Creates `dependency-graph.md` with query flow
- Generates initial tasks in `.claude/tasks/`
- Updates `CLAUDE.md` with Phase 1 instructions

**Review these files before proceeding!**

**Time**: 2-5 minutes

---

### Step 4: Extract Queries

```
@.claude/commands/extract-queries.md
```

**What happens**:
- Extracts all Power Query code from Excel files
- Saves individual `.m` files to `power-query/`
- Enables watch mode for auto-sync
- Creates git commit: "Phase 0 complete"

**Time**: 1-2 minutes

---

## Phase 1: Task Execution

After Phase 0, `CLAUDE.md` updates with task execution instructions.

### Working on Tasks

```
# View all tasks
View .claude/tasks/task-overview.md

# Start working on a task
@.claude/commands/complete-task.md 5

# If task is high-difficulty (≥7), break it down first
@.claude/commands/breakdown.md 5
```

### Task Workflow

1. **Check task overview**: See what needs to be done
2. **High-difficulty tasks**: Use `breakdown.md` to split into subtasks
3. **Execute task**: Use `complete-task.md [id]`
4. **Validation**: Claude auto-validates schema
5. **Watch syncs to Excel**: Changes auto-save to Excel file
6. **Review**: Check Excel file to verify results
7. **Commit**: Git commit when satisfied

### Continuous Sync

With `watchAlways` enabled (set in extension settings):
- Edit `.m` file → Save → Auto-syncs to Excel
- No manual intervention needed
- Backups created automatically

## Directory Structure Explained

```
your-project/
├── CLAUDE.md                          # Main router - Claude reads this first
├── QUICKSTART.md                      # This file
├── README.md                          # Human-readable project documentation
├── .gitignore                         # Excludes Excel files, backups, etc.
│
├── calculation-docs/                  # Your source documents
│   ├── .gitkeep                       # Keeps folder in git
│   ├── CFF-delegated-act.pdf         # (you add)
│   └── ISO-22628.pdf                  # (you add)
│
├── excel-files/                       # Your Excel files
│   ├── .gitkeep                       
│   ├── battery-template.xlsx         # (you add)
│   └── emission-factors.xlsx          # (you add)
│
├── power-query/                       # Extracted .m files (auto-generated)
│   ├── .gitkeep
│   ├── Bronze_Source_EmissionFactors.m
│   ├── Silver_Clean_EmissionFactors.m
│   └── Gold_Calculate_CFF.m
│
├── tests/                             # Testing data
│   ├── sample-data/                   # Test inputs
│   └── expected-outputs/              # Validation targets
│
└── .claude/                           # Claude-specific context
    ├── commands/                      # Reusable command templates
    │   ├── initialize-project.md      # Phase 0: Step 1
    │   ├── resolve-ambiguities.md     # Phase 0: Step 2
    │   ├── generate-artifacts.md      # Phase 0: Step 3
    │   ├── extract-queries.md         # Phase 0: Step 4
    │   ├── complete-task.md           # Phase 1: Execute task
    │   ├── breakdown.md               # Phase 1: Split high-difficulty
    │   ├── validate-query.md          # Validate schema
    │   ├── sync-tasks.md              # Update task overview
    │   └── update-tasks.md            # Validate task structure
    │
    ├── context/                       # Project understanding
    │   ├── overview.md                # Project description (YOU EDIT)
    │   ├── glossary.md                # Variable dictionary (Phase 0 creates)
    │   ├── assumptions.md             # Interpretation decisions (Phase 0 creates)
    │   ├── llm-pitfalls.md            # Regulatory doc checklist
    │   ├── data-architecture.md       # Bronze-silver-gold guide
    │   ├── validation-rules.md        # Task validation rules
    │   ├── power-query.md             # M-code conventions
    │   ├── naming.md                  # Naming rules
    │   ├── error-handling.md          # Error patterns
    │   └── critical_rules.md          # Critical development rules
    │
    ├── tasks/                         # Work tracking
    │   ├── _phase-0-status.md         # Phase 0 progress tracker
    │   ├── task-overview.md           # Main task table (auto-updated)
    │   ├── task-1.json                # (generated by Phase 0)
    │   ├── task-2.json                # (generated by Phase 0)
    │   └── ...
    │
    └── reference/                     # Information storage
        ├── ambiguity-report.md        # (generated by Phase 0)
        ├── data-contracts.md          # Expected schemas (Phase 0 creates)
        ├── query-manifest.md          # Query descriptions (Phase 0 creates)
        ├── dependency-graph.md        # Query flow (Phase 0 creates)
        ├── difficulty-guide-pq.md     # Task scoring guide
        └── breakdown-workflow.md      # Task hierarchy guide
```

## Files You Should Edit

**Before Phase 0**:
- `.claude/context/overview.md` - Add your project description

**During Phase 0**:
- Nothing! Just respond to Claude's ambiguity questions

**During Phase 1**:
- `.claude/context/assumptions.md` - Add new assumptions if needed
- `.claude/context/glossary.md` - Add new variables if discovered
- `power-query/*.m` - Edit queries (via Claude Code)

## Files Claude Auto-Manages

**Never edit these manually**:
- `.claude/tasks/task-overview.md` - Auto-updated by sync-tasks.md
- `.claude/tasks/task-*.json` - Auto-managed by commands
- `.claude/tasks/_phase-0-status.md` - Auto-updated during Phase 0

## Git Workflow

### Initial Setup
```bash
# After copying template
cd your-project
git init
git add .
git commit -m "Initial project setup from template"
```

### After Phase 0
```bash
# Extraction command creates this automatically
git commit -m "Phase 0 complete: Ambiguities resolved, artifacts generated"
```

### During Phase 1
```bash
# After completing each task
git add .
git commit -m "Completed task 5: Implement Bronze_Source_EmissionFactors"
```

## Extension Settings

Recommended settings for Excel Power Query Editor extension:

```json
{
  "excel-power-query-editor.watchAlways": true,
  "excel-power-query-editor.autoBackupBeforeSync": true,
  "excel-power-query-editor.backup.maxFiles": 5,
  "excel-power-query-editor.logLevel": "info",
  "excel-power-query-editor.showStatusBarInfo": true,
  "excel-power-query-editor.symbols.autoInstall": true
}
```

## Troubleshooting

### Problem: Claude doesn't load context
**Solution**: Check that `CLAUDE.md` exists in project root

### Problem: Ambiguity resolution seems incomplete
**Solution**: Run `resolve-ambiguities.md` again - it presents next batch

### Problem: Extension not syncing
**Solution**: 
1. Check watch mode is enabled (status bar in VS Code)
2. Right-click `.m` file → "Toggle Watch"
3. Verify Excel file isn't open/locked

### Problem: Task breakdown not working
**Solution**: Only tasks with difficulty ≥7 should be broken down

### Problem: Git merge conflicts in task files
**Solution**: 
1. Run `@.claude/commands/update-tasks.md` to validate
2. Resolve conflicts in `.json` files
3. Run `@.claude/commands/sync-tasks.md` to rebuild overview

## Tips for Success

1. **Complete Phase 0 thoroughly** - Don't rush ambiguity resolution
2. **Review artifacts before Phase 1** - Catch issues early
3. **Break down high-difficulty tasks** - Always split difficulty ≥7
4. **Use watch mode** - Let extension handle syncing
5. **Commit frequently** - After each completed task
6. **Validate early** - Use `validate-query.md` to catch schema issues
7. **Document assumptions** - Add to `assumptions.md` as you discover new edge cases

## Next Steps

1. Copy this template to your project directory
2. Add your calculation documents and Excel files  
3. Edit `.claude/context/overview.md`
4. Open in Claude Code
5. Run `@.claude/commands/initialize-project.md`

Good luck! 🚀
