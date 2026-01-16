# Show Health Status

## Purpose
Display current system health status and metrics from the observability layer

## Context Required
- Observability system must be initialized
- Health checks should be running

## Process

1. **Run health check**
   ```bash
   python3 .claude/monitor/scripts/health_checker.py
   ```

2. **View health status**
   ```bash
   cat .claude/monitor/health-checks.json | python3 -m json.tool
   ```

3. **Check for alerts**
   - Review any critical alerts
   - Note warning conditions
   - Check resource usage

4. **View recommendations**
   - Review suggested actions
   - Note performance optimizations

## Output Location
- Health status: `.claude/monitor/health-checks.json`
- Console output with summary

## Usage Examples

### Quick health check
```bash
python3 .claude/monitor/scripts/health_checker.py
```

### Detailed JSON output
```bash
cat .claude/monitor/health-checks.json | jq '.metrics'
```

### Check specific metrics
```bash
# Memory usage
cat .claude/monitor/health-checks.json | jq '.metrics.system.memory_usage_percent'

# Task queue
cat .claude/monitor/health-checks.json | jq '.metrics.task_system.queue_depth'

# Monitoring overhead
cat .claude/monitor/health-checks.json | jq '.metrics.observability.monitoring_overhead_percent'
```

## Alert Levels
- 🟢 **Healthy**: All systems normal
- 🟡 **Warning**: Some metrics approaching thresholds
- 🔴 **Critical**: Immediate attention required

## Notes
- Health checks run automatically every 5 minutes
- Manual checks can be run anytime
- Historical data saved in `.claude/monitor/history/`