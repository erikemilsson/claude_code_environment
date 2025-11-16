# Smart Bootstrap - Auto-Detect Template from Specification

## Purpose
Automatically analyze a project specification document and create the appropriate Claude Code environment with minimal user interaction. This command intelligently selects the right template based on the specification content.

## Usage

```
User: "Create the environment from claude_code_environment repo using this spec: [path/to/specification.md]"
```

## Context Required
- `.claude/reference/template-selection-rules.md` - Auto-detection patterns
- `templates/[name]/README.md` - Template specifications
- Project specification document (from Claude Desktop export)

## Process

### Step 1: Read and Analyze Specification

**Read the specification document** provided by user.

**Extract key indicators**:
- Technologies mentioned (Excel, Power Query, Python, SQL, React, etc.)
- Project type keywords (ETL, dashboard, research, analysis, calculation, etc.)
- Domain characteristics (regulatory, compliance, academic, experimental, etc.)
- Complexity indicators (timeline mentions, team size, deliverables count)
- Data characteristics (sensitive, regulatory, financial, medical, etc.)

### Step 2: Auto-Detect Template Type

**Apply pattern matching** using `.claude/reference/template-selection-rules.md`.

**Score each template** based on keyword matches and pattern indicators.

**Select highest-scoring template** as recommendation.

**Detection Logic** (see template-selection-rules.md for full patterns):

```
HIGH CONFIDENCE SIGNALS (auto-select without asking):

Power Query Template:
  - "Power Query" OR "M language" OR "Excel" mentioned
  - AND ("regulatory" OR "compliance" OR "calculation" OR "formula")

Research/Analysis Template:
  - "research question" OR "hypothesis" OR "literature review"
  - OR "experiment" OR "statistical analysis" OR "academic"
  - OR "data science" OR "exploratory analysis"

Life Projects Template:
  - "personal project" OR "organize" OR "plan"
  - OR "fitness" OR "learning" OR "budget" OR "goals"
  - OR mentions personal activities, not professional work

Documentation/Content Template:
  - "documentation" OR "technical writing" OR "content creation"
  - OR "blog" OR "tutorial" OR "guide" OR "knowledge base"

LOW CONFIDENCE (ask user to confirm):
  - Multiple template signals detected
  - Generic descriptions without clear indicators
  - Conflicting signals (e.g., both research and engineering keywords)
```

### Step 3: Detect Configuration Needs

**Analyze specification for**:

**A. Complexity Level**
- Count of deliverables/features mentioned
- Timeline indicators (weekend project vs. multi-month)
- Team size mentions (solo, small team, large team)

**B. Domain Characteristics**
- Regulatory/compliance requirements
- Ambiguous source documents (legal, regulations)
- Specialized domain knowledge needed
- Zero-error tolerance requirements

**C. Technology Stack**
- Specific languages/frameworks mentioned
- Data tools and platforms
- Infrastructure requirements

**D. Special Requirements**
- Custom difficulty dimensions needed (if domain is specialized)
- Phase 0 needed (if regulatory + ambiguous docs)
- Custom commands needed (if repeated workflows mentioned)

### Step 4: Ask Targeted Questions (Only if Needed)

**Only ask questions for**:
1. **Template ambiguity** (if multiple templates scored similarly)
2. **Missing critical info** (if can't determine essential config from spec)
3. **User preferences** (multi-dimension difficulty scoring preference)

**Example Targeted Questions**:

```
[If template unclear:]
"I detected both research and data engineering patterns in your spec.
Which better describes your focus?
  1. Research/academic focus (literature review, hypothesis testing, experiments)
  2. Data engineering focus (ETL pipelines, data transformation, infrastructure)"

[If Phase 0 unclear:]
"Your project involves [regulatory/compliance] requirements.
Do you have ambiguous source documents that need interpretation? (Y/N)
  - Y: Include Phase 0 ambiguity resolution workflow
  - N: Skip Phase 0, use standard workflow"

[If custom difficulty scoring might help:]
"Your domain involves [specialized area]. Would you like:
  1. Simple 1-10 difficulty scoring (recommended for most projects)
  2. Multi-dimension scoring (5 custom dimensions for specialized domains)"
```

**Don't ask about**:
- Project description (extract from spec)
- Technologies (extract from spec)
- Goals (extract from spec)
- Timeline estimates (infer from spec)

### Step 5: Generate Environment

**Based on detected template and configuration**, generate files:

#### A. Determine File Set

**Base files (all templates)**:
- `CLAUDE.md` - Router file
- `README.md` - Human documentation
- `.claude/context/overview.md` - Extracted from specification
- `.claude/context/validation-rules.md` - Standard rules
- `.claude/tasks/task-overview.md` - Empty initially
- `.claude/reference/difficulty-guide.md` - Appropriate for template

**Template-specific additions**:

**Power Query**:
- Phase 0 commands if regulatory + ambiguous docs detected
- Power Query-specific context files (critical_rules.md, llm-pitfalls.md)
- Query validation commands
- Phase 0 status tracker if needed

**Research/Analysis**:
- Research workflow commands (conduct-analysis.md, review-literature.md)
- Research standards (literature-review.md, hypothesis-tracking.md)
- Statistical methods reference
- Research directory structure

**Life Projects**:
- Minimal structure
- Goal tracking commands
- Simple context files

**Documentation/Content**:
- Content creation workflows
- Style guides
- Publishing commands

**Standard Commands** (unless minimal template):
- `complete-task.md`
- `breakdown.md`
- `sync-tasks.md`
- `update-tasks.md`

#### B. Populate Content from Specification

**CLAUDE.md**:
```markdown
# Project: [Extract project name from spec]

## What I'm Building
[Extract 2-3 sentence summary from spec]

## Template Type
[Auto-detected template]

## Auto-Detected Configuration
- **Template**: [Name] (detected from: [key indicators])
- **Complexity**: [Weekend project | Multi-week | Long-term] (based on [reasoning])
- **Domain**: [If specialized domain detected]
- **Phase 0**: [Yes/No] (based on [regulatory + ambiguous docs analysis])

## Current Tasks
See `.claude/tasks/task-overview.md`

## Key Commands
[List commands appropriate for detected template]

## Critical Context Files
- `.claude/context/overview.md` - Project overview (generated from specification)
[Add template-specific context files]

## Technology Stack
[Extract from specification]

## Next Action
[Context-appropriate next step based on template]
```

**context/overview.md**:
```markdown
# Project Overview

[Extract and structure content from specification document]

## Project Name
[From spec]

## Description
[From spec, expanded]

## Goals
[Extract from spec]

## Technology Stack
[Extract from spec]

## Success Criteria
[Extract from spec or infer from goals]

## Timeline
[Extract from spec if mentioned]

## Team
[Extract from spec if mentioned, else "Solo"]

## Template Configuration

**Selected Template**: [Name]
**Detection Confidence**: [High/Medium - based on signal strength]
**Key Indicators**: [List top 3-5 patterns that triggered this template]

**Configuration**:
- Difficulty Scoring: [Simple 1-10 | Multi-dimension]
- Phase 0: [Yes/No]
- Custom Components: [List if any]

## Source Specification
Original specification analyzed: [filename]
Analysis date: [current date]
```

**README.md**:
```markdown
# [Project Name]

[Extract project description from spec]

## Overview

[Extract goals and purpose from spec]

## Technology Stack

[Extract from spec]

## Quick Start

[Generate appropriate quick start based on detected template type]

## Development Workflow

[Insert template-appropriate workflow description]

## Project Structure

[Show structure appropriate for detected template]

## Documentation

For working with Claude Code on this project:
- **Start here**: `CLAUDE.md` - AI assistant router
- **Context**: `.claude/context/` - Project understanding
- **Commands**: `.claude/commands/` - Reusable workflows
- **Tasks**: `.claude/tasks/` - Work tracking

[Add template-specific sections]
```

#### C. Generate Template-Specific Files

Copy appropriate files from detected template's customizations directory.

Populate with project-specific content extracted from specification.

### Step 6: Create Initial Tasks (Optional)

**If specification contains clear deliverables/features**, offer to create initial tasks:

```
"I detected [N] potential tasks from your specification:
[List extracted tasks with estimated difficulty]

Would you like me to create these as initial task JSON files? (Y/N)"
```

**If YES**:
- Create `task-001.json` through `task-N.json`
- Populate from extracted deliverables
- Estimate difficulty based on descriptions
- Set all to "Pending" status
- Run sync-tasks to update overview

**If NO**:
- User will create tasks manually later

### Step 7: Present Summary

**Output**:

```
✓ Smart Bootstrap Complete!

PROJECT: [Name]
TEMPLATE: [Name] (auto-detected with [high/medium] confidence)

Detection Reasoning:
  ✓ [Indicator 1]: [evidence from spec]
  ✓ [Indicator 2]: [evidence from spec]
  ✓ [Indicator 3]: [evidence from spec]

Configuration Applied:
  - Difficulty Scoring: [Simple 1-10 | Multi-dimension]
  - Phase 0: [Yes/No] [if yes: (detected regulatory + ambiguous docs)]
  - Technology Stack: [extracted list]
  - Estimated Complexity: [Weekend | Multi-week | Long-term]

Files Created:
  ✓ CLAUDE.md - Router file
  ✓ README.md - Human documentation
  ✓ .claude/commands/ ([N] command files)
  ✓ .claude/context/ ([N] context files)
  ✓ .claude/tasks/ (task management)
  ✓ .claude/reference/ ([N] reference docs)
  [✓ Initial tasks created: [N] tasks] (if created)

Next Steps:
[Template-appropriate next steps, e.g.:]

[If Power Query + Phase 0:]
1. Review `.claude/tasks/_phase-0-status.md`
2. Run `@.claude/commands/initialize-project.md` to begin Phase 0
3. Follow Phase 0 workflow through all steps

[If Research/Analysis:]
1. Review `.claude/context/overview.md` - your project overview
2. Create initial research tasks or use generated tasks
3. Use `@.claude/commands/review-literature.md` to start literature review

[If standard template:]
1. Review `.claude/context/overview.md` - extracted from your spec
2. [Create initial tasks | Review generated tasks]
3. Run `@.claude/commands/sync-tasks.md` to update overview
4. Use `@.claude/commands/complete-task.md` to start first task

Quick Reference:
- Template info: `templates/[name]/README.md` in claude_code_environment repo
- Task management: `.claude/tasks/task-overview.md`
- All commands: `.claude/commands/`

Happy building! 🚀
```

## Output Location

All files created in user's current working directory:
- `./CLAUDE.md`
- `./README.md`
- `./.claude/commands/*.md`
- `./.claude/context/*.md`
- `./.claude/tasks/task-overview.md`
- `./.claude/tasks/task-*.json` (if initial tasks created)
- `./.claude/reference/*.md`

## Error Handling

**If specification not found**:
```
Error: Could not find specification document at [path]
Please provide the path to your project specification (.md file from Claude Desktop)
```

**If specification is too vague**:
```
Warning: Specification lacks clear indicators for template auto-detection.

I found generic descriptions but no strong signals for:
- Project type (web, data, research, etc.)
- Domain (regulatory, academic, business, personal, etc.)
- Technology stack

Please choose a template:
1. Base (general-purpose)
2. Power Query (Excel + regulatory calculations)
3. Research/Analysis (academic, data science, experiments)
4. Life Projects (personal goals and planning)
5. Documentation/Content (technical writing, content creation)

Or provide more details about: [specific missing info]
```

**If conflicting signals**:
```
Notice: I detected signals for multiple templates:
- [Template 1]: [evidence]
- [Template 2]: [evidence]

Which better fits your project?
[Present clear choice with reasoning]
```

## Validation Checklist

Before completing, verify:

- [ ] Specification was successfully read and parsed
- [ ] Template was detected with reasonable confidence
- [ ] All referenced files in CLAUDE.md exist
- [ ] context/overview.md contains extracted content from spec (not empty templates)
- [ ] README.md has project-specific content from spec
- [ ] Technology stack extracted and documented
- [ ] Appropriate commands for template type are present
- [ ] Cross-references between files are valid
- [ ] If Phase 0 enabled, status tracker exists
- [ ] If initial tasks created, they're valid JSON and synced

## Critical Rules

1. **Trust the specification** - Extract actual content, don't make up project details
2. **High confidence = don't ask** - If clear signals present, auto-select template
3. **Ask only when necessary** - Don't ask questions answered by the spec
4. **Populate, don't template** - Fill files with real content from spec, not placeholders
5. **Explain detection** - Tell user why template was selected (transparency)
6. **Allow override** - User can always switch templates if detection is wrong
7. **Extract, don't invent** - Use user's words from spec, don't paraphrase unnecessarily
8. **Be conservative** - When in doubt, choose simpler template (can upgrade later)

## Examples

### Example 1: High Confidence Power Query Detection

**User Input**:
```
"Create the environment from claude_code_environment repo using this spec: pension-calc-spec.md"
```

**Spec contains**:
- "Power Query M language"
- "Regulatory PDF from government"
- "Pension calculation formulas"
- "Excel workbook implementation"

**Result**: Auto-selects Power Query template with Phase 0, no questions asked.

---

### Example 2: High Confidence Research Detection

**User Input**:
```
"Create environment from claude_code_environment repo: ml-hypothesis-spec.md"
```

**Spec contains**:
- "Research question: Do transformer models..."
- "Hypothesis testing framework"
- "Literature review of 50+ papers"
- "Statistical analysis of results"

**Result**: Auto-selects Research/Analysis template, no questions asked.

---

### Example 3: Ambiguous - Ask for Clarification

**User Input**:
```
"Create environment: data-project-spec.md"
```

**Spec contains**:
- "Work with customer data"
- "Python and SQL"
- "Build some pipelines"
- No clear research or regulatory indicators

**Result**: Asks user:
```
"I see this is a data project with Python/SQL. Which focus?
1. Data Engineering (ETL pipelines, data infrastructure)
2. Research/Analysis (exploratory analysis, statistical modeling)
3. General (standard template)"
```

---

### Example 4: Life Project - High Confidence

**User Input**:
```
"Create environment: fitness-goals-spec.md"
```

**Spec contains**:
- "Track my workouts and nutrition"
- "Personal fitness goals for 2024"
- "Organize meal plans"

**Result**: Auto-selects Life Projects template, creates minimal structure.

## Template Selection Rules Reference

See `.claude/reference/template-selection-rules.md` for complete pattern matching rules and scoring logic.
