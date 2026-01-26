# Log Decision Command

## Purpose
Record important decisions with rationale, alternatives considered, confidence levels, and outcomes for future learning and pattern detection.

## Context Required
- Decision type (template selection, task breakdown, architecture, etc.)
- Current project context
- Available alternatives

## Process

### 1. Identify Decision Type
Determine which decision log to update:
- **Template Selection**: `.claude/decisions/template-selection.md`
- **Task Breakdown**: `.claude/decisions/task-breakdown.md`
- **Architecture**: `.claude/decisions/architecture.md` (create if needed)
- **Technology Choice**: `.claude/decisions/technology.md` (create if needed)
- **Process**: `.claude/decisions/process.md` (create if needed)

### 2. Gather Decision Context
Collect information about:
- **The Choice Made**: What was decided
- **Confidence Level**: How certain (percentage)
- **Decision Time**: How long to decide
- **Alternatives Considered**: Other options evaluated
- **Rejection Reasons**: Why alternatives weren't chosen

### 3. Document Rationale
Explain the reasoning:
- **Primary Factors**: Main reasons for the decision
- **Supporting Evidence**: Data or patterns observed
- **Assumptions Made**: What we're assuming to be true
- **Risks Acknowledged**: Known potential issues

### 4. Structure the Entry
Use consistent format:
```markdown
### [Date] - [Context/Project]
**Decision**: [What was decided]
**Confidence**: [X%]
**Decision Time**: [duration]

**Options Evaluated**:
1. **[Option 1]** (Confidence: X%)
   - Pros: [advantages]
   - Cons: [disadvantages]
   - Why chosen/rejected: [reason]

2. **[Option 2]** (Confidence: X%)
   - Pros: [advantages]
   - Cons: [disadvantages]
   - Why chosen/rejected: [reason]

**Rationale**:
[Detailed explanation]

**Assumptions**:
- [Assumption 1]
- [Assumption 2]

**Risks**:
- [Risk 1]: [Mitigation strategy]
- [Risk 2]: [Mitigation strategy]

**Success Criteria**:
- [How we'll know if this was the right decision]

**Outcome**: [Pending/Success/Partial/Failed]
**Lessons Learned**: [Added after outcome known]
```

### 5. Update Metrics
After logging, update the metrics section:
- Total decisions logged
- Average confidence
- Success rate (when outcomes known)
- Common patterns identified

### 6. Extract Patterns
Look for recurring decision patterns:
- Similar contexts leading to same choices
- Confidence correlation with success
- Common failure modes
- Improvement opportunities

## Output Location
- Decision logs: `.claude/decisions/[type].md`
- Pattern updates: `.claude/insights/pattern-detection.md`

## Example Usage

### Template Selection Decision
```bash
# After selecting Power Query template for a BI project
log-decision template-selection "BI Dashboard Project" \
  --selected "power-query" \
  --confidence 92 \
  --alternatives "base:60,research:30" \
  --rationale "Strong Excel and Power BI indicators"
```

### Task Breakdown Decision
```bash
# After deciding to break down a complex task
log-decision task-breakdown "Task #42: API Integration" \
  --breakdown "yes" \
  --subtasks 7 \
  --confidence 85 \
  --strategy "component-based"
```

## When to Log Decisions

### Always Log
- Template selection (every project)
- Major task breakdowns (difficulty ≥7)
- Architecture choices
- Technology selections
- Process changes

### Consider Logging
- Medium complexity decisions
- Decisions with low confidence (<70%)
- Decisions that took >5 minutes
- Decisions with significant alternatives

### Skip Logging
- Trivial decisions (obvious choice)
- Routine operations
- Decisions with no alternatives

## Decision Review Process

### Daily Review
- Check pending outcomes
- Update completed decisions
- Note any failures or surprises

### Weekly Analysis
- Identify decision patterns
- Calculate success rates
- Update confidence calibration

### Monthly Improvement
- Refine decision rules
- Update templates based on patterns
- Propose process improvements

## Integration Points

### With Smart Bootstrap
- Log every template selection
- Track confidence vs. outcome
- Improve selection algorithm

### With Task Management
- Log breakdown decisions
- Track estimation accuracy
- Refine breakdown triggers

### With Pattern Analyzer
- Feed decisions to pattern detection
- Update emerging insights
- Generate recommendations

## Quality Indicators

### Good Decision Logs Have
- Clear rationale with evidence
- All viable alternatives considered
- Specific success criteria
- Honest confidence assessment
- Documented assumptions and risks

### Poor Decision Logs Have
- Vague reasoning
- Missing alternatives
- Overconfident assessments
- No success criteria
- Hidden assumptions

## Automation Support

The pattern analyzer can extract insights from decision logs:
```python
python3 .claude/analyzers/pattern_analyzer.py --analyze-decisions
```

This will:
- Count decision types
- Calculate confidence distributions
- Identify success patterns
- Generate recommendations

## Benefits of Decision Logging

### Immediate Benefits
- Forces thorough thinking
- Documents rationale for future reference
- Identifies assumptions explicitly
- Acknowledges risks upfront

### Long-term Benefits
- Builds decision pattern database
- Improves future decision making
- Calibrates confidence levels
- Enables systematic improvement

## Critical Rules

- **Log immediately** after decision (while context is fresh)
- **Be honest** about confidence and uncertainty
- **Include failures** for learning opportunities
- **Update outcomes** when known
- **Extract patterns** regularly

---

*Template Version: 1.0*
*Last Updated: 2025-12-15*