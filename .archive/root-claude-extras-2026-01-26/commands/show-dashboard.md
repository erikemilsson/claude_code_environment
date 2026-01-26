# Show Dashboard Command

## Purpose
Display the current project health dashboard with real-time metrics from belief tracking data.

## Context Required
- Task files in `.claude/tasks/`
- Decision log in `.claude/decisions/`
- Assumption tracker in `.claude/validation/`
- Pattern insights in `.claude/insights/`

## Process

### 1. Data Collection
Read and aggregate metrics from:
- All task JSON files for status, confidence, momentum
- Decision log for decision patterns
- Assumption tracker for validation status
- Pattern insights for trend analysis

### 2. Metric Calculation

#### Task Momentum Distribution
```python
momentum_phases = {
    'initiating': 0,
    'building': 0,
    'cruising': 0,
    'declining': 0,
    'stalled': 0
}

for task in tasks:
    if task.momentum and task.momentum.phase:
        momentum_phases[task.momentum.phase] += 1
```

#### Confidence Metrics
```python
confidence_bands = {
    'high': [],      # 90-100%
    'good': [],      # 75-89%
    'moderate': [],  # 50-74%
    'low': []        # <50%
}

for task in tasks:
    if task.confidence:
        if task.confidence >= 90:
            confidence_bands['high'].append(task)
        elif task.confidence >= 75:
            confidence_bands['good'].append(task)
        elif task.confidence >= 50:
            confidence_bands['moderate'].append(task)
        else:
            confidence_bands['low'].append(task)

avg_confidence = sum(confidences) / len(confidences) if confidences else 0
```

#### Assumption Validation
```python
assumption_status = {
    'validated': 0,
    'needs_check': 0,
    'invalidated': 0,
    'pending': 0
}

for assumption in all_assumptions:
    assumption_status[assumption.validation_status] += 1
```

#### Risk Indicators
```python
risks = {
    'critical': [],  # Impact >= 8, Likelihood >= 0.7
    'moderate': [],  # Impact >= 5, Likelihood >= 0.5
    'low': []        # All others
}

for task in tasks:
    if task.risk_score:
        impact = task.risk_score.impact
        likelihood = task.risk_score.likelihood

        if impact >= 8 and likelihood >= 0.7:
            risks['critical'].append(task)
        elif impact >= 5 and likelihood >= 0.5:
            risks['moderate'].append(task)
        else:
            risks['low'].append(task)
```

### 3. Visualization Generation

#### Progress Bars
```python
def progress_bar(value, max_value=100, width=10):
    filled = int(value / max_value * width)
    bar = '█' * filled + '░' * (width - filled)
    return f'[{bar}] {value}%'
```

#### ASCII Charts
```python
def momentum_chart(phases):
    symbols = {
        'initiating': '█',
        'building': '▓',
        'cruising': '░',
        'declining': '○',
        'stalled': '•'
    }

    chart = ''
    for phase, count in phases.items():
        chart += f'{symbols[phase]} {phase.title()}: {count}\n'
    return chart
```

### 4. Pattern Detection

#### Velocity Trends
- Calculate average completion time for finished tasks
- Identify tasks with declining momentum
- Find bottleneck areas (blocked tasks, dependencies)

#### Quality Indicators
- Track assumption validation rate over time
- Monitor confidence changes
- Count decision reversals

### 5. Health Score Calculation
```python
health_components = {
    'task_momentum': calculate_momentum_score(),    # 0-100
    'confidence_level': avg_confidence,              # 0-100
    'assumption_valid': validation_rate * 100,       # 0-100
    'risk_management': calculate_risk_score(),       # 0-100
    'pattern_stability': calculate_stability()       # 0-100
}

overall_health = sum(health_components.values()) / len(health_components)

def get_health_grade(score):
    if score >= 90: return 'A'
    elif score >= 80: return 'B'
    elif score >= 70: return 'C'
    elif score >= 60: return 'D'
    else: return 'F'
```

### 6. Alert Generation
Check for threshold violations:
- Critical: Average confidence < 50%
- Warning: > 30% tasks stalled
- Risk: > 3 critical risks
- Pattern: > 50% tasks declining

### 7. Display Output
1. Clear terminal or create section separator
2. Display header with timestamp
3. Show each dashboard section with visualizations
4. Highlight alerts in color (if terminal supports)
5. Add footer with refresh instructions

## Output Location
- Terminal display (primary)
- Update `.claude/dashboard/project-health.md` with latest data
- Log alerts to `.claude/dashboard/alerts.log` if any

## Command Options
- `--section [name]` - Show only specific section
- `--json` - Output raw metrics as JSON
- `--refresh` - Force data refresh before display
- `--compact` - Show condensed view
- `--alerts-only` - Show only active alerts

## Example Usage
```bash
# Show full dashboard
/show-dashboard

# Show only confidence metrics
/show-dashboard --section confidence

# Get JSON data for external processing
/show-dashboard --json > metrics.json

# Show compact view with alerts
/show-dashboard --compact --alerts-only
```

## Integration Points
- Called by `sync-tasks` after updating overview
- Can trigger `analyze-patterns` if new patterns detected
- Updates decision log if critical alerts found
- Feeds into `generate-reports` for documentation

## Performance Considerations
- Cache calculations for 5 minutes
- Use incremental updates when possible
- Process tasks in batches for large projects
- Skip visualization for JSON output

## Error Handling
- Missing data: Show "N/A" or "No data"
- Corrupt JSON: Skip file, log error
- Division by zero: Use safe defaults
- File not found: Create with defaults