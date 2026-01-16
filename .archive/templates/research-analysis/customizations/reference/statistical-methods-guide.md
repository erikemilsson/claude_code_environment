# Statistical Methods Guide

## Overview

This guide helps you select appropriate statistical methods based on your research question, data characteristics, and study design. It provides decision trees, method descriptions, and implementation guidance.

## Method Selection Framework

### Key Questions

1. **What is your research goal?**
   - Describe/summarize data → Descriptive statistics
   - Test hypothesis about groups → Inferential tests
   - Examine relationships → Correlation/regression
   - Predict outcomes → Predictive modeling
   - Classify cases → Classification methods

2. **What type of outcome variable?**
   - Continuous (e.g., height, test score) → t-test, ANOVA, linear regression
   - Binary (yes/no) → Chi-square, logistic regression
   - Categorical (>2 categories) → Chi-square, multinomial regression
   - Count (0, 1, 2, 3...) → Poisson regression
   - Time-to-event → Survival analysis
   - Ordinal (ranked categories) → Ordinal regression, non-parametric tests

3. **How many groups/conditions?**
   - 1 group → One-sample tests
   - 2 groups → t-test, Mann-Whitney U
   - 3+ groups → ANOVA, Kruskal-Wallis

4. **Independent or related groups?**
   - Independent → Between-subjects tests
   - Related (same participants, matched pairs) → Within-subjects/paired tests

5. **What type of predictor variables?**
   - Continuous → Correlation, regression
   - Categorical → ANOVA, t-test
   - Mixed → ANCOVA, multiple regression

## Descriptive Statistics

### Continuous Variables

**Measures of Central Tendency**:
- **Mean**: Average; sensitive to outliers
- **Median**: Middle value; robust to outliers
- **Mode**: Most frequent value

**When to Use**:
- Mean: Normal/symmetric distributions
- Median: Skewed distributions or outliers
- Mode: Categorical data, multimodal distributions

**Measures of Dispersion**:
- **Standard Deviation (SD)**: Average distance from mean
- **Variance**: SD squared
- **Range**: Max - Min
- **Interquartile Range (IQR)**: 75th - 25th percentile

**Python Example**:
```python
import numpy as np

mean = np.mean(data)
median = np.median(data)
std = np.std(data, ddof=1)  # Sample SD
q25, q75 = np.percentile(data, [25, 75])
iqr = q75 - q25
```

**Reporting**:
- Normal distribution: M = 75.3, SD = 8.2
- Skewed distribution: Mdn = 45.0, IQR = 23.5

### Categorical Variables

**Frequency Tables**:
- Counts and proportions for each category

**Python Example**:
```python
import pandas as pd

freq_table = df['category'].value_counts()
prop_table = df['category'].value_counts(normalize=True)
```

**Reporting**:
- Table with counts and percentages
- Bar chart or pie chart (use sparingly)

## Comparing Groups

### Two Independent Groups

#### Independent Samples t-test

**Use When**:
- Outcome: Continuous
- Groups: 2 independent groups
- Assumptions: Normality, equal variances (or use Welch's t-test)

**Hypotheses**:
- H₀: μ₁ = μ₂ (group means are equal)
- H₁: μ₁ ≠ μ₂ (group means differ)

**Python Example**:
```python
from scipy import stats

group1 = df[df['group'] == 'A']['outcome']
group2 = df[df['group'] == 'B']['outcome']

# Check normality
stat, p = stats.shapiro(group1)
print(f"Group 1 normality: p = {p:.4f}")

# Check equal variances
stat, p = stats.levene(group1, group2)
print(f"Levene's test: p = {p:.4f}")

# t-test (assumes equal variances)
t_stat, p_value = stats.ttest_ind(group1, group2)

# Welch's t-test (unequal variances)
t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

# Effect size (Cohen's d)
pooled_std = np.sqrt(((len(group1)-1)*np.var(group1, ddof=1) +
                      (len(group2)-1)*np.var(group2, ddof=1)) /
                     (len(group1) + len(group2) - 2))
d = (np.mean(group1) - np.mean(group2)) / pooled_std

print(f"t({len(group1)+len(group2)-2}) = {t_stat:.3f}, p = {p_value:.4f}")
print(f"Cohen's d = {d:.3f}")
```

**Reporting**:
"An independent samples t-test revealed that Group A (M = 75.3, SD = 8.2) scored significantly higher than Group B (M = 68.5, SD = 9.1), t(98) = 3.94, p < .001, d = 0.79."

#### Mann-Whitney U Test

**Use When**:
- t-test assumptions violated (non-normal distributions)
- Ordinal data
- Small sample sizes

**Non-parametric alternative** to independent samples t-test.

**Python Example**:
```python
u_stat, p_value = stats.mannwhitneyu(group1, group2, alternative='two-sided')
print(f"U = {u_stat}, p = {p_value:.4f}")

# Effect size (r)
n1, n2 = len(group1), len(group2)
z = stats.norm.ppf(p_value / 2)  # Convert p to z
r = abs(z) / np.sqrt(n1 + n2)
print(f"Effect size r = {r:.3f}")
```

### Two Related Groups

#### Paired Samples t-test

**Use When**:
- Same participants measured twice (pre-post)
- Matched pairs
- Outcome: Continuous
- Assumption: Differences are normally distributed

**Python Example**:
```python
pre = df['pre_test']
post = df['post_test']

# Check normality of differences
differences = post - pre
stat, p = stats.shapiro(differences)
print(f"Normality of differences: p = {p:.4f}")

# Paired t-test
t_stat, p_value = stats.ttest_rel(post, pre)

# Effect size
d = np.mean(differences) / np.std(differences, ddof=1)

print(f"t({len(differences)-1}) = {t_stat:.3f}, p = {p_value:.4f}")
print(f"Cohen's d = {d:.3f}")
```

#### Wilcoxon Signed-Rank Test

**Non-parametric alternative** to paired t-test.

**Python Example**:
```python
w_stat, p_value = stats.wilcoxon(post, pre)
print(f"W = {w_stat}, p = {p_value:.4f}")
```

### Three or More Groups

#### One-Way ANOVA

**Use When**:
- Outcome: Continuous
- Groups: 3+ independent groups
- Assumptions: Normality, equal variances

**Hypotheses**:
- H₀: μ₁ = μ₂ = μ₃ = ... (all group means equal)
- H₁: At least one mean differs

**Python Example**:
```python
group_a = df[df['group'] == 'A']['outcome']
group_b = df[df['group'] == 'B']['outcome']
group_c = df[df['group'] == 'C']['outcome']

# ANOVA
f_stat, p_value = stats.f_oneway(group_a, group_b, group_c)
print(f"F(2, {len(df)-3}) = {f_stat:.3f}, p = {p_value:.4f}")

# Effect size (eta-squared)
import statsmodels.api as sm
from statsmodels.formula.api import ols

model = ols('outcome ~ C(group)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
eta_squared = anova_table['sum_sq'][0] / (anova_table['sum_sq'][0] + anova_table['sum_sq'][1])
print(f"η² = {eta_squared:.3f}")
```

**Post-Hoc Tests** (if ANOVA significant):
```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey = pairwise_tukeyhsd(df['outcome'], df['group'], alpha=0.05)
print(tukey)
```

#### Kruskal-Wallis Test

**Non-parametric alternative** to one-way ANOVA.

**Python Example**:
```python
h_stat, p_value = stats.kruskal(group_a, group_b, group_c)
print(f"H = {h_stat:.3f}, p = {p_value:.4f}")
```

**Post-Hoc**: Pairwise Mann-Whitney U with Bonferroni correction.

## Relationships Between Variables

### Correlation

#### Pearson Correlation

**Use When**:
- Both variables continuous
- Linear relationship
- Bivariate normal distribution

**Interpretation**:
- r = 1: Perfect positive correlation
- r = 0: No correlation
- r = -1: Perfect negative correlation
- |r| < 0.3: Weak
- |r| = 0.3-0.7: Moderate
- |r| > 0.7: Strong

**Python Example**:
```python
r, p = stats.pearsonr(df['var1'], df['var2'])
print(f"r = {r:.3f}, p = {p:.4f}")

# Confidence interval (using Fisher's z-transformation)
from scipy.stats import norm
z = np.arctanh(r)
se = 1 / np.sqrt(len(df) - 3)
ci_low = np.tanh(z - 1.96 * se)
ci_high = np.tanh(z + 1.96 * se)
print(f"95% CI: [{ci_low:.3f}, {ci_high:.3f}]")
```

#### Spearman Correlation

**Non-parametric alternative**; measures monotonic (not necessarily linear) relationships.

**Python Example**:
```python
rho, p = stats.spearmanr(df['var1'], df['var2'])
print(f"ρ = {rho:.3f}, p = {p:.4f}")
```

### Regression

#### Simple Linear Regression

**Use When**:
- Predicting continuous outcome from one continuous predictor

**Model**: Y = β₀ + β₁X + ε

**Python Example**:
```python
import statsmodels.api as sm

X = df['predictor']
X = sm.add_constant(X)  # Add intercept
y = df['outcome']

model = sm.OLS(y, X).fit()
print(model.summary())

# Predictions
predictions = model.predict(X)

# R²
r_squared = model.rsquared
print(f"R² = {r_squared:.3f}")
```

**Assumptions**:
1. Linearity
2. Independence of errors
3. Homoscedasticity (constant variance)
4. Normality of residuals

**Diagnostics**:
```python
import matplotlib.pyplot as plt

residuals = model.resid
fitted = model.fittedvalues

# Residual plot (check homoscedasticity)
plt.scatter(fitted, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()

# Q-Q plot (check normality)
from scipy import stats
stats.probplot(residuals, dist="norm", plot=plt)
plt.title('Q-Q Plot')
plt.show()
```

#### Multiple Linear Regression

**Use When**:
- Predicting continuous outcome from multiple predictors

**Model**: Y = β₀ + β₁X₁ + β₂X₂ + ... + ε

**Python Example**:
```python
X = df[['predictor1', 'predictor2', 'predictor3']]
X = sm.add_constant(X)
y = df['outcome']

model = sm.OLS(y, X).fit()
print(model.summary())

# Check multicollinearity (VIF)
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)
# VIF > 10 indicates problematic multicollinearity
```

#### Logistic Regression

**Use When**:
- Outcome is binary (0/1, yes/no)

**Model**: log(p/(1-p)) = β₀ + β₁X₁ + β₂X₂ + ...

**Python Example**:
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

X = df[['predictor1', 'predictor2']]
y = df['binary_outcome']

model = LogisticRegression()
model.fit(X, y)

# Coefficients
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Predictions
y_pred = model.predict(X)
y_prob = model.predict_proba(X)[:, 1]

# Evaluation
print(classification_report(y, y_pred))
print(confusion_matrix(y, y_pred))

# Odds ratios
odds_ratios = np.exp(model.coef_)
print("Odds Ratios:", odds_ratios)
```

**Using statsmodels** (for more detailed output):
```python
import statsmodels.api as sm

X = sm.add_constant(X)
model = sm.Logit(y, X).fit()
print(model.summary())
```

## Categorical Data Analysis

### Chi-Square Test of Independence

**Use When**:
- Both variables categorical
- Testing association between variables

**Hypotheses**:
- H₀: Variables are independent
- H₁: Variables are associated

**Python Example**:
```python
# Create contingency table
contingency_table = pd.crosstab(df['var1'], df['var2'])

# Chi-square test
chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

print(f"χ²({dof}) = {chi2:.3f}, p = {p:.4f}")

# Effect size (Cramér's V)
n = contingency_table.sum().sum()
min_dim = min(contingency_table.shape[0], contingency_table.shape[1]) - 1
cramers_v = np.sqrt(chi2 / (n * min_dim))
print(f"Cramér's V = {cramers_v:.3f}")
```

**Assumptions**:
- Expected frequencies ≥ 5 in at least 80% of cells
- If violated, use Fisher's Exact Test (for 2×2 tables)

### Fisher's Exact Test

**Use When**:
- 2×2 contingency table with small expected frequencies

**Python Example**:
```python
oddsratio, p = stats.fisher_exact(contingency_table)
print(f"Odds Ratio = {oddsratio:.3f}, p = {p:.4f}")
```

## Advanced Methods

### Mixed Effects Models (Multilevel Models)

**Use When**:
- Nested data (students within schools, measurements within individuals)
- Accounting for clustering

**Python Example**:
```python
import statsmodels.formula.api as smf

# Random intercept model
model = smf.mixedlm("outcome ~ predictor", df, groups=df["cluster_id"])
result = model.fit()
print(result.summary())
```

**R is more common for mixed models**:
```r
library(lme4)

# Random intercept
model <- lmer(outcome ~ predictor + (1|cluster_id), data=df)

# Random slope
model <- lmer(outcome ~ predictor + (predictor|cluster_id), data=df)

summary(model)
```

### Survival Analysis

**Use When**:
- Time-to-event outcome
- Censored data (some events not yet observed)

**Methods**:
- Kaplan-Meier curves
- Log-rank test
- Cox proportional hazards regression

**Python Example**:
```python
from lifelines import KaplanMeierFitter, CoxPHFitter

# Kaplan-Meier
kmf = KaplanMeierFitter()
kmf.fit(df['time'], df['event_occurred'])
kmf.plot_survival_function()

# Cox regression
cph = CoxPHFitter()
cph.fit(df[['time', 'event_occurred', 'predictor1', 'predictor2']],
        duration_col='time', event_col='event_occurred')
print(cph.summary)
```

### Structural Equation Modeling (SEM)

**Use When**:
- Testing complex theoretical models
- Latent variables
- Mediation/moderation

**Software**: Mplus, lavaan (R), semopy (Python)

### Time Series Analysis

**Use When**:
- Data collected over time
- Autocorrelation present

**Methods**:
- ARIMA models
- Seasonal decomposition
- Interrupted time series

**Python Example**:
```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(df['time_series'], order=(1, 1, 1))
results = model.fit()
print(results.summary())

# Forecasting
forecast = results.forecast(steps=10)
```

## Effect Sizes

### Cohen's d (for t-tests)

**Interpretation**:
- d = 0.2: Small
- d = 0.5: Medium
- d = 0.8: Large

### Eta-squared (η²) / Partial Eta-squared (for ANOVA)

**Interpretation**:
- η² = 0.01: Small
- η² = 0.06: Medium
- η² = 0.14: Large

### R² (for regression)

Proportion of variance in outcome explained by predictors.

**Interpretation**:
- R² = 0.02: Small
- R² = 0.13: Medium
- R² = 0.26: Large

### Odds Ratio (for logistic regression)

**Interpretation**:
- OR = 1: No effect
- OR > 1: Positive association
- OR < 1: Negative association

## Sample Size and Power

### Power Analysis

**Components**:
- **Effect size**: Expected magnitude of effect
- **Alpha (α)**: Significance level (usually 0.05)
- **Power (1 - β)**: Probability of detecting true effect (usually 0.80)
- **Sample size (N)**: Number of participants needed

### G*Power

Free software for power analysis.

**Python Alternative**:
```python
from statsmodels.stats.power import TTestIndPower

# Calculate required sample size
analysis = TTestIndPower()
sample_size = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.80)
print(f"Required sample size per group: {sample_size:.0f}")

# Calculate achieved power
power = analysis.solve_power(effect_size=0.5, nobs1=50, alpha=0.05)
print(f"Achieved power: {power:.3f}")
```

## Reporting Guidelines

### General Format

"A [test name] revealed [direction of effect], [test statistic], p [= or <] [value], [effect size] = [value]."

### Examples

**t-test**:
"An independent samples t-test showed that the treatment group (M = 85.3, SD = 7.2) scored significantly higher than the control group (M = 78.6, SD = 8.1), t(98) = 4.32, p < .001, d = 0.87."

**ANOVA**:
"A one-way ANOVA revealed a significant effect of condition on test scores, F(2, 147) = 8.52, p < .001, η² = 0.10."

**Regression**:
"Multiple regression analysis showed that the model significantly predicted outcomes, F(3, 96) = 15.23, p < .001, R² = 0.32. Both predictor1 (β = 0.45, p < .001) and predictor2 (β = 0.28, p = .003) were significant predictors."

**Chi-square**:
"A chi-square test of independence revealed a significant association between gender and preference, χ²(2) = 12.45, p = .002, Cramér's V = 0.25."

## Resources

### Books
- Field, A. (2018). *Discovering Statistics Using IBM SPSS Statistics*
- Tabachnick, B. G., & Fidell, L. S. (2019). *Using Multivariate Statistics*
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*

### Online Resources
- Cross Validated (stats.stackexchange.com)
- UCLA Statistical Consulting (stats.oarc.ucla.edu)
- Penn State STAT 500 (online.stat.psu.edu)

### Software Documentation
- Python: scipy.stats, statsmodels, scikit-learn
- R: Base stats, tidyverse, lme4
- SPSS: IBM Documentation
