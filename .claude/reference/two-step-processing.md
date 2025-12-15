# Two-Step Processing Framework

## Purpose
Implement a belief tracker-inspired two-step pipeline for more accurate and confident decision-making during project setup and template selection.

## Overview

The two-step processing framework separates analysis from decision-making:

1. **Step 1: Analysis & Question Generation** - Identify assumptions, extract patterns, generate clarifications
2. **Step 2: Confident Decision Making** - Process responses, validate assumptions, make decisions with high confidence

## Step 1: Analysis Phase

### Objectives
- Extract all relevant indicators from specification
- Identify implicit assumptions
- Generate targeted clarification questions
- Build comprehensive understanding

### Process

#### 1.1 Deep Specification Analysis
```python
def analyze_specification(spec_text):
    return {
        "explicit_indicators": extract_keywords(spec_text),
        "implicit_assumptions": detect_assumptions(spec_text),
        "ambiguous_areas": identify_ambiguities(spec_text),
        "confidence_factors": assess_confidence_indicators(spec_text)
    }
```

#### 1.2 Assumption Extraction
Identify assumptions about:
- **Technology Stack**: What tools/languages are assumed available
- **User Expertise**: What skills are assumed
- **Project Scope**: What's included/excluded
- **Data Availability**: What data sources are assumed
- **Timeline**: Implicit deadline assumptions
- **Team Structure**: Solo vs. collaborative assumptions

#### 1.3 Question Generation
Generate questions only for:
- **Critical Unknowns**: Information that would change template selection
- **High-Impact Assumptions**: Assumptions that if wrong would cause problems
- **Ambiguous Requirements**: Areas needing clarification

Example question structure:
```markdown
### Clarification Needed

**1. Primary Project Focus** (Critical for template selection)
Your specification mentions both "data analysis" and "dashboard creation".
Which is the primary goal?
- [ ] Data analysis and insights (Research template)
- [ ] Interactive dashboard (Power Query template)
- [ ] Both equally important (Hybrid approach)

**2. Data Source Complexity** (Affects Phase 0 need)
You mentioned "regulatory data sources". Are these:
- [ ] Well-structured with clear documentation
- [ ] Ambiguous requiring interpretation
- [ ] Mix of both

**3. Error Tolerance** (Affects validation requirements)
This project involves [financial/regulatory] data. What's the error tolerance?
- [ ] Zero errors acceptable (add extensive validation)
- [ ] Minor errors acceptable with documentation
- [ ] Exploratory analysis (errors expected and okay)
```

#### 1.4 Confidence Assessment
Rate confidence in each assumption:
- **High (90-100%)**: Strong explicit evidence
- **Medium (70-89%)**: Reasonable inference
- **Low (<70%)**: Guessing or unclear

### Output of Step 1
```json
{
  "analysis": {
    "template_indicators": {
      "power-query": ["excel", "power bi", "dax"],
      "research": ["hypothesis", "analysis"],
      "confidence_scores": {"power-query": 75, "research": 45}
    },
    "assumptions": [
      {
        "assumption": "User has Excel expertise",
        "confidence": 85,
        "impact": "high",
        "validation_needed": false
      },
      {
        "assumption": "Regulatory data is ambiguous",
        "confidence": 60,
        "impact": "critical",
        "validation_needed": true
      }
    ],
    "questions": [
      {
        "id": 1,
        "question": "Is regulatory data ambiguous?",
        "why_asking": "Determines if Phase 0 needed",
        "impact": "critical"
      }
    ]
  }
}
```

## Step 2: Decision Phase

### Objectives
- Process user responses to clarifications
- Validate or update assumptions
- Make confident template selection
- Generate complete environment

### Process

#### 2.1 Response Processing
```python
def process_responses(analysis, user_responses):
    # Update assumptions based on responses
    for response in user_responses:
        update_assumption_confidence(response)

    # Recalculate template scores
    template_scores = recalculate_with_validated_assumptions()

    # Make confident selection
    return select_template_with_confidence(template_scores)
```

#### 2.2 Assumption Validation
- Mark assumptions as validated/invalidated
- Update confidence levels based on responses
- Identify any new assumptions from responses

#### 2.3 Confident Decision Making
With validated assumptions:
1. **Recalculate template scores** with higher confidence
2. **Select template** with confidence >85%
3. **Document decision rationale** in decision log
4. **Generate environment** with appropriate configuration

#### 2.4 Decision Documentation
```markdown
### Template Selection Decision

**Selected**: Power Query Template
**Confidence**: 92% (increased from 75% after clarifications)

**Decision Basis**:
- Confirmed: Regulatory data is ambiguous (Phase 0 needed)
- Confirmed: Zero-error tolerance (extensive validation required)
- Confirmed: Excel/Power BI primary tools

**Assumptions Validated**:
- ✓ User has Excel expertise (confirmed)
- ✓ Regulatory interpretation needed (confirmed)
- ✓ Multi-month timeline (confirmed)

**Configuration Decisions**:
- Include Phase 0 workflow
- Add validation commands
- Use 5-dimension difficulty scoring
```

### Output of Step 2
Complete environment generation with:
- High-confidence template selection
- Validated configuration choices
- Comprehensive documentation
- Clear rationale for all decisions

## Benefits of Two-Step Processing

### Increased Accuracy
- Assumptions explicitly validated before decisions
- Ambiguities resolved before generation
- Higher confidence in selections

### Better User Experience
- Only asks necessary questions
- Questions are targeted and meaningful
- Clear reasoning for all decisions

### Improved Learning
- Captures assumptions for pattern detection
- Documents decision rationale
- Enables systematic improvement

## Implementation in Smart Bootstrap

### Modified Workflow
```markdown
1. User provides specification
2. **Step 1**: Analyze and generate clarifications
3. Present clarifications to user (if any)
4. Receive user responses
5. **Step 2**: Make confident decisions
6. Generate environment
7. Log decision with full rationale
```

### Code Structure
```python
class TwoStepBootstrap:
    def __init__(self, specification_path):
        self.spec = self.read_specification(specification_path)
        self.analysis = None
        self.decision = None

    def step1_analyze(self):
        """Analysis and question generation"""
        self.analysis = {
            "indicators": self.extract_indicators(),
            "assumptions": self.identify_assumptions(),
            "questions": self.generate_questions()
        }
        return self.analysis

    def step2_decide(self, responses=None):
        """Confident decision making"""
        if responses:
            self.process_responses(responses)

        self.decision = {
            "template": self.select_template(),
            "configuration": self.determine_configuration(),
            "confidence": self.calculate_confidence(),
            "rationale": self.document_rationale()
        }
        return self.decision

    def generate_environment(self):
        """Create the actual environment files"""
        return self.create_files_from_decision()
```

## Integration Points

### With Pattern Analyzer
- Feed assumptions and validations to pattern detection
- Learn from assumption accuracy over time
- Improve question generation

### With Decision Logger
- Automatically log all template selections
- Include assumption validation results
- Track confidence improvements

### With Belief Tracker
- Use confidence scoring methods
- Apply momentum tracking to project setup
- Monitor assumption validation rates

## Success Metrics

### Accuracy Metrics
- Template selection accuracy: >90%
- Assumption validation rate: >80%
- Configuration correctness: >85%

### Efficiency Metrics
- Questions asked: <3 average
- Decision time: <2 minutes
- User modifications needed: <20%

### Confidence Metrics
- Post-clarification confidence: >85% average
- Confidence calibration accuracy: ±10%
- False confidence rate: <5%

## Examples

### Example 1: Clear Power Query Project
**Specification**: "Build Excel dashboard for regulatory compliance calculations"

**Step 1 Analysis**:
- High confidence Power Query indicators
- No critical assumptions need validation
- No questions generated

**Step 2 Decision**:
- Power Query template selected (95% confidence)
- Phase 0 included (regulatory keyword)
- No user interaction needed

### Example 2: Ambiguous Research/Engineering Project
**Specification**: "Analyze data patterns and build prediction system"

**Step 1 Analysis**:
- Mixed indicators (research + engineering)
- Critical assumption: Primary focus unclear
- Generate question about main objective

**Step 2 Decision** (after user selects "research focus"):
- Research template selected (88% confidence)
- Include data engineering components
- Document hybrid nature

### Example 3: Novel Domain Project
**Specification**: "Quantum computing simulation framework"

**Step 1 Analysis**:
- No clear template match
- Multiple assumptions about requirements
- Generate questions about project structure

**Step 2 Decision** (after clarifications):
- Base template selected (75% confidence)
- Custom configuration based on responses
- Flag for pattern tracking (potential new template)

## Future Enhancements

### Machine Learning Integration
- Train on assumption validation outcomes
- Improve question generation
- Predict configuration needs

### Adaptive Questioning
- Adjust question depth based on user expertise
- Learn user preferences over time
- Skip questions with high-confidence defaults

### Multi-Round Processing
- Allow iterative refinement if needed
- Support progressive disclosure
- Enable mid-process pivots

---

*Framework Version: 1.0*
*Last Updated: 2025-12-15*
*Integration Status: Ready for implementation in smart-bootstrap.md*