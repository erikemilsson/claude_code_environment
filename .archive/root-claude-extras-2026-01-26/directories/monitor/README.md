# Real-Time Observability Layer

Welcome to the Universal Project's Real-Time Observability Layer with Self-Diagnosis capabilities.

## Overview

This monitoring system provides:
- 🔴 **Live Dashboard** - Real-time visibility into system operations
- 🏥 **Health Checks** - Continuous system health monitoring
- 🔍 **Self-Diagnosis** - Automated problem analysis
- 💊 **Self-Healing** - Intelligent fix recommendations
- 📈 **Predictive Warnings** - Issue prevention before they occur

## Quick Start

### View System Status
```bash
# Check current health
cat .claude/monitor/health-checks.json

# View live dashboard
cat .claude/monitor/live-dashboard.md

# Check latest diagnostics
cat .claude/monitor/diagnostics.md
```

### Run Manual Checks
```bash
# Update health status
python3 .claude/monitor/scripts/health_checker.py

# Run diagnosis on recent failures
python3 .claude/monitor/scripts/diagnose.py

# Generate fix recommendations
python3 .claude/monitor/scripts/self_heal.py
```

## File Structure

```
.claude/monitor/
├── README.md                    # This file
├── live-dashboard.md           # Real-time operation status
├── health-checks.json          # Current health metrics
├── diagnostics.md              # Problem analysis reports
├── self-heal.md               # Fix recommendations
├── history/                    # Historical data
│   ├── metrics/               # Performance metrics over time
│   ├── failures/              # Failure patterns
│   └── resolutions/           # Successful fixes
├── scripts/                    # Monitoring scripts
│   ├── health_checker.py      # Health check runner
│   ├── dashboard_updater.py   # Dashboard refresh
│   ├── diagnose.py           # Diagnosis engine
│   └── self_heal.py          # Fix generator
└── config/                     # Configuration
    ├── thresholds.json        # Alert thresholds
    └── patterns.json          # Diagnosis patterns
```

## Features

### 1. Live Dashboard

The dashboard (`live-dashboard.md`) updates in real-time showing:
- Current operation and progress
- System health status
- Active warnings and alerts
- Next recommended actions

### 2. Health Monitoring

Continuous health checks (`health-checks.json`) track:
- Memory usage
- File operation performance
- Task queue status
- Checkpoint freshness
- Error rates

### 3. Self-Diagnosis

When issues occur, the diagnosis engine:
- Identifies failure patterns
- Determines root causes
- Links to similar past issues
- Suggests relevant documentation

### 4. Self-Healing Recommendations

Based on diagnosis, the system provides:
- Step-by-step fix instructions
- Executable code snippets
- Risk assessment for each fix
- Rollback procedures if needed

### 5. Predictive Warnings

The system predicts issues by:
- Analyzing trends
- Detecting anomalies
- Pattern matching
- Resource forecasting

## Commands

### Monitor Commands
```bash
# Show current health
.claude/commands/show-health.md

# View live dashboard
.claude/commands/view-dashboard.md

# Run diagnosis
.claude/commands/run-diagnosis.md

# Apply recommended fix
.claude/commands/apply-fix.md

# Show historical trends
.claude/commands/show-trends.md
```

## Configuration

### Thresholds
Edit `.claude/monitor/config/thresholds.json`:
```json
{
  "memory_percent": 80,
  "file_ops_ms": 50,
  "task_queue_max": 10,
  "error_rate_percent": 5
}
```

### Alert Levels
- 🟢 **Healthy** - All metrics within normal range
- 🟡 **Warning** - Some metrics approaching thresholds
- 🔴 **Critical** - Immediate attention required

## Integration

The observability layer integrates with:
- **Task Management** - Monitors all task operations
- **Validation Gates** - Tracks validation success/failure
- **Checkpoint System** - Monitors recovery points
- **Agent System** - Tracks agent activities

## Performance Impact

Target: < 5% overhead
Current: ~2% average

The system auto-disables if overhead exceeds 5%.

## Troubleshooting

### Dashboard Not Updating
1. Check if updater is running
2. Verify file permissions
3. Check for locked files

### False Alerts
1. Adjust thresholds in config
2. Check baseline metrics
3. Review recent changes

### Missing Diagnostics
1. Ensure error logging is enabled
2. Check diagnosis patterns
3. Verify file paths

## Examples

### Example Health Check Output
```json
{
  "timestamp": "2025-12-29T19:00:00Z",
  "status": "healthy",
  "metrics": {
    "memory_percent": 45,
    "file_ops_ms": 12,
    "task_queue": 3,
    "error_rate": 0.5
  },
  "alerts": []
}
```

### Example Diagnosis
```markdown
## Diagnosis Report

**Error:** Task status transition failed
**Pattern:** Invalid state transition
**Root Cause:** Attempted to move from 'Finished' to 'Pending'

### Recommended Fix:
1. Check task status before transition
2. Validate allowed transitions
3. Add status guard clause

### Code Fix:
```python
if task['status'] != 'Finished':
    task['status'] = new_status
```
```

## Best Practices

1. **Regular Monitoring** - Check dashboard during operations
2. **Act on Warnings** - Don't ignore yellow alerts
3. **Apply Fixes Promptly** - Use self-healing recommendations
4. **Track Patterns** - Review historical data for trends
5. **Tune Thresholds** - Adjust based on your system

## Support

For issues or questions:
- Check this README first
- Review diagnostic reports
- Consult fix recommendations
- Report bugs in task system

---

*The Observability Layer: Making the invisible visible, the complex simple, and the broken fixable.*