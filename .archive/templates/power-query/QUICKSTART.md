# Power Query Project Starter - Quick Start Guide

## What You Have

A complete, ready-to-use template for building Power Query projects with Claude Code. This template implements your workflow requirements:

✅ Phase 0: Ambiguity resolution BEFORE coding
✅ Automatic glossary and assumption documentation
✅ Task breakdown for high-difficulty queries
✅ Excel Power Query Editor integration
✅ Schema validation without Excel execution
✅ Git-friendly .m files as source of truth

---

## Setup (5 minutes)

### 1. Copy Template for Your Project

```bash
cp -r pq-project-starter/ my-battery-cff-project/
cd my-battery-cff-project/
```

### 2. Add Your Files

**Place your documents:**
- Calculation method PDFs → `calculation-docs/`
- Excel files → `excel-files/`

**Edit project description:**
- Open `.claude/context/overview.md`
- Fill in project name, description, goals

### 3. Open in VS Code / Claude Code

```bash
code .
```

---

## Phase 0: Initialization Workflow

### Command Sequence

Run these commands in order:

```
1. @.claude/commands/initialize-project.md
   → Analyzes your documents
   → Generates ambiguity report
   
2. @.claude/commands/resolve-ambiguities.md
   → Presents 5 ambiguities at a time
   → You resolve each batch
   → Run multiple times until all resolved
   
3. @.claude/commands/generate-artifacts.md
   → Creates glossary with all variable definitions
   → Generates data contracts (schemas)
   → Creates query manifest
   → Generates initial tasks
   
4. @.claude/commands/extract-queries.md
   → Guides you through extracting .m files from Excel
   → Sets up watch mode for auto-sync
```

### What You Get

After Phase 0:
- **glossary.md**: Every variable defined (no more ambiguity!)
- **assumptions.md**: All interpretation decisions documented
- **data-contracts.md**: Expected schemas for each query
- **query-manifest.md**: What each query does
- **dependency-graph.md**: Query relationships
- **tasks/**: Initial task breakdown

---

## Phase 1: Task Execution

### Basic Commands

```bash
# Work on a task
@.claude/commands/complete-task.md [id]

# Break down complex task (difficulty ≥7)
@.claude/commands/breakdown.md [id]

# Validate query schema
@.claude/commands/validate-query.md [QueryName]

# Update task overview
@.claude/commands/sync-tasks.md
```

### How It Works

1. **Run complete-task.md 1**
   - Claude loads ALL relevant context (glossary, assumptions, contracts)
   - Claude implements query following specs
   - Extension auto-syncs to Excel
   - Schema validation runs
   - Task marked complete

2. **High-difficulty tasks auto-breakdown**
   - If task difficulty ≥7, you'll be prompted to break it down first
   - Creates 4-6 subtasks (difficulty ≤6 each)
   - Work on subtasks, parent auto-completes

3. **No more ambiguity questions**
   - All resolved in Phase 0
   - Claude just implements per specs

---

## Key Features

### 1. Ambiguity Resolution (Batches of 5)

Example from Phase 0:
```
Ambiguity Batch 1 of 4 (5 ambiguities)

1. Article 7(2): "production waste and/or post-consumer scrap"
   A) Exclusive OR
   B) Inclusive OR (cumulative)
   C) Weighted average
   
   Your decision: B
```

### 2. Automatic Glossary Generation

From your resolutions, Claude creates:
```markdown
| Variable Name | Type | Unit | Description | Source |
|---------------|------|------|-------------|--------|
| RecycledContentShare | Decimal | % | Share of recycled content | Art. 7(1) |
| PreConsumerScrap | Decimal | kg | Production waste | ISO 22628 §3.1.2 |
```

### 3. LLM Pitfalls Checklist

Claude checks against common mistakes BEFORE implementing:
- Unit inconsistencies
- Implicit calculation steps
- Circular references
- Null handling
- Error masking

### 4. Task Breakdown

Complex task (difficulty 8):
```
Task 5: Implement Gold_Calculate_CFF [Broken Down] 🔵
├─ Task 12: Extract inputs (diff 4) [Finished] ✅
├─ Task 13: Core formula (diff 5) [In Progress] ⏳
├─ Task 14: Error handling (diff 4) [Pending]
└─ Task 15: Validation (diff 3) [Pending]
```

### 5. Auto-Sync with Excel

When Claude saves a .m file:
1. Extension detects change
2. Backs up Excel file
3. Updates Excel workbook
4. Your Excel file stays current

---

## File Structure

```
your-project/
├── CLAUDE.md                     # Start here - Router file
├── README.md                     # Human-readable docs
├── calculation-docs/             # Your PDFs, specs
├── excel-files/                  # Your Excel workbooks
├── power-query/                  # Extracted .m files (git tracked)
│
└── .claude/                      # Claude-specific context
    ├── commands/                 # Reusable commands
    │   ├── initialize-project.md
    │   ├── resolve-ambiguities.md
    │   ├── generate-artifacts.md
    │   ├── extract-queries.md
    │   ├── complete-task.md
    │   ├── breakdown.md
    │   └── validate-query.md
    │
    ├── context/                  # Project understanding
    │   ├── overview.md           # ⚠️ EDIT THIS FIRST
    │   ├── glossary.md           # Generated Phase 0
    │   ├── assumptions.md        # Generated Phase 0
    │   ├── llm-pitfalls.md       # Pre-populated checklist
    │   ├── power-query.md        # M-code conventions
    │   ├── naming.md             # Naming rules
    │   ├── error-handling.md     # Error patterns
    │   └── critical_rules.md     # Critical development rules
    │
    ├── tasks/                    # Work tracking
    │   ├── task-overview.md
    │   └── task-*.json
    │
    └── reference/                # Generated docs
        ├── data-contracts.md
        ├── query-manifest.md
        ├── dependency-graph.md
        ├── difficulty-guide-pq.md
        └── breakdown-workflow.md
```

---

## Your Specific Requirements Met

✅ **"Front-load ambiguity resolution"**
   - Phase 0 does this BEFORE any coding

✅ **"No formulas in Excel"**
   - All logic in Power Query M code

✅ **"Watch mode auto-sync"**
   - Extension handles Excel updates

✅ **"Obfuscated data"**
   - You handle this externally, Claude works with obfuscated data

✅ **"Schema validation only"**
   - validate-query.md does static analysis

✅ **"Task difficulty grading"**
   - Built-in, with auto-breakdown at ≥7

✅ **"Variable naming dictionary"**
   - Generated glossary.md from Phase 0

✅ **"LLM pitfall awareness"**
   - Pre-populated llm-pitfalls.md checklist

---

## Extension Setup

### Install Excel Power Query Editor

1. Open VS Code Extensions (Ctrl+Shift+X)
2. Search: "Excel Power Query Editor"
3. Install (by EWC3 Labs)

### Recommended Settings

In VS Code settings (Ctrl+,):
```
excel-power-query-editor.watchAlways: true
excel-power-query-editor.autoBackupBeforeSync: true
```

---

## Example Session

```bash
# Day 1: Initialize project
cd battery-cff-project
code .

# Edit overview.md with project details
# Add calculation PDFs to calculation-docs/
# Add Excel files to excel-files/

# Run Phase 0
@.claude/commands/initialize-project.md
# → Finds 23 ambiguities

@.claude/commands/resolve-ambiguities.md
# → Present 5 ambiguities, you resolve
# → Run again for next batch (5 more)
# → Run again (5 more)
# → Run again (5 more)
# → Run again (3 remaining)
# → All resolved!

@.claude/commands/generate-artifacts.md
# → Glossary: 47 terms
# → Data contracts: 8 queries
# → Tasks: 15 created

@.claude/commands/extract-queries.md
# → Extract .m files from Excel
# → Enable watch mode
# → Git commit

# Phase 0 complete! ✅

# Day 2-N: Execute tasks
@.claude/commands/complete-task.md 1
# → Implements Bronze_Source_EmissionFactors
# → Auto-syncs to Excel
# → Task 1 complete ✅

@.claude/commands/complete-task.md 5
# → Difficulty 8! Break down first

@.claude/commands/breakdown.md 5
# → Creates tasks 12-16 (subtasks)

@.claude/commands/complete-task.md 12
# → First subtask done

# Continue until all tasks complete
```

---

## Tips

1. **Phase 0 takes time** - Budget 30min-2hr for ambiguity resolution
2. **Read llm-pitfalls.md** - Understand what Claude checks
3. **Break down early** - Don't start difficulty ≥7 tasks directly
4. **Git commit often** - After Phase 0, after each task
5. **Watch mode is key** - Keep Excel synced automatically
6. **Schema validation** - Use it, don't skip
7. **Trust the process** - Phase 0 investment pays off in Phase 1

---

## Common Questions

**Q: Can I skip Phase 0?**
A: No. That's where ambiguity resolution happens. Without it, you'll get circular LLM interpretations.

**Q: Can I edit generated files (glossary.md)?**
A: Yes! They're starting points. Edit as needed.

**Q: What if I find more ambiguities later?**
A: Add to assumptions.md manually, reference in code comments.

**Q: Do I need Excel installed?**
A: No! Extension works without Excel. But you can open Excel to verify results.

**Q: Can I use real data?**
A: Keep real data outside this project. Claude works with obfuscated data.

**Q: How do I deploy to production?**
A: Copy .m files to your real Excel environment with real data.

---

## Support

- Extension issues: https://github.com/ewc3labs/excel-power-query-editor
- Template issues: Check README.md in this folder
- Power Query reference: https://learn.microsoft.com/en-us/powerquery-m/

---

## What's Next?

1. Copy template to your project folder
2. Edit .claude/context/overview.md
3. Add your calculation docs and Excel files
4. Run @.claude/commands/initialize-project.md
5. Start Phase 0!

**Your CFF project is ready to begin! 🚀**
