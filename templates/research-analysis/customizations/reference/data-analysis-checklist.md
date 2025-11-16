# Data Analysis Checklist

## Overview

Use this checklist to ensure comprehensive, rigorous data analysis. Check off items as you complete them to maintain quality and avoid common mistakes.

## Pre-Analysis

### Research Design

- [ ] Research question is clearly defined
- [ ] Hypotheses are specific and testable
- [ ] Variables are operationalized
- [ ] Study design is appropriate for research question
- [ ] Sample size is justified (power analysis conducted)
- [ ] Potential confounds identified
- [ ] Ethics approval obtained (if applicable)

### Data Collection

- [ ] Data collection protocol documented
- [ ] Measurement instruments validated
- [ ] Data collection procedures standardized
- [ ] Quality control measures in place
- [ ] Data provenance documented (where data came from)
- [ ] Data use agreements/permissions secured

## Data Inspection

### Initial Review

- [ ] Data loaded successfully
- [ ] Correct number of rows/observations
- [ ] Correct number of columns/variables
- [ ] Variable names are meaningful and consistent
- [ ] Data types are correct (numeric, categorical, date, etc.)
- [ ] Units of measurement documented
- [ ] Codebook created (variable descriptions, value codes)

### Data Quality

- [ ] Checked for duplicate records
- [ ] Identified missing data patterns
- [ ] Missing data percentage calculated for each variable
- [ ] Missing data mechanism assessed (MCAR, MAR, MNAR)
- [ ] Outliers identified and investigated
- [ ] Data entry errors detected and corrected
- [ ] Range checks performed (values within expected range)
- [ ] Consistency checks across related variables
- [ ] Timestamps and dates validated

## Data Cleaning

### Missing Data

- [ ] Missing data handling strategy decided and justified
- [ ] Imputation method chosen (if applicable)
- [ ] Sensitivity analysis planned for missing data
- [ ] Documented what percentage of data is imputed
- [ ] Compared characteristics of complete vs. incomplete cases

### Outliers

- [ ] Outlier detection method specified
- [ ] Legitimate vs. error outliers distinguished
- [ ] Decision made: keep, remove, or transform
- [ ] Outlier handling documented and justified
- [ ] Sensitivity analysis planned with/without outliers

### Variable Cleaning

- [ ] Categorical variables checked for typos/inconsistencies
- [ ] Factor levels are meaningful and ordered (if ordinal)
- [ ] Text data cleaned (whitespace, case, encoding)
- [ ] Date/time variables parsed correctly
- [ ] Variable transformations documented
- [ ] Derived variables created with clear formulas

## Data Exploration

### Univariate Analysis

- [ ] Descriptive statistics calculated for all variables
- [ ] Distributions visualized (histograms, box plots, Q-Q plots)
- [ ] Normality assessed (for continuous variables)
- [ ] Skewness and kurtosis examined
- [ ] Frequency tables created (for categorical variables)
- [ ] Rare categories identified and handled

### Bivariate Analysis

- [ ] Correlations examined for key variable pairs
- [ ] Correlation matrix created and visualized
- [ ] Multicollinearity assessed (VIF for regression)
- [ ] Group differences explored
- [ ] Scatter plots created for continuous relationships
- [ ] Cross-tabulations for categorical relationships

### Multivariate Patterns

- [ ] Relationships among multiple variables explored
- [ ] Interaction effects considered
- [ ] Subgroup patterns identified
- [ ] Clustering or natural groupings explored (if relevant)

## Analysis Preparation

### Assumptions

- [ ] Statistical assumptions identified for chosen tests
- [ ] Assumption checks performed and documented
- [ ] Violations noted and addressed
- [ ] Alternative methods considered if assumptions violated
- [ ] Transformations applied if needed (log, square root, etc.)

### Sample Definition

- [ ] Inclusion/exclusion criteria applied
- [ ] Final analytic sample size determined
- [ ] Attrition/dropout analyzed
- [ ] Comparison of included vs. excluded cases
- [ ] Sample representativeness assessed

## Statistical Analysis

### Test Selection

- [ ] Statistical methods appropriate for research question
- [ ] Tests match data types (continuous, categorical, etc.)
- [ ] Tests appropriate for sample size
- [ ] One-tailed vs. two-tailed decision justified
- [ ] Significance level (α) set a priori
- [ ] Multiple testing correction considered

### Execution

- [ ] Analysis code is documented and commented
- [ ] Random seeds set for reproducibility
- [ ] Analysis follows pre-registered plan (if applicable)
- [ ] Deviations from analysis plan documented and justified
- [ ] Results saved and backed up
- [ ] Analysis can be reproduced from code

### Results Documentation

- [ ] Test statistics reported (t, F, χ², etc.)
- [ ] Degrees of freedom reported
- [ ] p-values reported (exact values, not just < .05)
- [ ] Effect sizes calculated and reported
- [ ] Confidence intervals reported
- [ ] Sample sizes for each analysis reported
- [ ] Tables formatted following style guide
- [ ] Figures are clear and publication-ready

## Model Building (if applicable)

### Model Specification

- [ ] Theoretical justification for model structure
- [ ] All relevant predictors included
- [ ] Interaction terms considered
- [ ] Non-linear relationships tested if appropriate
- [ ] Model complexity appropriate for sample size

### Model Fitting

- [ ] Estimation method justified
- [ ] Convergence achieved
- [ ] Model fit indices reported
- [ ] Residuals examined
- [ ] Influential cases identified (Cook's D, leverage)
- [ ] Goodness-of-fit assessed

### Model Comparison

- [ ] Alternative models tested
- [ ] Model comparison criteria applied (AIC, BIC, R²)
- [ ] Nested models compared (likelihood ratio test)
- [ ] Parsimony considered (Occam's razor)
- [ ] Best model selected and justified

### Model Validation

- [ ] Cross-validation performed (if predictive model)
- [ ] Training/test split appropriate
- [ ] Overfitting assessed
- [ ] Model generalization evaluated
- [ ] External validation (if data available)

## Sensitivity Analysis

### Robustness Checks

- [ ] Alternative specifications tested
- [ ] Different outlier handling approaches compared
- [ ] Different missing data methods compared
- [ ] Different variable transformations compared
- [ ] Subgroup analyses conducted
- [ ] Consistency of findings across approaches documented

### Assumptions

- [ ] Sensitivity to assumption violations tested
- [ ] Bootstrap or permutation methods used if appropriate
- [ ] Bayesian sensitivity analysis (if Bayesian approach)

## Interpretation

### Results

- [ ] Results interpreted in context of research question
- [ ] Statistical significance vs. practical significance distinguished
- [ ] Effect sizes interpreted (small, medium, large)
- [ ] Confidence intervals interpreted
- [ ] Null findings not dismissed (absence of evidence ≠ evidence of absence)
- [ ] Unexpected findings explored

### Causality

- [ ] Causal language used only if justified by design
- [ ] Confounds and alternative explanations considered
- [ ] Limitations to causal inference acknowledged
- [ ] Correlation vs. causation clearly distinguished

### Generalization

- [ ] Population to which results generalize specified
- [ ] Limitations to generalizability noted
- [ ] Sample representativeness discussed
- [ ] Setting and context considered

## Reporting

### Transparency

- [ ] All analyses reported, not just significant ones
- [ ] Pre-registered vs. exploratory analyses distinguished
- [ ] Deviations from analysis plan explained
- [ ] Null results reported
- [ ] Limitations discussed honestly

### Reproducibility

- [ ] Code is organized and commented
- [ ] Data and code archived
- [ ] Software versions documented
- [ ] Computational environment described
- [ ] Random seeds recorded
- [ ] Supplementary materials prepared (if needed)

### Compliance

- [ ] Reporting follows field standards (APA, CONSORT, STROBE, etc.)
- [ ] Journal guidelines followed
- [ ] All required information included
- [ ] Tables and figures follow style guide
- [ ] References formatted correctly

## Documentation

### Analysis Files

- [ ] Raw data preserved (never modified)
- [ ] Cleaning script documented
- [ ] Analysis script documented
- [ ] Output files organized
- [ ] Version control used (Git recommended)
- [ ] README file explains file organization

### Metadata

- [ ] Variable definitions documented (codebook)
- [ ] Data transformations logged
- [ ] Analysis decisions logged with rationale
- [ ] Software and package versions recorded
- [ ] Analysis date and analyst name recorded

## Ethical Considerations

### Data Privacy

- [ ] Personally identifiable information removed
- [ ] Data de-identified appropriately
- [ ] Data storage is secure
- [ ] Data sharing plan follows IRB approval
- [ ] Participant consent covers intended analyses

### Research Integrity

- [ ] No p-hacking (trying many tests until finding significance)
- [ ] No HARKing (hypothesizing after results known)
- [ ] No selective reporting of favorable results
- [ ] Conflicts of interest disclosed
- [ ] Proper attribution for collaborators and data sources

## Peer Review

### Internal Review

- [ ] Results reviewed by colleague or collaborator
- [ ] Code reviewed for errors
- [ ] Interpretation reviewed for bias or overreach
- [ ] Feedback incorporated

### External Review

- [ ] Ready for journal submission or conference presentation
- [ ] Supplementary materials prepared
- [ ] Pre-print posted (if appropriate)
- [ ] Data/code sharing plan in place

## Post-Analysis

### Archival

- [ ] Data archived in appropriate repository
- [ ] Code archived (GitHub, OSF, institutional repository)
- [ ] Analysis registered/documented (OSF, AsPredicted)
- [ ] Materials shared or made available upon request

### Follow-Up

- [ ] Unexpected findings flagged for follow-up
- [ ] Limitations inform future research design
- [ ] Replication study planned (if warranted)
- [ ] Results communicated to stakeholders

## Common Pitfalls to Avoid

**Data Issues**:
- [ ] Not checking for duplicates
- [ ] Ignoring missing data patterns
- [ ] Blindly removing outliers
- [ ] Not documenting data transformations

**Analysis Errors**:
- [ ] Using wrong test for data type
- [ ] Ignoring violated assumptions
- [ ] Not correcting for multiple comparisons
- [ ] Confusing correlation and causation

**Interpretation Mistakes**:
- [ ] Over-interpreting small effects
- [ ] Treating non-significance as proof of no effect
- [ ] Ignoring practical significance
- [ ] Generalizing beyond the sample

**Reporting Problems**:
- [ ] Only reporting significant results
- [ ] Not reporting effect sizes
- [ ] Not providing enough detail to replicate
- [ ] Cherry-picking results

## Resources

### Statistical Software Packages

**Python**:
- pandas, NumPy (data manipulation)
- scipy.stats (statistical tests)
- statsmodels (regression, time series)
- scikit-learn (machine learning)

**R**:
- tidyverse (data manipulation and visualization)
- stats (base statistical functions)
- lme4 (mixed effects models)
- ggplot2 (visualization)

**Other**:
- SPSS (point-and-click statistical software)
- SAS (enterprise statistics)
- Stata (econometrics, biostatistics)

### Reporting Guidelines

- CONSORT (randomized trials)
- STROBE (observational studies)
- PRISMA (systematic reviews)
- TRIPOD (prediction models)
- APA Publication Manual (psychology)

### Learning Resources

- Statistics textbooks for your field
- Cross Validated (stats.stackexchange.com)
- Online courses (Coursera, DataCamp, etc.)
- Statistical consulting services
