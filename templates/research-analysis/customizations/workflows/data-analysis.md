# Data Analysis Workflow

## Purpose

Step-by-step workflow for analyzing research data covering data preparation, exploratory analysis, statistical testing, visualization, and interpretation.

## Context Required

- Research questions and hypotheses
- Data source and collection method
- Data format and structure
- Analysis tools and software
- Statistical significance threshold (typically α = 0.05)

## Workflow Stages

### Stage 1: Data Preparation

**Objectives**:
1. Import and organize data
2. Clean and validate data
3. Transform and engineer features
4. Document data processing

**Data Import**:

```python
# Example: Python/pandas
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('research/data/raw/study_data.csv')

# Initial inspection
print(df.head())
print(df.info())
print(df.describe())
```

**Tasks**:
- [ ] Import raw data files
- [ ] Inspect data structure (columns, types, dimensions)
- [ ] Document data dictionary (variable names, types, descriptions)
- [ ] Check for expected number of records
- [ ] Verify data matches collection protocol

**Data Cleaning**:

1. **Missing Data**:
   - Identify missing values
   - Determine pattern (MCAR, MAR, MNAR)
   - Decide handling: delete, impute, or flag
   - Document decisions

2. **Outliers**:
   - Identify using box plots, z-scores, or IQR
   - Investigate cause (error vs. genuine extreme)
   - Decide: keep, remove, or winsorize
   - Document decisions

3. **Data Quality**:
   - Check for duplicate records
   - Validate ranges (e.g., age 0-120)
   - Check categorical values match expected levels
   - Verify date formats and sequences
   - Cross-check related fields for consistency

4. **Transformations**:
   - Standardize text (case, whitespace)
   - Parse dates into proper format
   - Convert data types as needed
   - Create derived variables
   - Code categorical variables

**Tasks**:
- [ ] Handle missing values
- [ ] Address outliers
- [ ] Remove duplicates
- [ ] Validate data ranges
- [ ] Transform variables as needed
- [ ] Document all cleaning steps in script
- [ ] Save cleaned data separately

**Output**:
- Cleaned dataset: `research/data/processed/cleaned_data.csv`
- Data cleaning script: `research/data/scripts/01_data_cleaning.py`
- Data quality report: `research/data/reports/data_quality.md`

---

### Stage 2: Exploratory Data Analysis (EDA)

**Objectives**:
1. Understand data distributions
2. Identify patterns and relationships
3. Detect anomalies
4. Generate hypotheses

**Univariate Analysis**:

For each variable:
- Distribution (histogram, density plot)
- Central tendency (mean, median, mode)
- Spread (standard deviation, IQR, range)
- Shape (skewness, kurtosis)
- Frequencies for categorical variables

```python
# Example: Univariate exploration
df['age'].hist(bins=20)
print(df['age'].describe())

df['treatment_group'].value_counts()
```

**Bivariate Analysis**:

Examine relationships:
- Numeric vs. Numeric: Scatter plots, correlation
- Numeric vs. Categorical: Box plots, group means
- Categorical vs. Categorical: Cross-tabs, chi-square

```python
# Example: Bivariate exploration
df.plot.scatter(x='age', y='response_time')
df.groupby('treatment_group')['outcome'].describe()
pd.crosstab(df['gender'], df['response_category'])
```

**Multivariate Analysis**:

- Correlation matrices
- Pair plots
- Dimensionality reduction (PCA) if many variables
- Identify collinearity

**Tasks**:
- [ ] Create summary statistics tables
- [ ] Generate distribution plots for continuous variables
- [ ] Create frequency tables for categorical variables
- [ ] Examine bivariate relationships
- [ ] Create correlation matrix
- [ ] Identify potential confounders
- [ ] Document interesting patterns
- [ ] Save all exploratory plots

**Output**:
- EDA script: `research/data/scripts/02_exploratory_analysis.py`
- EDA report: `research/data/reports/exploratory_analysis.md`
- Exploratory figures: `research/data/figures/eda/`

---

### Stage 3: Statistical Testing

**Hypothesis Testing Framework**:

1. **State Hypotheses**:
   - Null hypothesis (H₀)
   - Alternative hypothesis (H₁ or Hₐ)
   - Specify one-tailed or two-tailed

2. **Choose Significance Level**:
   - Typically α = 0.05
   - Adjust for multiple comparisons if needed (Bonferroni, FDR)

3. **Select Appropriate Test**:
   - Based on data type, distribution, sample size
   - Check test assumptions

4. **Calculate Test Statistic**:
   - Run the statistical test
   - Obtain p-value

5. **Make Decision**:
   - Compare p-value to α
   - Reject or fail to reject H₀
   - Interpret in context

**Common Tests**:

**Comparing Groups**:
- Two groups, continuous: Independent t-test or Mann-Whitney U
- Paired samples: Paired t-test or Wilcoxon signed-rank
- Three+ groups: ANOVA or Kruskal-Wallis
- Post-hoc: Tukey HSD, Bonferroni

**Associations**:
- Two continuous: Pearson or Spearman correlation
- Two categorical: Chi-square test or Fisher's exact
- Categorical predictors, continuous outcome: Linear regression
- Binary outcome: Logistic regression

**Example**:

```python
from scipy import stats

# Independent t-test
group1 = df[df['treatment'] == 'A']['outcome']
group2 = df[df['treatment'] == 'B']['outcome']
t_stat, p_value = stats.ttest_ind(group1, group2)

print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.3f}")

if p_value < 0.05:
    print("Reject null hypothesis")
else:
    print("Fail to reject null hypothesis")
```

**Check Assumptions**:

Before testing, verify:
- Normality (for parametric tests): Shapiro-Wilk, Q-Q plots
- Homogeneity of variance: Levene's test
- Independence: Study design
- Sample size: Adequate power

**Tasks**:
- [ ] List all hypotheses to test
- [ ] Select appropriate statistical tests
- [ ] Check test assumptions
- [ ] Run statistical tests
- [ ] Adjust for multiple comparisons if needed
- [ ] Calculate effect sizes (Cohen's d, r, odds ratio)
- [ ] Document test results with statistics and p-values
- [ ] Interpret findings in context

**Output**:
- Statistical analysis script: `research/data/scripts/03_statistical_tests.py`
- Results table: `research/data/reports/statistical_results.csv`
- Test report: `research/data/reports/hypothesis_tests.md`

---

### Stage 4: Visualization

**Objectives**:
1. Communicate findings clearly
2. Reveal patterns and trends
3. Support narrative

**Visualization Types**:

**Distribution Plots**:
- Histogram: Single variable distribution
- Box plot: Distribution comparison across groups
- Violin plot: Distribution shape across groups
- Density plot: Smooth distribution curve

**Relationship Plots**:
- Scatter plot: Two continuous variables
- Line plot: Trends over time
- Regression plot: Relationship with fit line

**Comparison Plots**:
- Bar chart: Compare group means
- Error bars: Show uncertainty (SE, CI)
- Heatmap: Show matrix of values

**Best Practices**:

1. **Clarity**:
   - Clear titles and labels
   - Axis labels with units
   - Legend when needed
   - Appropriate scale (linear, log)

2. **Honesty**:
   - Start y-axis at zero (for bar charts)
   - Show full range of data
   - Include error bars or confidence intervals
   - Don't cherry-pick scales to exaggerate

3. **Aesthetics**:
   - Readable font sizes
   - Color-blind friendly palettes
   - Consistent style across figures
   - High resolution for publication

**Example**:

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication-quality style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 12

# Create visualization
fig, ax = plt.subplots()
sns.barplot(data=df, x='treatment_group', y='outcome',
            errorbar=('ci', 95), ax=ax)
ax.set_xlabel('Treatment Group')
ax.set_ylabel('Outcome Score (mean ± 95% CI)')
ax.set_title('Treatment Effect on Outcome')

# Save high-resolution figure
plt.savefig('research/data/figures/treatment_effect.png',
            dpi=300, bbox_inches='tight')
plt.show()
```

**Tasks**:
- [ ] Plan figures to include in report/paper
- [ ] Create distribution visualizations
- [ ] Create relationship visualizations
- [ ] Create comparison visualizations
- [ ] Add error bars and confidence intervals
- [ ] Ensure figures are publication-ready
- [ ] Save figures in high resolution
- [ ] Create figure captions
- [ ] Number figures sequentially

**Output**:
- Visualization script: `research/data/scripts/04_visualizations.py`
- Figures: `research/data/figures/`
- Figure captions: `research/data/reports/figure_captions.md`

---

### Stage 5: Interpretation and Validation

**Interpretation**:

1. **Statistical Significance**:
   - What is the p-value?
   - Do results support or refute hypothesis?
   - What is the strength of evidence?

2. **Practical Significance**:
   - What is the effect size?
   - Is the effect meaningful in real-world terms?
   - Clinical/practical relevance?

3. **Context**:
   - How do results compare to prior research?
   - Are findings surprising or expected?
   - What mechanisms might explain results?

4. **Limitations**:
   - Sample size adequate?
   - Potential confounders not controlled?
   - Generalizability concerns?
   - Measurement limitations?

**Validation**:

1. **Sensitivity Analysis**:
   - Re-run with outliers removed
   - Try different data transformations
   - Test with alternative statistical methods
   - Check if conclusions robust

2. **Assumption Checks**:
   - Verify test assumptions met
   - Check residuals for regression models
   - Test for violations

3. **Cross-Validation** (if applicable):
   - Split data into train/test
   - Validate model on holdout data
   - Check for overfitting

**Tasks**:
- [ ] Interpret statistical results
- [ ] Calculate and interpret effect sizes
- [ ] Consider practical significance
- [ ] Identify limitations
- [ ] Perform sensitivity analyses
- [ ] Validate key findings
- [ ] Relate findings to research questions
- [ ] Note unexpected results
- [ ] Document interpretation

**Output**:
- Interpretation notes: `research/data/reports/interpretation.md`
- Sensitivity analysis: `research/data/scripts/05_sensitivity_analysis.py`

---

### Stage 6: Reporting

**Analysis Report Components**:

1. **Methods**:
   - Data source and collection
   - Sample size and characteristics
   - Variables and measures
   - Statistical methods used
   - Software and packages

2. **Results**:
   - Descriptive statistics (Table 1)
   - Assumption checks
   - Statistical test results
   - Effect sizes and confidence intervals
   - Figures and tables

3. **Interpretation**:
   - Summary of findings
   - Relation to hypotheses
   - Comparison to prior work
   - Limitations
   - Implications

**Tables**:

Table 1 (Sample Characteristics):
| Variable | Group A (n=50) | Group B (n=48) | Total (n=98) |
|----------|----------------|----------------|--------------|
| Age (mean ± SD) | 34.2 ± 8.1 | 35.6 ± 7.9 | 34.9 ± 8.0 |
| Gender (% female) | 60% | 58% | 59% |

Table 2 (Statistical Results):
| Comparison | Test | Statistic | p-value | Effect Size |
|------------|------|-----------|---------|-------------|
| A vs B on outcome | t-test | t(96)=2.45 | 0.016 | d=0.50 |

**Reporting Statistics**:

Follow APA style (or field-specific):
- Include test statistic, df, p-value, effect size
- Example: "Group A scored significantly higher than Group B, t(96) = 2.45, p = .016, d = 0.50"

**Tasks**:
- [ ] Create summary tables
- [ ] Compile final figures
- [ ] Write methods section
- [ ] Write results section
- [ ] Report all statistical details
- [ ] Proofread for accuracy
- [ ] Ensure reproducibility (include code)

**Output**:
- Analysis report: `research/findings/data_analysis_report.md`
- Tables: `research/data/tables/`
- Supplementary materials: Analysis scripts, raw outputs

---

## Process Flow

```
Data Preparation
    ↓
Exploratory Data Analysis
    ↓
Check Assumptions
    ↓
Statistical Testing
    ↓
Visualization
    ↓
Interpretation
    ↓
Validation
    ↓
Reporting
    ↓
Final Analysis Report
```

---

## Using This Workflow

### As a Command

This file is designed to be used as a `.claude/commands/data-analysis.md` command.

**Usage**:
```
/data-analysis [stage]
```

**Examples**:
```
/data-analysis prepare
/data-analysis explore
/data-analysis test
/data-analysis visualize
```

### Integration with Task Management

Create tasks for each analysis stage:
- Task: "Prepare and clean research data" (difficulty: 5)
- Task: "Conduct exploratory data analysis" (difficulty: 4)
- Task: "Perform statistical hypothesis tests" (difficulty: 6)
- Task: "Create publication-quality visualizations" (difficulty: 4)
- Task: "Interpret results and validate findings" (difficulty: 5)
- Task: "Write data analysis report" (difficulty: 5)

---

## Tools and Software

### Python Ecosystem
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **scipy**: Statistical tests
- **statsmodels**: Advanced statistical models
- **matplotlib**: Basic plotting
- **seaborn**: Statistical visualization
- **scikit-learn**: Machine learning, validation

### R Ecosystem
- **dplyr**: Data manipulation
- **ggplot2**: Visualization
- **tidyr**: Data tidying
- **stats**: Built-in statistical tests
- **car**: Regression diagnostics
- **psych**: Psychometrics

### Other Tools
- **SPSS**: Point-and-click statistical software
- **Excel**: Basic analysis and tables
- **GraphPad Prism**: Scientific graphing
- **Jamovi**: Free SPSS alternative

### Notebooks
- **Jupyter**: Python/R interactive notebooks
- **R Markdown**: R analysis reports
- **Quarto**: Next-gen notebook format

---

## Statistical Test Selection Guide

**Choosing the Right Test**:

| Research Question | Data Types | Sample | Test |
|------------------|------------|--------|------|
| Compare 2 group means | Continuous | Independent | Independent t-test |
| Compare 2 group means | Continuous | Paired | Paired t-test |
| Compare 3+ group means | Continuous | Independent | One-way ANOVA |
| Compare groups (non-normal) | Ordinal/Continuous | Independent | Mann-Whitney U |
| Test association | 2 Continuous | - | Pearson/Spearman correlation |
| Test association | 2 Categorical | - | Chi-square test |
| Predict continuous outcome | Mixed | - | Linear regression |
| Predict binary outcome | Mixed | - | Logistic regression |

**Non-Parametric Alternatives**:
- t-test → Mann-Whitney U or Wilcoxon
- ANOVA → Kruskal-Wallis
- Pearson correlation → Spearman correlation

---

## Common Pitfalls to Avoid

1. **P-Hacking**: Don't test multiple ways until p < 0.05
2. **HARKing**: Hypothesizing After Results Known
3. **Ignoring Assumptions**: Check before running parametric tests
4. **Multiple Comparisons**: Adjust α when testing many hypotheses
5. **Confusing Significance**: Statistical ≠ practical significance
6. **Cherry-Picking**: Report all analyses, not just "significant" ones
7. **Correlation ≠ Causation**: Association doesn't imply causation
8. **Data Snooping**: Don't fit model on data you're testing on
9. **Incomplete Reporting**: Report effect sizes, CIs, not just p-values
10. **Overfitting**: Complex models on small samples

---

## Best Practices

### Reproducibility
1. **Script Everything**: No manual data manipulations
2. **Version Control**: Track changes with Git
3. **Document Decisions**: Why did you exclude outliers, etc.?
4. **Organize Files**: Clear folder structure
5. **Use Relative Paths**: Make code portable
6. **Comment Code**: Explain what and why
7. **Set Random Seeds**: For reproducible random processes

### Rigor
1. **Preregister**: Specify hypotheses and analysis plan before data collection
2. **Power Analysis**: Ensure adequate sample size
3. **Check Assumptions**: Don't blindly apply tests
4. **Report Everything**: Null results, failed assumptions, etc.
5. **Effect Sizes**: Always report, not just p-values
6. **Confidence Intervals**: Show uncertainty
7. **Sensitivity Analysis**: Test robustness of findings

### Clarity
1. **Clear Variable Names**: "age_years" not "var1"
2. **Document Data**: Data dictionary with all variables
3. **Annotate Code**: Future you will thank you
4. **Modular Scripts**: Separate cleaning, analysis, visualization
5. **Consistent Style**: Use style guides (PEP8, tidyverse)

---

## Output Location

**Cleaned Data**: `research/data/processed/cleaned_data.csv`

**Analysis Scripts**: `research/data/scripts/`
- `01_data_cleaning.py`
- `02_exploratory_analysis.py`
- `03_statistical_tests.py`
- `04_visualizations.py`
- `05_sensitivity_analysis.py`

**Reports**: `research/data/reports/`
- `data_quality.md`
- `exploratory_analysis.md`
- `hypothesis_tests.md`
- `interpretation.md`

**Figures**: `research/data/figures/`

**Tables**: `research/data/tables/`

**Final Report**: `research/findings/data_analysis_report.md`
