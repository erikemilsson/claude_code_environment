# Literature Search Command

## Purpose
Execute systematic literature search across databases with documented strategy.

## Context Required
- Search terms defined
- Inclusion/exclusion criteria set
- Databases selected
- Date range specified

## Process

### 1. Prepare Search String
```
("climate change" OR "global warming" OR "temperature rise")
AND
("coastal ecosystem" OR "marine ecosystem" OR "intertidal")
AND
("biodiversity" OR "species richness" OR "species diversity")
```

### 2. Execute Database Queries
- Web of Science: Advanced search
- Scopus: Document search
- PubMed: MeSH terms + keywords
- Google Scholar: Supplementary search

### 3. Document Search Results
- Database name
- Search string used
- Date of search
- Number of results
- Filters applied

### 4. Export Results
- RIS format for reference manager
- CSV for screening spreadsheet
- Save search history

### 5. Remove Duplicates
- Import to reference manager
- Identify duplicates
- Document removal count

## Output Location
- `.claude/data/literature/search-results/`
- `.claude/data/literature/search-log.md`
- `.claude/context/search-strategy.md`

## PRISMA Compliance
- Document all search strategies
- Save database screenshots
- Record exact search dates
- Note any database limitations