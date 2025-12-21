# Validate M Code Command

## Purpose
Validate Power Query M code for syntax, performance, and best practices.

## Context Required
- M code to validate
- Query context (data source, expected volume)

## Process

### Validation Checks
1. **Syntax Validation**
   - Proper let/in structure
   - Variable naming conventions
   - Type annotations

2. **Performance Validation**
   - Query folding preservation
   - Efficient transformations
   - Buffer usage for multiple references

3. **Best Practice Validation**
   - Error handling presence
   - Code comments
   - Step naming clarity

4. **Common Pitfall Detection**
   - Nested iterations
   - Unnecessary type conversions
   - Row-by-row operations
   - Breaking query folding

## Output
- Validation report with:
  - Syntax errors
  - Performance warnings
  - Best practice violations
  - Improvement suggestions
  - Query folding status

## Example Issues Detected
- "Custom function breaks query folding at step 3"
- "Missing error handling for division operation"
- "Inefficient: Filter should come before merge"
- "Variable 'data' should be 'Data' per convention"