# Analyze Patterns Command

## Purpose
Detect and analyze patterns in template usage, task breakdown strategies, and project setup workflows to identify optimization opportunities.

## Context Required
- Access to task files in `.claude/tasks/`
- Pattern detection framework (pattern-detection.md)
- Historical project data (if available)

## Process

### 1. Run Pattern Analysis
Execute the pattern analyzer to collect data:
```bash
python3 .claude/analyzers/pattern_analyzer.py --verbose --update-md
```

### 2. Analysis Categories
The analyzer examines:

#### Template Usage Patterns
- Frequency of each template type
- Average confidence levels per template
- Selection indicators and keywords
- Success rates by template

#### Task Breakdown Patterns
- How tasks are broken down by difficulty
- Optimal subtask counts
- Difficulty estimation accuracy
- Common breakdown strategies

#### Assumption Patterns
- Validation success/failure rates
- Common failure categories
- Timing of validation
- Impact of failed assumptions

#### Workflow Patterns
- Task completion times by difficulty
- Bottleneck identification
- Momentum phase distribution
- Velocity trends

#### Emerging Patterns
- New project types
- Hybrid template needs
- Trending keywords
- Domain evolution

### 3. Generate Insights
Based on analysis, identify:
- **High-confidence patterns**: Recurring with >80% consistency
- **Medium-confidence patterns**: Recurring with 60-80% consistency
- **Emerging patterns**: New but growing trends

### 4. Create Recommendations
Generate actionable recommendations for:
- New template creation
- Workflow optimizations
- Task estimation improvements
- Assumption validation strategies

### 5. Update Documentation
Update pattern-detection.md with:
- Latest pattern counts
- Trend analysis
- Confidence levels
- Recommendations

## Output Location
- Analysis results: `.claude/insights/pattern_analysis_[timestamp].json`
- Updated patterns: `.claude/insights/pattern-detection.md`
- Recommendations: Included in both outputs

## Example Usage

### Basic Analysis
```bash
# Run analysis and save results
python3 .claude/analyzers/pattern_analyzer.py
```

### Full Analysis with Updates
```bash
# Run full analysis, update markdown, and show verbose output
python3 .claude/analyzers/pattern_analyzer.py --verbose --update-md
```

### Custom Output Location
```bash
# Save to specific location
python3 .claude/analyzers/pattern_analyzer.py --output ./analysis_results.json
```

## Interpretation Guide

### Template Usage Results
- **High usage (>5 instances)**: Consider as default template
- **Mixed usage**: May need template selection improvements
- **Low confidence**: Review selection criteria

### Task Breakdown Results
- **Consistent patterns**: Can automate breakdown
- **Variable patterns**: Need human judgment
- **Accuracy issues**: Adjust difficulty scoring

### Assumption Results
- **High failure rate (>20%)**: Need earlier validation
- **Category clusters**: Focus validation on problem areas
- **Late validation**: Move checks earlier in workflow

### Workflow Results
- **Long completion times**: Consider task breakdown
- **Many blocked tasks**: Review dependency management
- **Low velocity**: Check for process bottlenecks

## Automation Opportunities

Based on patterns detected, consider automating:

1. **Template Selection**: If confidence is consistently >90%
2. **Task Breakdown**: For recurring high-difficulty patterns
3. **Assumption Validation**: For common failure types
4. **Workflow Optimization**: For identified bottlenecks

## Integration Points

This command integrates with:
- `smart-bootstrap.md`: Uses patterns for template selection
- `breakdown.md`: Applies learned breakdown strategies
- `validate-assumptions.md`: Focuses on high-risk assumptions
- `show-dashboard.md`: Displays pattern insights

## Schedule Recommendations

Run pattern analysis:
- **After each project**: Capture fresh patterns
- **Weekly**: For active development
- **Monthly**: For maintenance mode
- **Before major updates**: To inform improvements

## Critical Notes

- Pattern detection improves with more data
- Manual review recommended for low-confidence patterns
- Patterns are project-specific; avoid over-generalization
- Regular updates keep patterns relevant