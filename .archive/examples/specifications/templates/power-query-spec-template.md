# [Your Project Name] - Power Query Specification

## What I'm Building

⚡ **Power Query** solution for [describe regulatory/calculation need]. This project will implement [specific calculation/transformation] using **M language** in **Excel**.

**Example**: "Power Query solution for pension regulatory calculations. This project will implement CEM-06 compliance reporting using M language in Excel."

## Technology Stack

⚡ Required (keep these for detection):
- **Power Query** (M language)
- **Excel** (version: [2016/2019/365])

Optional additions:
- Power BI Desktop (if creating dashboards)
- SQL Server (if connecting to database)
- SharePoint (if data source)

## Regulatory Context (if applicable)

⚡ **Regulatory calculation** details:
- Regulation/Standard: [e.g., CEM-06, Basel III, IFRS 17]
- Compliance deadline: [date]
- Reporting frequency: [monthly/quarterly/annual]
- Jurisdictions: [countries/regions]

## Goals

What do you want to achieve with this Power Query solution?

- [ ] Automate [specific calculation/report]
- [ ] Ensure compliance with [regulation]
- [ ] Replace manual Excel formulas with maintainable M code
- [ ] Create reproducible calculation workflow
- [ ] [Other goal]

## Timeline

Choose one:
- **Weekend project** (2-3 days)
- **Sprint** (1-2 weeks)
- **Multi-phase** (1-3 months)
- **Long-term** (3+ months with iterations)

**Deadline** (if applicable): [date]

## Data Sources

**Input data locations**:
1. [Excel file: path/name, sheet names]
2. [SQL database: server, database, tables]
3. [CSV files: location, format]
4. [SharePoint: site, list/library]

**Data refresh requirements**:
- Frequency: [manual/daily/weekly/monthly]
- Automation needed: [yes/no]

## Requirements & Deliverables

### Must Have (Critical)
1. [Specific calculation or transformation]
2. [Data validation rules]
3. [Output format requirements]
4. [Error handling for edge cases]

### Should Have (Important)
1. [Nice-to-have features]
2. [Additional validations]
3. [Documentation]

### Could Have (Optional)
1. [Future enhancements]
2. [Advanced features]

## Output Requirements

**Final output format**:
- File type: [Excel workbook/CSV/Power BI dataset]
- Sheet/table structure: [describe]
- Column specifications: [list key columns]
- Formatting requirements: [currency, dates, percentages]

**Sample output** (if available):
```
[Show example of expected output table structure]
```

## Known Challenges

⚡ **M language** complexity considerations:
- [ ] Complex date calculations
- [ ] Multi-source merges/joins
- [ ] Performance with large datasets (>100K rows)
- [ ] Dynamic column generation
- [ ] Error handling across transformations
- [ ] [Other M-specific challenges]

## Calculation Logic (if applicable)

**Formulas/algorithms to implement**:
1. [Formula name]: [description or actual formula]
2. [Calculation step]: [logic description]

**Example**:
```
Pension Value = (Salary × Years of Service × Accrual Rate) / 100
Where: Accrual Rate varies by employment type
```

## Validation Requirements

How will you verify correctness?
- [ ] Compare against existing manual calculations
- [ ] Test with sample data (describe test cases)
- [ ] Regulatory compliance checks
- [ ] Peer review by [domain expert]
- [ ] [Other validation methods]

## Additional Context

**Team/Stakeholders**:
- Primary user: [role/name]
- Reviewers: [who needs to approve]
- Domain experts: [who can clarify requirements]

**Existing documentation**:
- [Link to regulation text]
- [Link to calculation spec]
- [Link to existing Excel file]

**Special considerations**:
- [Anything else relevant]

---

## Detection Keywords Used ⚡

This template includes keywords that trigger Power Query template detection:
- "Power Query" (high confidence: 30pts)
- "M language" (high confidence: 30pts)
- "Excel" (medium confidence: 15pts)
- "regulatory calculation" (medium confidence: 15pts)

**Expected detection confidence**: 90%+ (auto-select)

## Tips for This Template

✅ **DO**:
- Mention specific regulations or compliance standards
- Describe actual formulas or calculation logic
- List exact data source paths/locations
- Include sample input/output examples
- Specify Excel version

❌ **DON'T**:
- Say just "data transformation" without mentioning Power Query
- Skip the regulatory context if this is compliance work
- Leave data sources vague
- Forget to describe M language challenges
