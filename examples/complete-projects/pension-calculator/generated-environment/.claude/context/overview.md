# Pension Calculator Power Query Project

## Purpose
Power Query solution for pension calculation and retirement planning using Excel/Power BI with complex financial formulas and data transformations.

## Core Components
- **Data Transformations**: Import, clean, validate, merge multiple sources
- **Custom M Functions**: Pension calculations, inflation projections, compound interest
- **DAX Measures**: Financial metrics, projections, scenario analysis
- **Data Model**: Star schema with fact and dimension tables

## Technical Stack
- **Platform**: Power Query in Excel/Power BI
- **Languages**: M (Power Query), DAX (Data Analysis Expressions)
- **Data Sources**: CSV, Excel, APIs, reference tables
- **Performance Target**: 10,000+ employee records, <30 second refresh

## Implementation Approach

### Phase 0: Ambiguity Resolution (CRITICAL)
- Stakeholder interviews for calculation rules
- Regulatory requirement clarification
- Edge case definition
- Data quality standards

### Phase 1: Data Foundation
- Connection setup
- Base transformations
- Validation rules

### Phase 2: Calculation Engine
- M functions for complex calculations
- DAX measures for reporting
- Testing with sample data

### Phase 3: Reporting
- Dashboard design
- Drill-through capabilities
- Interactive filters

## Power Query Challenges
- Iterative calculations in M
- Query folding optimization
- DAX circular dependencies
- Incremental refresh strategy

## Success Metrics
- Calculation accuracy within 0.01%
- Query refresh under 30 seconds
- Support for what-if scenarios
- Complete audit trail