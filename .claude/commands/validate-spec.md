# Validate Specification Command

## Purpose
Validate project specification quality before running bootstrap. Provides early feedback on template detection confidence, identifies missing signals, and suggests improvements to increase bootstrap success rate.

## Context Required
- Path to specification file (`.md` format)
- `.claude/reference/template-selection-rules.md` - Detection pattern rules

## Process

### Step 1: Load Specification

Read the specification file provided by user:
- Accept any path format (absolute, relative, ~, ., etc.)
- Validate file exists and is readable
- Validate file is `.md` format
- Extract full text content

### Step 2: Run Template Detection Analysis

Apply the same detection logic as smart-bootstrap (from template-selection-rules.md):

**For Each Template Type** (Power Query, Research/Analysis, Life Projects, Documentation, Base):

1. **Extract Keywords**: Scan spec for high/medium/low confidence indicators
2. **Calculate Score**: Sum points for all matched patterns
3. **Record Matches**: Track which patterns triggered and their point values

**Scoring Reference**:
- High confidence indicator: 30 points
- Medium confidence indicator: 15 points
- Low confidence indicator: 5 points

### Step 3: Analyze Detection Confidence

**Calculate Overall Confidence**:
- Highest template score determines primary recommendation
- Confidence level based on top score:
  - **90-100**: Very High (auto-select)
  - **70-89**: High (auto-select with explanation)
  - **50-69**: Medium (recommend with override option)
  - **Below 50**: Low (ask user to choose)

**Check for Ambiguity**:
- If multiple templates within 10 points: Flag as ambiguous
- If no template scores above 50: Flag as too generic

### Step 4: Identify Missing Signals

For the top 2-3 scoring templates, identify what's missing:

**Check Required Elements**:
- Technology stack mentions (languages, frameworks, tools)
- Domain indicators (research, regulatory, personal, etc.)
- Timeline/complexity hints (weekend project, multi-month, etc.)
- Deliverables or features mentioned
- Team size indicators (I, we, solo, team)

**Common Missing Signals**:
- No specific technology names
- Generic terms only ("data", "analysis")
- No project type indication
- No scope or timeline
- Unclear purpose

### Step 5: Generate Validation Report

Create structured feedback report:

```markdown
✓ Specification Quality Report

## Detection Results
**Top Template Detected**: [Template Name] ([Score]% confidence)
**Confidence Level**: [Very High | High | Medium | Low]

### Why This Template?
✓ [Pattern 1]: "[Quote from spec]" (30 pts)
✓ [Pattern 2]: "[Quote from spec]" (30 pts)
✓ [Pattern 3]: "[Quote from spec]" (15 pts)

### Alternative Matches
[Template 2]: [Score]% confidence
[Template 3]: [Score]% confidence

## Recommendation
[If ≥70%]: ✓ READY - Your spec is clear. Proceed with bootstrap.
[If 50-69%]: ⚠ IMPROVE RECOMMENDED - Consider adding more details (see below).
[If <50%]: ✗ NEEDS IMPROVEMENT - Spec is too generic for reliable detection.

## Improvement Suggestions

[If missing technology]:
• Add specific technologies: Instead of "database", say "PostgreSQL" or "MongoDB"
• Mention programming languages: Python, JavaScript, TypeScript, etc.
• Include frameworks if relevant: React, Django, Power Query, etc.

[If missing domain]:
• Clarify project type: Is this research, engineering, personal, or documentation?
• Add domain keywords: "research question", "Power Query", "personal goal", "API docs"

[If missing scope]:
• Indicate timeline: "weekend project", "multi-week", "ongoing"
• Mention deliverables: "dashboard", "paper", "calculator", "tutorial"
• List features or requirements

[If ambiguous]:
• Multiple templates scored similarly ([list templates with scores])
• Be more specific about your primary focus
• See template comparison at: templates/[name]/README.md

## Enhanced Spec Example

Based on your content, here's how you could improve clarity:

[Show 2-3 sentence rewrite with detection keywords added]

## Configuration Detection

[If Phase 0 applicable]:
✓ Phase 0 Workflow: ENABLED
  Reason: Regulatory/compliance context with ambiguous source documents

[If multi-dimension scoring suggested]:
⚠ Complex Domain Detected
  Consider: Multi-dimension difficulty scoring for [domain]

[If minimal structure suitable]:
ℹ Simple Project Detected
  Note: Minimal structure may be sufficient (< 10 tasks estimated)

## Next Steps

[If ready]:
1. Run smart-bootstrap: "Create the environment from claude_code_environment repo using spec: [path]"
2. Bootstrap will auto-select [Template Name] template

[If needs improvement]:
1. Add suggested details above
2. Re-run validate-spec to check improvements
3. Once score ≥ 70%, proceed with bootstrap

[If very generic]:
1. Review specification templates: examples/specifications/templates/
2. Use template matching your project type
3. Include required sections and detection keywords
4. Re-validate before bootstrap

## Detection Pattern Reference

See full detection rules: `.claude/reference/template-selection-rules.md`
Template descriptions: `templates/[name]/README.md`
Example specs: `examples/specifications/`
```

### Step 6: Special Case Handling

**Handle Edge Cases**:

1. **Empty or Very Short Spec** (< 100 characters):
   - Score: 0 across all templates
   - Message: "Specification too short. Minimum 2-3 sentences describing project, technology, and goals."

2. **Multiple Strong Signals** (2+ templates > 70%):
   - Show all high-scoring templates
   - Explain which keywords triggered each
   - Ask user to clarify primary focus

3. **No Clear Winner** (all templates < 30%):
   - Show generic base template recommendation
   - Provide examples from each template type
   - Link to specification template examples

4. **Perfect Score** (100%):
   - Celebrate clear specification
   - Show detected signals
   - Proceed with high confidence

### Step 7: Interactive Mode (Optional)

If user requests interactive feedback:

```
Would you like help improving your specification?
  [Y] Yes, show me how to improve it
  [N] No, proceed with current spec
  [E] Show me examples for [template type]
```

If Yes:
- Ask clarifying questions based on missing signals
- Generate improved version
- Re-validate automatically

## Output Location

Console output to user (not written to file)

## Usage Examples

### Example 1: Good Spec (High Confidence)

```bash
User: "Validate my specification at ~/Documents/pension-calc-spec.md"

Output:
✓ Specification Quality Report

Top Template Detected: Power Query (92% confidence)
Confidence Level: Very High

Why This Template?
✓ "Power Query M language" explicitly mentioned (30 pts)
✓ "Excel workbook with regulatory calculations" (30 pts)
✓ "Parse PDF regulation document" (30 pts)
✓ Phase 0 workflow enabled (regulatory + ambiguous source)

Recommendation: ✓ READY - Your spec is crystal clear. Proceed with bootstrap.

Next Steps:
1. Run: "Create the environment from claude_code_environment repo using spec: ~/Documents/pension-calc-spec.md"
2. Bootstrap will auto-select Power Query template with Phase 0
```

### Example 2: Needs Improvement (Low Confidence)

```bash
User: "Validate spec.md"

Output:
⚠ Specification Quality Report

Top Template Detected: Base (35% confidence)
Confidence Level: Low

Why This Template?
~ Generic "data analysis" mentioned (5 pts)
~ "Python" mentioned (15 pts)
~ "create dashboard" mentioned (15 pts)

Recommendation: ✗ NEEDS IMPROVEMENT - Spec is too generic for reliable detection.

Improvement Suggestions:

• Add specific technologies:
  - Which database? PostgreSQL, MongoDB, MySQL?
  - Which dashboard tool? Streamlit, Dash, Power BI, Tableau?
  - Which Python frameworks? pandas, numpy, scikit-learn?

• Clarify project type:
  - Is this research (hypothesis testing, literature review)?
  - Is this engineering (ETL, data pipeline, API)?
  - Is this analytics (BI, reporting, KPIs)?

• Add scope indicators:
  - How long will this take? (weekend, 2 weeks, 3 months)
  - What are the deliverables? (interactive dashboard, report, API)
  - Who will use it? (personal, team, customers)

Enhanced Spec Example:
"Create an interactive dashboard using Python Streamlit and PostgreSQL
to visualize sales KPIs for our marketing team. Research question:
Which campaigns drive the most conversions? Include 5-10 visualizations
with drill-down capability."

Next Steps:
1. Review specification templates: examples/specifications/templates/
2. Add details from suggestions above
3. Re-run validate-spec
4. Once score ≥ 70%, proceed with bootstrap
```

### Example 3: Ambiguous (Multiple Matches)

```bash
User: "Validate research-project.md"

Output:
⚠ Specification Quality Report

Top Template Detected: Research/Analysis (75% confidence)
⚠ Alternative: Data Engineering (68% confidence)

Why Research/Analysis?
✓ "Research question: How does X affect Y?" (30 pts)
✓ "Statistical analysis" mentioned (15 pts)
✓ "Literature review of 50 papers" (30 pts)

Why Data Engineering?
✓ "ETL pipeline" mentioned (30 pts)
✓ "Data transformation with Python" (23 pts)
✓ "Database schema design" (15 pts)

Recommendation: ⚠ CLARIFY PRIMARY FOCUS

Your spec contains signals for both research and engineering.
Which is your primary goal?

  Research Focus: Hypothesis testing, analysis, publication
  → Choose Research/Analysis template

  Engineering Focus: Data infrastructure, pipelines, production systems
  → Choose Data Engineering template (or create hybrid)

Enhancement Suggestions:
If Research: Emphasize methodology, hypothesis, analysis approach
If Engineering: Emphasize architecture, scalability, production requirements

Next Steps:
1. Clarify primary focus in specification
2. Re-validate to confirm single template scores ≥ 70%
3. Proceed with bootstrap
```

## Validation Checklist

Before completing this command, verify:

- [ ] Reads specification file from any path format
- [ ] Applies all detection patterns from template-selection-rules.md
- [ ] Calculates accurate confidence scores
- [ ] Identifies missing signals for top templates
- [ ] Generates actionable improvement suggestions
- [ ] Handles edge cases (empty, ambiguous, perfect)
- [ ] Output is clear and user-friendly
- [ ] Includes examples in suggestions
- [ ] References relevant documentation files
- [ ] Provides clear next steps based on confidence level

## Integration with Bootstrap

This command uses the **exact same detection logic** as smart-bootstrap.md.

**Validation Guarantee**:
- If validate-spec shows ≥70% confidence for a template
- Then smart-bootstrap will auto-select the same template
- No surprises or mismatches between validation and bootstrap

## Error Handling

**File Not Found**:
```
✗ Error: Specification file not found
  Path: [provided path]

  Try:
  • Check if file path is correct
  • Use absolute path: /full/path/to/spec.md
  • Use relative path: ./spec.md or ~/Documents/spec.md
  • Run from correct directory
```

**Invalid File Format**:
```
✗ Error: File must be Markdown (.md)
  Found: [extension]

  Specifications must be in Markdown format.
  Convert your file to .md or create new spec.
```

**Unreadable File**:
```
✗ Error: Cannot read file
  Path: [path]

  Check file permissions and try again.
```

## Performance Notes

- Validation completes in < 2 seconds for typical specs
- No file creation or modification
- Safe to run multiple times
- No side effects on repository

## Related Commands

- `smart-bootstrap.md` - Uses same detection logic to create environment
- `create-spec.md` - Interactive spec builder (Task 100)
- `.claude/reference/template-selection-rules.md` - Full detection patterns
- `examples/specifications/templates/` - Specification templates
