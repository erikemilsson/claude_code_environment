# Generate Reports Command

## Purpose
Create project deliverables including scientific publication draft, technical report, and dataset documentation.

## Usage
`/generate_reports [type]`

Options:
- `dashboard` - Update Power BI dashboards
- `progress` - Generate progress report
- `scientific` - Create publication draft
- `technical` - Generate technical report
- `dataset` - Prepare open dataset
- `all` - Generate all reports

## Actions

### Dashboard Generation
1. Refresh Power BI data connection
2. Update key metrics:
   - Factors identified
   - Evidence collected
   - Stakeholder participation
   - PESTLE distribution
3. Generate static exports

### Scientific Publication
1. Generate manuscript structure:
   - Abstract
   - Introduction
   - Methodology
   - Results
   - Discussion
   - Conclusions
2. Create figures and tables
3. Format for target journal
4. Export to LaTeX/Word

### Technical Report
1. Comprehensive methodology
2. All factors (not just top 150/50)
3. Detailed network analysis
4. Workshop proceedings
5. Implementation guidance
6. Appendices

### Dataset Preparation
1. Anonymize stakeholder data
2. Create data dictionary
3. Export to CSV/JSON
4. Generate DOI metadata
5. Prepare for Zenodo/Figshare

## Prerequisites
- Analysis complete
- Workshop data collected
- Power BI configured
- LaTeX/Word templates ready

## Files Used
- All specification documents
- Analysis results in `/data/results/`
- Templates in `/templates/`
- Database views

## Expected Output
- Power BI dashboard (PBIX)
- Progress report (PDF)
- Scientific manuscript (DOCX/TEX)
- Technical report (PDF, 50+ pages)
- Dataset package (ZIP)
- Figures folder (PNG/SVG)

## Quality Requirements
- Reproducible figures
- GDPR-compliant data
- Journal formatting guidelines
- Clear visualizations
- Complete documentation

## Publication Targets
- Journal: Resources, Conservation and Recycling
- Alternative: Journal of Cleaner Production
- Report: Environmental Research Institute format
- Dataset: Zenodo with CC-BY license

## Next Steps
1. Internal review
2. Co-author feedback
3. Submit to journal
4. Public dissemination