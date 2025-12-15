# Run Analysis Command

## Purpose
Execute the Theory of Constraints analysis pipeline to identify core system constraints and generate visualizations.

## Usage
`/run_analysis [stage]`

Options:
- `factor_extraction` - Extract and categorize factors from evidence
- `network_analysis` - Build causal network and identify constraints
- `workshop_prep` - Prepare materials for stakeholder workshops
- `full` - Run complete analysis pipeline

## Actions

### Factor Extraction
1. Query evidence from database
2. Group evidence into factors
3. Calculate priority scores:
   - Prevalence (frequency of mention)
   - Impact (severity × source quality)
   - Centrality (network position)
4. Apply PESTLE categorization
5. Select top 150 barriers + 50 drivers

### Network Analysis
1. Build causal links matrix
2. Calculate network metrics:
   - Degree centrality
   - Betweenness centrality
   - Clustering coefficients
3. Identify candidate constraints
4. Generate Current Reality Tree (CRT)
5. Find feedback loops

### Workshop Preparation
1. Create network visualizations
2. Generate voting materials
3. Prepare constraint candidates
4. Build presentation slides
5. Create participant packets

## Prerequisites
- Database populated with evidence
- Python environment activated
- NetworkX library installed

## Files Used
- `/toc_methodology.md` - Analysis methods
- `/database_schema.md` - Data structure
- Analysis scripts in `/scripts/analysis/`

## Expected Output
- Factor priority rankings
- Network visualization (PNG/PDF)
- Constraint candidates list
- CRT diagram
- Workshop materials package

## Quality Checks
- Minimum 100 factors identified
- PESTLE balance verified
- Network connectivity validated
- At least 3 constraint candidates

## Next Steps
1. Review analysis results
2. Validate with advisors
3. Prepare workshop presentation
4. Schedule stakeholder sessions