# Template File Manifest

Complete list of all files in the `pq-project-starter` template and their purposes.

## Root Level Files

### CLAUDE.md
**Purpose**: Main router file for Claude Code
**When to edit**: Never (auto-updated by Phase 0)
**Content**: 
- Phase status
- Current commands to run
- Quick reference to context files
- Next actions

### README.md
**Purpose**: Human-readable project documentation
**When to edit**: Customize for your specific project
**Content**:
- Project overview
- Setup instructions
- Dependencies
- How to run/deploy

### QUICKSTART.md
**Purpose**: Quick reference for common commands
**When to edit**: Never (reference only)
**Content**:
- Common command patterns
- Quick troubleshooting
- Cheat sheet

### SETUP-GUIDE.md
**Purpose**: Comprehensive setup and usage instructions
**When to edit**: Never (reference only)
**Content**:
- Detailed walkthrough of Phase 0 and Phase 1
- Directory structure explanation
- Git workflow
- Troubleshooting

### .gitignore
**Purpose**: Excludes files from git tracking
**When to edit**: Add project-specific exclusions if needed
**Excludes**:
- Excel files (*.xlsx, *.xlsm, *.xlsb)
- Backups (backups/, *.backup.*)
- System files (.DS_Store, Thumbs.db)
- Python cache if using Python validation

## Empty Directories (With .gitkeep)

### calculation-docs/
**Purpose**: Store source calculation method documents
**What to add**: PDFs, Word docs, calculation specifications
**Example**: CFF-delegated-act.pdf, ISO-22628.pdf

### excel-files/
**Purpose**: Store Excel files with Power Query
**What to add**: Excel workbooks (.xlsx, .xlsm)
**Note**: Use obfuscated/dummy data only

### power-query/
**Purpose**: Extracted .m files from Excel
**Auto-generated**: Yes, by extract-queries.md command
**Git tracked**: Yes (source of truth)

### tests/sample-data/
**Purpose**: Test input data for validation
**What to add**: Sample CSV, JSON, or Excel files
**Usage**: For automated testing (future enhancement)

### tests/expected-outputs/
**Purpose**: Expected results for validation
**What to add**: Expected output files
**Usage**: For automated testing (future enhancement)

## .claude/commands/ Directory

All command files follow this pattern:
- Read by Claude Code when you run `@.claude/commands/[filename]`
- Contain instructions for Claude to execute
- Can be run multiple times safely

### initialize-project.md
**Phase**: 0 (Step 1)
**Run once**: Yes
**Purpose**: Analyze calculation documents and extract ambiguities
**Inputs**: Files in calculation-docs/
**Outputs**: 
- .claude/reference/ambiguity-report.md
- Updates .claude/tasks/_phase-0-status.md

### resolve-ambiguities.md
**Phase**: 0 (Step 2)
**Run once**: No (run until all ambiguities resolved)
**Purpose**: Present ambiguities in batches of 5 for user resolution
**Interactive**: Yes - requires user input
**Outputs**: 
- Updates .claude/context/assumptions.md
- Tracks progress in _phase-0-status.md

### generate-artifacts.md
**Phase**: 0 (Step 3)
**Run once**: Yes
**Purpose**: Generate all project artifacts from resolved ambiguities
**Outputs**:
- .claude/context/glossary.md
- .claude/context/assumptions.md (finalized)
- .claude/reference/data-contracts.md
- .claude/reference/query-manifest.md
- .claude/reference/dependency-graph.md
- .claude/tasks/task-*.json files
- Updates CLAUDE.md for Phase 1

### extract-queries.md
**Phase**: 0 (Step 4)
**Run once**: Yes (or when Excel structure changes)
**Purpose**: Extract Power Query from Excel files
**Outputs**:
- Individual .m files in power-query/
- Enables watch mode
- Git commit

### complete-task.md
**Phase**: 1
**Run**: Per task
**Purpose**: Execute a specific task
**Usage**: `@.claude/commands/complete-task.md 5`
**Process**:
1. Loads task-5.json
2. Loads relevant context (glossary, assumptions, etc.)
3. Implements task
4. Updates task status
5. Validates schema
6. Updates task-overview.md

### breakdown.md
**Phase**: 1
**Run**: As needed for high-difficulty tasks
**Purpose**: Split task (difficulty ≥7) into subtasks
**Usage**: `@.claude/commands/breakdown.md 8`
**Process**:
1. Analyzes task-8.json
2. Splits into 4-8 subtasks (each difficulty <7)
3. Creates new task-*.json files for subtasks
4. Links parent-child relationships
5. Updates task-overview.md

### validate-query.md
**Phase**: 1
**Run**: As needed
**Purpose**: Validate query schema without executing
**Usage**: `@.claude/commands/validate-query.md Gold_Calculate_CFF`
**Process**:
1. Loads query .m file
2. Parses expected schema from data-contracts.md
3. Compares actual vs expected
4. Reports discrepancies

### sync-tasks.md
**Phase**: 1
**Run**: After manual task changes or periodically
**Purpose**: Rebuild task-overview.md from task-*.json files
**When to use**:
- After git pull (merge from others)
- After manual task file edits
- If overview seems out of sync

### update-tasks.md
**Phase**: 1
**Run**: Periodically (weekly)
**Purpose**: Validate task structure and consistency
**Checks**:
- Parent-child relationships valid
- Dependencies exist
- No orphaned subtasks
- Status consistency
- Flags outdated tasks

## .claude/context/ Directory

Context files that Claude loads to understand the project.

### overview.md
**Created by**: User (YOU EDIT THIS)
**When**: Before Phase 0
**Purpose**: High-level project description
**Content**:
- Project name and goals
- Calculation methods being implemented
- Data sources
- Special requirements
- Constraints

### glossary.md
**Created by**: generate-artifacts.md (Phase 0)
**Auto-managed**: Yes (but can be manually extended)
**Purpose**: Variable naming dictionary
**Content**:
- Every variable with exact name, type, unit, source
- Eliminates LLM interpretation ambiguity
**Format**: Markdown table
**Example**:
```
| Concept | Variable Name | Type | Unit | Source |
| Recycled content | RecycledContentShare | Decimal | % | Delegated Act Art. 7(1) |
```

### assumptions.md
**Created by**: resolve-ambiguities.md (Phase 0)
**Auto-managed**: During Phase 0, manually extended in Phase 1
**Purpose**: Document interpretation decisions
**Content**:
- Every ambiguity resolution
- Rationale for each decision
- Reference to source documents
**Format**: Numbered list with context

### llm-pitfalls.md
**Created by**: Template (pre-populated)
**Auto-managed**: No (reference document)
**Purpose**: Checklist of common LLM mistakes
**Content**:
- Regulatory doc interpretation pitfalls
- Power Query-specific mistakes
- Validation checklist
**Usage**: Claude reads this before implementing any calculation

### data-architecture.md
**Created by**: Template (pre-populated)
**Auto-managed**: No (customizable template)
**Purpose**: Explain bronze-silver-gold architecture
**Content**:
- Layer definitions
- Transformation rules per layer
- Dependency rules
- Anti-patterns to avoid

### validation-rules.md
**Created by**: Template (from your task system)
**Auto-managed**: No (reference document)
**Purpose**: Task validation criteria
**Content**:
- What makes a good task description
- Dependency rules
- Status transition rules

### standards/power-query.md
**Created by**: Template (pre-populated)
**Auto-managed**: No (reference document)
**Purpose**: M-code conventions and patterns
**Content**:
- Code formatting standards
- Common transformation patterns
- Performance best practices
- Example code snippets

### standards/naming.md
**Created by**: Template (pre-populated)
**Auto-managed**: No (reference document)
**Purpose**: Naming conventions enforcement
**Content**:
- Query naming pattern: [Stage]_[Action]_[Entity]
- Variable naming: PascalCase
- Column naming: snake_case
- Unit suffixes
- Examples and anti-patterns

### standards/error-handling.md
**Created by**: Template (pre-populated)
**Auto-managed**: No (reference document)
**Purpose**: Error handling patterns
**Content**:
- When to use try/otherwise
- Error record structure
- Validation patterns
- Forbidden patterns
- Example implementations

## .claude/tasks/ Directory

Task tracking files.

### _phase-0-status.md
**Created by**: Template
**Auto-managed**: Yes (during Phase 0)
**Purpose**: Track Phase 0 progress
**Content**:
- Checklist for each Phase 0 step
- Ambiguity resolution progress
- Current status
**Delete**: Can be deleted after Phase 0 complete

### task-overview.md
**Created by**: generate-artifacts.md (Phase 0)
**Auto-managed**: Yes (by sync-tasks.md)
**Purpose**: Main task table for human reference
**Content**:
- Table with all tasks
- Status indicators (🔴 🔵)
- Subtask hierarchy
- Current focus
**Never edit manually**: Always use sync-tasks.md to update

### task-*.json
**Created by**: generate-artifacts.md and breakdown.md
**Auto-managed**: Yes (by commands)
**Purpose**: Individual task data
**Format**: JSON
**Schema**:
```json
{
  "id": "5",
  "title": "Implement Bronze_Source_EmissionFactors",
  "description": "...",
  "difficulty": 4,
  "status": "Pending",
  "created_date": "2024-01-15",
  "dependencies": ["3"],
  "subtasks": [],
  "parent_task": null,
  "notes": ""
}
```

## .claude/reference/ Directory

Reference information that doesn't change during execution.

### ambiguity-report.md
**Created by**: initialize-project.md (Phase 0)
**Auto-managed**: Yes
**Purpose**: List all ambiguities found in calculation documents
**Content**:
- Numbered list of ambiguities
- Multiple interpretation options per ambiguity
- Source document references
**Usage**: Input for resolve-ambiguities.md

### data-contracts.md
**Created by**: generate-artifacts.md (Phase 0)
**Auto-managed**: No (manually extended as needed)
**Purpose**: Expected schema for each query
**Content**:
- Query name
- Output columns with types
- Required vs optional columns
- Validation rules
**Format**: Markdown sections per query
**Example**:
```
## Gold_Calculate_CFF

**Output Schema**:
- recycled_content_share: decimal, non-null, range 0-1
- total_emissions: decimal, non-null, >= 0
- compliance_flag: text, non-null, values: {"PASS", "FAIL"}
```

### query-manifest.md
**Created by**: generate-artifacts.md (Phase 0)
**Auto-managed**: No (manually extended as needed)
**Purpose**: Description of what each query does
**Content**:
- Query name
- Purpose
- Input sources
- Transformations
- Output description
**Format**: Markdown sections per query

### dependency-graph.md
**Created by**: generate-artifacts.md (Phase 0)
**Auto-managed**: No (manually extended as needed)
**Purpose**: Query execution order and dependencies
**Content**:
- Visual diagram (ASCII or mermaid)
- Bronze → Silver → Gold flow
- Which queries depend on which
**Format**: Text diagram

### difficulty-guide-pq.md
**Created by**: Template (pre-populated)
**Auto-managed**: No (reference document)
**Purpose**: Power Query-specific task difficulty scoring
**Content**:
- Scoring dimensions
- Difficulty levels 1-10 with examples
- Adjustment factors
- Breakdown strategies

### breakdown-workflow.md
**Created by**: Template (from your task system)
**Auto-managed**: No (reference document)
**Purpose**: How to break down high-difficulty tasks
**Content**:
- When to break down (difficulty ≥7)
- Parent-child task relationship rules
- Automatic parent completion
- Best practices

## Summary Statistics

**Total Files Created by Template**: 27
**Files You Edit**: 2-3 (overview.md, plus project-specific additions)
**Files Auto-Generated**: 8-15 (depending on project size)
**Command Files**: 9
**Reference Files**: 5
**Context Files**: 8
**Empty Directories**: 5

## File Lifecycle

### Pre-Phase 0
- Template files exist
- You add: overview.md content, calculation-docs/, excel-files/

### During Phase 0
- Generated: ambiguity-report.md
- Generated: glossary.md
- Generated: assumptions.md
- Generated: data-contracts.md
- Generated: query-manifest.md
- Generated: dependency-graph.md
- Generated: task-*.json files
- Updated: CLAUDE.md, _phase-0-status.md, task-overview.md

### During Phase 1
- Generated: power-query/*.m files (first time)
- Modified: power-query/*.m files (ongoing)
- Updated: task-*.json files (status changes)
- Updated: task-overview.md (via sync)
- Extended: glossary.md, assumptions.md (as needed)

### End of Project
- Archive: _phase-0-status.md (no longer needed)
- Keep: All other files for future reference/similar projects
