# Data Analysis Workflow

## Purpose

This command guides you through a structured data analysis process from data acquisition through result interpretation and validation. Following this workflow ensures reproducible, rigorous, and well-documented analysis.

## Context Required

- Research question or hypothesis to test
- Data source and format
- Analysis environment setup (Python, R, etc.)
- Statistical background knowledge for chosen methods

## Process

### Phase 1: Data Acquisition

#### 1.1 Obtain Data

**Sources**:
- Experimental data collection
- Survey responses
- Public datasets (Kaggle, UCI ML Repository, government data)
- API calls
- Web scraping
- Database queries

**Documentation**:
```markdown
## Data Acquisition Log

**Source**: [Where data came from]
**Date Obtained**: [YYYY-MM-DD]
**Version**: [If applicable]
**Format**: [CSV, JSON, Excel, SQL database, etc.]
**Size**: [Number of rows/observations]
**Variables**: [Number of columns/variables]
**License**: [Usage restrictions]
**Citation**: [How to cite this data]
```

#### 1.2 Load Data

**Python Example**:
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/raw/dataset.csv')

# Initial inspection
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.head())
print(df.info())
```

**R Example**:
```r
library(tidyverse)

# Load data
df <- read_csv('data/raw/dataset.csv')

# Initial inspection
dim(df)
glimpse(df)
head(df)
summary(df)
```

### Phase 2: Data Exploration

#### 2.1 Understand Data Structure

**Questions to Answer**:
- What is the unit of observation? (person, time point, transaction, etc.)
- How many observations?
- What variables are included?
- What are the data types? (numeric, categorical, date, text)
- Are there identifiers or keys?
- Is there a time dimension?

#### 2.2 Univariate Analysis

Examine each variable individually.

**Numeric Variables**:
```python
# Descriptive statistics
df.describe()

# Distribution visualization
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.hist(df['variable_name'], bins=30)
plt.title('Histogram')

plt.subplot(1, 3, 2)
plt.boxplot(df['variable_name'].dropna())
plt.title('Box Plot')

plt.subplot(1, 3, 3)
from scipy import stats
stats.probplot(df['variable_name'].dropna(), dist="norm", plot=plt)
plt.title('Q-Q Plot')
plt.tight_layout()
plt.show()
```

**Categorical Variables**:
```python
# Frequency tables
df['category_var'].value_counts()
df['category_var'].value_counts(normalize=True)  # Proportions

# Visualization
df['category_var'].value_counts().plot(kind='bar')
plt.title('Category Distribution')
plt.show()
```

#### 2.3 Bivariate Analysis

Examine relationships between variables.

**Numeric vs. Numeric**:
```python
# Correlation
correlation = df[['var1', 'var2']].corr()
print(correlation)

# Scatter plot
plt.scatter(df['var1'], df['var2'])
plt.xlabel('Variable 1')
plt.ylabel('Variable 2')
plt.title('Relationship between Var1 and Var2')
plt.show()
```

**Categorical vs. Numeric**:
```python
# Group comparisons
df.groupby('category')['numeric_var'].describe()

# Box plots
sns.boxplot(data=df, x='category', y='numeric_var')
plt.show()
```

**Categorical vs. Categorical**:
```python
# Cross-tabulation
pd.crosstab(df['cat_var1'], df['cat_var2'])

# With proportions
pd.crosstab(df['cat_var1'], df['cat_var2'], normalize='all')
```

#### 2.4 Identify Patterns and Anomalies

- Unexpected values or ranges
- Outliers (values far from the distribution)
- Missing data patterns
- Skewed distributions
- Interesting relationships
- Subgroup differences

### Phase 3: Data Cleaning

#### 3.1 Handle Missing Data

**Assess Missingness**:
```python
# Count missing values
missing_counts = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100

missing_summary = pd.DataFrame({
    'Missing_Count': missing_counts,
    'Percentage': missing_percent
})
print(missing_summary[missing_summary['Missing_Count'] > 0])

# Visualize missing patterns
import missingno as msno
msno.matrix(df)
plt.show()
```

**Missing Data Mechanisms**:
- **MCAR** (Missing Completely At Random): Missingness unrelated to any variables
- **MAR** (Missing At Random): Missingness related to observed variables
- **MNAR** (Missing Not At Random): Missingness related to unobserved values

**Handling Strategies**:

**1. Deletion**:
```python
# Listwise deletion (complete case analysis)
df_complete = df.dropna()

# Variable deletion (if >50% missing)
df_cleaned = df.loc[:, df.isnull().mean() < 0.5]
```

**2. Imputation**:
```python
# Mean/median imputation
df['numeric_var'].fillna(df['numeric_var'].mean(), inplace=True)

# Mode imputation (categorical)
df['cat_var'].fillna(df['cat_var'].mode()[0], inplace=True)

# Forward/backward fill (time series)
df['time_series_var'].fillna(method='ffill', inplace=True)

# Multiple imputation (more sophisticated)
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

imputer = IterativeImputer(random_state=42)
df_imputed = pd.DataFrame(
    imputer.fit_transform(df[numeric_columns]),
    columns=numeric_columns
)
```

#### 3.2 Handle Outliers

**Detection**:
```python
# IQR method
Q1 = df['var'].quantile(0.25)
Q3 = df['var'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['var'] < lower_bound) | (df['var'] > upper_bound)]
print(f"Number of outliers: {len(outliers)}")

# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(df['var'].dropna()))
outliers = df[z_scores > 3]
```

**Treatment**:
- **Remove**: If data errors or extreme cases not of interest
- **Transform**: Log, square root to reduce skew
- **Winsorize**: Cap at percentile (e.g., 1st and 99th)
- **Keep**: If legitimate values, report sensitivity analyses

```python
# Winsorization
from scipy.stats.mstats import winsorize
df['var_winsorized'] = winsorize(df['var'], limits=[0.01, 0.01])

# Transformation
df['var_log'] = np.log(df['var'] + 1)  # +1 if values include 0
```

#### 3.3 Data Type Corrections

```python
# Convert to appropriate types
df['date_var'] = pd.to_datetime(df['date_var'])
df['category_var'] = df['category_var'].astype('category')
df['numeric_var'] = pd.to_numeric(df['numeric_var'], errors='coerce')

# Ensure proper encoding
df['categorical_var'] = df['categorical_var'].str.strip()  # Remove whitespace
df['categorical_var'] = df['categorical_var'].str.lower()  # Standardize case
```

#### 3.4 Duplicates

```python
# Identify duplicates
duplicates = df[df.duplicated()]
print(f"Number of duplicate rows: {len(duplicates)}")

# Check duplicates on specific columns
duplicates = df[df.duplicated(subset=['id', 'date'])]

# Remove duplicates
df_unique = df.drop_duplicates()
```

### Phase 4: Data Transformation

#### 4.1 Feature Engineering

**Create New Variables**:
```python
# Derived variables
df['bmi'] = df['weight_kg'] / (df['height_m'] ** 2)

# Binning continuous variables
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 65, 100],
                         labels=['<18', '18-34', '35-49', '50-64', '65+'])

# Interaction terms
df['income_x_education'] = df['income'] * df['education_years']

# Time-based features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
```

**Encoding Categorical Variables**:
```python
# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['categorical_var'], drop_first=True)

# Label encoding (for ordinal)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['ordinal_encoded'] = le.fit_transform(df['ordinal_var'])
```

#### 4.2 Scaling and Normalization

**When Needed**:
- Machine learning algorithms (especially distance-based)
- Variables on different scales
- Gradient descent optimization

**Methods**:
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Standardization (z-score): mean=0, sd=1
scaler = StandardScaler()
df[['var1_scaled', 'var2_scaled']] = scaler.fit_transform(df[['var1', 'var2']])

# Min-Max scaling: range [0, 1]
scaler = MinMaxScaler()
df[['var1_scaled', 'var2_scaled']] = scaler.fit_transform(df[['var1', 'var2']])

# Robust scaling: less sensitive to outliers
scaler = RobustScaler()
df[['var1_scaled', 'var2_scaled']] = scaler.fit_transform(df[['var1', 'var2']])
```

### Phase 5: Statistical Analysis

#### 5.1 Choose Appropriate Test

**Decision Tree**:
- **Outcome Variable Type**:
  - Continuous → Regression, t-test, ANOVA
  - Binary → Logistic regression, chi-square
  - Count → Poisson regression
  - Categorical → Chi-square, multinomial regression
  - Time-to-event → Survival analysis

- **Number of Groups**:
  - 2 groups → t-test, Mann-Whitney U
  - 3+ groups → ANOVA, Kruskal-Wallis

- **Predictor Type**:
  - Continuous → Correlation, regression
  - Categorical → t-test, ANOVA, chi-square
  - Mixed → ANCOVA, multiple regression

#### 5.2 Check Assumptions

**Example: Independent samples t-test**

**Assumptions**:
1. Independence of observations
2. Normality (or large N)
3. Homogeneity of variance

**Checking**:
```python
from scipy import stats

# 1. Independence: Ensured by study design

# 2. Normality
group1 = df[df['group'] == 'A']['outcome']
group2 = df[df['group'] == 'B']['outcome']

# Shapiro-Wilk test
stat, p = stats.shapiro(group1)
print(f"Group 1 Shapiro-Wilk p-value: {p}")

# Visual check
stats.probplot(group1, dist="norm", plot=plt)
plt.title('Q-Q Plot Group 1')
plt.show()

# 3. Homogeneity of variance (Levene's test)
stat, p = stats.levene(group1, group2)
print(f"Levene's test p-value: {p}")
```

**If Assumptions Violated**:
- Normality → Non-parametric test (Mann-Whitney U)
- Unequal variances → Welch's t-test
- Both → Non-parametric test

#### 5.3 Run Analysis

**t-test Example**:
```python
# Independent samples t-test
t_stat, p_value = stats.ttest_ind(group1, group2)

# Effect size (Cohen's d)
def cohens_d(x, y):
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(
        ((nx-1)*np.std(x, ddof=1)**2 + (ny-1)*np.std(y, ddof=1)**2) / dof
    )

d = cohens_d(group1, group2)

print(f"t({len(group1)+len(group2)-2}) = {t_stat:.3f}, p = {p_value:.4f}")
print(f"Cohen's d = {d:.3f}")
```

**Regression Example**:
```python
import statsmodels.api as sm

# Prepare data
X = df[['predictor1', 'predictor2']]
X = sm.add_constant(X)  # Add intercept
y = df['outcome']

# Fit model
model = sm.OLS(y, X).fit()

# Results
print(model.summary())

# Predictions
predictions = model.predict(X)

# Residual diagnostics
residuals = y - predictions
plt.scatter(predictions, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()
```

#### 5.4 Interpret Results

**Report**:
- Test statistic and degrees of freedom
- p-value
- Effect size and confidence interval
- Descriptive statistics for each group
- Visualization

**Example Interpretation**:
```markdown
## Analysis Results

### Hypothesis
H₀: No difference in test scores between treatment and control groups
H₁: Treatment group has higher scores than control group

### Descriptive Statistics
| Group     | N  | Mean  | SD   | SE   |
|-----------|----|-------|------|------|
| Treatment | 50 | 82.4  | 8.2  | 1.16 |
| Control   | 50 | 76.8  | 9.1  | 1.29 |

### Inferential Statistics
- **Test**: Independent samples t-test
- **Result**: t(98) = 3.21, p = 0.002
- **Effect Size**: Cohen's d = 0.64 (medium effect)
- **95% CI for difference**: [2.1, 9.1]

### Interpretation
The treatment group scored significantly higher than the control group,
t(98) = 3.21, p = 0.002, d = 0.64. The mean difference was 5.6 points
(95% CI: [2.1, 9.1]), representing a medium effect size.
```

### Phase 6: Validation

#### 6.1 Sensitivity Analyses

Test robustness of findings:

**Alternative Specifications**:
```python
# Without outliers
df_no_outliers = df[np.abs(stats.zscore(df['outcome'])) < 3]
# Re-run analysis

# Different transformations
df['outcome_log'] = np.log(df['outcome'])
# Re-run analysis

# Different control variables
# Add/remove covariates and re-run
```

#### 6.2 Cross-Validation (for predictive models)

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

model = LinearRegression()
scores = cross_val_score(model, X, y, cv=5, scoring='r2')

print(f"Cross-validated R²: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

#### 6.3 Bootstrapping (for confidence intervals)

```python
from scipy.stats import bootstrap

# Bootstrap confidence interval for mean difference
def statistic(x, y):
    return np.mean(x) - np.mean(y)

rng = np.random.default_rng(seed=42)
res = bootstrap((group1, group2), statistic, n_resamples=10000,
                random_state=rng, method='percentile')

print(f"Bootstrap 95% CI: [{res.confidence_interval.low:.2f}, "
      f"{res.confidence_interval.high:.2f}]")
```

### Phase 7: Documentation

#### 7.1 Analysis Script

Include:
- Comments explaining each step
- Session info (package versions)
- Random seeds for reproducibility
- Output saved to files

```python
# At top of script
import sys
print(f"Python version: {sys.version}")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")

# For reproducibility
np.random.seed(42)

# Save outputs
results.to_csv('output/analysis_results.csv', index=False)
plt.savefig('output/figures/result_plot.png', dpi=300, bbox_inches='tight')
```

#### 7.2 Analysis Report

```markdown
# Data Analysis Report: [Study Title]

## 1. Introduction
- Research question
- Hypotheses
- Overview of analysis approach

## 2. Data
- Source and collection method
- Sample size and characteristics
- Variables included

## 3. Data Preparation
- Missing data handling
- Outlier treatment
- Transformations applied
- Final sample for analysis

## 4. Descriptive Statistics
- Sample characteristics
- Variable distributions
- Bivariate relationships

## 5. Analytical Methods
- Statistical tests used
- Justification for test selection
- Assumption checks
- Significance level

## 6. Results
- Main findings for each hypothesis
- Effect sizes and confidence intervals
- Tables and figures

## 7. Sensitivity Analyses
- Alternative specifications tested
- Robustness of findings

## 8. Limitations
- Data limitations
- Statistical limitations
- Generalizability constraints

## 9. Conclusions
- Summary of key findings
- Implications
- Future directions
```

## Output Location

- **Cleaned data**: `data/processed/cleaned_data.csv`
- **Analysis scripts**: `analysis/analysis_script.py` or `.R`
- **Results**: `output/analysis_results.csv`
- **Figures**: `output/figures/`
- **Report**: `output/analysis_report.md`

## Best Practices

1. **Version control**: Track all code and major data versions
2. **Reproducibility**: Document environment, use seeds, save session info
3. **Transparency**: Report all analyses, not just significant ones
4. **Effect sizes**: Always report alongside p-values
5. **Visualize**: Create plots for key findings
6. **Validate**: Run sensitivity analyses and diagnostics
7. **Document**: Comment code, write clear reports
8. **Collaborate**: Have analyses reviewed by colleague

## Common Pitfalls

- **p-hacking**: Running many tests until finding significance
- **HARKing**: Hypothesizing after results are known
- **Ignoring assumptions**: Using tests without checking assumptions
- **Confusing significance with importance**: Small p-value ≠ large effect
- **Multiple testing**: Not adjusting for multiple comparisons
- **Data leakage**: Using test data in training (machine learning)
- **Cherry-picking**: Only reporting favorable results
