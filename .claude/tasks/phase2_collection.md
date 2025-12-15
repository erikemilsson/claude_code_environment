# Phase 2: Data Collection (February Week 3 - March Week 4)

## Overview
Conduct systematic literature review and collect stakeholder input through interviews and forms.

## Critical Path Tasks

### Literature Review (Feb Week 3 - Mar Week 2)

1. **Define Search Strategy**
   - PESTLE-guided keywords
   - Database selection (Scopus, Web of Science)
   - Inclusion/exclusion criteria
   - Document search strings

2. **Literature Collection**
   - Academic papers on NdFeB recycling
   - EU policy documents (WEEE, CRM Act)
   - Industry reports
   - Grey literature
   - Target: 60+ sources

3. **Evidence Extraction**
   - Use literature extraction template
   - Code by PESTLE category
   - Identify barriers and drivers
   - Link to value chain stages
   - Enter into database

4. **PESTLE Balance Check**
   - Analyze distribution
   - Identify gaps
   - Targeted searches for underrepresented areas
   - Ensure <40% in any single category

### Stakeholder Engagement (Mar Week 1-4)

1. **Recruitment**
   - Send invitations (target 30+)
   - Industry contacts (10+)
   - Researchers (10+)
   - Policymakers (5+)
   - NGOs (5+)
   - Follow-up reminders

2. **Data Collection**
   - Deploy Microsoft Forms
   - Schedule key interviews (5+)
   - Send reminders at 2 weeks
   - Close forms end of March

3. **Interview Processing**
   - Transcribe recordings
   - Extract barriers/drivers
   - Code responses
   - Add to evidence database

## Checklist
- [ ] Search strategy documented
- [ ] 60+ sources collected
- [ ] Literature extraction complete
- [ ] PESTLE balance achieved
- [ ] 30+ stakeholders contacted
- [ ] 15+ form responses received
- [ ] 5+ interviews conducted
- [ ] All data in database
- [ ] Initial factor list created (100+)
- [ ] Evidence linked to factors

## Quality Metrics
- Source quality average >3.0/5.0
- Each factor supported by 2+ evidence items
- PESTLE distribution: no category >40%
- Geographic diversity in stakeholders
- Value chain coverage complete

## Data Entry Workflow
```
Literature → Extraction Template → Database (sources, evidence, factors)
                    ↓
Interviews → Transcription → Evidence → Link to Factors
                    ↓
Forms → SharePoint → Python Import → Database
```

## Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| Low response rate | Send personalized follow-ups |
| PESTLE imbalance | Targeted searches for gaps |
| Duplicate factors | Merge similar concepts |
| Missing evidence | Use expert elicitation |

## Files to Reference
- `/data_collection_templates.md` - Forms and templates
- `/toc_methodology.md` - Factor identification
- PESTLE framework guide

## Commands to Run
```bash
# Import form responses
python scripts/import_forms.py

# Check PESTLE distribution
python scripts/analyze_coverage.py

# Generate factor list
/run_analysis factor_extraction
```

## Time Estimate
- Literature search: 20 hours
- Evidence extraction: 30 hours
- Stakeholder recruitment: 10 hours
- Interview conduct/process: 15 hours
- Data entry: 10 hours
- **Total: 85 hours**

## Outputs
- Factor database with 100+ entries
- Evidence base with 200+ items
- Stakeholder contact list
- PESTLE coverage report
- Initial barrier prioritization

## Next Phase Trigger
When evidence collection complete and initial factors identified, begin Phase 3: Analysis & Workshop Preparation