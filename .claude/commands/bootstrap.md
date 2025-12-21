# Bootstrap New Project

## Purpose
Automate the creation of a new Claude Code project environment from templates. Interactively guide through template selection, component choices, and customization options to generate complete `.claude/` folder structure.

## Context Required
- `templates/[name]/README.md` - Template specifications
- `.claude/reference/template-customization-guide.md` - Customization options
- `.claude/reference/reusable-template-patterns.md` - Pattern library
- `legacy-template-reference.md` - Historical reference (optional)

## Pre-Flight Checks (CRITICAL - Run Before Gathering Information)

Before asking ANY questions or gathering information, perform these validation checks:

### 1. Validate Directory Safety

**Check current directory status**:
```bash
# Count files and list them
ls -A
```

**Directory States**:
- **Empty**: 0 files → ✓ SAFE TO PROCEED
- **Safe files only**: Only `.git/`, `.gitignore`, `README.md`, `LICENSE` → ✓ SAFE TO PROCEED
- **Has .claude/**: Directory already has environment → ❌ STOP - Show error
- **Has other files**: Project files present → ⚠️ WARN USER

### 2. Check for Conflicting Files

**Scan for existing environment**:
```bash
# Check for conflicts
[ -d ".claude" ] && echo "ERROR: .claude/ directory exists"
[ -f "CLAUDE.md" ] && echo "WARNING: CLAUDE.md file exists"
```

**Actions Based on Results**:

**If .claude/ exists**:
```
❌ ERROR: Claude Code environment already exists

📍 Where: [current_directory]/.claude/

🔍 Why this happened:
   This directory already has a Claude Code environment.

   You're either:
   • Re-bootstrapping an existing project
   • In the wrong directory
   • Previous bootstrap failed midway

💡 How to fix:

**Option 1: WRONG DIRECTORY**
   cd /path/to/your/new/project
   /bootstrap

**Option 2: REMOVE EXISTING** (⚠️  deletes environment)
   /undo-bootstrap
   # Then bootstrap fresh
   /bootstrap

**Option 3: KEEP EXISTING**
   The environment already exists! You can:
   • Start working: /complete-task [id]
   • View tasks: cat .claude/tasks/task-overview.md
   • Update context: Edit .claude/context/overview.md

**Option 4: INCOMPLETE BOOTSTRAP**
   # Check what exists
   ls -la .claude/

   # If incomplete, remove manually
   rm -rf .claude
   /bootstrap

🔗 Related:
   • Undo bootstrap: /undo-bootstrap
   • Working with environments: See CLAUDE.md
```
→ STOP - Do not proceed with bootstrap

**If CLAUDE.md exists but no .claude/**:
```
⚠️  WARNING: CLAUDE.md file exists without .claude/ directory

📍 Where: [current_directory]/CLAUDE.md

🔍 Why this happened:
   There's a CLAUDE.md file but no .claude/ directory.

   Possible reasons:
   • Partial bootstrap that failed
   • Manual file creation
   • .claude/ was deleted but CLAUDE.md remained
   • Different project using CLAUDE.md

💡 What happens if you proceed:
   Bootstrap will create .claude/ directory alongside existing CLAUDE.md.

   Your options:
   A) Continue - Bootstrap will work around existing file
   B) Remove CLAUDE.md first - Start completely fresh
   C) Back up CLAUDE.md - mv CLAUDE.md CLAUDE.md.old
   D) Cancel - Bootstrap in different directory

Proceed with bootstrap? This will create .claude/ directory. [y/N]
```
→ Get user confirmation before proceeding

**If other files present (no .claude/)**:
```
⚠️  NOTICE: Current directory is not empty

Found existing files:
  [list first 5-10 files]
  [and X more...]

Bootstrap will create:
  • CLAUDE.md (if not present)
  • .claude/ directory with environment files

Existing files will NOT be modified or deleted.

Is this the correct directory for bootstrap? [Y/n]
```
→ Get user confirmation before proceeding

**If directory is empty or only safe files**:
```
✓ Directory check passed - Safe to proceed
```
→ Continue to Step 1

### 3. Present Pre-Flight Summary

**Show quick summary before questions**:
```
═══════════════════════════════════════════════════════════
BOOTSTRAP PRE-FLIGHT CHECK
═══════════════════════════════════════════════════════════

DIRECTORY: [current directory path]
  Status: [Empty | Has safe files | Has project files]
  Conflicts: None ✓

Ready to configure new Claude Code environment.

This will ask ~5-8 questions (takes 2-3 minutes).

═══════════════════════════════════════════════════════════
```

## Process

### Step 1: Gather Project Information (After Pre-Flight Success)

Ask user the following questions:

**1. Project Description**
- "What are you building? (Brief description is fine)"
- "What's the main goal or purpose?"

**2. Project Type**
- "What type of work is this?"
  - [ ] Data Engineering (ETL, pipelines, data transformation)
  - [ ] BI/Dashboard (Analytics, reporting, visualization)
  - [ ] Power Query (Excel, regulatory calculations)
  - [ ] Web Development (Frontend, backend, full-stack)
  - [ ] DevOps/Infrastructure (CI/CD, cloud, containers)
  - [ ] Machine Learning (Models, training, deployment)
  - [ ] General Purpose (Other)

**3. Estimated Complexity**
- "How many tasks do you estimate?" (helps determine minimal vs full)
  - [ ] < 10 tasks (weekend project)
  - [ ] 10-30 tasks (multi-week project)
  - [ ] 30+ tasks (long-term project)

**4. Team Size**
- "Who will work on this?"
  - [ ] Solo
  - [ ] Small team (2-3 people)
  - [ ] Medium/Large team (4+ people)

**5. Domain Characteristics**
- "Does this project involve:" (check all that apply)
  - [ ] Regulatory/compliance requirements
  - [ ] Ambiguous source requirements (legal docs, regulations)
  - [ ] Specialized domain knowledge (medical, financial, legal)
  - [ ] Need for audit trail
  - [ ] Zero error tolerance

---

### Step 2: Determine Template Type

Based on responses, recommend template:

**Logic**:

```
IF tasks < 10 AND solo AND no regulatory requirements:
  → Recommend MINIMAL

ELSE IF project_type == "Power Query" OR (regulatory requirements AND ambiguous docs):
  → Recommend POWER QUERY (with Phase 0)

ELSE IF project_type == "Data Engineering":
  → Recommend DATA ENGINEERING

ELSE IF project_type == "BI/Dashboard":
  → Recommend BI/DASHBOARD

ELSE IF project_type in ["Data Engineering", "BI/Dashboard"] AND both needed:
  → Recommend HYBRID

ELSE:
  → Recommend BASE (full)
```

**Present Recommendation**:
- "Based on your answers, I recommend the **[TEMPLATE NAME]** template."
- "This template includes: [list key features]"
- "Does this sound right, or would you prefer a different template?"

Allow user to override recommendation.

---

### Step 3: Choose Components

Based on template choice, ask about optional components:

#### For All Templates (except Minimal)

**A. Custom Difficulty Scoring**
- "Would you like to use multi-dimension difficulty scoring instead of simple 1-10?"
  - If YES: Ask for 5 dimensions relevant to domain
  - If NO: Use standard 1-10 scoring

**B. Domain-Specific Context Files**
- "Does your domain have specialized knowledge or common pitfalls?"
  - If YES: Offer to create:
    - `llm-pitfalls.md` - Common mistake checklist
    - `critical_rules.md` - DO/DON'T rules for technology
    - `glossary.md` - Term definitions (if not using Phase 0)

**C. Custom Commands**
- "Do you have repeated workflows that would benefit from custom commands?"
  - If YES: Ask for workflow descriptions
  - If NO: Include only standard commands

#### For Regulatory/Ambiguous Requirements

**D. Phase 0 Workflow**
- "Your project has ambiguous requirements. Include Phase 0 ambiguity resolution workflow?"
  - If YES: Include Phase 0 commands and status tracker
  - If NO: Skip Phase 0 components

---

### Step 4: Customize Difficulty Scoring (if chosen)

If user chose multi-dimension scoring:

**Ask for 5 dimensions** relevant to their domain:

- "What 5 dimensions best capture task difficulty for your domain?"
- "Examples:"
  - Web: UI Complexity, State Management, API Integration, Performance, Accessibility
  - Data: Data Volume, Transformation Complexity, Dependencies, Error Recovery, Performance SLA
  - DevOps: Infrastructure Scope, Security Impact, Rollback Complexity, Monitoring, Cross-Team Deps
  - ML: Data Complexity, Model Complexity, Training Time, Interpretability, Deployment

**For each dimension**, confirm:
- Dimension name
- What 1-2 means (trivial)
- What 5-6 means (moderate)
- What 9-10 means (extreme)

---

### Step 5: Generate Folder Structure

Create the directory structure based on template choice:

#### Minimal Template Structure

```
project/
├── CLAUDE.md
└── .claude/
    └── tasks/
        ├── task-overview.md
        └── (task JSON files created separately)
```

#### Base Template Structure

```
project/
├── CLAUDE.md
├── README.md
└── .claude/
    ├── commands/
    │   ├── complete-task.md
    │   ├── breakdown.md
    │   ├── sync-tasks.md
    │   └── update-tasks.md
    ├── context/
    │   ├── overview.md
    │   ├── validation-rules.md
    │   └── standards/
    ├── tasks/
    │   ├── task-overview.md
    │   └── (task JSON files created separately)
    └── reference/
        ├── difficulty-guide.md
        └── breakdown-workflow.md
```

#### Domain-Specific Additions

**Power Query** (add to Base):
```
├── commands/
│   ├── initialize-project.md       # Phase 0 Step 1
│   ├── resolve-ambiguities.md      # Phase 0 Step 2
│   ├── generate-artifacts.md       # Phase 0 Step 3
│   ├── extract-queries.md          # Phase 0 Step 4
│   └── validate-query.md
├── context/
│   ├── glossary.md                 # Phase 0 output
│   ├── assumptions.md              # Phase 0 output
│   ├── llm-pitfalls.md
│   ├── data-architecture.md
│   ├── power-query.md
│   ├── naming.md
│   ├── error-handling.md
│   └── critical_rules.md
├── tasks/
│   └── _phase-0-status.md
└── reference/
    ├── ambiguity-report.md         # Phase 0 output
    ├── data-contracts.md           # Phase 0 output
    ├── query-manifest.md           # Phase 0 output
    ├── dependency-graph.md         # Phase 0 output
    └── difficulty-guide-pq.md
```

**Data Engineering** (add to Base):
```
├── commands/
│   ├── create-pipeline.md
│   ├── test-pipeline.md
│   └── deploy-pipeline.md
├── context/
│   ├── data-architecture.md
│   ├── naming.md
│   ├── error-handling.md
│   └── schema-evolution.md
└── reference/
    └── pipeline-patterns.md
```

**BI/Dashboard** (add to Base):
```
├── commands/
│   ├── create-dashboard.md
│   ├── validate-metrics.md
│   └── optimize-queries.md
├── context/
│   ├── visualization-standards.md
│   ├── data-refresh.md
│   ├── performance.md
│   └── security.md
└── reference/
    └── dashboard-patterns.md
```

**Custom Components** (add as selected):
- If `llm-pitfalls.md`: Add to `context/`
- If `critical_rules.md`: Add to `context/`
- If `glossary.md` (non-Phase-0): Add to `context/`
- If custom difficulty: Create `reference/difficulty-guide-[domain].md`
- If custom commands: Add to `commands/`

---

### Step 6: Generate File Contents

#### A. CLAUDE.md

```markdown
# Project: [Project Name]

## What I'm Building
[User's project description, 2-3 sentences]

## Template Type
[Minimal | Base | Power Query | Data Engineering | BI/Dashboard | Hybrid]

## Current Phase
[Phase 0: Requirements Resolution | Implementation | Maintenance]

## Current Tasks
See `.claude/tasks/task-overview.md`

## Key Commands
- `@.claude/commands/complete-task.md` - Start/finish tasks
- `@.claude/commands/breakdown.md` - Split difficult tasks
- `@.claude/commands/sync-tasks.md` - Update task overview
[Add Phase 0 commands if applicable]
[Add custom commands if created]

## Critical Context Files
- `.claude/context/overview.md` - Project overview
[Add domain-specific context files if created]

## Difficulty Scoring
[Simple 1-10 | Multi-dimension (5 factors)]
[If multi-dimension: See `.claude/reference/difficulty-guide-[domain].md`]

## Next Action
[Phase 0 Step 1: initialize-project.md | Create initial tasks | Start first task]
```

#### B. README.md

```markdown
# [Project Name]

[User's project description]

## Purpose

[Expand on project goals]

## Technology Stack

[List technologies/frameworks based on project type]

## Getting Started

[Provide setup instructions based on project type]

## Development Workflow

[Explain task management approach]

1. Review tasks in `.claude/tasks/task-overview.md`
2. Use `.claude/commands/complete-task.md` to start work
3. Break down difficult tasks (difficulty ≥7) using `.claude/commands/breakdown.md`
4. Keep task overview updated with `.claude/commands/sync-tasks.md`

[If Phase 0: Add Phase 0 workflow section]

## Project Structure

[Describe folder organization based on project type]

## Documentation

- `.claude/context/` - Project context and standards
- `.claude/commands/` - Reusable workflows
- `.claude/tasks/` - Task management
- `.claude/reference/` - Supporting documentation

## Contributing

[Team collaboration guidelines if team size > 1]
```

#### C. context/overview.md

```markdown
# Project Overview

## Project Name
[Name]

## Description
[User's description expanded]

## Goals
[Extract from user input]

## Technology Stack
[Based on project type]

## Template Configuration

**Template Type**: [Type]
**Difficulty Scoring**: [Simple | Multi-dimension]
**Phase 0**: [Yes | No]

[If Phase 0:]
## Phase 0 Status
See `.claude/tasks/_phase-0-status.md` for current progress.

## Domain Characteristics
[If regulatory/specialized domain, describe here]

## Success Criteria
[What does "done" look like?]

## Constraints
[Any known limitations or requirements]

## Team
[Team size and roles if applicable]
```

#### D. context/validation-rules.md

```markdown
# Task Validation Rules

## Task Creation Rules

1. **Every task must have**:
   - Unique ID (sequential integers)
   - Clear title (action-oriented)
   - Detailed description
   - Difficulty score (1-10)
   - Status (Pending | In Progress | Blocked | Broken Down | Finished)
   - Created date
   - Dependencies array (task IDs that must complete first)
   - Subtasks array (child task IDs)
   - Parent task ID (if this is a subtask)
   - Notes field

2. **Difficulty Scoring**:
   [If simple:]
   - Use 1-10 scale
   - Tasks ≥7 must be broken down before starting

   [If multi-dimension:]
   - Score across 5 dimensions (see difficulty-guide-[domain].md)
   - Average and round to nearest integer
   - Tasks ≥7 must be broken down before starting

3. **Status Rules**:
   - Tasks start as "Pending"
   - Only one task "In Progress" at a time (recommended)
   - "Broken Down" tasks cannot be worked on directly (work on subtasks)
   - "Broken Down" tasks auto-complete when all subtasks finish
   - "Finished" tasks are complete and verified

4. **Dependency Rules**:
   - Cannot start task until all dependencies are "Finished"
   - No circular dependencies
   - Subtasks inherit parent's dependencies

5. **Breakdown Rules**:
   - Tasks with difficulty ≥7 must be broken down
   - Broken down task gets status "Broken Down (0/N done)"
   - Create 2-5 subtasks
   - Subtasks reference parent_task ID
   - Parent task auto-completes when last subtask finishes

## Task Update Rules

1. Use `complete-task.md` to change status to "In Progress" or "Finished"
2. Add notes when completing tasks (what was done, issues encountered)
3. Run `sync-tasks.md` after status changes to update overview
4. Check parent task when completing subtasks

## Validation Checks

Run `update-tasks.md` to validate:
- All tasks have required fields
- No circular dependencies
- Subtask/parent relationships are bidirectional
- Difficulty scores are in valid range
- Status values are valid
- Broken Down tasks have subtasks
```

#### E. reference/difficulty-guide.md

[If Simple Scoring:]
```markdown
# Difficulty Scoring Guide

## 1-10 Scale

- **1-2**: Trivial (fix typo, update text, simple config change)
- **3-4**: Low (basic CRUD, simple UI component, straightforward logic)
- **5-6**: Moderate (form validation, API integration, basic algorithms)
- **7-8**: High (authentication setup, database migration, complex features)
  - **MUST BREAK DOWN** before starting
- **9-10**: Extreme (architecture changes, distributed systems, major refactors)
  - **MUST BREAK DOWN** before starting

## Breakdown Rule

Tasks with difficulty ≥7 MUST be broken down using `breakdown.md` before work begins.

## Examples

[Provide 3-5 examples relevant to project type]
```

[If Multi-Dimension Scoring:]
```markdown
# Difficulty Scoring Guide for [Domain]

## 5-Dimension Scoring System

This project uses multi-dimension difficulty scoring for more accurate task assessment.

### Dimension 1: [Name] (1-10)
- **1-2**: [Criteria]
- **3-4**: [Criteria]
- **5-6**: [Criteria]
- **7-8**: [Criteria]
- **9-10**: [Criteria]

[Repeat for all 5 dimensions with user-specified names and criteria]

## Final Score Calculation

**Final Difficulty = ROUND(AVERAGE(Dim1, Dim2, Dim3, Dim4, Dim5))**

## Breakdown Rule

Tasks with final difficulty ≥7 MUST be broken down using `breakdown.md` before work begins.

## Examples

[Provide 2-3 examples showing dimension scoring]
```

#### F. tasks/task-overview.md (initial)

```markdown
# Task Overview

**Project**: [Name]
**Last Updated**: [Date]
**Total Tasks**: 0
**Completed**: 0
**In Progress**: 0
**Pending**: 0

## Status Summary

No tasks created yet.

[If Phase 0:]
Complete Phase 0 workflow first:
1. Run `@.claude/commands/initialize-project.md`
2. Run `@.claude/commands/resolve-ambiguities.md`
3. Run `@.claude/commands/generate-artifacts.md`
4. Run `@.claude/commands/extract-queries.md` [or equivalent]

[Else:]
Create your first task and run `@.claude/commands/sync-tasks.md` to see it here.

## Next Steps

[Phase 0 workflow | Create initial tasks based on project scope]
```

#### G. Phase 0 Status (if applicable)

`tasks/_phase-0-status.md`:
```markdown
# Phase 0: Requirements Resolution

**Started**: [Not yet started]
**Last Updated**: [Date]
**Status**: Not Started

## Purpose

Resolve ambiguities in source requirements before implementation to ensure:
- Consistent interpretation of terms
- All decisions documented
- Zero ambiguity in specifications

## Steps

- [ ] Step 1: Initialize Project (`initialize-project.md`)
  - Analyze source documents
  - Extract ambiguities and inconsistencies
  - Generate ambiguity report

- [ ] Step 2: Resolve Ambiguities (`resolve-ambiguities.md`)
  - Interactive batch resolution (5 at a time)
  - User makes interpretation decisions
  - Document in assumptions.md

- [ ] Step 3: Generate Artifacts (`generate-artifacts.md`)
  - Create glossary.md (variable definitions)
  - Create data-contracts.md (schemas)
  - Create manifest and dependency graph
  - Generate initial tasks

- [ ] Step 4: Extract/Initialize (`extract-queries.md` or equivalent)
  - Set up project structure for implementation
  - Version control setup
  - Ready for implementation

## Outputs Generated

- [ ] `context/glossary.md`
- [ ] `context/assumptions.md`
- [ ] `reference/ambiguity-report.md`
- [ ] `reference/data-contracts.md`
- [ ] `reference/[domain]-manifest.md`
- [ ] `reference/dependency-graph.md`
- [ ] Initial task JSON files

## Next Action

Run `@.claude/commands/initialize-project.md` to begin Phase 0.

## Completion Criteria

- All ambiguities resolved (nothing in ambiguity-report.md unresolved)
- Every variable/term has definition in glossary.md
- All interpretation decisions documented in assumptions.md
- Expected schemas defined in data-contracts.md
- Initial task list created

**Phase 0 is complete when all steps are checked and all outputs generated.**
```

#### H. Domain-Specific Context Files

**If llm-pitfalls.md selected**:

Create `context/llm-pitfalls.md` with template:
```markdown
# LLM Pitfalls for [Domain]

This checklist catalogs common mistakes LLMs make when working with [domain] materials.

IMPORTANT: Review this checklist before implementing tasks in this domain.

## Category 1: [e.g., Security]

### Common Mistakes:
- [ ] [Specific mistake 1]
- [ ] [Specific mistake 2]

**Correct Approach**: [How to avoid]

## Category 2: [e.g., Performance]

### Common Mistakes:
- [ ] [Specific mistake 3]
- [ ] [Specific mistake 4]

**Correct Approach**: [How to avoid]

[Add 3-6 categories based on domain]

## When to Review

- [ ] Before starting any new task
- [ ] During code review
- [ ] When encountering unexpected behavior
```

**If critical_rules.md selected**:

Create `context/critical_rules.md` with template:
```markdown
# Critical Rules for [Technology]

These rules MUST be followed. Violations lead to [consequences].

## Rule 1: [Category]

**DO**: [Correct approach]
**DON'T**: [What to avoid]
**WHY**: [Consequence of violation]

**Example**:
```[language]
// CORRECT
[code example]

// INCORRECT
[code example]
```

[Add 5-10 rules based on technology]
```

#### I. Command Files

**Standard Commands** (always include unless Minimal):

Copy from this repository:
- `complete-task.md`
- `breakdown.md`
- `sync-tasks.md`
- `update-tasks.md`

**Phase 0 Commands** (if Phase 0 selected):

Create domain-appropriate versions based on `reusable-template-patterns.md` section 1.

**Custom Commands** (if user requested):

Create based on user-described workflows using command template from `template-customization-guide.md`.

---

### Step 7: Summary and Next Steps

**Present to user**:

```
✓ Bootstrap Complete!

Created [TEMPLATE TYPE] environment for: [Project Name]

Structure:
- CLAUDE.md (router file)
- README.md (human documentation)
- .claude/commands/ ([N] commands)
- .claude/context/ ([N] context files)
- .claude/tasks/ (task management)
- .claude/reference/ ([N] reference docs)

Configuration:
- Difficulty Scoring: [Simple 1-10 | Multi-dimension (5 factors)]
[If Phase 0:] - Phase 0: Enabled
[If custom files:] - Custom Components: [list]

📋 IMMEDIATE NEXT STEP (do this first):
   → Read: .claude/context/overview.md

⏰ THEN:
[If Phase 0 enabled:]
   □ Phase 0: Resolve Ambiguities (1-2 hours)
     → Run: /initialize-project
     Why: [Reason - e.g., "Detected regulatory requirements + ambiguous calculations"]
     Expected: 4-step workflow to clarify all variables and assumptions

     Phase 0 Steps:
     1. Initialize Project (15-20 min) - Extract ambiguities
     2. Resolve Ambiguities (30-60 min) - Interactive decisions
     3. Generate Artifacts (15-20 min) - Create glossary & contracts
     4. Extract Queries (10-15 min) - Set up for implementation

     After Phase 0: Begin implementation with /complete-task [first-task-id]

[If initial tasks created:]
   □ Review Generated Tasks (5 minutes)
     → Open: .claude/tasks/task-overview.md
     → [N] tasks created from bootstrap
     → Start work: /complete-task [suggested-first-task-id]

     Suggested first task: [ID] - [Title] (difficulty: [N], est. [X]h)
     [Reason - e.g., "Foundation task, blocks others", "High priority"]

[If no tasks created:]
   □ Create Your First Tasks (10 minutes)
     → Review project scope in overview.md
     → Create task JSON files in .claude/tasks/
     → Run: /sync-tasks to update overview
     → Then: /complete-task [id] to start work

[If Life Projects or simple template:]
   □ Get Started (5 minutes)
     → Review goals in overview.md
     → Create 2-3 initial tasks for quick wins
     → Or jump in: /complete-task to start first task

Quick Reference:
- Task management: .claude/tasks/task-overview.md
- Commands: .claude/commands/
- Context: .claude/context/
[If PQ:] - PQ Quick Ref: .claude/reference/power-query-quick-reference.md
[If custom difficulty:] - Difficulty Guide: .claude/reference/difficulty-guide-[domain].md

Happy building!
```

---

## Output Location

All files created in user's current project directory:
- `./CLAUDE.md`
- `./README.md`
- `./.claude/commands/*.md`
- `./.claude/context/*.md`
- `./.claude/tasks/task-overview.md`
- `./.claude/tasks/_phase-0-status.md` (if Phase 0)
- `./.claude/reference/*.md`

---

## Critical Rules

1. **Always ask before creating** - Don't assume user wants default template
2. **Customize, don't just copy** - Adapt content to user's specific domain
3. **Explain recommendations** - Tell user WHY you recommend a template
4. **Allow overrides** - User can choose different template than recommended
5. **Start simple** - When in doubt, recommend simpler template (can upgrade later)
6. **Create only selected components** - Don't add files user didn't choose
7. **Populate content** - Don't create empty files, add appropriate starter content
8. **Be consistent** - Use naming conventions and patterns from `templates/[name]/README.md`
9. **Link documentation** - Reference full docs in generated files
10. **Test structure** - Ensure all cross-references between files are valid

---

## Template Recommendation Decision Tree

```
[Tasks < 10] AND [Solo] AND [No Regulatory]
    → MINIMAL

[Power Query Project] OR [Excel + Regulatory]
    → POWER QUERY (ask about Phase 0)

[Regulatory] AND [Ambiguous Source Docs]
    → BASE + PHASE 0 + Domain Customizations

[Data Engineering] AND NOT [BI/Dashboard]
    → DATA ENGINEERING

[BI/Dashboard] AND NOT [Data Engineering]
    → BI/DASHBOARD

[Data Engineering] AND [BI/Dashboard]
    → HYBRID

[Web Dev] OR [DevOps] OR [ML] OR [General]
    → BASE (offer domain customizations)
```

---

## Examples

### Example 1: Simple Weekend Project

**User Input**:
- Description: "Build a todo list app"
- Type: Web Development
- Tasks: ~5
- Team: Solo

**Recommendation**: Minimal
**Rationale**: Simple project, few tasks, solo developer
**Files Created**: CLAUDE.md, .claude/tasks/ only

---

### Example 2: Regulatory Calculation Project

**User Input**:
- Description: "Implement pension calculation from regulatory PDF"
- Type: Power Query
- Tasks: ~20
- Team: 2 people
- Regulatory: Yes, ambiguous source docs

**Recommendation**: Power Query with Phase 0
**Rationale**: Regulatory requirements + ambiguous docs = need Phase 0
**Files Created**: Full PQ structure including Phase 0 commands and status tracker

---

### Example 3: Data Engineering Pipeline

**User Input**:
- Description: "ETL pipeline for customer data"
- Type: Data Engineering
- Tasks: ~15
- Team: 3 people
- Regulatory: No

**Recommendation**: Data Engineering Template
**Rationale**: Clear domain, medium complexity, team collaboration
**Files Created**: Base + data engineering commands and context files
**Custom**: Offer multi-dimension scoring for data domain

---

## Validation Checklist

Before completing bootstrap, verify:

- [ ] All required folders created
- [ ] CLAUDE.md contains correct template type and commands
- [ ] README.md has appropriate getting started section
- [ ] context/overview.md describes project
- [ ] validation-rules.md matches scoring system chosen
- [ ] difficulty-guide.md (or domain variant) exists and is correct
- [ ] All command files referenced in CLAUDE.md exist
- [ ] Phase 0 status tracker present if Phase 0 enabled
- [ ] Domain-specific context files have starter content (not empty)
- [ ] No broken cross-references between files
- [ ] task-overview.md has appropriate "next steps" for template type
