# Statistical Standards for Research

## Required Reporting

### Effect Sizes
Always report effect sizes with confidence intervals:
- Cohen's d for mean differences
- Pearson's r for correlations
- Odds ratios for categorical outcomes
- Hedges' g for small sample corrections

### Example Reporting
"The meta-analysis revealed a significant negative correlation between temperature increase and species richness (r = -0.67, 95% CI [-0.74, -0.59], p < 0.001, k = 45 studies, n = 12,847 observations)."

## Meta-Analysis Standards

### Model Selection
- **Fixed-Effects**: Only if I² < 25% and similar study designs
- **Random-Effects**: Default choice for ecological studies
- **Mixed-Effects**: When moderator variables are tested

### Heterogeneity Assessment
```r
# Required statistics
Q-statistic with p-value
I² (with 95% CI)
τ² (tau-squared)
Prediction interval
```

### Publication Bias
1. Funnel plot (visual inspection)
2. Egger's test (statistical test)
3. Trim-and-fill analysis
4. Fail-safe N calculation
5. P-curve analysis

## Hypothesis Testing Protocol

### Pre-Registration Requirements
Before analysis, document:
- Exact statistical tests to be used
- Alpha level (typically 0.05)
- Power analysis results
- Multiple comparison corrections
- Sensitivity analysis plan

### Multiple Testing Corrections
When testing multiple hypotheses:
- Bonferroni: α_adjusted = α / k
- False Discovery Rate (FDR): For exploratory analyses
- Hierarchical testing: For planned comparisons

## Reproducibility Standards

### Code Documentation
```r
# Analysis script template
# Author: [Name]
# Date: [YYYY-MM-DD]
# Purpose: [Specific analysis]
# Data: [Source file]
# Output: [Results file]

# Load packages
library(metafor)
library(tidyverse)

# Set seed for reproducibility
set.seed(42)

# Document session info
sessionInfo()
```

### Data Management
1. Raw data: Never modify, keep read-only
2. Processed data: Document all transformations
3. Analysis data: Final dataset used for statistics
4. Version control: Git for all scripts

## Common Statistical Errors to Avoid

### In Meta-Analysis
- ❌ Mixing effect size types
- ❌ Double-counting studies
- ❌ Ignoring study quality
- ❌ Not checking assumptions
- ❌ P-hacking through subgroup analysis

### In Hypothesis Testing
- ❌ HARKing (Hypothesizing After Results Known)
- ❌ Selective reporting
- ❌ Ignoring effect sizes
- ❌ Treating p = 0.06 as "trending"
- ❌ Not reporting non-significant results

## R Code Templates

### Basic Meta-Analysis
```r
# Load data
data <- read.csv("extracted_data.csv")

# Calculate effect sizes
es <- escalc(measure = "SMD",
             m1i = mean_treatment,
             m2i = mean_control,
             sd1i = sd_treatment,
             sd2i = sd_control,
             n1i = n_treatment,
             n2i = n_control,
             data = data)

# Random-effects model
model <- rma(yi, vi, data = es)

# Forest plot
forest(model, slab = paste(data$author, data$year))

# Heterogeneity
confint(model)

# Publication bias
funnel(model)
regtest(model)
```

### Hypothesis Test Template
```r
# Test H1: Temperature-biodiversity correlation
cor_test <- cor.test(data$temp_change,
                      data$biodiversity_index,
                      method = "pearson")

# Effect size with CI
library(psychometric)
CIr(r = cor_test$estimate,
    n = nrow(data),
    level = 0.95)

# Document result
result_H1 <- list(
  hypothesis = "H1",
  test = "Pearson correlation",
  statistic = cor_test$estimate,
  p_value = cor_test$p.value,
  ci_lower = cor_test$conf.int[1],
  ci_upper = cor_test$conf.int[2],
  conclusion = ifelse(cor_test$p.value < 0.05,
                      "Supported", "Not supported")
)
```

## Reporting Checklist

Before submitting results:
- [ ] All statistics include effect sizes
- [ ] Confidence intervals reported
- [ ] Sample sizes clear
- [ ] Assumptions checked and reported
- [ ] Multiple testing corrections applied
- [ ] Sensitivity analyses conducted
- [ ] Raw data and code available
- [ ] PRISMA checklist completed