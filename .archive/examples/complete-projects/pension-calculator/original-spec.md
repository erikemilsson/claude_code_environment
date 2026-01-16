# Pension Calculator Power Query Project

## Project Overview
Create a Power Query solution for pension calculation and retirement planning using Excel/Power BI with complex financial formulas and data transformations.

## Requirements

### Business Requirements
1. **Pension Calculations**
   - Calculate pension benefits based on contribution history
   - Project future pension values with inflation
   - Compare different retirement scenarios
   - Analyze optimal retirement age

2. **Data Sources**
   - Employee contribution data (CSV/Excel)
   - Historical inflation rates (API/Excel)
   - Investment return rates (Market data)
   - Government pension rules (Reference tables)

3. **Reporting**
   - Individual pension statements
   - Scenario comparison dashboard
   - Risk analysis reports
   - Regulatory compliance reports

### Technical Requirements
- **Platform**: Power Query in Excel/Power BI
- **Data Model**: Star schema with fact and dimension tables
- **DAX Measures**: Complex financial calculations
- **M Code**: Custom transformations and functions
- **Performance**: Handle 10,000+ employee records

## Power Query Components

### Data Transformations
1. **Import and Clean**
   - Standardize date formats
   - Handle missing values
   - Validate contribution amounts
   - Merge multiple data sources

2. **Custom Functions (M)**
   - `fnCalculatePension`: Core pension calculation
   - `fnProjectInflation`: Inflation adjustment
   - `fnCompoundInterest`: Investment growth
   - `fnTaxCalculation`: Tax implications

3. **DAX Measures**
   - Total Contributions
   - Projected Pension Value
   - Replacement Ratio
   - Break-even Analysis

### Data Model
```
FactContributions
├── EmployeeKey
├── DateKey
├── ContributionAmount
├── EmployerMatch
└── InvestmentReturn

DimEmployee
├── EmployeeKey
├── Name
├── BirthDate
├── HireDate
└── SalaryGrade

DimDate
├── DateKey
├── Year
├── Quarter
├── Month
└── FiscalPeriod

DimScenario
├── ScenarioKey
├── RetirementAge
├── ContributionRate
└── ExpectedReturn
```

## Implementation Phases

### Phase 0: Ambiguity Resolution
- Interview stakeholders about calculation rules
- Clarify regulatory requirements
- Define edge cases (early retirement, disabilities)
- Establish data quality standards

### Phase 1: Data Foundation
- Set up data connections
- Create base transformations
- Implement data validation

### Phase 2: Calculation Engine
- Build M functions for calculations
- Create DAX measures
- Test with sample data

### Phase 3: Reporting
- Design dashboard layouts
- Create drill-through pages
- Add slicers and filters

## Success Criteria
- Calculations match manual verification within 0.01%
- Query refresh under 30 seconds
- Support what-if scenarios
- Audit trail for all calculations

## Power Query Specific Challenges
- Handling iterative calculations in M
- Managing query folding for performance
- Dealing with circular dependencies in DAX
- Optimizing for incremental refresh