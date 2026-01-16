# Run Diagnosis

## Purpose
Analyze failures and errors to identify root causes and generate fix recommendations

## Context Required
- Error or failure to diagnose
- Test results file or error log

## Process

1. **Run diagnosis on test results**
   ```bash
   python3 .claude/monitor/scripts/diagnose.py --test-results
   ```

2. **Diagnose specific error**
   ```bash
   python3 .claude/monitor/scripts/diagnose.py --error "error message"
   ```

3. **Analyze error log file**
   ```bash
   python3 .claude/monitor/scripts/diagnose.py --file error.log
   ```

4. **Review diagnosis report**
   ```bash
   cat .claude/monitor/diagnostics.md
   ```

## Output Location
- Diagnosis report: `.claude/monitor/diagnostics.md`
- Historical diagnoses: `.claude/monitor/history/failures/`

## Usage Examples

### Diagnose recent test failures
```bash
# Analyze test results
python3 .claude/monitor/scripts/diagnose.py --test-results

# View diagnosis
cat .claude/monitor/diagnostics.md
```

### Diagnose specific error
```bash
# Provide error message
python3 .claude/monitor/scripts/diagnose.py --error "FileNotFoundError: task-001.json"

# Diagnose from traceback
python3 .claude/monitor/scripts/diagnose.py --file traceback.txt
```

### Pattern analysis
```bash
# Check diagnosis patterns
cat .claude/monitor/config/patterns.json | jq '.[] | .indicators'

# View confidence scores
cat .claude/monitor/diagnostics.md | grep "Confidence:"
```

## Diagnosis Components
- **Error Analysis**: Parse and understand error
- **Pattern Matching**: Match against known patterns
- **Root Cause**: Identify likely causes
- **Code Fixes**: Generate fix code
- **Similar Issues**: Find historical matches
- **Prevention**: Suggest preventive measures

## Pattern Types
- Status transition errors
- File not found errors
- Assertion failures
- Import errors
- Timeout issues
- Permission errors
- Memory errors

## Notes
- Diagnosis improves over time with more data
- Patterns can be customized in config/patterns.json
- Historical data helps identify recurring issues