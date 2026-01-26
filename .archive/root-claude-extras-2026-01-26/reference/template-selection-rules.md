# Template Selection Rules - Auto-Detection Patterns

## Purpose

This document defines the pattern matching rules used by `smart-bootstrap.md` to automatically detect the appropriate template for a project based on its specification document.

## Scoring System

Each template receives a **confidence score (0-100)** based on keyword matches and pattern detection.

**Decision Thresholds**:
- **90-100**: High confidence - Auto-select without asking
- **70-89**: Medium-high confidence - Auto-select but explain reasoning
- **50-69**: Medium confidence - Present as recommendation, allow easy override
- **Below 50**: Low confidence - Ask user to choose from top 2-3 options

**Tie-breaking**: If multiple templates score within 10 points, ask user to choose.

## Educational Feedback (Enhanced Reporting)

When reporting template detection results, use **educational feedback mode** to help users understand the pattern matching system and learn to write better specifications.

### Visual Confidence Bars

Show template scores as visual bar charts for quick comparison:

```
Research Template:    ████████████████████ 92% ✓ SELECTED
Base Template:        ████████░░░░░░░░░░░░ 45%
Power Query:          ████░░░░░░░░░░░░░░░░ 20%
Life Projects:        ██░░░░░░░░░░░░░░░░░░ 10%
Documentation:        █░░░░░░░░░░░░░░░░░░░ 5%
```

**Format**: 20 blocks total, filled proportionally to percentage
- Filled blocks: █ (represents achieved confidence)
- Empty blocks: ░ (represents remaining confidence)
- Winner marker: ✓ SELECTED

### Scoring Breakdown (Why This Template Won)

For the winning template, show:
1. **Each keyword match** with point value
2. **Where found** in spec (exact quote or section)
3. **Why it matters** (educational explanation)

**Example**:
```
✓ "research question" (HIGH signal, +30pts)
  Found in: "Research question: How does remote work..."
  Why it matters: Strong academic research indicator

✓ "hypothesis" (HIGH signal, +30pts)
  Found in: "Primary hypothesis: Remote workers will show..."
  Why it matters: Confirms scientific methodology
```

### Missing Keyword Education

Show what keywords were NOT found but would have changed the outcome:

```
× "Power Query" (not found)
  Would have added: +30pts to Power Query template
  How to trigger: Mention "Power Query", "M language", or "Excel queries"

× "personal project" (not found)
  Would have added: +30pts to Life Projects template
  How to trigger: Use "personal goal", "fitness", "learning journey"
```

### Other Templates Comparison

For each non-selected template, explain:
- What points it scored and why
- What it was missing (specific keywords)
- Why it wasn't selected
- **When to use** this template (educational)

**Example**:
```
Power Query Template (20%):
  • "Excel" mentioned once in passing (+5pts)
  • "data" keyword (+5pts × 2)
  • Missing: No "Power Query", "M language", "regulatory" keywords
  • Why not selected: No specialized calculation/Excel focus
  • When to use: Excel + regulatory calculations + Power Query
```

### Spec Quality Feedback

Provide feedback on how well-written the spec was for detection:

**For high-confidence specs (90%+)**:
```
Your spec was EXCELLENT for detection! Here's why:

✓ Clear domain terminology ("research question", "hypothesis")
✓ Specific methodology section
✓ Domain-specific workflows mentioned (literature review)
✓ Technology stack clear (statistical tools)
```

**For medium-confidence specs (50-89%)**:
```
Your spec had some good signals but could be improved:

✓ Technology mentioned (Python, SQL)
✗ Domain unclear - research? engineering? general?
✗ No workflow indicators

To improve:
• Add domain-specific terms (hypothesis, regulatory, personal goal)
• Mention specific workflows (Phase 0, literature review, etc.)
• Include more context about project type
```

**For low-confidence specs (<50%)**:
```
Your spec needs more detail for automatic detection:

✗ Very generic terms ("project", "data", "analysis")
✗ No technology stack mentioned
✗ No clear domain indicators

To improve:
• Be specific about technologies (Excel, Python, Power Query)
• Use domain terminology (research question, regulatory, personal)
• Mention key workflows or methodologies
• Include project type in description
```

### Tips for Better Specs

Always include actionable tips for future specifications:

```
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
```

### Optional Flags for User Control

**--explain flag** (maximum detail):
- Full scoring breakdown for all templates
- Every keyword match with line numbers in spec
- Alternative interpretations considered
- Assumption validation process
- Pattern matching rule references
- Decision rationale with full context

**--quiet flag** (minimal output):
- Template selected + confidence %
- Top 3 reasons why
- Immediate next step only

**Default mode** (educational, balanced):
- Visual confidence bars
- Winning template explanation
- Other templates summary
- Spec quality feedback
- Tips for improvement

## Template Detection Patterns

### Power Query Template

**High Confidence Indicators** (30 points each):
- Contains "Power Query" (case insensitive)
- Contains "M language" or ".m file"
- Contains "Excel" AND ("formula" OR "calculation" OR "query")
- Contains "regulatory calculation" or "compliance calculation"

**Medium Confidence Indicators** (15 points each):
- Contains "Excel" AND "Power Query" not mentioned (possible implicit)
- Contains "Power BI" with data transformation focus
- Contains regulatory domain keywords: "pension", "tax calculation", "benefits calculation"
- Mentions "Excel workbook" with complex logic

**Low Confidence Indicators** (5 points each):
- Contains "Excel" (alone)
- Contains "spreadsheet" with calculations
- Contains "formula" or "calculation" (without other context)

**Phase 0 Trigger** (adds Phase 0 workflow if Power Query selected):
- Contains "regulatory" OR "compliance" OR "legal requirement"
- AND contains: "ambiguous" OR "interpretation" OR "unclear" OR "PDF document" OR "regulation text"

**Example Patterns**:
```
"Implement pension calculation formulas from regulatory PDF using Power Query"
→ Score: 60+ (Power Query + regulatory + calculation)
→ Template: Power Query with Phase 0

"Create Excel queries to transform sales data"
→ Score: 45 (Excel + query + transform)
→ Ask user: Power Query or general template?
```

---

### Research/Analysis Template

**High Confidence Indicators** (30 points each):
- Contains "research question" OR "research proposal"
- Contains "hypothesis" AND ("test" OR "testing" OR "validation")
- Contains "literature review" OR "systematic review"
- Contains "experiment" AND ("design" OR "conduct" OR "protocol")
- Contains "statistical analysis" AND research context
- Contains "academic" AND ("paper" OR "publication" OR "study")

**Medium Confidence Indicators** (15 points each):
- Contains "data science" with exploratory focus
- Contains "thesis" OR "dissertation"
- Contains "exploratory data analysis" OR "EDA"
- Contains "machine learning" AND "experiment"
- Contains "A/B test" OR "hypothesis testing"
- Contains "survey" OR "questionnaire" AND analysis

**Low Confidence Indicators** (5 points each):
- Contains "research" (general context)
- Contains "analysis" (without other context)
- Contains "data" AND "analyze"

**Example Patterns**:
```
"Research question: Do transformer models improve accuracy?
Hypothesis testing with literature review of 50+ papers."
→ Score: 90+ (research question + hypothesis + literature review)
→ Template: Research/Analysis (auto-select)

"Analyze sales data to find trends"
→ Score: 10 (generic analysis)
→ Ask user or default to base template
```

---

### Life Projects Template

**High Confidence Indicators** (30 points each):
- Contains "personal project" OR "personal goal"
- Contains personal activity keywords: "fitness", "workout", "diet", "nutrition", "meal plan"
- Contains "learning journey" OR "skill development" (personal context)
- Contains "budget" OR "finance tracker" (personal context)
- Contains "organize my" OR "track my" OR "plan my" (first person personal)
- Contains "habit tracker" OR "goal setting"

**Medium Confidence Indicators** (15 points each):
- Contains "home" AND ("organization" OR "improvement" OR "renovation")
- Contains "reading list" OR "book tracking"
- Contains "travel planning" OR "trip planning"
- Contains "journal" OR "diary"
- First-person language with personal activities (not business)

**Low Confidence Indicators** (5 points each):
- Contains "organize" OR "plan" (without personal context)
- Contains personal pronouns ("I", "my", "me") frequently

**Example Patterns**:
```
"Track my fitness goals, meal plans, and workout progress for 2024"
→ Score: 90+ (personal goal + fitness + first person)
→ Template: Life Projects (auto-select)

"I want to organize my data"
→ Score: 10 (ambiguous - could be work or personal)
→ Ask user or need more context
```

---

### Documentation/Content Template

**High Confidence Indicators** (30 points each):
- Contains "documentation" AND ("write" OR "create" OR "generate")
- Contains "technical writing" OR "content creation"
- Contains "knowledge base" OR "wiki"
- Contains "blog" AND ("posts" OR "articles")
- Contains "tutorial" OR "guide" AND creating them (not following)
- Contains "API documentation" OR "developer docs"

**Medium Confidence Indicators** (15 points each):
- Contains "content" AND ("strategy" OR "calendar" OR "planning")
- Contains "write" AND ("articles" OR "posts" OR "documentation")
- Contains "documentation site" OR "docs site"
- Contains "style guide" OR "writing standards"
- Contains "Markdown" OR "reStructuredText" with documentation focus

**Low Confidence Indicators** (5 points each):
- Contains "documentation" (general mention)
- Contains "write" (without specific content type)

**Example Patterns**:
```
"Create technical documentation for API with tutorials and guides"
→ Score: 90+ (technical writing + API docs + tutorial)
→ Template: Documentation/Content (auto-select)

"Document the project"
→ Score: 5 (too generic)
→ Likely not documentation-focused project
```

---

### Base Template (Fallback)

The **Base Template** is the default when:
- No template scores above 50
- Specification is too generic
- Multiple templates tie without clear winner
- User explicitly requests "general" or "standard" template

**Use Base Template for**:
- Web development projects (frontend, backend, full-stack)
- Mobile app development
- General software engineering
- DevOps/infrastructure projects (unless specialized template exists)
- API development
- Database projects
- Projects that don't fit other specialized templates

**Indicators for Base Template** (don't score, just confirm):
- Contains technology names: React, Vue, Angular, Node.js, Django, Flask, Java, C++, etc.
- Contains "web application" OR "mobile app" OR "API" OR "microservice"
- Contains "backend" OR "frontend" OR "full-stack"
- Contains "database" OR "SQL" OR "NoSQL"

---

## Configuration Detection

Beyond template selection, detect these configuration needs:

### Phase 0 Workflow

**Enable Phase 0 if ALL conditions met**:
1. Template is Power Query, Research/Analysis, or Base with regulatory context
2. Contains "regulatory" OR "compliance" OR "legal" OR "government requirement"
3. Contains ambiguity indicators:
   - "PDF document" OR "regulation text" OR "legal document"
   - "interpretation" OR "ambiguous" OR "unclear" OR "vague"
   - "multiple interpretations" OR "conflicting" OR "inconsistent"

**Example**:
```
"Implement calculations from ambiguous regulatory PDF"
→ Phase 0: YES (regulatory + ambiguous + PDF)
```

### Multi-Dimension Difficulty Scoring

**Suggest multi-dimension scoring if**:
- Specification mentions specialized domain: medical, financial trading, aerospace, etc.
- Mentions "complex" with domain-specific challenges
- User explicitly asks for detailed difficulty tracking

**Default**: Simple 1-10 scoring (works for 95% of projects)

### Complexity Level Estimation

**Timeline-based estimation**:
- **Weekend project**: "weekend", "quick", "simple", "few hours", < 5 deliverables
- **Multi-week project**: "few weeks", "month", "several features", 5-20 deliverables
- **Long-term project**: "multi-month", "quarter", "ongoing", 20+ deliverables

**Team size detection**:
- **Solo**: "I", "me", "my", "solo", or no team mentions
- **Small team**: "we", "team of 2-3", "pair"
- **Large team**: "team of 4+", "department", "multiple teams"

### Technology Stack Extraction

**Extract from specification**:
- Language names: Python, JavaScript, TypeScript, Java, C++, Go, Rust, etc.
- Frameworks: React, Vue, Angular, Django, Flask, Express, Spring, etc.
- Databases: PostgreSQL, MySQL, MongoDB, Redis, etc.
- Tools: Docker, Kubernetes, Jenkins, GitHub Actions, etc.
- Cloud: AWS, Azure, GCP, etc.

**Add to context/overview.md** under "Technology Stack"

## Decision Tree

```
READ specification document
↓
EXTRACT keywords and patterns
↓
SCORE each template (0-100)
↓
GET highest score(s)
↓
IF score >= 90:
    → AUTO-SELECT template (high confidence)
    → EXPLAIN detection reasoning
    → PROCEED to configuration detection
↓
ELSE IF score >= 70:
    → AUTO-SELECT template (medium-high confidence)
    → EXPLAIN detection reasoning
    → OFFER easy override option
    → PROCEED to configuration detection
↓
ELSE IF score >= 50:
    → RECOMMEND template
    → ASK "Does this sound right? [Y/N or choose different]"
    → PROCEED based on user choice
↓
ELSE IF multiple scores within 10 points:
    → PRESENT top 2-3 as options
    → ASK user to choose
    → EXPLAIN why each is relevant
    → PROCEED with user choice
↓
ELSE (all scores < 50):
    → LIST all templates with brief descriptions
    → ASK user to choose
    → PROCEED with user choice
↓
DETECT configuration needs:
    ├─ Phase 0 needed?
    ├─ Multi-dimension difficulty?
    ├─ Complexity level?
    ├─ Technology stack?
    └─ Special requirements?
↓
ASK only necessary clarifying questions (if any)
↓
GENERATE environment files
↓
PRESENT summary with detection reasoning
```

## Pattern Matching Examples

### Example 1: Clear Power Query Signal

**Specification excerpt**:
```
Project: Implement pension calculation formulas from regulatory PDF.
Technology: Power Query M language in Excel.
Requirements: Parse government regulation document, interpret calculation rules,
implement in Power Query with proper error handling.
```

**Scoring**:
- Power Query mentions: 30 + 30 = 60
- Excel + calculation: 30
- Regulatory + PDF: 15 (Phase 0 trigger)
- **Total: 90+ → Power Query template**

**Phase 0**: YES (regulatory + PDF + interpretation)
**Confidence**: High - auto-select

---

### Example 2: Clear Research Signal

**Specification excerpt**:
```
Research Question: Do BERT-based models outperform GPT for sentiment analysis?
Methodology: Literature review of 60+ papers, design experiments with 3 datasets,
hypothesis testing using statistical significance tests (p < 0.05).
Deliverables: Research paper for conference submission.
```

**Scoring**:
- Research question: 30
- Literature review: 30
- Hypothesis testing: 30
- Experiments: 30
- Statistical analysis: 15
- Academic paper: 30
- **Total: 165 → Research/Analysis template**

**Confidence**: Very high - auto-select

---

### Example 3: Ambiguous - Ask User

**Specification excerpt**:
```
Project: Work with customer data to improve business outcomes.
Use Python and SQL to analyze patterns.
Create some visualizations.
```

**Scoring**:
- Research/Analysis: 5 (generic "analyze")
- Base: Confirmed (Python, SQL mentioned)
- Documentation: 0
- Power Query: 5 (generic "data")
- Life: 0
- **Highest: Base template (by technology match)**

**Confidence**: Low (no clear domain signals)

**Action**: Present as recommendation:
```
"I recommend the Base (general-purpose) template for your Python/SQL project.
This provides standard task management and commands without specialized workflows.

Is this correct, or would you prefer:
  - Research/Analysis template (if this is exploratory data science)
  - Different template?"
```

---

### Example 4: Life Project Signal

**Specification excerpt**:
```
Goal: Track my fitness journey in 2024.
Features:
- Log workouts and exercises
- Plan meal prep for the week
- Track body measurements
- Set and monitor fitness goals
```

**Scoring**:
- Life Projects: 30 (personal goal) + 30 (fitness) + 15 (first person) = 75
- Others: 0-5
- **Total: 75 → Life Projects template**

**Confidence**: Medium-high - auto-select with explanation

---

## Special Cases

### Case 1: Multiple Template Signals (Hybrid Project)

**If specification matches multiple templates strongly**:

Example: "Research project to build a data engineering pipeline"
- Research/Analysis: 60 points
- Data Engineering: 55 points (if we had this template)

**Action**:
```
"I detected signals for both research and data engineering:
- Research: [evidence]
- Data Engineering: [evidence]

Which is your primary focus? The template you choose will determine
the workflow commands and standards provided."
```

### Case 2: Minimal vs. Full Structure

**Use minimal structure if**:
- Specification mentions "quick", "simple", "small"
- < 5 deliverables estimated
- Solo developer
- No regulatory requirements
- No specialized domain

**Example**:
```
"Quick weekend project to build a todo app"
→ Life Projects template with minimal structure (just tasks/, no full commands)
```

### Case 3: Custom Template Needed

**If specification doesn't match existing templates well**:

```
"Your project involves [unique domain] that doesn't match our standard templates well.

I recommend:
1. Start with Base template (provides core task management)
2. Customize commands and context files for your domain
3. Consider contributing this as a new template pattern

Would you like to proceed with Base template and customize?"
```

## Validation Rules

Before finalizing template selection:

- [ ] Template score is documented with reasoning
- [ ] Phase 0 decision has clear justification
- [ ] Technology stack extracted from specification
- [ ] Complexity level estimated (weekend/multi-week/long-term)
- [ ] If asking user, provide clear options with context
- [ ] If auto-selecting, explain top 2-3 indicators that triggered selection

## Continuous Improvement

**Track detection accuracy**:
- If user overrides auto-selection, note the patterns that caused mismatch
- Update scoring weights based on real-world usage
- Add new templates as common patterns emerge

**Template additions**:
When adding a new template, define:
1. High confidence indicators (30 points each)
2. Medium confidence indicators (15 points each)
3. Low confidence indicators (5 points each)
4. Example specifications that should trigger it
5. Differentiation from existing templates

## Quick Reference Table

| Template | Top 3 Triggers | Confidence Threshold | Special Config |
|----------|----------------|---------------------|----------------|
| Power Query | "Power Query", "M language", Excel+regulatory | 90 | Phase 0 if regulatory+ambiguous |
| Research/Analysis | "research question", "hypothesis", "literature review" | 90 | Multi-dimension difficulty optional |
| Life Projects | "personal goal", fitness keywords, "my"/"I" personal | 75 | Minimal structure |
| Documentation | "technical writing", "API docs", "knowledge base" | 90 | Style guide optional |
| Base | Technology stack, no specialized domain | 50 | Fallback default |
