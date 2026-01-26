# Insights Directory

## Purpose

The `.claude/insights/` directory contains **learned patterns and emergent intelligence** from using the Claude Code environment across multiple projects. These are actionable insights extracted from analysis data.

## Key Distinction

- **Analysis Directory**: Raw analytical reports (what happened?)
- **Insights Directory**: Extracted learnings (what should we do?)
- **Reference Directory**: How-to guides (how to use?)

Think of it as:
- **Analysis** = Data collection
- **Insights** = Pattern recognition
- **Reference** = Documentation

## Contents

### pattern-detection.md
**Type**: Pattern catalog
**Purpose**: Tracks recurring patterns to improve decision-making
**Scope**:
- Template selection patterns
- Task difficulty patterns
- Assumption failure patterns
- Success patterns

**When to Update**: After completing projects or major milestones

**Example Patterns**:
- Power Query projects often underestimate DAX complexity (difficulty +2)
- Authentication tasks typically need 3-4 subtasks
- Data migration tasks require explicit rollback planning

### emerging-patterns.md
**Type**: Dynamic pattern tracker
**Purpose**: Captures new patterns as they emerge
**Scope**:
- Recently observed trends
- Experimental patterns being validated
- Hypothesis testing results

**When to Update**: As new patterns are observed

**Example Emerging Patterns**:
- Using Gemini for research before Claude for implementation reduces errors 40%
- Breaking down difficulty 8 tasks into 4 subtasks vs 3 improves completion rate
- Confidence scores below 60% correlate with 3x higher failure rate

## How Insights Differ from Analysis

### Analysis Reports (`.claude/analysis/`)
- **Format**: Comprehensive reports with methodology
- **Frequency**: Periodic (monthly, quarterly)
- **Content**: Detailed findings, metrics, recommendations
- **Audience**: Template developers

### Insights Files (`.claude/insights/`)
- **Format**: Pattern catalogs, quick reference
- **Frequency**: Continuous updates
- **Content**: Actionable patterns, rules of thumb
- **Audience**: Both developers and users

## When to Add Files Here

### Good Candidates for .claude/insights/
- **Pattern Catalogs**: Recurring successful/failed patterns
- **Rules of Thumb**: Quick decision guides
- **Best Practices**: Extracted from experience
- **Anti-Patterns**: What to avoid and why
- **Success Recipes**: Proven approaches

### DON'T Put Here
- **Raw Data**: Put in analysis/ instead
- **How-To Guides**: Put in reference/ instead
- **Project Context**: Put in context/ instead
- **Detailed Reports**: Put in analysis/ instead

## How Insights Are Used

### Decision Support
When making decisions, consult insights for:
- Template selection (pattern-detection.md → Template Selection Patterns)
- Task difficulty estimation (pattern-detection.md → Task Difficulty Patterns)
- Assumption validation (pattern-detection.md → Assumption Failure Patterns)
- Breakdown strategies (emerging-patterns.md → Breakdown Optimization)

### Continuous Improvement
Insights inform:
- **Template Evolution**: Add new templates for common patterns
- **Pattern Library**: Codify successful approaches
- **Command Updates**: Incorporate learned best practices
- **Validation Gates**: Add checks for common failure modes

## Data Flow

```
Projects/Usage
    ↓
.claude/analysis/ (collect data)
    ↓
.claude/insights/ (extract patterns)
    ↓
Templates/Commands (apply learnings)
    ↓
Projects/Usage (improved outcomes)
```

## Insight Types

### 1. Selection Patterns
**Purpose**: Guide template/approach selection
**Example**:
```markdown
## Power Query Projects

Pattern: Excel-heavy requirements
Indicators: "Excel", "Power BI", "DAX", "M language"
Template: power-query
Confidence Required: 90%+

Common Pitfalls:
- Underestimating DAX complexity
- Missing Phase 0 (environment setup)
- Skipping LLM pitfalls checklist
```

### 2. Difficulty Calibration
**Purpose**: Improve task difficulty estimation
**Example**:
```markdown
## Authentication System Tasks

Typical Difficulty: 8
Common Breakdown: 4 subtasks
- Auth flow design (5)
- Token management (6)
- Session handling (5)
- Security hardening (6)

Indicators for Higher Difficulty (+1-2):
- Multi-factor auth required
- External provider integration
- Refresh token rotation
```

### 3. Assumption Patterns
**Purpose**: Predict and validate assumptions
**Example**:
```markdown
## Technology Stack Assumptions

High-Risk Assumption: "Library supports required features"
Validation Method: Check documentation BEFORE starting
Failure Rate: 35% when skipped
Impact: Major rework (avg 40% time increase)

Best Practice: Create proof-of-concept for critical features
```

### 4. Success Recipes
**Purpose**: Replicate successful approaches
**Example**:
```markdown
## Database Migration Success Pattern

Steps:
1. Create rollback script FIRST
2. Test on copy of production data
3. Break into small batches (max 1000 records)
4. Validate each batch before next
5. Keep detailed log of changes

Success Rate: 95% when followed
Vs. 60% without structured approach
```

## Maintaining Insights

### Update Frequency

**pattern-detection.md**:
- Update monthly
- Add new patterns as discovered
- Archive invalidated patterns

**emerging-patterns.md**:
- Update continuously
- Promote validated patterns to pattern-detection.md
- Remove patterns that don't hold up

### Validation Process

Before adding a pattern:
1. **Observe**: See pattern in 3+ independent cases
2. **Document**: Record pattern with evidence
3. **Test**: Validate pattern holds in new cases
4. **Codify**: Add to emerging-patterns.md
5. **Promote**: Move to pattern-detection.md after validation

### Pattern Lifecycle

```
Observation (1-2 cases)
    ↓
Hypothesis (emerging-patterns.md)
    ↓
Validation (3+ cases)
    ↓
Confirmed Pattern (pattern-detection.md)
    ↓
Codified (pattern-library/ or commands/)
```

## Using Insights in Workflows

### During Template Selection
```markdown
1. Read user requirements
2. CHECK: pattern-detection.md → Template Selection Patterns
3. Match keywords to template indicators
4. Verify confidence threshold met
5. Proceed with template
```

### During Task Breakdown
```markdown
1. Identify task type
2. CHECK: pattern-detection.md → Task Difficulty Patterns
3. Apply recommended breakdown structure
4. Adjust for project-specific factors
5. Create subtasks
```

### During Assumption Validation
```markdown
1. List all assumptions
2. CHECK: pattern-detection.md → Assumption Failure Patterns
3. Flag high-risk assumptions
4. Apply recommended validation methods
5. Test before proceeding
```

## Contributing Insights

### Adding New Patterns

When you discover a pattern:

1. **Document the Pattern**:
   ```markdown
   ## [Pattern Name]

   Observation: [What you noticed]
   Frequency: [How often it occurs]
   Indicators: [How to recognize it]
   Impact: [What happens]
   Recommendation: [What to do]
   ```

2. **Provide Evidence**:
   - Link to specific cases
   - Include metrics if available
   - Note context/conditions

3. **Test the Pattern**:
   - Apply in new cases
   - Track success/failure
   - Refine based on results

4. **Share with Team**:
   - Add to emerging-patterns.md
   - Discuss in reviews
   - Iterate based on feedback

## Example Workflow

### Discovering a New Pattern

1. **Observe**: "Tasks involving authentication often take 2x longer than estimated"

2. **Document** in emerging-patterns.md:
   ```markdown
   ## Authentication Task Underestimation

   Observation: Auth tasks consistently exceed time estimates
   Frequency: 8 out of 10 auth tasks observed
   Average Overrun: 2x original estimate

   Hypothesis: Standard difficulty scoring doesn't account for:
   - Security considerations
   - Token lifecycle complexity
   - Error handling requirements

   Recommendation: Add +2 to difficulty for auth tasks
   ```

3. **Validate**: Track next 5 auth tasks with adjusted difficulty

4. **Confirm**: If pattern holds, move to pattern-detection.md

5. **Codify**: Update difficulty-guide.md with auth task considerations

## Summary

**Insights Directory Purpose**: Actionable patterns extracted from experience

**Key Differences**:
- **Analysis**: "Here's what happened" (reports)
- **Insights**: "Here's what to do" (patterns)
- **Reference**: "Here's how to do it" (guides)

**Workflow**: Observe → Document → Validate → Apply → Refine

**Value**: Insights accelerate decision-making and improve outcomes by learning from past experience

**Maintenance**: Continuously updated with validated patterns, archived when superseded
