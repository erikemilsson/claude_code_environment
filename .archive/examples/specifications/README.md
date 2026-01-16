# Example Project Specifications

This directory contains example project specifications that demonstrate automatic template detection by the smart-bootstrap command.

## Purpose

These specifications show how different project types trigger the appropriate template selection based on content analysis.

## Examples

### power-query-example.md
**Expected Template**: Power Query with Phase 0

**Detection Signals**:
- "Power Query M language" (high confidence)
- "Excel" + "calculation" (medium confidence)
- "regulatory PDF" + "ambiguous" (Phase 0 trigger)
- "interpretation decisions" (Phase 0 trigger)

**Score**: 90+ (auto-select)

---

### research-example.md
**Expected Template**: Research/Analysis

**Detection Signals**:
- "Research Question" (high confidence)
- "Hypothesis" with testing (high confidence)
- "Literature review" (high confidence)
- "Experiment design" (high confidence)
- "Statistical analysis" (medium confidence)

**Score**: 150+ (very high confidence, auto-select)

---

### life-project-example.md
**Expected Template**: Life Projects

**Detection Signals**:
- "My 2024" + "personal goals" (high confidence)
- "fitness" keywords (high confidence)
- First-person language throughout (medium confidence)
- Personal tracking focus (medium confidence)

**Score**: 75+ (medium-high confidence, auto-select)

---

### documentation-example.md
**Expected Template**: Documentation/Content

**Detection Signals**:
- "technical documentation" (high confidence)
- "API documentation" (high confidence)
- "developer guides" + "tutorials" (high confidence)
- "content creation" focus (medium confidence)

**Score**: 90+ (auto-select)

---

### ambiguous-example.md
**Expected Template**: Base (after asking user)

**Detection Signals**:
- Generic "data" and "analysis" (low confidence, 5-10 points)
- Python/SQL mentioned (Base template indicator)
- No strong domain signals for specialized templates

**Score**: < 50 (ask user to confirm or choose)

**Expected User Interaction**:
```
"I see this is a data project with Python/SQL. Which focus?
1. Data Engineering (ETL pipelines, data infrastructure)
2. Research/Analysis (exploratory analysis, statistical modeling)
3. General (standard template)"
```

## Testing Smart Bootstrap

To test the smart bootstrap with these examples:

1. Navigate to a new empty directory
2. Run: "Create the environment from claude_code_environment repo using spec: [path/to/example]"
3. Observe the template detection reasoning
4. Verify correct template was selected
5. Check that files are populated with content from the specification

## Adding New Examples

When adding new example specifications:

1. Create a realistic project description
2. Include clear signals for the intended template
3. Document expected detection signals
4. Note expected score range
5. Specify whether it should auto-select or ask user
6. Update this README with the new example
