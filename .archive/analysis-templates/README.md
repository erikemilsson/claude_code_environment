# Analysis Directory

## Purpose

The `.claude/analysis/` directory contains **analytical reports and audits** of the Claude Code environment itself. This is a META directory - it analyzes and improves the template repository, not individual projects.

## Key Distinction

- **Context Directory**: Project-specific understanding and standards
- **Reference Directory**: Reusable guides and documentation
- **Analysis Directory**: Meta-analysis of this repository's patterns and effectiveness

## Contents

### instruction-audit.md
**Type**: Quality audit report
**Purpose**: Analyzes instruction patterns in the repository to identify areas for improvement
**Scope**:
- Passive vs active voice usage
- Implicit vs explicit instructions
- Command file clarity
- Compliance with Claude 4 best practices

**When to Read**: Before refactoring command files or updating CLAUDE.md

**Example Insights**:
- 27% of instructions use passive voice
- Vague directives in template selection logic
- Opportunities for more explicit, imperative commands

### performance-report.md
**Type**: Performance analysis
**Purpose**: Tracks metrics about repository effectiveness
**Scope**:
- Template selection accuracy
- Task completion rates
- Common bottlenecks
- User feedback patterns

**When to Read**: Before making architectural changes to template system

**Example Metrics**:
- Template detection confidence rates
- Most frequently broken down tasks
- Common error patterns

## When to Add Files Here

### Good Candidates for .claude/analysis/
- **Audits**: Pattern audits, instruction analysis, compliance checks
- **Performance Reports**: Metrics tracking, efficiency analysis
- **Retrospectives**: Post-implementation reviews, what worked/didn't
- **Comparison Studies**: Template effectiveness comparisons
- **User Feedback Analysis**: Aggregated user experience data

### DON'T Put Here
- **Project-specific context**: Goes in `.claude/context/`
- **General reference docs**: Goes in `.claude/reference/`
- **Task information**: Goes in `.claude/tasks/`
- **Temporary notes**: Consider `.claude/insights/` instead

## How Analysis Files Are Used

### Repository Improvement Cycle
1. **Analyze**: Generate reports in `.claude/analysis/`
2. **Insights**: Extract patterns in `.claude/insights/`
3. **Action**: Update templates, commands, or documentation
4. **Measure**: Track improvements in next analysis

### Example Workflow
```
instruction-audit.md identifies passive voice issues
→ Update command files with imperative language
→ Track improvement in next audit cycle
→ Document successful patterns in insights/
```

## Relationship to Other Directories

```
.claude/
├── context/         User-facing: Project understanding
├── reference/       User-facing: How-to guides
├── tasks/           User-facing: Work tracking
├── analysis/        Meta: Repository quality
└── insights/        Meta: Learned patterns
```

**User Journey**:
- Start: `context/` - Understand the project
- Learn: `reference/` - How to do things
- Work: `tasks/` - Track progress

**Developer Journey**:
- Measure: `analysis/` - How well is the system working?
- Learn: `insights/` - What patterns emerge?
- Improve: Update templates based on findings

## Maintaining Analysis Files

### Frequency
- **Audits**: Quarterly or before major releases
- **Performance Reports**: Monthly or after significant usage
- **Retrospectives**: After major feature implementations

### Format
All analysis files should include:
- **Generated Date**: When the analysis was performed
- **Scope**: What was analyzed
- **Methodology**: How the analysis was conducted
- **Findings**: Key discoveries
- **Recommendations**: Suggested improvements
- **Metrics**: Quantitative data where possible

### Archiving
Old analysis files can be:
- Moved to `.claude/analysis/archive/YYYY-MM/`
- Compressed if no longer referenced
- Deleted after 1 year if superseded

## Example Analysis Workflow

### Running an Instruction Audit

1. **Scan all command files**:
   ```bash
   find .claude/commands -name "*.md" -exec grep -n "should be" {} \;
   ```

2. **Identify patterns**:
   - Passive voice usage
   - Implicit instructions
   - Missing action verbs

3. **Generate report**:
   - Create/update `instruction-audit.md`
   - Document findings with examples
   - Provide specific recommendations

4. **Create action items**:
   - Update affected command files
   - Document improvements
   - Schedule follow-up audit

### Running a Performance Analysis

1. **Collect metrics**:
   - Template selection confidence scores
   - Task breakdown frequency
   - Completion times

2. **Analyze trends**:
   - Which templates are most used?
   - Which tasks commonly require breakdown?
   - Where do users struggle?

3. **Generate report**:
   - Create/update `performance-report.md`
   - Include quantitative data
   - Identify improvement opportunities

4. **Implement improvements**:
   - Optimize high-friction areas
   - Add patterns to library
   - Update documentation

## Contributing Analysis

### Creating New Analysis Files

When adding new analysis files:

1. **Use descriptive names**: `[topic]-[type].md`
   - Examples: `command-clarity-audit.md`, `template-usage-report.md`

2. **Include metadata**:
   ```markdown
   # [Title]
   *Generated: YYYY-MM-DD*
   *Scope: What was analyzed*
   *Methodology: How it was analyzed*
   ```

3. **Provide actionable insights**:
   - Not just problems, but solutions
   - Specific recommendations
   - Priority ordering

4. **Link to related files**:
   - Reference affected templates/commands
   - Link to related insights
   - Note dependencies

## Common Analysis Types

### Instruction Clarity Audit
**Focus**: Are instructions clear, explicit, and actionable?
**Checks**:
- Passive vs active voice
- Implicit vs explicit commands
- Vague vs specific directives

### Performance Analysis
**Focus**: How efficiently does the system work?
**Metrics**:
- Template selection accuracy
- Task completion times
- Error rates
- User satisfaction

### Pattern Effectiveness Study
**Focus**: Do patterns reduce errors?
**Measures**:
- Pattern adoption rates
- Error reduction when patterns used
- Pattern coverage of common tasks

### User Experience Review
**Focus**: Where do users struggle?
**Sources**:
- Common questions
- Frequent errors
- Documentation gaps
- Workflow bottlenecks

## Summary

**Analysis Directory Purpose**: Meta-analysis of the Claude Code environment itself

**Key Differences**:
- **Context**: What the PROJECT is about
- **Reference**: How to USE the system
- **Analysis**: How WELL the system works
- **Insights**: What PATTERNS emerge

**Workflow**: Analyze → Extract insights → Improve → Measure → Repeat

**Audience**: Template developers and maintainers, not end users
