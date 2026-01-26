<!-- Type: Direct Execution -->

# Create Specification - Interactive Spec Builder

## Purpose

Guide users through creating a project specification interactively in VS Code, eliminating the need to switch to Claude Desktop. Generates a detection-optimized `spec.md` file that triggers correct template auto-selection with >85% confidence when used with `smart-bootstrap.md`.

**User benefit**: Stay in your development environment while creating comprehensive, template-optimized project specifications.

## When to Use This Command

Use `/create-spec` when:
- Starting a new project and need to create a specification
- Want template-optimized spec for automatic environment detection
- Prefer interactive Q&A over writing spec from scratch
- Need guidance on what information to include

**Alternative**: If you already have a specification document, use `/smart-bootstrap [spec-path]` directly.

## Context Required

- `.claude/tasks/task-100_1.json` - Question flow design
- `.claude/tasks/task-100_2.json` - Keyword injection logic
- `.claude/reference/template-selection-rules.md` - Detection patterns
- `examples/specifications/templates/*.md` - Template examples

## Interactive Question Flow

This command asks **8 questions** (7 required, 1 optional) to build your specification:

### Question 1: Project Name
**What is your project name?**

- Type: Single-line text (required)
- Validation: 3-100 characters, letters/numbers/spaces/hyphens only
- Example: "Pension Regulatory Calculator" or "My Half-Marathon Training Plan"

### Question 2: Project Type
**What type of project is this?**

Choose the option that best describes your project:

- [ ] **Power Query/Excel calculation project** - Regulatory calculations, compliance, Excel automations
- [ ] **Research or analysis study** - Academic research, hypothesis testing, data science experiments
- [ ] **Personal/life project** - Fitness goals, learning journeys, home organization, habit tracking
- [ ] **Documentation or content creation** - Technical docs, API documentation, knowledge bases, blogs
- [ ] **General software development** - Web apps, mobile apps, APIs, standard software projects
- [ ] **Other** (please describe)

**Why this matters**: Your selection determines keyword injection strategy and which template your spec will trigger.

### Question 3: Project Description
**What are you building? (2-3 sentences)**

- Type: Multi-line text (required)
- Validation: 50-500 characters minimum
- Tip: Be specific about what you're creating and why

**Examples by type**:
- **Power Query**: "Implement CEM-06 pension compliance calculations from regulatory PDF using M language in Excel to automate monthly reporting and eliminate manual errors."
- **Research**: "Investigate how remote work impacts employee productivity and job satisfaction in the technology sector through survey analysis of 500+ workers and statistical hypothesis testing."
- **Life Project**: "Train for my first half-marathon by building from zero running experience to completing 21K distance in under 2 hours over 9 months."
- **Documentation**: "Create comprehensive API documentation for our customer management REST API including endpoint reference, authentication guides, and code examples in Python, JavaScript, and cURL."

### Question 4: Technology Stack
**What technologies/tools will you use?**

- Type: Multi-line or comma-separated list (required)
- Validation: At least 1 technology
- Tip: Be explicit about frameworks, languages, and tools

**Examples**:
- Power Query: "Power Query, M language, Excel 365, SQL Server"
- Research: "Python (pandas, scipy, statsmodels), R, Jupyter notebooks, Qualtrics"
- Life Project: "Strava app, Garmin watch, Google Sheets for tracking"
- Documentation: "MkDocs, Markdown, Python (source code), GitHub Pages"
- General: "React, Node.js, PostgreSQL, Docker, AWS"

**What gets enhanced**: Based on your project type, technologies will be formatted with detection keywords:
- "Power Query" → "**Power Query** (M language)"
- "Python" (Research) → "Python (for statistical analysis using pandas, scipy, statsmodels)"
- "Markdown" (Documentation) → "**Markdown** files (static site generator)"

### Question 5: Project Goals
**What are your main goals? (3-5 bullet points)**

- Type: Multi-line text (required)
- Validation: At least 2 goals
- Format: Will be converted to checklist (- [ ] format)

**Examples**:
- "Automate monthly regulatory calculations"
- "Reduce manual errors to zero"
- "Complete in 6 weeks before Q2 deadline"
- "Train stakeholders on new process"

**Domain-specific guidance**:
- **Power Query**: Focus on automation, compliance, accuracy, maintainability
- **Research**: Include hypothesis testing, publication goals, academic contribution
- **Life Projects**: Personal milestones, habit building, measurement targets
- **Documentation**: Reduce support tickets, improve onboarding, increase adoption

### Question 6: Timeline/Duration
**How long do you expect this project to take?**

Choose one:
- [ ] **Weekend project** (2-3 days) - Quick prototype or small task
- [ ] **Sprint** (1-2 weeks) - Single feature or focused deliverable
- [ ] **Multi-week** (1-3 months) - Standard project scope
- [ ] **Long-term** (3+ months) - Major initiative or ongoing work
- [ ] **Custom** (specify your timeline)

**Optional follow-up**: "Any specific deadline?" (e.g., "End of Q2", "June 15, 2024")

### Question 7: Key Requirements (Domain-Specific)

**Prompt varies based on Question 2 answer**:

#### If "Power Query/Excel calculation project":
**What are your key requirements?**

Include:
- Data sources (Excel files, SQL databases, APIs)
- Calculation logic (formulas, regulatory rules)
- Output format (workbook structure, column specifications)
- Regulatory context (if applicable): regulation name, compliance deadline

Example: "Data from SQL Server employee table, implement CEM-06 pension formula (Pension = Salary × Years × Accrual Rate / 100), output to Excel workbook with validation sheet, monthly refresh required"

#### If "Research or analysis study":
**Describe your research methodology**

Include:
- Research question (specific, testable question)
- Hypothesis (your predicted finding)
- Data collection approach (surveys, experiments, datasets)
- Analysis plan (statistical tests, tools, sample size)

Example: "Research question: Do remote workers show higher job satisfaction? Hypothesis: Remote workers will score 15-20% higher on satisfaction surveys. Survey 500 tech workers, use t-tests and regression analysis in Python/R."

#### If "Personal/life project":
**What are your milestones and weekly habits?**

Include:
- Major milestones with target dates
- Weekly/daily habits or routines
- How you'll track progress
- Any resources or support needed

Example: "Milestones: Run 5K in 3 months, 10K in 6 months, half-marathon in 9 months. Weekly: Run 3x per week (Mon/Wed/Sat mornings, 30-60min), cross-training 1x per week. Track in Strava app."

#### If "Documentation or content creation":
**What sections will your documentation include? Who is the audience?**

Include:
- Documentation type (API docs, user guide, tutorials)
- Target audience (developers, end users, internal team)
- Main sections or content outline
- Documentation tool/platform

Example: "API documentation for backend developers. Sections: Getting Started, Authentication, Endpoint Reference (Users, Products, Orders), Error Codes, Code Examples. Using MkDocs, hosted on GitHub Pages."

#### If "General software development":
**List your main features or deliverables (3-10 items)**

Include:
- Core features (must-have functionality)
- User roles or personas
- Integration requirements
- Performance or scale requirements

Example: "User authentication, product catalog with search/filter, shopping cart, checkout flow with Stripe, order history, admin dashboard for inventory management. Support 1000+ concurrent users."

**Validation**: Minimum 100 characters to ensure sufficient detail

### Question 8: Additional Context (Optional)
**Anything else we should know?**

Include:
- Known challenges or constraints
- Regulatory compliance requirements
- Ambiguous requirements needing clarification
- Team/stakeholder information
- Budget or resource constraints

**Phase 0 detection triggers**: If you mention "regulatory", "compliance", "PDF document", "ambiguous interpretation", "unclear requirements" - the spec will automatically include Phase 0 workflow guidance.

Example: "Working from ambiguous CEM-06 regulation PDF that has conflicting interpretation guidance. Need Phase 0 analysis to clarify calculation rules before implementation. Finance team approval required."

## Spec Generation Process

### Step 1: Collect Answers

Ask each question sequentially, providing guidance and examples based on previous answers.

**Validation per question**:
- Q1: Check length (3-100 chars), format (alphanumeric/spaces/hyphens)
- Q2: Must select one option
- Q3: Minimum 50 characters, encourage complete sentences
- Q4: At least one technology mentioned
- Q5: At least 2 goals, suggest action verb starters if needed
- Q6: Valid timeline selection
- Q7: Minimum 100 characters, domain-appropriate content
- Q8: Optional, no validation

**Content warnings** (helpful suggestions, not errors):
- If Q2="Power Query" but Q4 doesn't mention "Power Query" or "Excel":
  → Suggest: "Consider explicitly mentioning Power Query in tech stack for better template detection"
- If Q2="Research" but Q7 doesn't include "hypothesis" or "research question":
  → Suggest: "Strong research specs include explicit research question and hypothesis"
- If Q6="Weekend" but Q7 suggests complex requirements:
  → Suggest: "Your requirements may take longer than a weekend - consider 'Sprint' or 'Multi-week'"

### Step 2: Apply Keyword Injection

Based on Q2 (Project Type), enhance content with detection keywords:

#### Power Query Injection:
- Q3 prefix: "Power Query solution for [user description]. This project will implement [specific calculations] using M language in Excel."
- Q4 enhancements:
  - Add "**Power Query** (M language)" if not mentioned
  - Add "**Excel** (version: 365)" if not mentioned
  - Format: "SQL Server (data source)" for databases
- Section headers: "Regulatory Context", "Data Sources", "Calculation Logic", "M language" challenges
- Content keywords: "regulatory calculation", "Excel workbook", "M code", "compliance"

#### Research Injection:
- Q3 prefix: "Research study investigating [user description]. This research will [methodology] to test the hypothesis that [extracted from Q7]."
- Q4 enhancements:
  - "Python" → "Python (for statistical analysis using pandas, scipy, statsmodels)"
  - "R" → "R (for statistical analysis and visualization)"
- Section headers: "Research Question", "Hypothesis", "Literature Review", "Methodology", "Statistical Analysis"
- Content keywords: "hypothesis testing", "statistical significance", "academic publication", "literature review"

#### Life Projects Injection:
- Q3 prefix: "My personal goal is to [user description]."
- Use first-person throughout: "What I Want to Achieve", "What I Need to Do", "My Goals"
- Section headers: Personal language ("My", "I want", "I will")
- Content keywords: "personal goal", "track my progress", "fitness journey", "learning journey", "my commitment"
- Add relevant category checkboxes (Fitness, Learning, Home, etc.) based on Q7 keywords

#### Documentation Injection:
- Q3 prefix: "Documentation project to create [type] for [audience]. This project will produce [deliverables]."
- Q4 enhancements:
  - "MkDocs" → "**MkDocs** (documentation generator)"
  - Group into "Documentation Tools" and "Source Material"
- Section headers: "Technical Writing", "API Documentation", "Documentation Site", "Content Creation"
- Content keywords: "technical documentation", "API reference", "developer docs", "knowledge base"

#### General (No injection):
- Keep user's natural language
- Format tech stack clearly with categories (Frontend, Backend, Database, Tools)
- Standard section headers ("Overview", "Features", "Requirements", "Technical Considerations")

### Step 3: Generate Spec Sections

Build complete specification with domain-appropriate structure:

#### Common Sections (All Templates):
```markdown
# [Q1: Project Name]

## What I'm Building / What I Want to Achieve
[Q3 with prefix based on Q2]

## Technology Stack
[Q4 formatted with keyword enhancements]

## Goals
[Q5 as checklist format]
- [ ] [Goal 1]
- [ ] [Goal 2]
- [ ] [Goal 3]

## Timeline
**Duration**: [Q6 selection]
**Deadline**: [Q6 optional deadline if provided]
```

#### Power Query-Specific Sections:
```markdown
## Regulatory Context (if mentioned in Q7/Q8)
**Regulation/Standard**: [Extract from Q7/Q8]
**Compliance deadline**: [Extract from Q7/Q8 or "TBD"]
**Reporting frequency**: [Extract from Q7/Q8]

## Data Sources
**Input data locations**:
[Parse from Q7]

## Calculation Logic
[Extract formulas/rules from Q7]

## Requirements & Deliverables
### Must Have (Critical)
[Parse from Q7]

### Should Have (Important)
[Secondary requirements from Q7]

## Output Requirements
**Final output format**: [From Q7]

## Known Challenges
**M language complexity considerations**:
[From Q7/Q8]

## Validation Requirements
[From Q7/Q8 or provide guidance]

## Additional Context
[Q8 content + stakeholder info]
```

#### Research-Specific Sections:
```markdown
## Research Question
[Extract specific question from Q7 - REQUIRED]

## Hypothesis
[Extract hypothesis from Q7 - REQUIRED]

## Background & Motivation
[Expand on Q3 context]

## Methodology
### Study Design
[Parse from Q7]

### Data Collection
**Sample**: [From Q7]
**Data sources**: [From Q7]

### Data Analysis
**Statistical analysis plan**:
[Parse tests/methods from Q7]

**Software/Tools**: [From Q4]

## Timeline
**Research phases**:
1. Literature review ([duration from Q6])
2. Data collection ([duration])
3. Analysis ([duration])
4. Writing & dissemination ([duration])

## Expected Outcomes
[Derive from Q5 + Q7]

### Deliverables
1. Research paper ([venue if mentioned])
2. Dataset (if sharing)
3. Analysis code (GitHub repository)

## Ethical Considerations (if mentioned in Q8)
[Extract IRB, consent, privacy details from Q8]

## Resources Needed
[From Q7/Q8]

## Challenges & Limitations
[From Q8]
```

#### Life Projects-Specific Sections:
```markdown
## What I Want to Achieve
[Q3 with personal prefix]

## Project Type
**[Category based on Q7 keywords]**:
- [x] [Detected category: Fitness/Learning/Home/etc.]

## Current Situation
**Where I'm starting from**: [Infer from Q7/Q8 or note "to be determined"]

## What I Need to Do
### Main Milestones
[Parse from Q7 - structured with dates]

1. **[Milestone 1]** - Target: [date]
   - What I need to accomplish: [specific outcome]
   - How I'll know I'm done: [criteria]

2. **[Milestone 2]** - Target: [date]
   ...

### Weekly Habits
**Frequency**: [From Q7]

- [ ] [Habit 1 from Q7]
- [ ] [Habit 2 from Q7]
- [ ] [Track progress in [tool from Q4]]

## Tracking & Accountability
**Metrics I'll track**: [From Q7]
**Tracking method**: [From Q4]
[From Q7/Q8]

## Resources & Budget
[From Q7/Q8 - equipment, subscriptions, time commitment]

## Potential Obstacles
[From Q8 with mitigation strategies]

## Support System (if mentioned)
[From Q8]
```

#### Documentation-Specific Sections:
```markdown
## What I'm Creating
**Documentation type**: [From Q7]

[Q3 with documentation prefix]

## Purpose & Audience
**Primary readers**: [From Q7]
**Success metrics**: [Infer from Q5/Q7]

## Scope & Content
**Main sections**:
[Parse outline from Q7]

1. **[Section 1]**
   - [Subsections]
2. **[Section 2]**
   ...

## Technology Stack
### Documentation Tools
[From Q4 - documentation-specific]

### Source Material
[What's being documented - from Q7]

## Structure & Organization
[From Q7 - navigation structure]

## Content Requirements
[Standards from Q7 - API endpoint format, tutorial structure, etc.]

## Timeline & Milestones
**Project phases**:
1. Planning & Setup ([duration])
2. Content Creation ([duration])
3. Review & Editing ([duration])
4. Publication & Launch ([target date])

## Maintenance Plan
[Guidance based on Q7/Q8]

## Review & Quality Control
[From Q7/Q8 - reviewers, quality checklist]

## Additional Context
[Q8 content]
```

#### General Template Sections:
```markdown
## Project Overview
[Q3 expanded]

## Technology Stack
**Frontend**: [From Q4]
**Backend**: [From Q4]
**Database**: [From Q4]
**Tools & Infrastructure**: [From Q4]

## Goals & Objectives
[Q5 as checklist]

## Features & Requirements
### Core Features (Must-Have)
[Parse must-haves from Q7]

### Additional Features (Nice-to-Have)
[Parse optional items from Q7]

## Timeline & Phases
[Q6 broken into phases if multi-week+]

## Technical Considerations
[From Q7/Q8 - architecture, scalability, integrations]

## Constraints & Challenges
[From Q8]

## Additional Context
[Q8 content]
```

### Step 4: Phase 0 Detection

Scan Q7 and Q8 for Phase 0 triggers:

**Conditions** (ALL must be met):
1. Q2 is "Power Query", "Research", or "General" with regulatory context
2. Contains: "regulatory" OR "compliance" OR "legal" OR "government requirement"
3. Contains: "PDF document" OR "regulation text" OR "legal document" OR "interpretation" OR "ambiguous" OR "unclear" OR "vague" OR "multiple interpretations" OR "conflicting"

**If triggered, add section**:
```markdown
## Phase 0: Regulation Analysis

This project requires Phase 0 analysis due to ambiguous regulatory requirements.

**Regulatory documents to analyze**:
- [List PDFs/documents from Q7/Q8]

**Ambiguities to resolve**:
- [Interpretation questions from Q8]
- [Conflicting guidance from Q8]

**Phase 0 deliverables**:
- [ ] Regulation interpretation document
- [ ] Calculation logic specification
- [ ] Edge case definitions
- [ ] Stakeholder validation

**Estimated Phase 0 duration**: 1-2 weeks before implementation
```

### Step 5: Add Detection Keywords Footer (Optional)

For educational purposes, optionally add a footer showing keywords used:

```markdown
---

## Detection Keywords Used ⚡

This spec includes keywords that trigger [Template Name] template detection:
- "[Keyword 1]" (high confidence: 30pts)
- "[Keyword 2]" (high confidence: 30pts)
- "[Keyword 3]" (medium confidence: 15pts)

**Expected detection confidence**: [Calculate: 90%+] (auto-select)
```

### Step 6: Confidence Self-Check

Before finalizing, calculate expected detection confidence:

```
Count high-confidence keywords (30pts each)
Count medium-confidence keywords (15pts each)
Count low-confidence keywords (5pts each)

predicted_score = (high × 30) + (medium × 15) + (low × 5)
predicted_confidence = min(predicted_score, 100)

IF predicted_confidence < 85:
    IF Q2 in ["Power Query", "Research", "Documentation"]:
        WARN: "This spec may not achieve 85% detection confidence."
        SUGGEST: "Consider adding more domain-specific details in Questions 7-8."
    ELSE IF Q2 = "Life Projects":
        IF predicted_confidence < 75:
            WARN: "This spec may not trigger Life Projects template."
            SUGGEST: "Add more personal language and specific activity type."
    # General template has no minimum (fallback)
```

### Step 7: Write Spec File

**Location**: `./spec.md` (in current directory) or ask user for custom location

**Final steps**:
1. Generate complete markdown content
2. Write to `spec.md`
3. Show summary of what was created
4. Provide next steps

## Output Format

Show user:
```
✓ Created specification: spec.md

📊 Spec Summary:
   Project: [Q1 Project Name]
   Type: [Q2 selection]
   Timeline: [Q6 selection]
   Technologies: [Count from Q4]
   Goals: [Count from Q5]

📍 Template Detection:
   Expected template: [Template name]
   Confidence: [XX%] (high/medium/low)

🎯 Next Steps:
   1. Review spec.md and make any adjustments
   2. Run: /smart-bootstrap spec.md
   3. Claude will auto-detect [Template Name] template and create your environment

💡 Tip: You can edit spec.md anytime to add more details or fix errors before running smart-bootstrap.
```

## Examples

### Example 1: Power Query Project

**User interaction**:
```
Q1: "Pension Regulatory Calculator"
Q2: "Power Query/Excel calculation project"
Q3: "Automate CEM-06 pension compliance calculations from regulatory PDF"
Q4: "Excel, Power Query, SQL Server"
Q5: "Automate calculations, ensure compliance, reduce errors, train team"
Q6: "Multi-week (2 months)"
Q7: "Data from SQL Server employee table. Implement CEM-06 formula: Pension = Salary × Years × Accrual Rate. Output to Excel with validation sheet. Monthly refresh."
Q8: "CEM-06 regulation PDF has ambiguous edge case handling for part-time employees. Need clarification before implementation."
```

**Generated spec** (excerpt):
```markdown
# Pension Regulatory Calculator

## What I'm Building

Power Query solution for automating CEM-06 pension compliance calculations from regulatory PDF. This project will implement monthly reporting calculations using M language in Excel.

## Technology Stack

- **Power Query** (M language)
- **Excel** (version: 365)
- SQL Server (data source)

## Regulatory Context

**Regulation/Standard**: CEM-06 pension compliance
**Compliance deadline**: TBD
**Reporting frequency**: Monthly

## Phase 0: Regulation Analysis

This project requires Phase 0 analysis due to ambiguous regulatory requirements.

**Regulatory documents to analyze**:
- CEM-06 regulation PDF

**Ambiguities to resolve**:
- Edge case handling for part-time employees

**Expected detection confidence**: 95% → Power Query template (auto-select)
```

### Example 2: Research Project

**User interaction**:
```
Q1: "Remote Work Productivity Study"
Q2: "Research or analysis study"
Q3: "Investigate impact of remote work on employee productivity and satisfaction"
Q4: "Python, R, Qualtrics, Jupyter"
Q5: "Test hypothesis, publish paper, contribute to literature, inform policy"
Q6: "Long-term (6 months)"
Q7: "Research question: How does remote work affect productivity? Hypothesis: Remote workers show 15-20% higher satisfaction with similar productivity. Survey 500 tech workers. Use t-tests and regression in Python/R. Target p<0.05 significance."
Q8: "Need IRB approval. Ethics concerns around employee privacy. Anonymous survey design required."
```

**Generated spec** (excerpt):
```markdown
# Remote Work Productivity Study

## Research Question

How does remote work affect employee productivity and job satisfaction in the technology sector?

## Hypothesis

Remote workers will show 15-20% higher job satisfaction with similar productivity levels compared to office workers.

## Technology Stack

- Python (for statistical analysis using pandas, scipy, statsmodels)
- R (for statistical analysis and visualization)
- Qualtrics (survey platform)
- Jupyter notebooks (analysis environment)

## Methodology

### Data Collection
**Sample**: 500 technology workers
**Approach**: Anonymous survey comparing remote vs office workers

### Data Analysis
**Statistical analysis plan**:
- Hypothesis testing using t-tests
- Regression analysis
- Statistical significance tests (p < 0.05)

## Ethical Considerations

- IRB approval required
- Anonymous survey design to protect employee privacy
- [Additional ethics details]

**Expected detection confidence**: 100% → Research/Analysis template (auto-select)
```

### Example 3: Life Project

**User interaction**:
```
Q1: "My Half-Marathon Training"
Q2: "Personal/life project (fitness, learning, home)"
Q3: "Train for first half-marathon, going from zero to 21K in 9 months"
Q4: "Strava app, running shoes, foam roller"
Q5: "Run 21K distance, finish in under 2 hours, build consistent habit, avoid injury"
Q6: "Long-term (9 months)"
Q7: "Milestones: Run 5K in 3 months, 10K in 6 months, half-marathon in 9 months. Weekly: Run 3x per week (Mon/Wed/Sat mornings, 30-60 min), strength training 1x. Track every run in Strava."
Q8: "History of knee issues - need to be careful with mileage increases. Time constraints with work schedule."
```

**Generated spec** (excerpt):
```markdown
# My Half-Marathon Training

## What I Want to Achieve

My personal goal is to train for my first half-marathon, going from zero running experience to completing 21K distance in 9 months.

## Project Type

**Fitness & Health**:
- [x] Running/marathon training
- [x] Fitness journey

## What I Need to Do

### Main Milestones

1. **Build base fitness** - Target: 3 months from start
   - What I need to accomplish: Run 5K comfortably without stopping
   - How I'll know I'm done: Completed 5K run

2. **Increase distance** - Target: 6 months from start
   - What I need to accomplish: Run 10K regularly

3. **Race readiness** - Target: 9 months from start
   - What I need to accomplish: Complete half-marathon in under 2 hours

### Weekly Habits

**Frequency**: 3x per week running + 1x strength training

- [ ] Run Monday/Wednesday/Saturday mornings (30-60 min)
- [ ] Strength training 1x per week
- [ ] Track my progress in Strava app after every run

## Potential Obstacles

**Challenge**: History of knee issues
- **Mitigation**: Careful mileage increases, foam rolling, listen to body

**Challenge**: Time constraints with work schedule
- **Mitigation**: Early morning runs (6am), fixed schedule commitment

**Expected detection confidence**: 85% → Life Projects template (auto-select)
```

## Common Issues & Troubleshooting

### Issue 1: Low Confidence Warning

**Problem**: Predicted confidence < 85% (or < 75% for Life Projects)

**Solutions**:
- Add more domain-specific terminology in Q7
- Explicitly mention key technologies in Q4
- Include methodology details in Q7 (research) or calculation logic (Power Query)
- Use domain-appropriate language (first-person for Life, technical for Documentation)

### Issue 2: Ambiguous Project Type

**Problem**: User selects "Other" or answers suggest multiple templates

**Solution**:
- Ask follow-up: "This sounds like it could be [Type A] or [Type B]. Which better describes your primary focus?"
- Explain differences: "Power Query focuses on Excel calculations, while General focuses on software development"
- Default to General if truly ambiguous

### Issue 3: Insufficient Detail in Q7

**Problem**: User provides < 100 characters in Q7

**Solution**:
- Prompt with specific sub-questions based on Q2:
  - Power Query: "What data sources will you use? What calculations are needed?"
  - Research: "What is your research question? What's your hypothesis?"
  - Life: "What are your milestones? What will you do weekly?"
- Show example from similar project
- Allow user to skip but warn: "Minimal details may reduce template detection confidence"

### Issue 4: Conflicting Information

**Problem**: Q2 says "Power Query" but Q4 mentions "React, Node.js"

**Solution**:
- Detect mismatch: IF Q2 = "Power Query" AND Q4 lacks "Power Query"/"Excel"
- Ask clarification: "You selected Power Query but didn't mention it in tech stack. Did you mean to select 'General software development'?"
- Allow user to correct Q2 or confirm intentional

## Validation Rules Summary

| Question | Required | Min Length | Format | Content Check |
|----------|----------|------------|--------|---------------|
| Q1 | Yes | 3 chars | Alphanumeric + spaces/hyphens | Proper capitalization |
| Q2 | Yes | N/A | Single select | Valid option |
| Q3 | Yes | 50 chars | Free text | Complete sentences |
| Q4 | Yes | 1 tech | Comma-separated or multi-line | At least one valid technology |
| Q5 | Yes | 2 goals | Multi-line | Action verb starters preferred |
| Q6 | Yes | N/A | Single select | Valid timeline option |
| Q7 | Yes | 100 chars | Multi-line | Domain-appropriate content |
| Q8 | No | 0 chars | Free text | Phase 0 trigger detection |

## Success Metrics

After running `/create-spec`:

✓ Spec file created in < 15 minutes
✓ Contains all essential sections for template detection
✓ Achieves target confidence (>85% or >75% for Life Projects)
✓ User can immediately run `/smart-bootstrap spec.md` with auto-selection
✓ Generated environment matches user's project type

## Tips for Best Results

**For all projects**:
- Be specific in Q3 (avoid "build an app" - say what kind of app)
- List explicit technologies in Q4 (don't assume, state clearly)
- Include measurable goals in Q5 (not "improve" but "reduce by 50%")
- Provide detail in Q7 (this is your chance to explain requirements)

**For Power Query projects**:
- Mention regulatory context if applicable
- Specify data sources and Excel version
- Include formula examples if known
- Flag ambiguous requirements in Q8 for Phase 0

**For Research projects**:
- State research question as a question ("How does X affect Y?")
- Include explicit hypothesis with prediction
- Mention statistical tests you plan to use
- Note IRB/ethics requirements in Q8

**For Life Projects**:
- Use first-person language naturally ("I want to...", "My goal is...")
- Include concrete milestones with dates
- Specify weekly/daily habits
- Mention tracking methods

**For Documentation projects**:
- Specify audience explicitly (developers, end users, etc.)
- Outline main sections/structure
- Mention documentation tool/platform
- Include content standards or style guide references

## Output Location

- **Default**: `./spec.md` (current directory)
- **Custom**: Ask user: "Where should I save the spec file?" if they want different location
- **Validation**: Check if file already exists → Ask to overwrite or choose new name

## Next Steps After Spec Creation

Once spec.md is created:

1. **Review**: User should review spec.md for accuracy
2. **Edit if needed**: User can manually edit spec.md to add details, fix errors, or adjust content
3. **Run smart-bootstrap**: `/smart-bootstrap spec.md` to generate environment
4. **Verify detection**: Check that correct template was auto-selected with high confidence
5. **Begin work**: Start implementing project with optimized environment

---

## Command Usage Summary

```bash
# In Claude Code terminal/chat
/create-spec

# Claude will ask 8 questions interactively
# Answers are used to generate detection-optimized spec.md
# Then run smart-bootstrap with the generated spec
/smart-bootstrap spec.md
```

**Total time**: 10-17 minutes to complete questionnaire
**Output**: Template-optimized spec.md ready for environment generation
