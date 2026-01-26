# Standard Operating Procedure: Quality Checks

## Purpose
Ensure data quality, analysis validity, and deliverable standards throughout the SIREN project.

## Quality Check Points

### Phase 1: Setup
- [ ] Database schema matches specification
- [ ] All constraints and indexes created
- [ ] Test data loads successfully
- [ ] Forms capture all required fields
- [ ] Backup procedures verified

### Phase 2: Data Collection
- [ ] Source quality scores assigned
- [ ] PESTLE balance checked (<40% per category)
- [ ] Evidence properly linked to sources
- [ ] Factors have 2+ supporting evidence
- [ ] No duplicate factors
- [ ] Stakeholder consent documented

### Phase 3: Analysis
- [ ] Network connectivity verified
- [ ] Centrality metrics calculated
- [ ] Logic chains validated
- [ ] Constraint candidates documented
- [ ] Workshop materials reviewed
- [ ] Consensus scores recorded

### Phase 4: Dissemination
- [ ] Figures reproducible
- [ ] Citations complete
- [ ] Data anonymized
- [ ] Code documented
- [ ] Results validated

## Data Quality Metrics

### Completeness
- No NULL values in required fields
- All factors have descriptions
- All evidence linked to sources
- All causal links have rationale

### Accuracy
- Cross-check 10% sample
- Verify calculations
- Validate categorizations
- Confirm stakeholder details

### Consistency
- Standardized terminology
- Uniform categorization
- Consistent scoring
- Matching database/reports

## Analysis Validation

### Factor Prioritization
```python
# Verify scoring calculation
assert significance_score == (0.4 * prevalence +
                              0.4 * impact +
                              0.2 * centrality)

# Check selection criteria
assert len(barriers) == 150
assert len(drivers) == 50
```

### Network Analysis
- Minimum 100 factors in network
- No isolated components
- Centrality metrics normalized
- Communities detected
- Feedback loops identified

### Constraint Identification
- Multiple methods converge
- Stakeholder consensus >70%
- Clear causal pathway
- Root cause not symptom
- Addressable through intervention

## Workshop Quality

### Preparation
- Materials reviewed by advisor
- Technical setup tested
- Participant packets complete
- Voting system functional
- Recording equipment ready

### Execution
- Minimum 15 participants
- All stakeholder types present
- Agenda followed
- Consensus documented
- Actions captured

### Follow-up
- Summary sent within 48 hours
- Feedback incorporated
- Data entered in database
- Recordings processed
- Thank you sent

## Document Standards

### Scientific Publication
- Journal guidelines followed
- Figures high resolution (300+ DPI)
- Tables formatted correctly
- References complete
- Supplementary materials included

### Technical Report
- Comprehensive methodology
- All results included
- Clear recommendations
- Professional formatting
- Executive summary accurate

### Dataset
- FAIR principles met
- Metadata complete
- Data dictionary accurate
- License specified
- DOI obtained

## Code Quality

### Standards
- Comments explain logic
- Functions documented
- Variables clearly named
- Error handling included
- Dependencies listed

### Testing
```python
# Run test suite
pytest tests/

# Check coverage
coverage run -m pytest
coverage report

# Lint code
pylint scripts/
```

## Review Checkpoints

### Internal Review
| Checkpoint | Reviewer | Criteria |
|------------|----------|----------|
| Database design | Technical lead | Schema normalized, indexed |
| Analysis methods | Advisor | Statistically sound |
| Workshop materials | Team | Clear, comprehensive |
| Publication draft | All authors | Accurate, complete |
| Dataset | Data manager | GDPR compliant |

### External Validation
- Advisor review of methodology
- Stakeholder validation of findings
- Peer review of publication
- Ethics review if required

## Error Prevention

### Common Mistakes
| Mistake | Prevention |
|---------|------------|
| Data entry errors | Double-entry verification |
| Calculation errors | Automated scripts |
| Missing citations | Reference manager |
| Version conflicts | Git version control |
| Lost work | Regular backups |

### Quality Control Log
```
Date:
Checker:
Item Checked:
Method:
Result:
Issues Found:
Actions Taken:
```

## Continuous Improvement

### Weekly Review
- Check progress against plan
- Identify quality issues
- Update procedures
- Document lessons learned

### Post-Phase Review
- Assess phase outputs
- Gather team feedback
- Update SOPs
- Implement improvements

### Project Retrospective
- Overall quality assessment
- Success factors
- Improvement areas
- Recommendations for future

## Escalation Process

1. **Minor Issues**: Fix immediately, document
2. **Major Issues**: Team discussion, solution plan
3. **Critical Issues**: Advisor consultation, formal review
4. **Ethical Concerns**: Ethics committee referral

## Documentation Required

### For Each Phase
- Quality check completed
- Issues log maintained
- Corrections documented
- Sign-off obtained

### Final Archive
- All quality documentation
- Review meeting notes
- Correction records
- Final approval