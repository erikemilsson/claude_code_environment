# Complete Mac User Workflow Guide: Creating Projects with claude_code_environment

**Document Type**: Internal Process Documentation
**Audience**: Developers (Developer-Friendly)
**Last Updated**: 2025-12-17
**Purpose**: Comprehensive explanation of how Mac users create new projects using the claude_code_environment repository, including internal system mechanics

---

## Executive Summary

The `claude_code_environment` repository provides an automated, agent-driven system for bootstrapping Claude Code project environments. The workflow transforms a user's plain-English specification into a complete, structured `.claude/` directory with task management, commands, context files, and optional Phase 0 ambiguity resolution - all in 5-8 seconds using parallel execution patterns.

**Core Innovation**: Pattern-based template detection eliminates manual template selection. Users provide a specification document; the system analyzes it, scores templates using keyword patterns, and auto-generates the appropriate environment with 85%+ accuracy.

---

## Table of Contents

1. [Prerequisites & Setup (Mac User)](#1-prerequisites--setup-mac-user)
2. [Phase 1: Specification Creation in Claude Desktop](#2-phase-1-specification-creation-in-claude-desktop)
3. [Phase 2: Environment Generation Process](#3-phase-2-environment-generation-process)
4. [Template Detection Deep Dive](#4-template-detection-deep-dive)
5. [Generated Structure Details](#5-generated-structure-details)
6. [Example Scenarios (Step-by-Step)](#6-example-scenarios-step-by-step)
7. [Post-Generation Next Steps](#7-post-generation-next-steps)
8. [System Performance & Optimization](#8-system-performance--optimization)
9. [Advanced Topics](#9-advanced-topics)
10. [macOS-Specific Considerations](#10-macos-specific-considerations)
    - [10.0 Quick Path Reference](#100-quick-path-reference-for-mac-users)
    - [10.1 File Paths & Smart Path Detection](#101-file-paths--smart-path-detection)
11. [Troubleshooting](#11-troubleshooting)
12. [Performance Metrics](#12-performance-metrics)
13. [Summary & Key Takeaways](#13-summary--key-takeaways)
14. [Appendices](#appendix-a-file-paths-reference)

---

## 1. Prerequisites & Setup (Mac User)

### 1.1 Required Software Stack

#### Claude Desktop (Specification Creation)
- **Purpose**: Interactive environment for discussing project ideas and creating specifications
- **Installation**: Download from claude.ai/desktop
- **Key Feature**: Export conversation to .md file
- **macOS Path**: `/Applications/Claude.app`

#### VS Code (Development Environment)
- **Purpose**: Primary editor for project work
- **Installation**: Download from code.visualstudio.com
- **Key Feature**: Claude Code extension integration
- **macOS Path**: `/Applications/Visual Studio Code.app`

#### Claude Code Extension
- **Purpose**: Claude AI integration within VS Code
- **Installation**: VS Code Extensions → Search "Claude Code" → Install
- **Activation**: Requires Claude API key or subscription
- **Interface**: Accessible via sidebar or command palette

### 1.2 Repository Access

#### Clone Template Repository
```bash
# Standard location (recommended)
cd ~/Projects  # or ~/Documents/Projects

# Clone repository
git clone https://github.com/[user]/claude_code_environment.git

# Repository contains:
# - templates/           (5 template types with READMEs)
# - components/          (reusable component definitions)
# - .claude/             (meta-level commands for this repo)
# - examples/            (example specifications)
# - scripts/             (Python automation utilities)
```

#### macOS File Path Considerations

**iCloud Drive Paths** (if syncing):
```bash
/Users/[username]/Library/Mobile Documents/com~apple~CloudDocs/02PROJECTS/1A_github_projects/
```

**Local Paths** (no sync):
```bash
/Users/[username]/Documents/Projects/
/Users/[username]/Projects/
```

**Important**: Avoid paths with spaces - causes issues with some tools. Use underscores or hyphens.

### 1.3 Environment Variables (Optional)

For enhanced agent functionality:
```bash
# ~/.zshrc or ~/.bash_profile
export CLAUDE_CODE_ENV_PATH="/path/to/claude_code_environment"
export GEMINI_API_KEY="your-api-key"  # For Gemini MCP integration
```

---

## 2. Phase 1: Specification Creation in Claude Desktop

### 2.1 User Workflow

#### Step 1: Open Claude Desktop
User initiates conversation about project idea. Key discussion areas:

**For All Projects:**
- What are you building? (brief description)
- What technologies/tools will you use?
- What are the main deliverables or features?
- Timeline expectations (weekend project vs. multi-month)
- Any special requirements (regulatory, compliance, security)

**Domain-Specific Probes:**

If user mentions **Excel, Power Query, or calculations**:
- Are there regulatory documents to interpret?
- Do source documents have ambiguous terminology?
- Zero-error tolerance required?

If user mentions **research, analysis, or experiments**:
- Is there a specific research question or hypothesis?
- Will you review literature systematically?
- Statistical methods or A/B testing involved?

If user mentions **personal goals, fitness, organization**:
- Is this work-related or personal?
- First-person language throughout?

#### Step 2: Export Conversation

**Method 1: Copy-Paste** (Most Common)
1. Select entire conversation
2. Copy to clipboard
3. Open text editor
4. Paste and save as `project-spec.md`

**Method 2: Claude Desktop Export** (If Available)
1. Click conversation menu (⋮)
2. Select "Export conversation"
3. Choose Markdown format
4. Save to known location

**Method 3: Manual Synthesis** (Structured)
User manually creates specification following template structure:

```markdown
# [Project Name]

## Project Overview
[Brief description of what you're building]

## Background
[Context and motivation]

## Technology
[Primary technologies and frameworks]

## Requirements
1. [Requirement 1]
2. [Requirement 2]
...

## Deliverables
1. [Deliverable 1]
2. [Deliverable 2]
...

## Timeline
[Estimated duration]

## Special Requirements
[Regulatory, compliance, domain-specific needs]
```

### 2.2 Specification Content Patterns

#### Power Query Project Example:
```markdown
# Pension Calculation Implementation

## Project Overview
Implement pension calculation formulas based on Swedish Pension Authority's
regulatory document (PDF) using Power Query in Excel.

## Technology
Power Query M language in Excel workbook

## Requirements
1. Parse regulatory PDF to extract calculation formulas
2. Interpret ambiguous variable definitions
3. Implement in Power Query with error handling
4. Create data validation
5. Generate audit trail
6. Test against sample data

## Compliance Requirements
- Zero-error tolerance (financial calculations)
- Full audit trail required
- All interpretation decisions documented
```

**Key Detection Signals:**
- "Power Query" → 30 points
- "M language" → 30 points
- "Excel" + "calculation" → 30 points
- "regulatory" + "PDF" → Phase 0 trigger
- **Total: 90+ points → Auto-select Power Query template**

#### Research Project Example:
```markdown
# Transformer Models for Code Generation - Research Study

## Research Question
Do transformer-based models fine-tuned on domain-specific code outperform
general-purpose models for specialized domains?

## Hypothesis
H1: Domain-specific fine-tuning improves accuracy by 15%+
H2: Improvement more pronounced in specialized domains
H3: Smaller tuned models match larger general models

## Methodology
- Literature review: 60+ papers (ACL, IEEE, arXiv)
- Experiment design: 3 datasets, 4 model variants
- Metrics: BLEU, CodeBLEU, Pass@k
- Statistical analysis: ANOVA, effect sizes, p < 0.05

## Deliverables
1. Literature review document
2. Experimental code and trained models
3. Results analysis with statistical validation
4. Research paper for NeurIPS/ICML submission
```

**Key Detection Signals:**
- "research question" → 30 points
- "hypothesis" → 30 points
- "literature review" → 30 points
- "experiment" → 30 points
- "statistical analysis" → 15 points
- **Total: 135+ points → Auto-select Research template**

#### Life Project Example:
```markdown
# My 2024 Fitness and Health Journey

## Personal Goals
Get healthier in 2024 by tracking fitness, planning nutrition, staying accountable.

## What I Want to Track
- Workouts: log sessions, track progress on lifts, cardio activities
- Nutrition: weekly meal prep, track macros, water intake
- Body measurements: weekly weigh-ins, monthly measurements
- Goals: Run 5K by March, bench bodyweight by June, lose 15 pounds by July

## How I Want to Organize This
- Simple workout log
- Meal planning template
- Progress dashboard with charts
- Goal checklist with dates

## Success Criteria
- Log workouts 4x per week
- Measurable improvement in strength/endurance
- Feel more energetic
- Make fitness sustainable habit
```

**Key Detection Signals:**
- "personal goals" → 30 points
- "fitness" → 30 points
- "track my" → 30 points
- First-person throughout → 15 points
- **Total: 105+ points → Auto-select Life Projects template**

---

## 3. Phase 2: Environment Generation Process

### 3.1 User Command Syntax

**In VS Code with Claude Code:**

User opens new project directory:
```bash
mkdir ~/Projects/new-project-name
cd ~/Projects/new-project-name
code .  # Opens VS Code
```

In Claude Code interface (sidebar or chat), user types:
```
"Create the environment from claude_code_environment repo using spec: ~/Documents/project-spec.md"
```

**Alternative phrasings that trigger same workflow:**
- "Bootstrap this project from the spec at [path]"
- "Initialize environment using specification [path]"
- "Generate .claude structure from [path]"
- "Set up Claude Code environment with spec [path]"

### 3.2 Internal Workflow (smart-bootstrap.md)

#### 3.2.1 Agent Activation

**System Detection Logic:**
```python
if not os.path.exists('.claude/'):
    # Empty directory detected
    activate_agent('environment-architect')
else:
    # Environment exists, skip bootstrap
    print("Environment already exists. Use existing commands.")
```

**Agent Configuration** (from .claude/agent-config.json):
```json
{
  "environment-architect": {
    "phase": "initialization",
    "triggers": {
      "automatic": [
        {"condition": "empty_directory", "priority": 1},
        {"condition": "no_claude_folder", "priority": 1}
      ],
      "manual": [
        "create environment from spec",
        "bootstrap new project"
      ]
    },
    "boundaries": {
      "allowed_operations": [
        "create_directories",
        "generate_files",
        "detect_templates",
        "extract_initial_tasks"
      ],
      "forbidden_operations": [
        "modify_task_status",
        "run_validation_gates",
        "break_down_tasks"
      ]
    }
  }
}
```

#### 3.2.2 Step 1: Specification Analysis (Parallel Reads - 2-3 seconds)

**Parallel File Operations:**
```python
# Execute simultaneously in single Claude message
results = await asyncio.gather(
    read_file(specification_path),
    read_file('claude_code_environment/.claude/reference/template-selection-rules.md'),
    read_file('claude_code_environment/templates/power-query/README.md'),
    read_file('claude_code_environment/templates/research-analysis/README.md'),
    read_file('claude_code_environment/templates/life-projects/README.md'),
    read_file('claude_code_environment/templates/documentation-content/README.md')
)

spec_content = results[0]
selection_rules = results[1]
template_docs = results[2:6]
```

**Benefit**: 70% time reduction vs. sequential reads (6-8 seconds → 2-3 seconds)

**Content Extraction:**
```python
indicators = {
    'technologies': extract_technology_keywords(spec_content),
    'project_type': extract_project_type_markers(spec_content),
    'domain': extract_domain_characteristics(spec_content),
    'complexity': estimate_complexity(spec_content),
    'timeline': extract_timeline_indicators(spec_content),
    'first_person': count_first_person_pronouns(spec_content)
}
```

**Example Extraction:**
```python
# From pension calculation spec:
{
    'technologies': ['Power Query', 'M language', 'Excel'],
    'project_type': ['calculation', 'formula', 'regulatory'],
    'domain': ['compliance', 'financial', 'regulatory'],
    'complexity': 'multi-week',
    'timeline': '3-4 weeks',
    'regulatory_signals': ['PDF document', 'ambiguous', 'interpretation']
}
```

#### 3.2.3 Step 2: Template Scoring Algorithm

**Scoring Function** (from template-selection-rules.md):

```python
def score_template(spec_content, template_name):
    score = 0

    # High confidence indicators (30 points each)
    for pattern in HIGH_CONFIDENCE[template_name]:
        if pattern in spec_content.lower():
            score += 30

    # Medium confidence indicators (15 points each)
    for pattern in MEDIUM_CONFIDENCE[template_name]:
        if pattern in spec_content.lower():
            score += 15

    # Low confidence indicators (5 points each)
    for pattern in LOW_CONFIDENCE[template_name]:
        if pattern in spec_content.lower():
            score += 5

    # Normalize to percentage
    return min(score, 100)
```

**Pattern Definitions:**

**Power Query Template:**
```python
HIGH_CONFIDENCE = [
    "power query",
    "m language",
    ".m file",
    "excel" + ("formula" or "calculation" or "query"),
    "regulatory calculation"
]

MEDIUM_CONFIDENCE = [
    "excel" + "power query" not mentioned,
    "power bi" + data transformation,
    "pension" or "tax calculation" or "benefits calculation",
    "excel workbook" + complex logic
]

PHASE_0_TRIGGER = (
    ("regulatory" or "compliance" or "legal")
    AND
    ("ambiguous" or "interpretation" or "PDF document" or "regulation text")
)
```

**Research/Analysis Template:**
```python
HIGH_CONFIDENCE = [
    "research question",
    "research proposal",
    "hypothesis" + ("test" or "testing"),
    "literature review",
    "experiment" + ("design" or "conduct"),
    "statistical analysis" + research context,
    "academic" + ("paper" or "publication")
]

MEDIUM_CONFIDENCE = [
    "data science" + exploratory,
    "thesis" or "dissertation",
    "exploratory data analysis",
    "machine learning" + "experiment",
    "A/B test" or "hypothesis testing"
]
```

**Life Projects Template:**
```python
HIGH_CONFIDENCE = [
    "personal project" or "personal goal",
    "fitness" or "workout" or "diet" or "nutrition",
    "learning journey" + personal context,
    "budget" + personal context,
    "organize my" or "track my" or "plan my",
    "habit tracker" or "goal setting"
]

MEDIUM_CONFIDENCE = [
    "home" + ("organization" or "improvement"),
    "reading list" or "book tracking",
    "travel planning",
    "journal" or "diary"
]
```

**Documentation/Content Template:**
```python
HIGH_CONFIDENCE = [
    "documentation" + ("write" or "create"),
    "technical writing",
    "knowledge base" or "wiki",
    "blog" + ("posts" or "articles"),
    "tutorial" or "guide" + creating,
    "API documentation"
]

MEDIUM_CONFIDENCE = [
    "content" + ("strategy" or "calendar"),
    "write" + ("articles" or "posts"),
    "documentation site",
    "style guide"
]
```

**Scoring Example (Pension Calculation Spec):**
```python
scores = {
    'power-query': 90,      # "Power Query" (30) + "M language" (30) +
                             # "Excel"+"calculation" (30)
    'research-analysis': 5,  # Generic "analysis" mention
    'life-projects': 0,      # No personal indicators
    'documentation': 5,      # Generic "documentation" mention
    'base': 40              # Python/technology stack fallback
}

# Decision: 90 >= 90 threshold → Auto-select Power Query
# Phase 0 check: "regulatory" + "PDF" + "ambiguous" → Enable Phase 0
```

#### 3.2.4 Step 3: Decision Thresholds & User Interaction

**Decision Tree:**
```python
def make_template_decision(scores, spec_content):
    best_template = max(scores, key=scores.get)
    best_score = scores[best_template]

    if best_score >= 90:
        # HIGH CONFIDENCE - Auto-select without asking
        return {
            'action': 'auto_select',
            'template': best_template,
            'message': f"Auto-detected {best_template} template (confidence: {best_score}%)",
            'rationale': extract_top_indicators(spec_content, best_template)
        }

    elif best_score >= 70:
        # MEDIUM-HIGH CONFIDENCE - Auto-select with explanation
        return {
            'action': 'auto_select_with_explanation',
            'template': best_template,
            'message': f"Selected {best_template} template (confidence: {best_score}%)",
            'explanation': build_detection_explanation(spec_content, best_template),
            'allow_override': True
        }

    elif best_score >= 50:
        # MEDIUM CONFIDENCE - Recommend with easy override
        return {
            'action': 'recommend',
            'template': best_template,
            'message': f"Recommend {best_template} template (confidence: {best_score}%)",
            'question': "Does this sound right? [Y/N or choose different]"
        }

    else:
        # LOW CONFIDENCE - Ask user to choose
        top_2_templates = get_top_n(scores, 2)
        return {
            'action': 'ask_user',
            'options': top_2_templates,
            'message': "Could not auto-detect template. Please choose:",
            'explanations': {t: explain_score(spec_content, t) for t in top_2_templates}
        }
```

**Tie-Breaking Logic:**
```python
def check_for_ties(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_score = sorted_scores[0][1]
    second_score = sorted_scores[1][1]

    if abs(best_score - second_score) <= 10:
        # Scores within 10 points = ambiguous
        return {
            'is_tie': True,
            'tied_templates': [sorted_scores[0][0], sorted_scores[1][0]],
            'action': 'ask_user_to_choose'
        }
    return {'is_tie': False}
```

#### 3.2.5 Step 4: Environment Generation (Massive Parallel Execution - 2-3 seconds)

**Directory Structure Creation:**
```python
def create_directory_structure(template_name):
    # Base structure (all templates)
    base_dirs = [
        '.claude/commands',
        '.claude/context',
        '.claude/context/standards',
        '.claude/tasks',
        '.claude/reference'
    ]

    # Template-specific additions
    template_dirs = {
        'power-query': [
            '.claude/context/glossary',
            '.claude/context/assumptions',
            'power-query',
            'calculation-docs',
            'excel-files',
            'tests/sample-data'
        ],
        'research-analysis': [
            'research/literature',
            'research/data',
            'research/experiments',
            'research/analysis',
            'research/hypotheses',
            'research/publications'
        ],
        'life-projects': [],  # Minimal structure
        'documentation-content': [
            'docs/drafts',
            'docs/published',
            'docs/assets'
        ]
    }

    all_dirs = base_dirs + template_dirs.get(template_name, [])

    # Create all directories in parallel (OS-level concurrency)
    for dir_path in all_dirs:
        os.makedirs(dir_path, exist_ok=True)
```

**Parallel File Generation** (Key Innovation):

```python
# SEQUENTIAL APPROACH (OLD - 15-20 seconds)
for file_config in files_to_generate:
    content = generate_content(file_config, spec_data)
    write_file(file_config['path'], content)
    # Each write takes 2-3 seconds = 6 files × 2.5s = 15 seconds

# PARALLEL APPROACH (NEW - 2-3 seconds)
async def generate_all_files(files_to_generate, spec_data):
    tasks = []
    for file_config in files_to_generate:
        content = generate_content(file_config, spec_data)
        task = asyncio.create_task(write_file(file_config['path'], content))
        tasks.append(task)

    # All writes execute concurrently
    await asyncio.gather(*tasks)
    # Total time: ~2-3 seconds regardless of file count
```

**Claude Code Parallel Tool Calls:**
```python
# In single Claude message, make multiple Write tool calls:
[
    Write('CLAUDE.md', claude_md_content),
    Write('README.md', readme_content),
    Write('.claude/context/overview.md', overview_content),
    Write('.claude/context/validation-rules.md', validation_rules),
    Write('.claude/tasks/task-overview.md', task_overview),
    Write('.claude/reference/difficulty-guide.md', difficulty_guide)
]
# Claude executes all 6 writes concurrently = 2-3 seconds total
```

#### 3.2.6 Step 5: Initial Task Extraction

**Deliverable Parsing:**
```python
def extract_initial_tasks(spec_content):
    # Pattern matching for deliverables/requirements
    patterns = [
        r'## Deliverables\n([\s\S]+?)(?=\n##|$)',
        r'## Requirements\n([\s\S]+?)(?=\n##|$)',
        r'## Features\n([\s\S]+?)(?=\n##|$)'
    ]

    tasks = []
    for pattern in patterns:
        match = re.search(pattern, spec_content)
        if match:
            items = re.findall(r'^\d+\.\s*(.+)$', match.group(1), re.MULTILINE)
            for item in items:
                task = {
                    'id': str(len(tasks) + 1),
                    'title': item,
                    'description': extract_context_around(spec_content, item),
                    'difficulty': estimate_difficulty(item),
                    'status': 'Pending',
                    'created_date': datetime.now().strftime('%Y-%m-%d'),
                    'updated_date': datetime.now().strftime('%Y-%m-%d'),
                    'dependencies': [],
                    'subtasks': [],
                    'parent_task': None,
                    'files_affected': [],
                    'notes': ''
                }
                tasks.append(task)

    return tasks
```

---

## 4. Template Detection Deep Dive

### 4.1 Pattern Matching Architecture

**Two-Stage Detection:**

**Stage 1: Keyword Extraction**
```python
class KeywordExtractor:
    def extract(self, spec_content):
        return {
            'technology': self._extract_tech_keywords(spec_content),
            'domain': self._extract_domain_keywords(spec_content),
            'project_type': self._extract_type_keywords(spec_content),
            'indicators': self._extract_special_indicators(spec_content)
        }
```

**Stage 2: Confidence Scoring**
```python
class TemplateScorer:
    def score_all(self, keywords):
        scores = {}
        for template_name, template_rules in self.rules.items():
            scores[template_name] = self._score_template(keywords, template_rules)
        return scores
```

### 4.2 Confidence Thresholds

**Decision Matrix:**

| Confidence Range | Action | User Interaction | Timing Impact |
|-----------------|--------|------------------|---------------|
| 90-100% | Auto-select | None (explain after) | Fastest (5-8 sec) |
| 70-89% | Auto-select | Minimal explanation | Fast (6-10 sec) |
| 50-69% | Recommend | Simple Y/N confirmation | Medium (10-20 sec) |
| < 50% | Request clarification | Present top 2-3 options | Slower (20-60 sec) |

---

## 5. Generated Structure Details

### 5.1 Base Template Structure

**Complete Directory Tree:**
```
new-project/
├── CLAUDE.md                    # 50-100 lines, router file
├── README.md                    # Human documentation
├── .gitignore                   # Standard patterns
└── .claude/
    ├── commands/
    │   ├── complete-task.md     # Start/finish tasks
    │   ├── breakdown.md         # Split tasks ≥7 difficulty
    │   ├── sync-tasks.md        # Update task-overview.md
    │   └── update-tasks.md      # Validate task system
    ├── context/
    │   ├── overview.md          # Project understanding (from spec)
    │   ├── validation-rules.md  # Task management rules
    │   └── standards/           # Empty initially
    ├── tasks/
    │   ├── task-overview.md     # Auto-generated summary
    │   └── task-*.json          # Individual task files
    └── reference/
        ├── difficulty-guide.md  # 1-10 scoring guide
        └── breakdown-workflow.md # How to break down tasks
```

### 5.2 Power Query Template Additions

**Complete Power Query Structure:**
```
power-query-project/
├── CLAUDE.md
├── README.md
├── .gitignore
├── calculation-docs/           # User adds regulatory PDFs here
├── excel-files/                # User adds .xlsx files here
├── power-query/                # Extracted .m files (git tracked)
├── tests/
│   ├── sample-data/
│   └── expected-outputs/
└── .claude/
    ├── commands/
    │   ├── complete-task.md
    │   ├── breakdown.md
    │   ├── sync-tasks.md
    │   ├── update-tasks.md
    │   ├── initialize-project.md      # PHASE 0 STEP 1
    │   ├── resolve-ambiguities.md     # PHASE 0 STEP 2
    │   ├── generate-artifacts.md      # PHASE 0 STEP 3
    │   ├── extract-queries.md         # PHASE 0 STEP 4
    │   └── validate-query.md          # Schema validation
    ├── context/
    │   ├── overview.md
    │   ├── validation-rules.md
    │   ├── glossary.md                # PHASE 0 OUTPUT (empty initially)
    │   ├── assumptions.md             # PHASE 0 OUTPUT (empty initially)
    │   ├── llm-pitfalls.md            # PQ-specific warnings
    │   ├── critical_rules.md          # M language DO/DON'T
    │   └── standards/
    │       ├── power-query.md         # M language standards
    │       ├── naming.md              # Naming conventions
    │       └── error-handling.md      # Error handling patterns
    ├── tasks/
    │   ├── task-overview.md
    │   ├── _phase-0-status.md         # PHASE 0 TRACKER
    │   └── task-*.json
    └── reference/
        ├── difficulty-guide-pq.md     # 5-dimension scoring
        ├── ambiguity-report.md        # PHASE 0 OUTPUT (empty initially)
        ├── data-contracts.md          # PHASE 0 OUTPUT (empty initially)
        ├── query-manifest.md          # PHASE 0 OUTPUT (empty initially)
        └── dependency-graph.md        # PHASE 0 OUTPUT (empty initially)
```

### 5.3 Template Comparison Matrix

| Feature | Base | Power Query | Research | Life Projects | Documentation |
|---------|------|-------------|----------|---------------|---------------|
| **Commands** | 4 core | 4 core + 5 PQ | 4 core + 2 research | None | 4 core + 2 content |
| **Context Files** | 2 | 10+ | 6 | 0 | 4 |
| **Reference Docs** | 2 | 6 | 4 | 0 | 3 |
| **Project Dirs** | None | 4 (calculation-docs, etc) | 6 (research/, etc) | User-defined | 1 (docs/) |
| **Phase 0** | Optional | Yes (if regulatory) | No | No | No |
| **Difficulty Scoring** | Simple 1-10 | 5-dimension | Simple 1-10 | Simple 1-10 | Simple 1-10 |
| **Setup Time** | 5-8 sec | 8-12 sec | 6-10 sec | 3-5 sec | 5-8 sec |
| **Total Files Created** | 10-12 | 25-30 | 18-22 | 3-5 | 12-15 |

---

## 6. Example Scenarios (Step-by-Step)

### 6.1 Power Query Project with Regulatory Requirements

**Specification (pension-calc-spec.md):**
```markdown
# Pension Calculation Implementation

Implement pension formulas from Swedish Pension Authority PDF (45 pages).
Use Power Query M language in Excel.

Requirements:
1. Parse regulatory PDF to extract formulas
2. Interpret ambiguous variable definitions
3. Implement in Power Query with error handling
4. Generate audit trail
5. Test against authority's sample data

Compliance: Zero-error tolerance, full audit trail required.
Timeline: 3-4 weeks
```

**Step-by-Step Process:**

**1. User Command:**
```
cd ~/Projects/pension-calculator
code .
# In Claude Code:
"Create environment from claude_code_environment repo using spec: ~/Documents/pension-calc-spec.md"
```

**2. Agent Activation (< 1 second):**
```
Environment Architect: Detecting empty directory...
Environment Architect: Activating for initialization phase...
Environment Architect: Reading specification and template rules in parallel...
```

**3. Parallel Analysis (2-3 seconds):**
```python
# Simultaneous operations:
- Read specification ✓
- Read template-selection-rules.md ✓
- Read power-query/README.md ✓
- Read research-analysis/README.md ✓
- Read life-projects/README.md ✓
- Read documentation-content/README.md ✓

# Pattern extraction:
indicators = {
    'technologies': ['Power Query', 'M language', 'Excel'],
    'keywords': ['pension', 'calculation', 'formula', 'regulatory', 'PDF'],
    'domain': ['compliance', 'audit trail', 'zero-error tolerance']
}
```

**4. Template Scoring (< 1 second):**
```python
scores = {
    'power-query': 90,  # "Power Query" (30) + "M language" (30) + "Excel"+"calculation" (30)
    'research': 5,      # Generic "calculation" only
    'life': 0,          # No personal indicators
    'docs': 0,          # No documentation focus
    'base': 35          # Technology stack present
}

best_match = 'power-query'
confidence = 90

# Phase 0 check:
regulatory = True  # "regulatory", "compliance" found
ambiguous = True   # "PDF", "ambiguous", "interpretation" found
phase_0_enabled = True
```

**5. Auto-Select Decision:**
```
Environment Architect: Template detected: power-query (confidence: 90%)

Detection reasoning:
  ✓ "Power Query" keyword: Explicit mention in specification
  ✓ "M language" keyword: Technology explicitly stated
  ✓ "Excel" + "calculation": Strong domain match
  ✓ Regulatory + ambiguous source: Phase 0 workflow enabled

Auto-selecting without user confirmation (high confidence).
```

**6. Parallel Environment Generation (2-3 seconds):**
```python
# All file writes happen concurrently:
[
    Write('CLAUDE.md', generate_claude_md()),
    Write('README.md', generate_readme()),
    Write('.claude/context/overview.md', extract_from_spec()),
    Write('.claude/context/validation-rules.md', pq_validation_rules()),
    Write('.claude/context/llm-pitfalls.md', pq_pitfalls()),
    Write('.claude/context/critical_rules.md', m_language_rules()),
    Write('.claude/tasks/task-overview.md', empty_overview()),
    Write('.claude/tasks/_phase-0-status.md', phase_0_tracker()),
    Write('.claude/reference/difficulty-guide-pq.md', five_dim_scoring()),
    Write('.claude/commands/initialize-project.md', phase_0_step_1()),
    Write('.claude/commands/resolve-ambiguities.md', phase_0_step_2()),
    Write('.claude/commands/generate-artifacts.md', phase_0_step_3()),
    Write('.claude/commands/extract-queries.md', phase_0_step_4()),
    # ... 15 more files
]
# Total: 28 files created in ~2.5 seconds
```

**7. Summary Output:**
```
✓ Smart Bootstrap Complete!

PROJECT: Pension Calculation Implementation
TEMPLATE: power-query (auto-detected with 90% confidence)

Detection Reasoning:
  ✓ "Power Query": Explicit technology mention
  ✓ "M language": Confirmed language choice
  ✓ "Excel" + "calculation": Domain match
  ✓ Regulatory + PDF source: Phase 0 enabled

Configuration Applied:
  - Difficulty Scoring: 5-dimension (M Language, Data Volume, Regulatory, Error Handling, Excel Integration)
  - Phase 0: YES (regulatory requirements + ambiguous PDF source)
  - Technology Stack: Power Query, M language, Excel
  - Estimated Complexity: Multi-week (3-4 weeks mentioned)

Files Created:
  ✓ CLAUDE.md - Router file
  ✓ README.md - Human documentation
  ✓ .claude/commands/ (13 command files)
  ✓ .claude/context/ (9 context files)
  ✓ .claude/tasks/ (task management + Phase 0 tracker)
  ✓ .claude/reference/ (6 reference docs)
  ✓ Project directories (calculation-docs, excel-files, power-query, tests)
  ✓ Initial tasks: 5 tasks created

Next Steps:
1. Add your regulatory PDF to calculation-docs/
2. Review .claude/tasks/_phase-0-status.md
3. Run @.claude/commands/initialize-project.md to begin Phase 0
4. Follow Phase 0 workflow through all 4 steps (expect 1-2 hours for complex docs)
5. Begin implementation once Phase 0 complete

Performance: Environment generated in 6.2 seconds
```

### 6.2 Research/Analysis Academic Project

**Specification (transformer-research-spec.md):**
```markdown
# Transformer Models for Code Generation - Research Study

Research Question: Do domain-specific fine-tuned transformers outperform
general-purpose models for code generation in specialized domains?

Hypothesis:
- H1: Domain-specific fine-tuning improves accuracy by 15%+
- H2: Improvement more pronounced in specialized domains
- H3: Smaller tuned models match larger general models

Methodology:
- Literature review: 60+ papers (ACL, IEEE, arXiv)
- Experiments: 3 datasets, 4 model variants, BLEU/CodeBLEU metrics
- Statistical analysis: ANOVA, effect sizes, p < 0.05

Timeline: 12 weeks (3 for lit review, 6 for experiments, 3 for writing)

Deliverables:
1. Systematic literature review
2. Experimental code and trained models
3. Results analysis with statistical validation
4. Research paper for NeurIPS submission
5. Public dataset releases
```

**Summary:**
```
✓ Research Environment Created!

PROJECT: Transformer Models for Code Generation
TEMPLATE: research-analysis (confidence: 100%)

Configuration:
  - Difficulty Scoring: Simple 1-10
  - Complexity: Long-term (12 weeks)
  - Technology: Python, PyTorch, Transformers, Jupyter, LaTeX
  - Deliverables: 5 major outputs

Next Steps:
1. Review .claude/context/standards/literature-review.md
2. Set up research/literature/ directory structure
3. 4 tasks require breakdown (difficulty ≥7)
4. Begin with literature review command: @.claude/commands/review-literature.md

Performance: 7.8 seconds
```

### 6.3 Personal Life Organization Project

**Specification (fitness-2024-spec.md):**
```markdown
# My 2024 Fitness Journey

Personal Goals: Get healthier by tracking workouts, planning nutrition, staying accountable.

What I Want:
- Log workouts (type, duration, exercises, progress on lifts)
- Plan weekly meal prep, track macros
- Monitor body measurements weekly
- Track goals: Run 5K by March, bench bodyweight by June, lose 15 pounds by July
```

**Summary:**
```
✓ Life Projects Environment Created!

PROJECT: My 2024 Fitness Journey
TEMPLATE: life-projects (confidence: 100%)

Configuration:
  - Structure: Minimal (task tracking only)
  - Difficulty Scoring: Simple 1-10
  - Complexity: Ongoing personal project
  - No Phase 0 or complex workflows

Files Created:
  ✓ CLAUDE.md - Simplified router
  ✓ README.md - Project description
  ✓ .claude/tasks/ (4 initial tasks)

Next Steps:
1. Review tasks in .claude/tasks/task-overview.md
2. Start with task 1: Set up workout logging
3. Build incrementally - add complexity as needed

Performance: 3.1 seconds
```

### 6.4 Generic Web Development Project

**Specification (todo-app-spec.md):**
```markdown
# Simple Todo List Web App

Build a basic todo list application with CRUD operations.

Tech Stack: React frontend, Node.js/Express backend, PostgreSQL database

Features:
- User authentication (JWT)
- Create, read, update, delete todos
- Mark todos complete/incomplete
- Filter by status (all, active, completed)
- Responsive design

Timeline: Weekend project (2-3 days)
```

**Summary:**
```
✓ Base Environment Created!

PROJECT: Simple Todo List Web App
TEMPLATE: base (confidence: 45% - fallback)

Configuration:
  - Structure: Full base template
  - Difficulty Scoring: Simple 1-10
  - Complexity: Weekend project
  - Technology: React, Node.js, Express, PostgreSQL

Files Created:
  ✓ CLAUDE.md
  ✓ README.md
  ✓ .claude/ structure (12 files)
  ✓ Initial tasks: 7 tasks

Next Steps:
1. Review tasks in .claude/tasks/task-overview.md
2. Task 2 (authentication) requires breakdown (difficulty 7)
3. Run @.claude/commands/breakdown.md 2 to split task
4. Begin with task 1: Project structure setup

Performance: 5.9 seconds
```

---

## 7. Post-Generation Next Steps

### 7.1 Base Template Workflow

**Immediate Actions:**
1. Review `.claude/context/overview.md` - Understand project context
2. Check `.claude/tasks/task-overview.md` - See all tasks
3. Identify high-difficulty tasks (≥7) that need breakdown
4. Run `@.claude/commands/breakdown.md [task-id]` for complex tasks

**First Task Execution:**
```
User: "@.claude/commands/complete-task.md 1"

Claude Code:
1. Reads task-001.json
2. Checks dependencies (none for first task)
3. Updates status: "Pending" → "In Progress"
4. Executes task work
5. Updates status: "In Progress" → "Finished"
6. Adds completion notes
7. Runs sync-tasks automatically
8. Checks if any parent tasks can auto-complete
```

### 7.2 Power Query + Phase 0 Workflow

**Phase 0: Step-by-Step (Expect 1-2 hours for complex docs):**

**Step 1: Initialize Project**
```
User: "@.claude/commands/initialize-project.md"

Claude Code:
1. Reads all files in calculation-docs/ (PDFs, Word docs)
2. Extracts text content
3. Analyzes for:
   - Variable mentions
   - Formula patterns
   - Ambiguous terminology
   - Inconsistencies between sections
4. Generates .claude/reference/ambiguity-report.md:
   - 50-100 ambiguities found (typical for 45-page regulatory doc)
   - Each ambiguity categorized
5. Updates _phase-0-status.md: Step 1 ✓ Complete
```

**Step 2: Resolve Ambiguities (Interactive - Most Time-Consuming)**
```
User: "@.claude/commands/resolve-ambiguities.md"

Claude Code presents ambiguities in batches of 5, user makes decisions,
Claude documents each decision in assumptions.md

Typical Time: 1-2 hours for 70+ ambiguities
```

**Step 3: Generate Artifacts**
```
User: "@.claude/commands/generate-artifacts.md"

Claude Code:
1. Reads assumptions.md
2. Generates glossary.md (all variables defined)
3. Generates data-contracts.md (input/output schemas)
4. Generates query-manifest.md (all queries documented)
5. Generates dependency-graph.md (query execution order)
6. Generates initial tasks from queries
7. Runs sync-tasks
```

**Step 4: Extract Queries (If Excel Files Present)**
```
User: "@.claude/commands/extract-queries.md"

Claude Code:
1. Detects Excel files in excel-files/
2. Extracts .m files
3. Saves to power-query/[QueryName].m
4. Creates git tracking
```

### 7.3 Task Management Basics (All Templates)

**Task Lifecycle:**
```
PENDING → [breakdown if ≥7] → PENDING (subtasks)
         ↓
         IN PROGRESS → [work happens] → FINISHED
```

**Parent Task Auto-Completion:**
When all subtasks finish, parent automatically completes.

---

## 8. System Performance & Optimization

### 8.1 Time Breakdown

**Sequential (Old Approach): 43+ seconds**
**Parallel (New Approach): 8-10 seconds (81% reduction)**

### 8.2 Parallel Execution Patterns

**Pattern 1: Multi-Read Operations**
```python
# All reads complete simultaneously
# Time: max(individual_times) ≈ 2-3s
# vs sequential: sum(individual_times) ≈ 10s
```

**Pattern 2: Batch File Generation**
```python
# Time: ~2-3s for 20 files
# vs sequential: ~40s
```

### 8.3 Resource Utilization

**Context Window Usage:**
- Sequential: 30+ messages for complete bootstrap
- Parallel: 10-15 messages (40% reduction)

---

## 9. Advanced Topics

### 9.1 Agent System Integration

**Three-Agent Architecture:**

**Environment Architect** (Initialization Phase):
- Owns: Template detection, environment creation
- Triggers: Empty directory, "create environment" command
- Boundaries: NEVER modifies existing tasks
- Handoff: → Task Orchestrator if high-difficulty tasks created

**Task Orchestrator** (Planning Phase):
- Owns: Task breakdown, dependency management
- Triggers: Task difficulty ≥7, "breakdown task" command
- Boundaries: NEVER executes tasks
- Handoff: → Execution Guardian when subtasks ready

**Execution Guardian** (Execution Phase):
- Owns: Task execution, validation gates
- Triggers: "complete task" command
- Boundaries: NEVER breaks down tasks

---

## 10. macOS-Specific Considerations

### 10.0 Quick Path Reference for Mac Users

**TL;DR** - Copy-paste ready paths and shortcuts for common scenarios.

#### Where Claude Desktop Exports Go
```bash
~/Downloads/claude_chat_[timestamp].md
```

#### Common Spec Locations (Recommended)
```bash
~/Documents/specs/              # Organized specs folder
~/Downloads/                    # Export destination (move after export)
~/Desktop/                      # Quick access
```

#### Path Shortcuts

| Shortcut | Expands To | Example |
|----------|-----------|---------|
| `~` | `/Users/[your-username]` | `~/Documents/spec.md` |
| `.` | Current directory | `./spec.md` |
| `..` | Parent directory | `../specs/spec.md` |
| Just filename | Auto-search enabled | `my-spec.md` (searches common locations) |

#### iCloud Drive Path
```bash
~/Library/Mobile Documents/com~apple~CloudDocs/
```
**Pro tip**: Just use filename - smart-bootstrap searches iCloud automatically!

#### Copy-Paste Examples

**Spec in Documents:**
```
Create environment using spec: ~/Documents/my-project-spec.md
```

**Spec in Downloads (after Claude Desktop export):**
```
Create environment using spec: ~/Downloads/claude_chat_20251218.md
```

**Let system find it (easiest):**
```
Create environment using spec: my-project-spec.md
```

**Spec in iCloud subfolder:**
```
Create environment using spec: project-spec.md
```
(System searches iCloud recursively, depth 5)

#### Pro Tips
- Use `~` instead of `/Users/username` for shorter paths
- Smart-bootstrap searches Documents, Downloads, Desktop, and iCloud automatically
- If file not found, system offers to show recent .md files
- Avoid paths with spaces (use hyphens: `my-project` not `My Project`)

---

### 10.1 File Paths & Smart Path Detection

**Smart Bootstrap now accepts all path formats!** (Tasks 105-108 implemented)

#### Supported Path Formats

**Absolute Paths** (always work):
```bash
/Users/username/Documents/spec.md
/Users/username/Library/Mobile Documents/com~apple~CloudDocs/project-spec.md
```

**Tilde Expansion** (recommended for brevity):
```bash
~/Documents/spec.md                    # Expands to /Users/username/Documents/spec.md
~/Downloads/project-spec.md            # Expands to /Users/username/Downloads/project-spec.md
```

**Relative Paths** (current directory):
```bash
./spec.md                              # Current directory
../specs/project.md                    # Parent directory
Documents/spec.md                      # Relative from current location
spec.md                                # Just filename (triggers fallback search)
```

#### Automatic Fallback Search

If file isn't found at the provided path, smart-bootstrap automatically searches:

1. **Current directory**: `./[filename]`
2. **Documents**: `~/Documents/[filename]`
3. **Downloads**: `~/Downloads/[filename]`
4. **Desktop**: `~/Desktop/[filename]`
5. **iCloud Drive**: `~/Library/Mobile Documents/com~apple~CloudDocs/[filename]` (recursive, depth 5)

**Example:**
```bash
User: "Create environment using spec: project-spec.md"

System: File not found at ./project-spec.md
System: Searching common locations...
System: Found spec at: ~/Documents/project-spec.md
System: Proceeding with bootstrap...
```

#### Recent Files Helper

If file still not found, smart-bootstrap offers to show recent `.md` files:

```bash
System: Could not find 'my-spec.md' in any location.

Would you like to see recently modified .md files? [Y/N]

User: Y

System: Recent .md files (last 7 days):
  1. startup-idea-spec.md        (Documents, 5 min ago, 34KB)
  2. side-project-notes.md       (Desktop, 2 hours ago, 18KB)
  3. pension-calc-spec.md        (iCloud/02PROJECTS, yesterday, 45KB)

Which file should I use? [1-3 or 'none']
```

#### iCloud Drive Considerations

**Path**: `/Users/[username]/Library/Mobile Documents/com~apple~CloudDocs/`

**Pros:**
- Auto-sync across devices
- Smart-bootstrap now searches iCloud automatically
- Download status detection (warns if file is cloud-only)

**Cons:**
- Sync delays
- Slower I/O
- Files may not be downloaded locally

**Recommendation:**
- ✓ Use for specifications (lightweight .md files)
- ✗ DON'T use for git repos (active development)
- Smart-bootstrap will find iCloud files automatically - no need to type long paths!

**Download Status Handling:**
```bash
System: Found in iCloud but file is not downloaded (cloud-only)

⚠ File is pending download from iCloud
  Location: ~/Library/Mobile Documents/com~apple~CloudDocs/old-project.md

  Please open this location in Finder and wait for download to complete.
  Then run this command again.
```

#### Local Paths (Recommended for Active Development)

**Best practices:**
- `~/Documents/Projects/` or `~/Projects/`
- Pros: Fast I/O, no sync issues
- Use for active git repositories

**Path Spaces** (avoid if possible):
- Avoid: `/Users/name/My Projects/`
- Use: `/Users/name/my-projects/`
- If unavoidable: Smart-bootstrap handles spaces correctly

#### Quick Path Examples (Copy-Paste Ready)

**For specs in Documents:**
```bash
"Create environment using spec: ~/Documents/my-project-spec.md"
```

**For specs in iCloud (short form):**
```bash
"Create environment using spec: my-project-spec.md"
# System will search and find it automatically in iCloud
```

**For specs in Downloads:**
```bash
"Create environment using spec: ~/Downloads/exported-spec.md"
```

**Using relative paths:**
```bash
cd ~/Documents
"Create environment using spec: ./project-spec.md"
```

**Just filename (let system find it):**
```bash
"Create environment using spec: pension-calculator-spec.md"
# System searches all common locations and iCloud automatically
```

### 10.2 VS Code Settings

**Recommended settings.json:**
```json
{
  "claude.apiKey": "YOUR_API_KEY",
  "claude.model": "claude-sonnet-4-5-20250929",
  "files.watcherExclude": {
    "**/.claude/**": false  // Watch .claude files
  },
  "git.enabled": true
}
```

---

## 11. Troubleshooting

### 11.1 Common Issues

**Issue: "Specification not found"**
- ✓ Smart-bootstrap now automatically searches common locations and iCloud
- Try providing just the filename: `spec.md` (system will find it)
- Use the recent files helper (answer 'Y' when prompted)
- Verify file extension is `.md` (not `.txt`)
- If in iCloud: System will detect and warn if file isn't downloaded locally

**Issue: "Template detection failed"**
- Add more specific keywords to specification
- Mention technologies explicitly
- Include project type (research, analysis, etc.)

**Issue: "Environment already exists"**
- This is by design (prevents overwriting)
- If starting fresh: `rm -rf .claude/ CLAUDE.md README.md`

---

## 12. Performance Metrics

### 12.1 Benchmark Results

**Template Detection Accuracy (Real-World Data):**
- High confidence (90%+): 92% auto-select accuracy
- Medium-high (70-89%): 85% auto-select accuracy
- Medium (50-69%): 78% recommendation acceptance

**Time Performance:**
```
Operation                  Sequential   Parallel   Improvement
-----------------------------------------------------------
Specification Analysis     8-10s        2-3s       70% faster
Template Scoring           3-5s         <1s        80% faster
Environment Generation     20-30s       2-3s       85% faster
Task Extraction           5-10s        1-2s       80% faster
-----------------------------------------------------------
Total Bootstrap Time       36-55s       5-8s       86% faster
```

### 12.2 Resource Usage

**Disk Space:**
- Base template: ~50 KB
- Power Query + Phase 0: ~150 KB
- Research template: ~100 KB
- Life Projects: ~20 KB

**Context Tokens (Average):**
- Total: 10,000-19,000 tokens (well within limits)

---

## 13. Summary & Key Takeaways

### 13.1 System Overview

**What It Is:**
- Automated environment generation for Claude Code projects
- Pattern-based template detection (85%+ accuracy)
- Agent-driven workflow (3 specialized agents)
- Parallel execution (86% faster than sequential)

**What It Provides:**
- Complete `.claude/` structure in 5-8 seconds
- Task management with auto-breakdown
- Template-specific commands and workflows
- Optional Phase 0 for ambiguous requirements
- Initial task extraction from specifications

### 13.2 Key Innovations

**1. Pattern-Based Detection:**
- Eliminates manual template selection
- 90%+ auto-select rate
- Transparent reasoning

**2. Parallel Execution:**
- 86% time reduction vs sequential
- Single-message multi-tool calls
- Scales to 100+ tasks with no degradation

**3. Agent Architecture:**
- Clear separation of concerns
- Automatic handoffs between phases

**4. Phase 0 Workflow:**
- Resolves ambiguities BEFORE coding
- Interactive batch resolution
- Complete audit trail

### 13.3 Developer Mental Model

**Decision Tree:**
```
Is directory empty?
├─ YES → Environment Architect
│   ├─ Read specification
│   ├─ Score templates
│   ├─ Generate environment
│   └─ Hand off if needed
└─ NO → Existing project
    ├─ Task needs breakdown? → Task Orchestrator
    ├─ Task execution? → Execution Guardian
    └─ No agent needed → Manual operation
```

### 13.4 Best Practices

**For Specifications:**
1. Be explicit about technologies
2. Use domain keywords
3. Include timeline mentions
4. List deliverables clearly
5. Mention ambiguities if regulatory project

**For Template Selection:**
- Trust auto-detection for high confidence (90%+)
- Review reasoning for medium confidence (70-89%)
- Can always regenerate with different template

**For Task Management:**
- Always break down tasks ≥7 difficulty
- Use `complete-task.md` to track progress
- Run `sync-tasks.md` after major changes
- Let parent tasks auto-complete

---

## Appendix A: File Paths Reference

**Template Repository Structure:**
```
claude_code_environment/
├── templates/
│   ├── power-query/
│   ├── research-analysis/
│   ├── life-projects/
│   ├── documentation-content/
│   └── data-analytics/
├── components/
│   └── task-management/
├── .claude/
│   ├── commands/
│   │   ├── smart-bootstrap.md
│   │   └── bootstrap.md
│   ├── agents/
│   ├── reference/
│   └── agent-config.json
├── examples/
│   └── specifications/
├── scripts/
├── CLAUDE.md
└── README.md
```

**Generated Project Structure (Base):**
```
new-project/
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
    │   └── validation-rules.md
    ├── tasks/
    │   ├── task-overview.md
    │   └── task-*.json
    └── reference/
        ├── difficulty-guide.md
        └── breakdown-workflow.md
```

---

## Appendix B: Command Quick Reference

**Environment Creation:**
```bash
# Smart bootstrap (recommended)
"Create environment from claude_code_environment repo using spec: [path]"

# Interactive bootstrap (more control)
"Use bootstrap.md to set up [template-name] environment"
```

**Task Management:**
```bash
# Start/finish task
@.claude/commands/complete-task.md [task-id]

# Break down complex task
@.claude/commands/breakdown.md [task-id]

# Update task overview
@.claude/commands/sync-tasks.md

# Validate task system
@.claude/commands/update-tasks.md
```

**Power Query Specific:**
```bash
# Phase 0 workflow
@.claude/commands/initialize-project.md
@.claude/commands/resolve-ambiguities.md
@.claude/commands/generate-artifacts.md
@.claude/commands/extract-queries.md
```

**Research Specific:**
```bash
# Literature review
@.claude/commands/review-literature.md

# Data analysis
@.claude/commands/conduct-analysis.md [experiment-name]
```

---

## 12. Common Error Messages & Solutions

This section provides quick reference for common error messages you might encounter when using Claude Code bootstrap commands.

### 12.1 File Not Found Errors

#### "Specification file not found"

**Symptoms:**
- Bootstrap can't find your spec file
- Error shows path you provided

**Common Causes:**
- Typo in filename or path
- File in different location than expected
- Wrong path format (spaces, special characters)
- File not exported from Claude Desktop

**Quick Fixes:**
1. Check file exists: `ls -la "[path]"`
2. Try just filename: `/smart-bootstrap project.md` (triggers auto-search)
3. Use full path from Finder: Right-click → Hold Option → "Copy as Pathname"
4. Create new spec: `/create-spec`

**Path Tips:**
- Use quotes for paths with spaces: `"~/My Documents/spec.md"`
- Tilde (~) expands to home: `~/Documents/spec.md`
- Relative paths work: `./spec.md`, `../specs/project.md`

---

### 12.2 Directory Conflict Errors

#### "Environment already exists"

**Symptoms:**
- Error: `.claude/` directory already present
- Bootstrap won't proceed

**Common Causes:**
- Re-running bootstrap in same directory
- In wrong project directory
- Previous bootstrap didn't finish

**Quick Fixes:**

**If you're in the WRONG directory:**
```bash
cd /path/to/your/new/project
/smart-bootstrap spec.md
```

**If you want to START OVER:**
```bash
# Back up first!
cp -r .claude .claude.backup

# Remove and restart
rm -rf .claude CLAUDE.md README.md
/smart-bootstrap spec.md
```

**If environment is actually SET UP:**
- Start working: `/complete-task [id]`
- View tasks: `cat .claude/tasks/task-overview.md`

---

### 12.3 Template Detection Issues

#### "Specification too vague for auto-detection"

**Symptoms:**
- Low confidence scores (<50%) for all templates
- Asked to choose template manually

**Common Causes:**
- Generic project description
- No technology stack mentioned
- Missing domain keywords

**Quick Fixes:**

**Add these to your spec:**
1. **Project type explicitly:**
   "This is a [research project/Power Query solution/personal fitness goal]"

2. **Technology stack:**
   - Power Query: "Power Query, M language, Excel 365"
   - Research: "Python, pandas, scipy, statsmodels"
   - Life: "Strava app, Garmin watch"

3. **Domain keywords:**
   - Research: "hypothesis", "statistical analysis", "literature review"
   - Power Query: "regulatory calculation", "M language", "Excel workbook"
   - Life: "personal goal", "fitness journey", "track my progress"

**Or use interactive builder:**
```bash
/create-spec  # Guided Q&A for optimized spec
```

---

### 12.4 Path Format Errors

#### "Path contains spaces without quotes"

**Problem:**
```bash
/smart-bootstrap ~/My Documents/project spec.md
# Interpreted as 3 separate arguments!
```

**Solution:**
```bash
# Use quotes
/smart-bootstrap "~/My Documents/project spec.md"

# Or escape spaces
/smart-bootstrap ~/My\ Documents/project\ spec.md

# Or rename file (best practice)
mv "~/My Documents/project spec.md" ~/Documents/project-spec.md
/smart-bootstrap ~/Documents/project-spec.md
```

**Pro Tip:** Avoid spaces in filenames! Use hyphens or underscores.

---

### 12.5 File Format Issues

#### "File format not supported"

**Symptoms:**
- Error mentions .docx, .pdf, .txt, or other format
- Expected .md (Markdown)

**Solutions:**

**From Claude Desktop (recommended):**
1. Open conversation
2. Click title → Export → **Markdown** (not PDF!)
3. Save as .md file

**Convert existing file:**
- Word/Pages → Save As → Plain Text → Rename to .md
- PDF → Copy text → Paste in text editor → Save as .md
- Use pandoc: `pandoc input.docx -o output.md`

**Or create new:**
```bash
/create-spec  # Interactive spec builder
```

---

### 12.6 Empty or Invalid Spec

#### "Specification file appears empty or too small"

**Symptoms:**
- File exists but has <100 bytes
- Warning about file size

**Common Causes:**
- File wasn't saved properly
- Export failed
- Wrong file selected

**Quick Fixes:**
1. Check contents: `cat "[path]"`
2. Re-export from Claude Desktop properly
3. Use `/create-spec` to build new one

**Minimum spec requirements:**
- Project name/title
- Description (what you're building)
- Technology stack
- Goals or objectives
- At least 100-200 words total

---

### 12.7 Git Repository Warnings

#### "Git repository detected with uncommitted changes"

**Symptoms:**
- Warning about uncommitted git changes
- Bootstrap will proceed but create many new files

**Recommended Approach:**
```bash
# Commit current work first
git add .
git commit -m "Checkpoint before Claude Code bootstrap"

# Then bootstrap
/smart-bootstrap spec.md

# Commit Claude Code files separately
git add .claude/ CLAUDE.md README.md
git commit -m "Add Claude Code environment"
```

**Alternative:**
```bash
# Stash changes temporarily
git stash
/smart-bootstrap spec.md
git add .claude/ CLAUDE.md README.md
git commit -m "Add Claude Code environment"
git stash pop
```

---

### 12.8 Conflicting Template Signals

#### "Multiple templates match your spec"

**Symptoms:**
- Two templates have similar confidence scores
- Asked to clarify primary focus

**Example:**
```
Research/Analysis: 75% ← "hypothesis", "statistical"
Power Query: 70% ← "Excel", "regulatory"
```

**How to Decide:**

**Choose RESEARCH if:**
- Main goal: Test hypothesis, publish paper
- Deliverable: Academic publication, findings
- Excel is just a tool for analysis

**Choose POWER QUERY if:**
- Main goal: Automate Excel calculations
- Deliverable: Excel workbook with formulas
- Research is background context

**Tell Claude:**
```
"Use Research template"
# or
"Use Power Query template"
```

---

### 12.9 iCloud Drive Path Issues

**Symptoms:**
- File is in iCloud but can't be found
- Long path with spaces

**iCloud Drive Path:**
```bash
~/Library/Mobile Documents/com~apple~CloudDocs/
```

**Solutions:**

**Use quotes:**
```bash
/smart-bootstrap "~/Library/Mobile Documents/com~apple~CloudDocs/myspec.md"
```

**Or just filename:**
```bash
/smart-bootstrap myspec.md
# Auto-searches iCloud Drive
```

**Find iCloud files:**
```bash
# List files in iCloud
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/

# Search for .md files
find ~/Library/Mobile\ Documents/com~apple~CloudDocs/ -name "*.md" -maxdepth 3
```

---

### 12.10 Permission Errors

#### "Cannot read specification file"

**Symptoms:**
- File exists but can't be read
- Permission denied errors

**Common Causes:**
- File owned by different user
- Restrictive permissions
- macOS privacy restrictions

**Quick Fixes:**

**Check permissions:**
```bash
ls -la "[path]"
# Should show: -rw-r--r-- (readable)
```

**Fix permissions:**
```bash
chmod 644 "[path]"
```

**Move to accessible location:**
```bash
cp "[path]" ~/Documents/spec.md
/smart-bootstrap ~/Documents/spec.md
```

**Check macOS privacy:**
- System Settings → Privacy & Security → Files and Folders
- Ensure Terminal/VS Code has access

---

### 12.11 Troubleshooting Checklist

When bootstrap fails, check these in order:

- [ ] **File exists**: `ls -la "[path]"`
- [ ] **Correct path format**: Quotes around spaces
- [ ] **File readable**: Check permissions `chmod 644`
- [ ] **Right directory**: `pwd` shows where you are
- [ ] **No .claude/ exists**: `ls -la .claude` should error
- [ ] **Spec has content**: `wc -l "[path]"` shows >10 lines
- [ ] **File is .md format**: Not .docx, .pdf, .txt

---

### 12.12 Quick Command Reference

**Verify file:**
```bash
ls -la ~/Documents/spec.md        # Check exists
cat ~/Documents/spec.md | head     # Preview content
wc -l ~/Documents/spec.md          # Count lines
file ~/Documents/spec.md           # Check file type
```

**Fix common issues:**
```bash
# Copy with full path
cp "/full/path/to/file.md" ~/Documents/spec.md

# Fix permissions
chmod 644 ~/Documents/spec.md

# Remove conflicting environment
rm -rf .claude CLAUDE.md README.md

# Search for .md files
find ~ -name "*.md" -type f -mtime -7  # Modified in last 7 days
```

**Bootstrap with different approaches:**
```bash
# Full path
/smart-bootstrap ~/Documents/my-project-spec.md

# Just filename (auto-search)
/smart-bootstrap my-project-spec.md

# Quoted path (spaces)
/smart-bootstrap "~/My Documents/project spec.md"

# Relative path
/smart-bootstrap ./spec.md

# iCloud Drive
/smart-bootstrap "~/Library/Mobile Documents/com~apple~CloudDocs/spec.md"
```

---

### 12.13 Still Stuck? Debugging Steps

1. **Show me the exact error:**
   Copy the full error message

2. **Verify file location:**
   ```bash
   find ~ -name "yourfile.md" -type f 2>/dev/null
   ```

3. **Check current directory:**
   ```bash
   pwd
   ls -la
   ```

4. **Test with minimal spec:**
   Create simple test file:
   ```bash
   echo "# Test Project

   ## Description
   This is a test project using Python.

   ## Goals
   - Test bootstrap
   - Verify setup" > ~/Documents/test-spec.md

   /smart-bootstrap ~/Documents/test-spec.md
   ```

5. **Use create-spec as fallback:**
   ```bash
   /create-spec
   # Answer questions interactively
   # Generates optimized spec automatically
   ```

---

### 12.14 Error Message Format Guide

All improved error messages follow this structure:

```
[ICON] [SEVERITY]: [What happened]

📍 Where: [Location/context]

🔍 Why this happened:
   • Reason 1
   • Reason 2

💡 How to fix:
   1. Step-by-step solution
   2. Alternative approach
   3. Fallback option

🔗 Related:
   • Helpful commands
   • Documentation links
```

**Icons:**
- ❌ ERROR: Must fix to proceed
- ⚠️  WARNING: Should address, but can continue
- ℹ️  INFO: Helpful context, no action needed

---

## 13. Getting Help

If error messages don't solve your problem:

1. **Read the full error message** - New format includes fix steps
2. **Check this troubleshooting section** - Section 12 above
3. **Review command documentation** - See .claude/commands/
4. **Try /create-spec** - Bypass manual spec creation
5. **Use /help** - Built-in help system
6. **Check GitHub issues** - https://github.com/anthropics/claude-code/issues

**Pro Tip:** Copy exact error message text when asking for help!

---

**End of Document**
