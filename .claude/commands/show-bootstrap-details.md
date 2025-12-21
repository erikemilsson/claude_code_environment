# Show Bootstrap Details - Comprehensive Bootstrap Information Display

## Purpose
Display detailed information about a bootstrap operation including template selection reasoning, configuration decisions, complete file structure, and next steps. Provides the verbose "Tier 2" information that complements the minimal completion message.

## Context Required
- Bootstrap operation must have been completed
- `.claude/` directory structure exists
- `CLAUDE.md` and related configuration files present

## Process

### Step 1: Verify Bootstrap Exists

Check for presence of bootstrap artifacts:
1. Verify `CLAUDE.md` exists
2. Verify `.claude/` directory exists
3. Verify `.claude/context/overview.md` exists

If not found, inform user that no bootstrap has been performed yet.

### Step 2: Collect Bootstrap Information

Gather information from multiple sources:

**A. Template Information**
- Read `CLAUDE.md` to identify template type
- Read `.claude/context/overview.md` for configuration details
- Look for template selection reasoning (keywords, confidence scores)

**B. Configuration Details**
- Difficulty scoring system (Simple 1-10 vs Multi-dimension)
- Phase 0 status (if Power Query template)
- Complexity level estimate
- Technology stack
- Team size indicators
- Special requirements

**C. File Structure**
- Scan `.claude/commands/` directory and count files
- Scan `.claude/context/` directory and count files
- Scan `.claude/reference/` directory and count files
- Scan `.claude/tasks/` directory and count files
- List any template-specific additions

**D. Task Information**
- Count initial tasks created
- List task IDs and titles
- Show task priorities if set

### Step 3: Display Comprehensive Report

Format and display information in structured sections:

```
═══════════════════════════════════════════════════════════════
  BOOTSTRAP DETAILS - COMPREHENSIVE REPORT
═══════════════════════════════════════════════════════════════

TEMPLATE SELECTION
------------------------------------------------------------------
Template:        [Template Name]
Confidence:      [Percentage] [Visual bar: ████████░░ 80%]
Detection:       [Auto-detected / Manual selection]

Selection Reasoning:
  • [Key indicator 1 found in specification]
  • [Key indicator 2 found in specification]
  • [Key indicator 3 found in specification]

Template Comparison:
  ✓ [Selected Template]    [XX%] - [Why it won]
  ○ [Alternative 1]        [XX%] - [Why it didn't win]
  ○ [Alternative 2]        [XX%] - [Why it didn't win]

Specification Quality:
  • Clarity:        [High/Medium/Low]
  • Completeness:   [High/Medium/Low]
  • Structure:      [High/Medium/Low]


CONFIGURATION SUMMARY
------------------------------------------------------------------
Difficulty System:    [Simple 1-10 / Multi-dimension]
  Reasoning: [Why this system was chosen]

Phase 0 Workflow:     [Enabled / Disabled]
  Reasoning: [Why Phase 0 is/isn't needed]

Project Complexity:   [Weekend / Multi-week / Long-term]
  Indicators: [What suggests this complexity level]

Technology Stack:
  • [Technology 1]
  • [Technology 2]
  • [Technology 3]

Team Size:            [Solo / Small team / Large team]
  Indicators: [What suggests this team size]

Special Requirements:
  • [Requirement 1 if any]
  • [Requirement 2 if any]


FILE STRUCTURE CREATED
------------------------------------------------------------------
Total Files: [XX]

Project Root:
  ├── CLAUDE.md                    Router file (points to context)
  ├── README.md                    Human-readable documentation
  └── .claude/
      ├── commands/                [XX files]
      │   ├── complete-task.md
      │   ├── breakdown.md
      │   ├── sync-tasks.md
      │   ├── update-tasks.md
      │   └── [template-specific commands...]
      │
      ├── context/                 [XX files]
      │   ├── overview.md
      │   ├── standards/
      │   │   └── [technology-specific files...]
      │   └── validation-rules.md
      │
      ├── tasks/                   [XX files]
      │   ├── task-overview.md
      │   └── task-*.json
      │
      └── reference/               [XX files]
          ├── difficulty-guide.md
          ├── breakdown-workflow.md
          └── [template-specific references...]

Template-Specific Additions:
  • [Addition 1 description]
  • [Addition 2 description]


INITIAL TASKS CREATED
------------------------------------------------------------------
[If tasks were created from specification:]

  Task [ID]: [Title]
    Priority:    [Priority level]
    Difficulty:  [Score]
    Estimated:   [Hours] hours

  Task [ID]: [Title]
    Priority:    [Priority level]
    Difficulty:  [Score]
    Estimated:   [Hours] hours

Total Tasks: [XX]
Total Estimated Hours: [XXX]

[If no tasks created:]
No initial tasks extracted from specification.
Use /breakdown or manually create tasks in .claude/tasks/


NEXT STEPS - DETAILED WORKFLOW
------------------------------------------------------------------
[For Phase 0 Power Query projects:]

Phase 0: Requirements Validation & Setup (Recommended First)
  Step 1: Inventory Existing Queries    [2-4 hours]
    - Run /extract-queries command
    - Document all Power Query usage
    - Map data lineage

  Step 2: Resolve Ambiguities           [1-3 hours]
    - Run /resolve-ambiguities command
    - Clarify unclear requirements
    - Validate assumptions

  Step 3: Generate Project Artifacts    [1-2 hours]
    - Run /generate-artifacts command
    - Create data dictionary
    - Document query inventory

  Step 4: Initialize Tracking           [30 min]
    - Run /initialize-project command
    - Create baseline tasks
    - Set up monitoring

  Completion Criteria:
    ✓ All queries inventoried and documented
    ✓ All ambiguities resolved and validated
    ✓ Project artifacts generated and reviewed
    ✓ Task tracking initialized

  Then proceed to standard workflow below.

[For all projects:]

Standard Workflow:
  1. Review Environment                 [15 min]
     - Read CLAUDE.md (router file)
     - Review .claude/context/overview.md
     - Understand template configuration

  2. Review/Create Tasks                [30-60 min]
     - Check .claude/tasks/task-overview.md
     - Review initial tasks (if any)
     - Create additional tasks as needed
     - Break down high-difficulty tasks (≥7)

  3. Begin Development                  [Varies]
     - Use /complete-task [id] to start work
     - Follow task management workflow
     - Update status regularly

  4. Maintain Sync                      [Ongoing]
     - Run /sync-tasks after completing tasks
     - Run /update-tasks to validate system health


QUICK REFERENCE
------------------------------------------------------------------
Key Commands:
  /complete-task [id]     Start and finish tasks
  /breakdown [id]         Split high-difficulty tasks
  /sync-tasks             Update task overview
  /show-dashboard         View project health metrics

Important Files:
  CLAUDE.md                           Entry point for Claude
  .claude/context/overview.md         Project understanding
  .claude/tasks/task-overview.md      Current work status
  .claude/reference/difficulty-guide.md   Scoring reference

Template Documentation:
  See: templates/[template-name]/README.md in claude_code_environment repo

Validation:
  /update-tasks           Check task system health
  /validate-assumptions   Verify pending assumptions


═══════════════════════════════════════════════════════════════
  For minimal view, see the bootstrap completion message
  For help with commands, use /show-commands
═══════════════════════════════════════════════════════════════
```

### Step 4: Handle Missing Information Gracefully

If certain information is not available:
- Show "Not specified" or "Not detected"
- Provide default/assumed values where appropriate
- Don't show empty sections
- Explain what information would be available if specification was more detailed

### Step 5: Provide Actionable Next Steps

Based on project state:
- If Phase 0 applicable: Show complete Phase 0 workflow first
- If tasks exist: Point to /show-dashboard for overview
- If no tasks: Suggest /breakdown or manual task creation
- Always show immediate next action clearly

## Output Format Examples

### Example 1: Power Query Project with Phase 0

```
═══════════════════════════════════════════════════════════════
  BOOTSTRAP DETAILS - COMPREHENSIVE REPORT
═══════════════════════════════════════════════════════════════

TEMPLATE SELECTION
------------------------------------------------------------------
Template:        Power Query
Confidence:      92% ████████████████████░░ (Very High)
Detection:       Auto-detected from specification keywords

Selection Reasoning:
  • "Power Query" found 8 times in specification
  • "M language" mentioned in technical requirements
  • "Power BI" mentioned as delivery platform
  • "DAX measures" found in data modeling section

Template Comparison:
  ✓ Power Query         92% - Strong indicators, specialized tooling needed
  ○ Data Engineering    45% - Some overlap but missing ETL keywords
  ○ Base                20% - Generic match only

Specification Quality:
  • Clarity:        High - Clear requirements and success criteria
  • Completeness:   Medium - Missing some data source details
  • Structure:      High - Well-organized sections


CONFIGURATION SUMMARY
------------------------------------------------------------------
Difficulty System:    Multi-dimension (5D scoring)
  Reasoning: Power Query complexity requires specialized assessment
    - Data source complexity
    - Transformation logic depth
    - Performance considerations
    - Error handling needs
    - Testing requirements

Phase 0 Workflow:     Enabled
  Reasoning: Power Query projects benefit from upfront inventory
    - Existing queries need documentation
    - Ambiguities common in data requirements
    - Baseline artifacts prevent rework

Project Complexity:   Multi-week project
  Indicators: Multiple data sources, complex transformations,
              production deployment requirements

Technology Stack:
  • Power Query (M language)
  • DAX (Power BI measures)
  • SQL Server (data source)
  • Power BI (delivery platform)

Team Size:            Solo developer
  Indicators: No team collaboration mentioned

Special Requirements:
  • Performance optimization needed (large datasets)
  • Incremental refresh required
  • Error logging and monitoring


FILE STRUCTURE CREATED
------------------------------------------------------------------
Total Files: 23

Project Root:
  ├── CLAUDE.md
  ├── README.md
  └── .claude/
      ├── commands/                12 files
      │   ├── complete-task.md
      │   ├── breakdown.md
      │   ├── sync-tasks.md
      │   ├── update-tasks.md
      │   ├── extract-queries.md           [Power Query]
      │   ├── resolve-ambiguities.md       [Power Query]
      │   ├── generate-artifacts.md        [Power Query]
      │   └── initialize-project.md        [Power Query]
      │
      ├── context/                 6 files
      │   ├── overview.md
      │   ├── standards/
      │   │   ├── power-query-standards.md [Power Query]
      │   │   └── dax-standards.md         [Power Query]
      │   └── validation-rules.md
      │
      ├── tasks/                   1 file
      │   └── task-overview.md
      │
      └── reference/               4 files
          ├── difficulty-guide.md
          ├── breakdown-workflow.md
          ├── phase-0-workflow.md          [Power Query]
          └── llm-pitfalls.md              [Power Query]

Template-Specific Additions:
  • Phase 0 command workflow (4 commands)
  • Power Query and DAX coding standards
  • 5-dimension difficulty scoring guide
  • LLM pitfalls checklist for M language


INITIAL TASKS CREATED
------------------------------------------------------------------
No initial tasks extracted from specification.

Recommended: Complete Phase 0 first, then use /initialize-project
to create baseline tasks from validated requirements.


NEXT STEPS - DETAILED WORKFLOW
------------------------------------------------------------------
Phase 0: Requirements Validation & Setup (Recommended First)

  Step 1: Inventory Existing Queries    [2-4 hours]
    Command: /extract-queries
    - Document all Power Query usage
    - Map data lineage
    - Identify dependencies

  Step 2: Resolve Ambiguities           [1-3 hours]
    Command: /resolve-ambiguities
    - Clarify unclear requirements
    - Validate assumptions
    - Document decisions

  Step 3: Generate Project Artifacts    [1-2 hours]
    Command: /generate-artifacts
    - Create data dictionary
    - Document query inventory
    - Generate baseline documentation

  Step 4: Initialize Tracking           [30 min]
    Command: /initialize-project
    - Create baseline tasks
    - Set up monitoring
    - Establish checkpoints

  Completion Criteria:
    ✓ All queries inventoried and documented
    ✓ All ambiguities resolved and validated
    ✓ Project artifacts generated and reviewed
    ✓ Task tracking initialized

Then proceed to standard development workflow.


QUICK REFERENCE
------------------------------------------------------------------
Phase 0 Commands:
  /extract-queries        Inventory existing Power Query code
  /resolve-ambiguities    Clarify requirements
  /generate-artifacts     Create project documentation
  /initialize-project     Set up task tracking

Standard Commands:
  /complete-task [id]     Start and finish tasks
  /breakdown [id]         Split high-difficulty tasks
  /sync-tasks             Update task overview
  /show-dashboard         View project metrics

Important Files:
  .claude/reference/phase-0-workflow.md      Phase 0 guide
  .claude/reference/llm-pitfalls.md          M language gotchas
  .claude/context/standards/power-query-standards.md   Coding style

Template Documentation:
  See: templates/power-query/README.md in claude_code_environment repo


═══════════════════════════════════════════════════════════════
  IMMEDIATE NEXT ACTION: Run /extract-queries to begin Phase 0
  Estimated time: 2-4 hours
═══════════════════════════════════════════════════════════════
```

### Example 2: Simple Base Template Project

```
═══════════════════════════════════════════════════════════════
  BOOTSTRAP DETAILS - COMPREHENSIVE REPORT
═══════════════════════════════════════════════════════════════

TEMPLATE SELECTION
------------------------------------------------------------------
Template:        Base
Confidence:      60% ████████████░░░░░░░░ (Medium)
Detection:       Auto-detected (no specific template indicators)

Selection Reasoning:
  • No specialized keywords found (Power Query, DAX, etc.)
  • General software development project
  • Standard task management needs

Template Comparison:
  ✓ Base                60% - Default choice, no specialized needs
  ○ Power Query         10% - No Power Query indicators
  ○ Research            15% - No research keywords
  ○ Documentation       20% - Some docs but not primary focus

Specification Quality:
  • Clarity:        Medium - Some requirements need clarification
  • Completeness:   Low - High-level overview only
  • Structure:      Medium - Basic sections present


CONFIGURATION SUMMARY
------------------------------------------------------------------
Difficulty System:    Simple 1-10 scale
  Reasoning: Standard software project, no specialized complexity

Phase 0 Workflow:     Disabled
  Reasoning: Not applicable to base template

Project Complexity:   Weekend project
  Indicators: Small scope, simple requirements, quick turnaround

Technology Stack:
  • Python
  • Flask
  • SQLite

Team Size:            Solo developer
  Indicators: Single developer mentioned

Special Requirements:
  None specified


FILE STRUCTURE CREATED
------------------------------------------------------------------
Total Files: 11

Project Root:
  ├── CLAUDE.md
  ├── README.md
  └── .claude/
      ├── commands/                4 files
      │   ├── complete-task.md
      │   ├── breakdown.md
      │   ├── sync-tasks.md
      │   └── update-tasks.md
      │
      ├── context/                 3 files
      │   ├── overview.md
      │   ├── standards/
      │   │   └── python-standards.md
      │   └── validation-rules.md
      │
      ├── tasks/                   1 file
      │   └── task-overview.md
      │
      └── reference/               3 files
          ├── difficulty-guide.md
          └── breakdown-workflow.md

Template-Specific Additions:
  • Python coding standards


INITIAL TASKS CREATED
------------------------------------------------------------------
  Task 1: Set up Flask application structure
    Priority:    high
    Difficulty:  3
    Estimated:   2 hours

  Task 2: Create SQLite database schema
    Priority:    high
    Difficulty:  4
    Estimated:   3 hours

  Task 3: Implement user authentication
    Priority:    medium
    Difficulty:  6
    Estimated:   5 hours

  Task 4: Build REST API endpoints
    Priority:    medium
    Difficulty:  5
    Estimated:   4 hours

Total Tasks: 4
Total Estimated Hours: 14


NEXT STEPS - DETAILED WORKFLOW
------------------------------------------------------------------
Standard Workflow:

  1. Review Environment                 [15 min]
     - Read CLAUDE.md
     - Review .claude/context/overview.md
     - Understand project structure

  2. Review Initial Tasks               [30 min]
     - Check .claude/tasks/task-overview.md
     - Verify task priorities and estimates
     - Break down Task 3 (difficulty 6) if needed

  3. Begin Development                  [Varies]
     - Start with Task 1 (Flask setup)
     - Use /complete-task 1 to begin
     - Follow task sequence

  4. Maintain Sync                      [Ongoing]
     - Run /sync-tasks after each completion
     - Use /show-dashboard to track progress


QUICK REFERENCE
------------------------------------------------------------------
Key Commands:
  /complete-task [id]     Start and finish tasks
  /breakdown [id]         Split high-difficulty tasks
  /sync-tasks             Update task overview
  /show-dashboard         View project health metrics

Important Files:
  CLAUDE.md                           Entry point
  .claude/context/overview.md         Project context
  .claude/tasks/task-overview.md      Work tracking
  .claude/context/standards/python-standards.md   Code style

Template Documentation:
  See: templates/base/README.md in claude_code_environment repo


═══════════════════════════════════════════════════════════════
  IMMEDIATE NEXT ACTION: Run /complete-task 1 to start Flask setup
  Estimated time: 2 hours
═══════════════════════════════════════════════════════════════
```

## Implementation Details

### Reading Template Information

```javascript
// Pseudocode for extracting template type
1. Read CLAUDE.md
2. Look for patterns like:
   - "Power Query template"
   - "Research template"
   - "Base template"
   - Or parse from router instructions
3. Extract template name
```

### Calculating Confidence Bars

```javascript
// Visual confidence representation
function confidenceBar(percentage) {
  const filled = Math.round(percentage / 5);  // 20 chars max
  const empty = 20 - filled;
  return '█'.repeat(filled) + '░'.repeat(empty);
}

// Examples:
// 92% = ████████████████████░░
// 60% = ████████████░░░░░░░░
// 35% = ███████░░░░░░░░░░░░░
```

### Scanning Directory Structure

```bash
# Count files in each directory
find .claude/commands -type f -name "*.md" | wc -l
find .claude/context -type f -name "*.md" | wc -l
find .claude/reference -type f -name "*.md" | wc -l
find .claude/tasks -type f -name "*.json" | wc -l
```

### Extracting Task Information

```javascript
// Pseudocode for task summary
1. Scan .claude/tasks/ for task-*.json files
2. For each task file:
   - Parse JSON
   - Extract: id, title, priority, difficulty, estimated_hours
3. Calculate totals:
   - Total tasks
   - Total estimated hours
4. Format for display
```

## Output Location
- Terminal display (no files modified)
- Read-only operation

## Notes
- This command provides "Tier 2" detailed information
- Complements the minimal bootstrap completion message (Tier 1)
- Supports the tiered information display approach from task 90
- Educational content helps users understand template selection
- Visual formatting improves readability
- Gracefully handles missing or incomplete information
- Always provides clear immediate next action
