# Check Hypotheses Command

## Purpose
Test research hypotheses against collected data and update hypothesis status.

## Context Required
- Hypotheses defined in `.claude/context/hypotheses.md`
- Data analysis completed
- Statistical results available

## Process

### 1. Load Hypothesis File
Read current hypothesis status and test criteria

### 2. For Each Hypothesis
- Review test criteria
- Check statistical results against criteria
- Document evidence (for/against)
- Calculate effect sizes
- Assess confidence level

### 3. Update Hypothesis Status
```json
{
  "status": "supported|rejected|inconclusive",
  "statistical_support": {
    "test": "correlation",
    "statistic": 0.72,
    "p_value": 0.001,
    "effect_size": 0.85,
    "confidence_interval": [0.65, 0.79]
  },
  "evidence_for": ["Study A (2020)", "Study B (2021)"],
  "evidence_against": ["Study C (2019)"],
  "conclusion": "Strong support for hypothesis",
  "tested_date": "2025-01-15"
}
```

### 4. Generate Summary Report
- Overall hypothesis support
- Strength of evidence
- Limitations and caveats
- Implications for research questions

### 5. Update Research Conclusions
- Revise `.claude/context/conclusions.md`
- Update abstract/summary
- Flag any surprising results

## Output Location
- Updated `.claude/context/hypotheses.md`
- `.claude/analysis/hypothesis-test-results.md`
- `.claude/context/conclusions.md`

## Statistical Rigor
- Report all tests conducted
- Include effect sizes and CIs
- Document multiple testing corrections
- Note any deviations from pre-registration