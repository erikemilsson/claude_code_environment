# Smart Bootstrap - Auto-Detect Template from Specification

## Purpose
Automatically analyze a project specification document and create the appropriate Claude Code environment with minimal user interaction. This command now uses the **Environment Architect Agent** for intelligent template selection and environment generation.

## Agent Integration

**This command invokes the Environment Architect Agent**:
```markdown
AGENT: Environment Architect
PHASE: Project Initialization
OWNERSHIP: Template detection, environment generation, initial task extraction
```

The Environment Architect will:
1. Analyze your specification with pattern matching
2. Auto-detect appropriate template (>85% confidence = auto-select)
3. Generate complete .claude/ structure
4. Extract initial tasks from requirements
5. Hand off to Task Orchestrator if high-difficulty tasks detected

## Usage

```
User: "Create the environment from claude_code_environment repo using this spec: [path/to/specification.md]"
```

## Context Required
- `.claude/agents/environment-architect.md` - Agent definition
- `.claude/agent-config.json` - Agent ownership matrix
- `.claude/reference/template-selection-rules.md` - Auto-detection patterns
- `templates/[name]/README.md` - Template specifications
- Project specification document (from Claude Desktop export)

## Pre-Flight Checks (CRITICAL - Run Before Any Generation)

Before starting environment generation, perform these validation checks:

### 1. Validate Directory Safety

**Check current directory status**:
```bash
# Count files in current directory (excluding hidden)
ls -A | wc -l
```

**Directory States**:
- **Empty**: 0 files → ✓ SAFE TO PROCEED
- **Safe files only**: Only `.git/`, `.gitignore`, `README.md`, `LICENSE` → ✓ SAFE TO PROCEED
- **Has .claude/**: Directory already has environment → ⚠️ WARN USER
- **Has other files**: Project files present → ⚠️ WARN USER

### 2. Validate Specification Access

**Check specification file**:
```bash
# Test if file exists and is readable
test -r [spec_path] && echo "OK" || echo "ERROR"
```

**Path Expansion** (see Path Handling section for full details):
- Expand `~` to home directory
- Expand relative paths (`.`, `..`)
- Try fallback search if not found

**File Validation**:
- File exists and is readable → ✓ PROCEED
- File not found → Try fallback search (Documents, Downloads, Desktop, iCloud)
- File found but not readable → ERROR
- File is empty (< 100 bytes) → ⚠️ WARN USER

### 3. Template Detection Confidence

**Calculate confidence before showing report**:
- Run template detection analysis
- Score all templates
- Determine highest confidence

**Confidence Levels**:
- **High (> 85%)**: Auto-select without asking → ✓ PROCEED
- **Medium (70-85%)**: Auto-select but show reasoning → ✓ PROCEED WITH EXPLANATION
- **Low (< 70%)**: Must ask clarifying questions → ⚠️ NEED USER INPUT

### 4. Check for Conflicting Files

**Scan for potential conflicts**:
```bash
# Check for existing environment files
[ -d ".claude" ] && echo "CONFLICT: .claude/ exists"
[ -f "CLAUDE.md" ] && echo "CONFLICT: CLAUDE.md exists"
```

**Conflict Resolution**:
- `.claude/` exists → ERROR: Environment already present
- `CLAUDE.md` exists → ERROR: May be existing project
- Both missing → ✓ SAFE TO PROCEED

### 5. Present Pre-Flight Summary

**Before generating ANY files, show summary**:
```
═══════════════════════════════════════════════════════════
PRE-FLIGHT CHECKS
═══════════════════════════════════════════════════════════

DIRECTORY: /Users/username/project-name/
  Status: Empty ✓
  Safe to proceed: YES

SPECIFICATION: ~/Documents/project-spec.md
  Found: YES ✓
  Size: 45 KB
  Readable: YES ✓

TEMPLATE DETECTION:
  Selected: Research Template
  Confidence: 92% (HIGH) ✓
  Auto-selecting without confirmation

CONFLICTS:
  .claude/ directory: Not present ✓
  CLAUDE.md file: Not present ✓
  No conflicts detected ✓

═══════════════════════════════════════════════════════════
READY TO GENERATE
═══════════════════════════════════════════════════════════

Will create:
  • CLAUDE.md - Project router
  • README.md - Documentation
  • .claude/commands/ - 8 commands
  • .claude/context/ - 4 context files
  • .claude/tasks/ - Task management
  • .claude/reference/ - 3 reference docs

Template: Research (hypothesis tracking, literature review, statistical standards)

═══════════════════════════════════════════════════════════

Proceed with environment generation? [Y/n]
```

**User Confirmation**:
- If user says YES or just hits enter → PROCEED
- If user says NO → ABORT

### 6. Handle Pre-Flight Warnings

**Warning: Directory Not Empty**
```
⚠️  WARNING: Current directory is not empty

Found existing files:
  • src/ (directory)
  • package.json
  • .gitignore
  • README.md

This may be an existing project. Bootstrap will add:
  • CLAUDE.md
  • .claude/ directory

Existing files will NOT be modified.

Proceed anyway? [y/N]
```

**Warning: .claude/ Already Exists**
```
❌ ERROR: Environment already exists

Found existing .claude/ directory in current location.

This directory already has a Claude Code environment.

Options:
  1. Use /undo-bootstrap to remove existing environment
  2. Navigate to a different directory
  3. Cancel bootstrap operation

What would you like to do? [1/2/3]
```

**Warning: Specification File Issues**
```
⚠️  WARNING: Specification file seems unusual

File: ~/Documents/spec.md
Size: 0.3 KB (very small)
Content: Appears to be mostly empty

This may not be a complete specification.

Options:
  1. Proceed anyway (may result in minimal environment)
  2. Cancel and provide different specification
  3. Show me the file contents first

What would you like to do? [1/2/3]
```

**Warning: Low Template Confidence**
```
⚠️  NOTICE: Template detection confidence is moderate

Best match: Base Template (65% confidence)
Reasons: Generic project keywords, no domain-specific indicators

I need to ask a few questions to select the right template.
This will only take 30 seconds.

Proceed with questions? [Y/n]
```

## Process (Agent-Driven)

### 1. Run Pre-Flight Checks First

**CRITICAL: Complete all pre-flight checks before invoking agent**

If any check fails or requires user input:
- Show appropriate warning/error
- Get user confirmation
- Only proceed if user approves

### 2. Invoke Environment Architect (After Pre-Flight Success)
```markdown
System: Detecting empty directory...
System: Activating Environment Architect Agent

Environment Architect: "Analyzing specification document..."
Environment Architect: "Extracting project indicators and requirements..."
```

### 2. Agent Performs Analysis
The Environment Architect will:
- Read specification and template rules in parallel
- Extract technology, domain, and complexity indicators
- Build assumption confidence map
- Calculate template scores

### 3. Agent Makes Template Decision (Enhanced with Educational Feedback)

**EDUCATIONAL REPORTING MODE** (always enabled for transparency):

```markdown
Environment Architect: "Template Detection Results"

═══════════════════════════════════════════════════════════
TEMPLATE CONFIDENCE SCORES
═══════════════════════════════════════════════════════════

[Template Name]        ████████████████████ 92% ✓ SELECTED
[Other Template 1]     ████████░░░░░░░░░░░░ 45%
[Other Template 2]     ████░░░░░░░░░░░░░░░░ 20%
[Other Template 3]     ██░░░░░░░░░░░░░░░░░░ 10%
[Other Template 4]     █░░░░░░░░░░░░░░░░░░░ 5%

CONFIDENCE LEVEL: HIGH (92% > 85% threshold)
ACTION: Auto-selecting [Template Name]

═══════════════════════════════════════════════════════════
WHY THIS TEMPLATE WON
═══════════════════════════════════════════════════════════

✓ "research question" (HIGH signal, +30pts)
  Found in: "Research question: How does remote work..."
  Why it matters: Strong academic research indicator

✓ "hypothesis" (HIGH signal, +30pts)
  Found in: "Primary hypothesis: Remote workers will show..."
  Why it matters: Confirms scientific methodology

✓ "literature review" (MEDIUM signal, +15pts)
  Found in section heading
  Why it matters: Academic research workflow needed

✓ "statistical analysis" (MEDIUM signal, +15pts)
  Found in: "Methodology > Data Analysis > Statistical analysis plan"
  Why it matters: Needs research-specific analysis tools

× "Power Query" (not found)
  Would have added: +30pts to Power Query template

× "personal project" (not found)
  Would have added: +30pts to Life Projects template

TOTAL SCORE: 90 points

═══════════════════════════════════════════════════════════
OTHER TEMPLATES CONSIDERED
═══════════════════════════════════════════════════════════

Base Template (45%):
  • Generic "project" mentions (+5pts × 3)
  • General "data" and "analysis" keywords (+5pts × 6)
  • Why not selected: No domain-specific indicators
  • When to use: Generic projects without clear domain

Power Query Template (20%):
  • "Excel" mentioned once in passing (+5pts)
  • "data" keyword (+5pts × 2)
  • Missing: No "Power Query", "M language", "regulatory" keywords
  • Why not selected: No specialized calculation/Excel focus
  • When to use: Excel + regulatory calculations + Power Query

Life Projects (10%):
  • "project" mentioned (+5pts × 2)
  • Missing: No personal/fitness/goal keywords
  • Why not selected: This is professional/academic work
  • When to use: Personal goals, fitness, home projects

Documentation (5%):
  • Generic text content (+5pts)
  • Missing: No "documentation", "technical writing" keywords
  • Why not selected: Not a documentation project
  • When to use: Writing docs, guides, tutorials, content

═══════════════════════════════════════════════════════════
LEARNING: WRITING BETTER SPECS
═══════════════════════════════════════════════════════════

Your spec was EXCELLENT for detection! Here's why:

✓ Clear domain terminology ("research question", "hypothesis")
✓ Specific methodology section
✓ Domain-specific workflows mentioned (literature review)
✓ Technology stack clear (statistical tools)

Tips for future specs:
• Include domain-specific terms early in description
• Mention key technologies explicitly (Python, R, Excel, etc.)
• Use standard terminology for your field
• Include workflow indicators (Phase 0, research methodology, etc.)

Confidence breakdown:
90-100% = Strong signals, obvious choice ✓ (Your spec: 92%)
70-89%  = Good signals, minor clarification may help
50-69%  = Mixed signals, add more domain keywords
<50%    = Vague spec, needs substantial clarification

═══════════════════════════════════════════════════════════
DECISION: AUTO-SELECT [Template Name]
═══════════════════════════════════════════════════════════

Confidence: 92% (HIGH)
Threshold: 85% (for auto-selection)
Result: Proceeding without confirmation

If confidence > 85%:
  → Auto-select without asking ✓ YOU ARE HERE
If confidence 70-85%:
  → Confirm with minimal questions
If confidence < 70%:
  → Request specific clarifications
```

**Optional --explain Flag** (show even more detail):
```
User: "Create environment with --explain flag from spec: [path]"

Shows additional detail:
- Full scoring breakdown for all templates
- Every keyword match with line numbers
- Alternative interpretations considered
- Assumption validation process
- Pattern matching rule references
```

**Compact Mode** (for experienced users who want less detail):
```
User: "Create environment with --quiet flag from spec: [path]"

Shows only:
- Template selected + confidence %
- Top 3 reasons why
- Immediate next step
```

### 4. Agent Generates Environment
The Environment Architect will create all files in parallel:
- CLAUDE.md router file
- README.md documentation
- .claude/ directory structure
- Template-specific files
- Initial tasks from requirements

### 5. Agent Handoff (if needed)
```markdown
Environment Architect: "Environment created successfully!"
Environment Architect: "Detected N tasks with difficulty ≥7"
Environment Architect: "Handing off to Task Orchestrator for breakdown..."

Task Orchestrator: "Received handoff. Analyzing high-difficulty tasks..."
```

## Script Integration (If Available)

**The Environment Architect can use Python scripts for acceleration:**
```bash
# Auto-detect template from specification
python scripts/bootstrap.py detect --spec {SPEC_FILE}

# Generate complete environment
python scripts/bootstrap.py bootstrap --spec {SPEC_FILE} --output {OUTPUT_DIR}
```

**Script Benefits (when used by agent):**
- Template detection in 100ms
- Environment generation in 2-3 seconds
- Automatic task creation from requirements
- Consistent structure every time

## Path Handling (Smart Detection)

Before processing the specification, expand and resolve the provided path:

### Path Expansion Logic

**Accept all path formats:**
- **Absolute**: `/Users/username/Documents/spec.md`
- **Tilde expansion**: `~/Documents/spec.md` → expand ~ to $HOME
- **Current directory**: `./spec.md` or `spec.md` → expand to full path from pwd
- **Parent directory**: `../spec.md` → expand .. to parent of pwd
- **Relative paths**: `Documents/spec.md` → expand from pwd

**Expansion Process:**
1. If path starts with `~`, replace with user's home directory
2. If path starts with `.` or `..`, resolve relative to current directory
3. If path has no directory component (just filename), keep as-is for fallback search
4. Convert to absolute path for validation

**Example Expansions:**
```bash
~/Documents/spec.md        → /Users/username/Documents/spec.md
./spec.md                  → /Users/username/current-project/spec.md
../specs/project.md        → /Users/username/specs/project.md
spec.md                    → spec.md (will trigger fallback search)
```

**Implementation Note**: This path expansion is the foundation for Tasks 106-108 (fallback search, iCloud search, recent files).

### Fallback Search (File Not Found)

If the expanded path doesn't exist, search common macOS locations:

**Search Order** (prefer closer locations first):
1. Current directory: `./[filename]`
2. Documents: `~/Documents/[filename]`
3. Downloads: `~/Downloads/[filename]`
4. Desktop: `~/Desktop/[filename]`

**Search Process:**
```
IF file not found at expanded path:
  1. Extract filename from path
  2. Search each location in order
  3. Collect all matches

  IF exactly 1 match found:
    → Use that file automatically
    → Inform user: "Found spec at: [full path]"

  IF multiple matches found:
    → List all with modification times
    → Ask user to choose:
       1. ~/Documents/spec.md (modified 2 min ago, 45KB)
       2. ~/Downloads/spec.md (modified 1 hour ago, 32KB)
       3. ~/Desktop/spec.md (modified yesterday, 45KB)
       Which file should I use? [1/2/3]

  IF no matches found:
    → Proceed to iCloud search (Task 107)
```

**Example Interaction:**
```
User: "Create environment using spec: project-spec.md"

System: File not found at ./project-spec.md
System: Searching common locations...
System: Found spec at: ~/Documents/project-spec.md
System: Proceeding with bootstrap...
```

### iCloud Drive Search (Extended Fallback)

If not found in common locations, search iCloud Drive:

**iCloud Path**: `~/Library/Mobile Documents/com~apple~CloudDocs/`

**Search Process:**
```
IF no matches in common locations:
  1. Check if iCloud Drive exists
  2. Search recursively for [filename] in iCloud directory
  3. Check file is downloaded (not .icloud placeholder)
  4. Limit search depth to 5 levels (performance)

  IF matches found:
    → Verify file is downloaded (size > 0 bytes)
    → List all matches with paths and timestamps
    → Ask user to choose if multiple

  IF file is pending download (.icloud file):
    → Warn user: "File '[filename]' found in iCloud but not downloaded"
    → Suggest: "Open Finder and wait for file to download, then retry"

  IF still no matches:
    → Proceed to 'recent files' helper (Task 108)
```

**iCloud-Specific Checks:**
- **Downloaded files**: Full file with actual size
- **Placeholder files**: `.icloud` extension, zero bytes
- **Synced but not downloaded**: File appears in Finder but isn't local yet

**Example Interaction:**
```
User: "Create environment using spec: pension-spec.md"

System: File not found at ./pension-spec.md
System: Searching common locations...
System: Not found in Documents, Downloads, Desktop
System: Searching iCloud Drive...
System: Found spec at: ~/Library/Mobile Documents/com~apple~CloudDocs/02PROJECTS/pension-spec.md
System: Proceeding with bootstrap...
```

**Warning Example:**
```
User: "Create environment using spec: old-project.md"

System: Searching all locations...
System: Found in iCloud but file is not downloaded (cloud-only)
System:
⚠ File is pending download from iCloud
  Location: ~/Library/Mobile Documents/com~apple~CloudDocs/old-project.md

  Please open this location in Finder and wait for download to complete.
  Then run this command again.
```

### Recent Files Helper (Last Resort)

If file still not found after all searches, offer to show recent `.md` files:

**Trigger**: After iCloud search returns no matches

**Process:**
```
System: Could not find '[filename]' in any location.

Would you like to see recently modified .md files?
  [Y] Yes, show me recent specs
  [N] No, I'll provide the correct path

IF user says Yes:
  1. Search all locations (Documents, Downloads, Desktop, iCloud)
  2. Find all .md files modified in last 7 days
  3. Sort by modification time (newest first)
  4. Limit to 10 most recent
  5. Display with relative paths and details

  Recent .md files (last 7 days):
   1. project-spec.md         (Documents, 2 min ago, 45KB)
   2. pension-calculator.md   (iCloud/02PROJECTS, 1 hour ago, 38KB)
   3. research-notes.md       (Desktop, yesterday, 12KB)
   4. old-project.md          (Downloads, 3 days ago, 52KB)
   5. draft-spec.md           (Documents, 5 days ago, 23KB)

  Which file should I use? [1-5 or 'none']

  IF user selects number:
    → Use that file
    → Proceed with bootstrap

  IF user says 'none':
    → Ask for correct path
    → Return to path expansion step
```

**Search Command** (uses find or mdfind):
```bash
# Fast search using Spotlight (mdfind)
mdfind -onlyin ~/Documents -onlyin ~/Downloads -onlyin ~/Desktop \
  -onlyin ~/Library/Mobile\ Documents/com~apple~CloudDocs \
  'kMDItemContentType == "net.daringfireball.markdown" && kMDItemFSContentChangeDate >= $time.today(-7)'

# Fallback using find (if mdfind unavailable)
find ~/Documents ~/Downloads ~/Desktop \
  ~/Library/Mobile\ Documents/com~apple~CloudDocs \
  -name "*.md" -mtime -7 -type f 2>/dev/null
```

**Performance Notes:**
- Uses Spotlight (mdfind) for speed when available
- Falls back to find if Spotlight unavailable
- Limits to 7 days to keep results relevant
- Shows top 10 to avoid overwhelming user

**Example Interaction:**
```
User: "Create environment using spec: my-project.md"

System: Searching all locations...
System: File 'my-project.md' not found

Would you like to see recently modified .md files? [Y/N]

User: Y

System: Recent .md files (last 7 days):
  1. startup-idea-spec.md        (Documents, 5 min ago, 34KB)
  2. side-project-notes.md       (Desktop, 2 hours ago, 18KB)
  3. pension-calc-spec.md        (iCloud/02PROJECTS, yesterday, 45KB)

Which file should I use? [1-3 or 'none']

User: 3

System: Using: ~/Library/Mobile Documents/com~apple~CloudDocs/02PROJECTS/pension-calc-spec.md
System: Proceeding with bootstrap...
```

## Manual Process (Fallback if agent unavailable)

### Phase 1: Analysis & Assumption Extraction (⏱️ Target: 2-3 seconds)

#### Step 1A: Read and Deep-Analyze Specification [PARALLEL EXECUTION]

**PARALLEL READ OPERATIONS**:
```
Execute simultaneously in single message:
1. Read specification document
2. Read template-selection-rules.md
3. Read available template READMEs (if paths known)
4. Read existing project files (if any)
```

**Extract comprehensive indicators** (process in memory):
- Technologies mentioned (Excel, Power Query, Python, SQL, React, etc.)
- Project type keywords (ETL, dashboard, research, analysis, calculation, etc.)
- Domain characteristics (regulatory, compliance, academic, experimental, etc.)
- Complexity indicators (timeline mentions, team size, deliverables count)
- Data characteristics (sensitive, regulatory, financial, medical, etc.)

**Identify implicit assumptions** (concurrent analysis):
- Technology stack availability
- User expertise level
- Data source accessibility
- Timeline feasibility
- Error tolerance requirements
- Team collaboration needs

**Build assumption confidence map** (in-memory processing):
```
For each assumption:
  - Evidence: What in the spec supports this?
  - Confidence: How certain are we? (percentage)
  - Impact: What happens if wrong? (low/medium/high/critical)
  - Validation: Do we need to confirm? (yes/no)
```

**Performance Benefits**:
- Parallel reads: 60-70% time reduction vs sequential
- Single tool message: Reduces context switches
- In-memory processing: No intermediate writes

#### Step 1B: Generate Targeted Clarifications

**Only generate questions for**:
- Critical assumptions with <70% confidence
- High-impact unknowns that affect template selection
- Ambiguities that would change configuration

**Skip questions if**:
- All critical assumptions have >85% confidence
- Template selection is unambiguous (>90% confidence)
- Configuration needs are clear from specification

**Question format** (if needed):
```
Based on your specification, I need to clarify a few critical points:

1. [Question about highest-impact unknown]
   Why this matters: [Impact on template/configuration]

2. [Question about critical assumption]
   Why this matters: [What changes based on answer]
```

### Phase 2: Confident Decision & Generation (⏱️ Target: 3-5 seconds)

#### Step 2A: Process Responses & Validate Assumptions [OPTIMIZED]

**If questions were asked** (batch processing):
- Update assumption confidence based on responses
- Mark assumptions as validated/invalidated
- Identify any new assumptions from responses

**Recalculate template scores** (parallel evaluation):
- Apply pattern matching using `.claude/reference/template-selection-rules.md`
- Weight scores by assumption confidence
- Boost scores for validated assumptions

**Make confident template selection** (instant decision):
- Select highest-scoring template (must be >85% confidence)
- If still ambiguous, use Base template with notes
- Document full decision rationale

**Performance Optimizations**:
- Batch all updates in single operation
- Score all templates simultaneously
- No file I/O until decision finalized

#### Step 2B: Log Decision with Full Context

**Create decision log entry** in `.claude/decisions/template-selection.md`:
```markdown
### [Date] - [Project Name from Spec]
**Selected Template**: [template-name]
**Confidence**: [percentage] (increased from X% after clarifications)
**Decision Time**: [time taken]

**Indicators Present**:
- [List all indicators found]

**Assumptions Validated**:
- ✓ [Validated assumption 1]
- ✓ [Validated assumption 2]
- ✗ [Invalidated assumption]
- ? [Unvalidated assumption]

**Alternatives Considered**:
1. **[Alternative Template]** (Confidence: X%)
   - Why considered: [indicators]
   - Why rejected: [reasoning]

**Rationale**:
[Detailed explanation including assumption validation impact]

**Configuration Decisions**:
- Phase 0: [Yes/No] because [reasoning]
- Validation level: [Standard/Extensive] because [reasoning]
- Difficulty scoring: [Simple/Multi-dimension] because [reasoning]
```

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

#### Step 2C: Generate Environment with High Confidence [MASSIVE PARALLEL EXECUTION]

**PARALLEL FILE GENERATION** (⏱️ Target: 2-3 seconds for entire environment):

#### A. Determine File Set

**Base files (all templates)** - Generate ALL simultaneously:
```
Single message with multiple Write tool calls:
- `CLAUDE.md` - Router file
- `README.md` - Human documentation
- `.claude/context/overview.md` - Extracted from specification
- `.claude/context/validation-rules.md` - Standard rules
- `.claude/tasks/task-overview.md` - Empty initially
- `.claude/reference/difficulty-guide.md` - Appropriate for template
```

**Performance Impact**:
- Sequential generation: 15-20 seconds (6 files × 2-3 sec each)
- Parallel generation: 2-3 seconds total (all concurrent)
- **85% time reduction**

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

**Standard Commands** (generate in parallel unless minimal template):
```
Parallel Write operations:
- `complete-task.md`
- `breakdown.md`
- `sync-tasks.md`
- `update-tasks.md`
```

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

### Step 6: Create Initial Tasks [PARALLEL BATCH CREATION]

**If specification contains clear deliverables/features**, offer to create initial tasks:

```
"I detected [N] potential tasks from your specification:
[List extracted tasks with estimated difficulty]

Would you like me to create these as initial task JSON files? (Y/N)"
```

**If YES** (⏱️ Target: 1-2 seconds for all tasks):
```
PARALLEL OPERATIONS:
1. Create ALL task JSON files simultaneously:
   - task-001.json
   - task-002.json
   - ...
   - task-N.json
   (Single message, multiple Write calls)

2. Then run sync-tasks to update overview
```

**Performance Benefits**:
- Sequential: N × 2 seconds
- Parallel: 2 seconds total
- **90% reduction for 10+ tasks**

**If NO**:
- User will create tasks manually later

### Step 7: Present Summary

**Output**:

```
## Completion Message (Tiered Display)

### Tier 1: Essential Information (Always Show)

```
✓ Environment Ready! ([time taken, e.g., 6.2s])

PROJECT: [Project Name]
TEMPLATE: [Template Name] (auto-selected, [X]% confidence)

📋 IMMEDIATE NEXT STEP (do this first):
   → Read: .claude/context/overview.md

⏰ THEN (choose one path):

   [If Phase 0 enabled:]
   □ Phase 0: Resolve Ambiguities (1-2 hours)
     → Run: @.claude/commands/initialize-project.md
     Why: Your project has regulatory/ambiguous requirements
     Expected: 4-step workflow to eliminate all ambiguities

   [If standard project:]
   □ Start Development (5 minutes)
     → Review generated tasks: .claude/tasks/task-overview.md
     → Run: @.claude/commands/complete-task.md [id]
     Why: [N] tasks were extracted from your specification

💡 Type "show details" to see full configuration and file list
```

### Tier 2: Detailed Information (On Request Only)

**Trigger**: User types "show details" or "show bootstrap details"

```
📊 Bootstrap Details

DETECTION:
  Template: [Template Name]
  Confidence: [X]%

  Why this template?
    ✓ [Indicator 1] - "[quote from spec]"
    ✓ [Indicator 2] - "[quote from spec]"
    ✓ [Indicator 3] - "[quote from spec]"

CONFIGURATION:
  • Difficulty Scoring: [Simple 1-10 | Multi-dimension (5 factors)]
  • Phase 0: [Enabled | Disabled]
    [If enabled: Reason - Regulatory requirements + ambiguous source docs]
  • Technology Stack: [extracted list]
  • Estimated Complexity: [Weekend project | Multi-week | Long-term]
  • Initial Tasks: [N tasks created | Create tasks manually]

FILES CREATED:
  Structure:
    ├── CLAUDE.md (router file)
    ├── README.md (human docs)
    └── .claude/
        ├── commands/ ([N] commands)
        ├── context/ ([N] context files)
        ├── tasks/ (task management)
        └── reference/ ([N] docs)

  Template-Specific:
    [List any template-specific files added]

NEXT STEPS (detailed):
  [If Phase 0:]
  Phase 0 Workflow (1-2 hours total):
    1. Initialize (15-20 min)
       → @.claude/commands/initialize-project.md
       Extracts ambiguities from source documents

    2. Resolve Ambiguities (45-60 min)
       → @.claude/commands/resolve-ambiguities.md
       Interactive: Review and decide on interpretations

    3. Generate Artifacts (10-15 min)
       → @.claude/commands/generate-artifacts.md
       Creates glossary, data contracts, initial tasks

    4. Extract/Initialize (5-10 min)
       → @.claude/commands/extract-queries.md (or equivalent)
       Sets up project structure for implementation

  Phase 0 completion criteria:
    - All ambiguities resolved
    - Every variable defined in glossary
    - All decisions documented in assumptions.md

  [If standard project:]
  Standard Workflow:
    1. Review project overview (2-3 min)
       → .claude/context/overview.md
       Confirms extracted requirements and goals

    2. Review/create tasks (5-10 min)
       → .claude/tasks/task-overview.md
       [N tasks already created | Create initial tasks]

    3. Start first task (immediate)
       → @.claude/commands/complete-task.md [task-id]
       Use complete-task to start AND finish tasks

    4. Break down difficult tasks (as needed)
       → @.claude/commands/breakdown.md [task-id]
       Required for any task with difficulty ≥ 7

QUICK REFERENCE:
  • Template docs: templates/[name]/README.md (in claude_code_environment repo)
  • Task management: .claude/tasks/task-overview.md
  • All commands: .claude/commands/
  • Context files: .claude/context/
  • Validation: @.claude/commands/update-tasks.md (check system health)

TIME ESTIMATES:
  Phase 0 (if enabled): 1-2 hours
  First task setup: 5 minutes
  Weekend project: 5-10 hours total
  Multi-week project: 20-40 hours
  Long-term project: 80+ hours
```

### Message Selection Logic

**Show Tier 1 (Essential) By Default:**
- Always show project name, template, and immediate next step
- Keep output to 10-12 lines max
- Make next action crystal clear with time estimate
- Offer "show details" option

**Show Tier 2 (Detailed) Only When:**
- User explicitly requests: "show details", "show bootstrap details", "show more"
- User asks about configuration: "what was configured?", "what files were created?"
- User needs troubleshooting: link to detailed view

**Benefits of Tiered Display:**
- Reduces cognitive load (10 lines vs 30+ lines)
- Makes immediate action obvious
- Prevents decision paralysis
- Details available when needed
- Faster comprehension

### Example Outputs

**Example 1: Power Query with Phase 0**
```
✓ Environment Ready! (5.8s)

PROJECT: Pension Calculator Implementation
TEMPLATE: Power Query (auto-selected, 92% confidence)

📋 IMMEDIATE NEXT STEP (do this first):
   → Read: .claude/context/overview.md

⏰ THEN (Phase 0 workflow):
   □ Phase 0: Resolve Ambiguities (1-2 hours)
     → Run: @.claude/commands/initialize-project.md
     Why: Detected regulatory requirements + ambiguous PDF source
     Expected: 4-step workflow to clarify all calculations

💡 Type "show details" for full configuration and file list
```

**Example 2: Standard Research Project**
```
✓ Environment Ready! (4.2s)

PROJECT: Machine Learning Performance Analysis
TEMPLATE: Research/Analysis (auto-selected, 88% confidence)

📋 IMMEDIATE NEXT STEP (do this first):
   → Read: .claude/context/overview.md

⏰ THEN (start research):
   □ Review Generated Tasks (5 minutes)
     → Open: .claude/tasks/task-overview.md
     → 12 tasks created from your specification
     → Run: @.claude/commands/complete-task.md [id]

💡 Type "show details" for full configuration and file list
```

**Example 3: Simple Life Project**
```
✓ Environment Ready! (3.1s)

PROJECT: 2024 Fitness Goals Tracker
TEMPLATE: Life Projects (auto-selected, 75% confidence)

📋 IMMEDIATE NEXT STEP (do this first):
   → Read: .claude/context/overview.md

⏰ THEN (get started):
   □ Create Your First Tasks (5 minutes)
     → Run: @.claude/commands/sync-tasks.md after creating
     → Or use: @.claude/commands/complete-task.md to start work

💡 Type "show details" for full configuration and file list
```
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

### File Not Found Errors

**If specification not found (initial attempt)**:
```
❌ ERROR: Specification file not found

📍 Where: Looking for file at "[path_provided]"

🔍 Why this happened:
   • File doesn't exist at this path
   • Path may have typo or incorrect location
   • File might be in a different folder

💡 How to fix:

1. **Verify file exists**:
   ls -la "[path_provided]"

2. **Check common locations**:
   ls ~/Documents/*.md      # Documents folder
   ls ~/Downloads/*.md      # Downloads folder
   ls ~/Desktop/*.md        # Desktop

3. **Use just filename** (I'll search for it):
   /smart-bootstrap myproject.md

4. **Create new spec interactively**:
   /create-spec

5. **Get full path from Finder**:
   • Right-click file in Finder
   • Hold Option key
   • Click "Copy [filename] as Pathname"
   • Paste here

🔗 Related:
   • Mac paths guide: .claude/reference/mac-user-workflow-guide.md
   • Create spec: /create-spec
```

**If specification not found (after searching all locations)**:
```
❌ ERROR: Specification file not found after searching

📍 Searched:
   ✗ Current directory: [pwd]
   ✗ ~/Documents/
   ✗ ~/Downloads/
   ✗ ~/Desktop/
   ✗ iCloud Drive: ~/Library/Mobile Documents/com~apple~CloudDocs/

🔍 Why this happened:
   I searched all common Mac locations but couldn't find "[filename]".

💡 How to fix:

1. **Check filename spelling**:
   You provided: "[filename]"

2. **Show recent .md files**:
   Would you like to see recently modified .md files?
   Say "yes" and I'll list them for you.

3. **Use absolute path** if file is elsewhere:
   /smart-bootstrap /full/path/to/your/spec.md

4. **Create new spec**:
   /create-spec

5. **Export from Claude Desktop**:
   • Open conversation in Claude Desktop
   • Click conversation title → Export → Markdown
   • Save file and note the location

🔗 Related:
   • Export guide: .claude/reference/mac-user-workflow-guide.md
   • Create spec: /create-spec
```

### Template Detection Issues

**If specification is too vague**:
```
⚠️  WARNING: Specification too vague for auto-detection

📍 Issue: Template confidence below 50%
   • Power Query: 15%
   • Research: 10%
   • Life Projects: 5%
   • Documentation: 5%
   • Base: 20% (default fallback)

🔍 Why this happened:
   Your spec lacks clear indicators for template selection.

   Missing signals for:
   • Project type (web app, data analysis, research, personal)
   • Technology stack (specific tools/languages)
   • Domain keywords (regulatory, academic, fitness, API)

💡 How to fix:

**Option A: ADD MORE DETAILS to your spec**

   Edit spec.md and add:
   1. Project type: "This is a [research project/Power Query solution/etc.]"
   2. Technologies: "Python, pandas, scipy" or "Power Query, Excel 365"
   3. Domain keywords:
      - Research: "hypothesis", "statistical analysis"
      - Power Query: "regulatory calculation", "M language"
      - Life: "personal goal", "fitness journey"

   Then retry: /smart-bootstrap spec.md

**Option B: USE CREATE-SPEC for guided creation**
   /create-spec

**Option C: CHOOSE TEMPLATE MANUALLY**

   1. Power Query - Excel calculations, regulatory, M language
   2. Research - Academic, hypothesis testing, data science
   3. Life Projects - Personal goals, fitness, learning
   4. Documentation - API docs, technical writing
   5. Base - Standard software projects

   Say: "Use [template name] template"

🔗 Related:
   • Template guide: .claude/reference/template-selection-rules.md
   • Spec examples: examples/specifications/templates/
```

**If conflicting signals**:
```
ℹ️  NOTICE: Multiple templates match your spec

📍 Detection scores:
   • Research/Analysis: 75% ← "hypothesis", "statistical analysis"
   • Power Query: 70% ← "Excel", "calculation", "regulatory"

🔍 Why this happened:
   Your spec contains keywords matching multiple templates.

💡 How to clarify:

**Which is your PRIMARY focus?**

If RESEARCH is primary:
   • Testing hypothesis
   • Publishing findings
   • Statistical significance
   → Use Research template

If POWER QUERY is primary:
   • Automating Excel reports
   • M language implementation
   • Compliance calculations
   → Use Power Query template

Say: "Use [template name] template"

🔗 Related:
   • Template comparison: legacy-template-reference.md
   • Detection rules: .claude/reference/template-selection-rules.md
```

### Directory and File Issues

**If .claude/ already exists**:
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

**Option A: WRONG DIRECTORY**
   cd /path/to/your/new/project
   /smart-bootstrap spec.md

**Option B: START OVER** (⚠️  deletes existing environment)
   # Back up first
   cp -r .claude .claude.backup

   # Remove and restart
   rm -rf .claude CLAUDE.md README.md
   /smart-bootstrap spec.md

**Option C: UPDATE EXISTING**
   The environment already exists! You can:
   • Start working: /complete-task [id]
   • View tasks: cat .claude/tasks/task-overview.md
   • Update context: Edit .claude/context/overview.md

**Option D: INCOMPLETE BOOTSTRAP**
   # Check what exists
   ls -la .claude/

   # If incomplete, remove and retry
   rm -rf .claude
   /smart-bootstrap spec.md

🔗 Related:
   • Working with environments: See CLAUDE.md
```

**If specification file is empty or too small**:
```
⚠️  WARNING: Specification file appears empty or too small

📍 Where: "[path]"
   File size: [N] bytes (expected: >100 bytes)

🔍 Why this happened:
   The file exists but has little/no content.

   Possible causes:
   • File wasn't saved properly
   • Export from Claude Desktop failed
   • Wrong file opened

💡 How to fix:

1. **Check file contents**:
   cat "[path]"

2. **Re-export from Claude Desktop**:
   • Open conversation
   • Click title → Export → Markdown
   • Save and note the path

3. **Create new spec**:
   /create-spec

4. **Minimum spec requirements**:
   • Project name/title
   • Description (what you're building)
   • Technology stack
   • Goals or objectives
   • At least 100-200 words

🔗 Related:
   • Spec templates: examples/specifications/templates/
   • Export guide: .claude/reference/mac-user-workflow-guide.md
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

## Performance Metrics & Optimization

### Time Reduction Summary

| Phase | Sequential (Old) | Parallel (New) | Improvement |
|-------|-----------------|-----------------|-------------|
| **Phase 1: Analysis** | 8-10 seconds | 2-3 seconds | **70% faster** |
| - Read spec + rules | 4-5 sec | 1-2 sec | Parallel reads |
| - Template analysis | 4-5 sec | 1 sec | In-memory processing |
| **Phase 2: Generation** | 20-30 seconds | 3-5 seconds | **85% faster** |
| - File generation | 15-20 sec | 2-3 sec | Parallel writes |
| - Task creation | 5-10 sec | 1-2 sec | Batch creation |
| **Total Setup Time** | 28-40 seconds | 5-8 seconds | **80% faster** |

### Parallel Execution Patterns

#### Pattern 1: Multi-Read Operations
```javascript
// Execute in single message:
[
  Read(specification.md),
  Read(template-rules.md),
  Read(template-readme.md)
]
// All complete simultaneously
```

#### Pattern 2: Batch File Generation
```javascript
// Generate entire environment at once:
[
  Write(CLAUDE.md, content1),
  Write(README.md, content2),
  Write(overview.md, content3),
  Write(task-001.json, content4),
  Write(task-002.json, content5)
]
// 10 files = still ~3 seconds
```

#### Pattern 3: Concurrent Validation
```javascript
// Validate all assumptions simultaneously:
[
  ValidateTemplate(indicators),
  ValidateComplexity(metrics),
  ValidateRequirements(spec)
]
```

### Resource Utilization

- **Context Usage**: 40% reduction (fewer tool round-trips)
- **Token Efficiency**: Better batching reduces overhead
- **Error Recovery**: Faster retry on failures

## Two-Step Processing Benefits

### Enhanced Accuracy
- **Assumption Validation**: Explicitly validates assumptions before making decisions
- **Higher Confidence**: Decisions made with >85% confidence after clarifications
- **Reduced Errors**: Catches misunderstandings before environment generation

### Better User Experience
- **Minimal Questions**: Only asks when truly necessary (critical unknowns)
- **Transparent Reasoning**: Shows exactly why each question matters
- **Faster Resolution**: Targeted questions lead to quicker accurate setup (5-8 sec total)

### Improved Learning
- **Decision Tracking**: All decisions logged with full rationale
- **Pattern Detection**: Feeds validated assumptions to pattern analyzer
- **Continuous Improvement**: System learns from each project setup

### Implementation Details
See `.claude/reference/two-step-processing.md` for complete framework documentation.

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
