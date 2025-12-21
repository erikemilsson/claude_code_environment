# Decision-Making Framework for Claude 4

## Core Principle

**Act with confidence when certain, clarify only when necessary**

Decision-making follows a confidence-based approach:
- **>90% confidence**: Auto-proceed without asking
- **70-90% confidence**: Minimal clarification (1-2 questions max)
- **50-70% confidence**: Targeted questions for critical unknowns
- **<50% confidence**: Comprehensive requirements gathering

## Decision Trees for Common Scenarios

### 1. Template Selection Decision Tree

```
START: Analyze specification document
│
├─> Power Query indicators found?
│   ├─> YES + "regulatory/compliance" → SELECT Power Query (95% confidence)
│   └─> YES alone → SELECT Power Query (85% confidence)
│
├─> Research indicators found?
│   ├─> "hypothesis" or "literature review" → SELECT Research (90% confidence)
│   └─> "analysis" but no research terms → CHECK for other signals
│
├─> Personal/life indicators found?
│   ├─> "fitness", "budget", "personal" → SELECT Life Projects (95% confidence)
│   └─> "goals" alone → CHECK context (personal vs professional)
│
├─> Documentation indicators found?
│   ├─> "technical writing", "blog" → SELECT Documentation (90% confidence)
│   └─> "documentation" alone → CHECK if main focus or side requirement
│
└─> No clear indicators → SELECT Base template (inform user)
```

**Decision Implementation**:
```python
def select_template(indicators):
    scores = {
        'power-query': calculate_score(indicators, POWER_QUERY_PATTERNS),
        'research': calculate_score(indicators, RESEARCH_PATTERNS),
        'life-projects': calculate_score(indicators, LIFE_PATTERNS),
        'documentation': calculate_score(indicators, DOC_PATTERNS),
        'base': 50  # Default baseline
    }

    best_match = max(scores, key=scores.get)
    confidence = scores[best_match]

    if confidence > 90:
        return auto_select(best_match)
    elif confidence > 70:
        return confirm_with_user(best_match, minimal=True)
    else:
        return ask_user_choice(scores)
```

### 2. Task Breakdown Strategy Decision

```
START: Evaluate task difficulty
│
├─> Difficulty >= 7?
│   ├─> YES → MUST break down (mandatory)
│   └─> NO → Continue to next check
│
├─> User requested breakdown?
│   ├─> YES → Break down regardless of difficulty
│   └─> NO → Continue to next check
│
├─> Difficulty 5-6 with high complexity?
│   ├─> Multiple domains involved → SUGGEST breakdown
│   ├─> Unclear requirements → SUGGEST breakdown
│   └─> Single domain, clear requirements → NO breakdown
│
└─> Difficulty <= 4 → NO breakdown needed
```

**Complexity Factors for Breakdown Decision**:
```
HIGH COMPLEXITY SIGNALS (suggest breakdown even if difficulty < 7):
- Involves 3+ different technologies
- Requires coordination across multiple files
- Has conditional logic branches
- Contains research + implementation phases
- Spans multiple user sessions

LOW COMPLEXITY SIGNALS (avoid breakdown even if difficulty = 7):
- Single file modification
- Straightforward algorithm implementation
- Documentation only task
- Pure refactoring without logic changes
```

### 3. Tool Choice Decision (Claude vs Gemini)

```
START: Analyze task requirements
│
├─> Needs current/real-time information?
│   ├─> YES → USE Gemini with grounding
│   └─> NO → Continue to next check
│
├─> Primary activity is coding?
│   ├─> YES → USE Claude (native tools)
│   └─> NO → Continue to next check
│
├─> Domain expertise needed?
│   ├─> Regulatory/compliance → USE Gemini for research, Claude for implementation
│   ├─> Academic/theoretical → USE Gemini for concepts
│   └─> Technical/engineering → USE Claude
│
├─> Image analysis required?
│   ├─> YES → USE Gemini for analysis, Claude for code based on results
│   └─> NO → Continue
│
└─> Default → USE Claude (better integration)
```

**Tool Selection Matrix**:

| Task Type | Primary Tool | Secondary Tool | Confidence Threshold |
|-----------|--------------|----------------|---------------------|
| Web research | Gemini (grounding) | Claude (synthesis) | 95% |
| Code implementation | Claude | - | 99% |
| Current events | Gemini | - | 100% |
| Architecture design | Claude | Gemini (review) | 85% |
| Data analysis | Claude | Gemini (validation) | 90% |
| Content generation | Gemini | Claude (editing) | 80% |

### 4. Difficulty Scoring Decision

```
START: Assess task characteristics
│
├─> Has clear, single outcome?
│   ├─> YES → Check implementation complexity
│   │   ├─> <20 lines of code → Difficulty 1-2
│   │   ├─> 20-100 lines → Difficulty 3-4
│   │   ├─> 100-500 lines → Difficulty 5-6
│   │   └─> >500 lines or multiple files → Difficulty 7+
│   └─> NO → Continue to multi-factor assessment
│
├─> Multiple interacting components?
│   ├─> 2-3 components → Base difficulty +2
│   ├─> 4-5 components → Base difficulty +3
│   └─> 6+ components → Base difficulty +4
│
├─> External dependencies?
│   ├─> Well-documented APIs → +1
│   ├─> Poor/no documentation → +3
│   └─> Regulatory/compliance → +2
│
└─> Risk factors?
    ├─> Data loss possible → +2
    ├─> Security sensitive → +2
    └─> Performance critical → +1
```

## Confidence Calculation Framework

### Base Confidence Calculation

```python
def calculate_confidence(evidence):
    """
    Calculate confidence score based on available evidence
    """
    confidence = 50  # Start at neutral

    # Strong positive signals (+10-20 each)
    strong_signals = [
        'explicit_technology_mentioned',
        'clear_deliverables_listed',
        'similar_past_project',
        'detailed_requirements'
    ]

    # Moderate positive signals (+5-10 each)
    moderate_signals = [
        'domain_keywords_present',
        'timeline_specified',
        'success_criteria_defined',
        'examples_provided'
    ]

    # Negative signals (-10-20 each)
    negative_signals = [
        'contradictory_requirements',
        'vague_descriptions',
        'multiple_possible_interpretations',
        'missing_critical_info'
    ]

    for signal in strong_signals:
        if evidence.get(signal):
            confidence += 15

    for signal in moderate_signals:
        if evidence.get(signal):
            confidence += 7

    for signal in negative_signals:
        if evidence.get(signal):
            confidence -= 15

    return min(100, max(0, confidence))
```

### Confidence Adjustment Rules

**Increase Confidence**:
- User confirms assumption: +20
- Pattern matches previous successful case: +15
- All dependencies validated: +10
- Clear examples provided: +10

**Decrease Confidence**:
- Assumption invalidated: -20
- Unexpected complexity discovered: -15
- Missing dependency found: -10
- Ambiguous requirements: -15

## Decision Escalation Patterns

### Level 1: Autonomous Decision (>90% confidence)
```
Action: Proceed without user interaction
Log: Record decision and reasoning
Example: "Selected Power Query template (95% confidence: Excel + regulatory keywords detected)"
```

### Level 2: Quick Confirmation (70-90% confidence)
```
Action: Single confirmatory question
Format: "Based on [evidence], I'll use [decision]. Is this correct? (Y/N)"
Example: "Detected research patterns. Using Research template. Correct?"
Timeout: Auto-proceed after 10 seconds if no response
```

### Level 3: Targeted Clarification (50-70% confidence)
```
Action: Ask 1-2 specific questions
Format: Present options with reasoning
Example:
  "I see both data analysis and research elements.
   What's your primary focus?
   1. Academic research (hypothesis testing, literature review)
   2. Data engineering (ETL, pipelines, infrastructure)"
```

### Level 4: Guided Discovery (<50% confidence)
```
Action: Structured information gathering
Process:
  1. Explain what's missing
  2. Ask for specific details
  3. Provide examples of good answers
Example: Full template selection wizard
```

## Decision Caching & Learning

### Decision Cache Structure
```json
{
  "decision_type": "template_selection",
  "input_hash": "hash_of_indicators",
  "decision": "power-query",
  "confidence": 92,
  "reasoning": ["Excel mentioned", "Regulatory compliance", "Calculations required"],
  "outcome": "successful",
  "timestamp": "2025-12-16T10:00:00Z"
}
```

### Pattern Learning Rules
1. **Successful patterns**: Boost confidence by 5% for similar future cases
2. **Failed patterns**: Reduce confidence by 10% for similar cases
3. **User corrections**: Create override rule for specific pattern
4. **Frequency tracking**: Common patterns get higher base confidence

## Quick Decision Reference Card

### Template Selection
| Confidence | Action |
|------------|--------|
| >90% | Auto-select |
| 70-90% | Quick confirm |
| 50-70% | Ask primary focus |
| <50% | Show all options |

### Task Breakdown
| Difficulty | Action |
|------------|--------|
| ≥7 | Must break down |
| 5-6 + complex | Suggest breakdown |
| 5-6 simple | No breakdown |
| ≤4 | Never break down |

### Tool Selection
| Need | Use |
|------|-----|
| Current info | Gemini + grounding |
| Coding | Claude |
| Image analysis | Gemini |
| File operations | Claude |
| Research | Gemini → Claude |

### Confidence Thresholds
| Level | Range | User Interaction |
|-------|-------|------------------|
| High | >90% | None |
| Medium | 70-90% | Minimal (confirm) |
| Low | 50-70% | Targeted (1-2 questions) |
| Very Low | <50% | Comprehensive |

## Implementation Examples

### Example 1: High Confidence Auto-Decision
```
Input: "Create Excel Power Query solution for pension calculations using government regulations"
Indicators: Excel ✓, Power Query ✓, Regulatory ✓, Calculations ✓
Confidence: 98%
Decision: AUTO-SELECT Power Query template with Phase 0
User Interaction: None - proceed immediately
```

### Example 2: Medium Confidence Quick Confirm
```
Input: "Build data pipeline for analytics"
Indicators: Data ✓, Pipeline ✓, Analytics ✓ (but ambiguous)
Confidence: 75%
Decision: "Planning to use data-analytics template. Quick confirm? (Y/N)"
User Interaction: Single confirmation
```

### Example 3: Low Confidence Targeted Questions
```
Input: "Create system for tracking information"
Indicators: Vague, multiple interpretations possible
Confidence: 45%
Decision: Need clarification
User Interaction:
  "What type of information?
   1. Personal (life projects template)
   2. Research data (research template)
   3. Business metrics (data-analytics template)"
```

## Anti-Patterns to Avoid

### 1. Over-Questioning
```
BAD: Asking 10 questions when confidence is 85%
GOOD: Single confirmation at 85% confidence
```

### 2. Under-Confidence
```
BAD: Treating 95% confidence as "uncertain"
GOOD: Auto-proceed at >90% confidence
```

### 3. Generic Questions
```
BAD: "What would you like to do?"
GOOD: "Should I use template X because of Y?"
```

### 4. Ignoring Context
```
BAD: Asking about template when user specified it
GOOD: Using user's explicit choice regardless of patterns
```

## Continuous Improvement

### Metrics to Track
1. **Decision accuracy**: % of auto-decisions confirmed correct
2. **Question efficiency**: Average questions per decision
3. **Time to decision**: Seconds from input to action
4. **User corrections**: Frequency of user overrides
5. **Confidence calibration**: Predicted vs actual success rate

### Review Process
- Weekly: Review decision logs
- Identify: Patterns in failures
- Adjust: Confidence thresholds
- Update: Decision trees
- Document: New patterns discovered