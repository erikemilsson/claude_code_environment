# View Live Dashboard

## Purpose
Display the real-time monitoring dashboard showing current system status and operations

## Context Required
- Dashboard updater should be running
- Or run once to generate current snapshot

## Process

1. **Start dashboard updater (if not running)**
   ```bash
   python3 .claude/monitor/scripts/dashboard_updater.py &
   ```

2. **View dashboard**
   ```bash
   cat .claude/monitor/live-dashboard.md
   ```

3. **Monitor specific sections**
   - Current operation progress
   - System health metrics
   - Active alerts
   - Task summary

## Output Location
- Live dashboard: `.claude/monitor/live-dashboard.md`
- Auto-refreshes every 5 seconds

## Usage Examples

### One-time dashboard update
```bash
python3 .claude/monitor/scripts/dashboard_updater.py --once
```

### Continuous monitoring
```bash
# Start in background
python3 .claude/monitor/scripts/dashboard_updater.py &

# Watch dashboard updates
watch -n 5 cat .claude/monitor/live-dashboard.md
```

### View specific metrics
```bash
# Current task progress
grep -A 5 "Current Operation" .claude/monitor/live-dashboard.md

# System health
grep -A 10 "System Health" .claude/monitor/live-dashboard.md

# Active alerts
grep -A 5 "Alerts & Warnings" .claude/monitor/live-dashboard.md
```

## Dashboard Sections
- **Current Operation**: Active task and progress
- **System Health**: Resource metrics and performance
- **Alerts & Warnings**: Active issues
- **Trends**: Historical patterns
- **Predictions**: Forecast and recommendations
- **Task Summary**: Work status breakdown
- **Next Actions**: Recommended immediate steps

## Notes
- Dashboard updates automatically when updater is running
- Manual refresh available with --once flag
- Historical dashboards saved in history folder