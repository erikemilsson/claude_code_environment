# Monitor - Unified Observability Command

## Purpose
Single command for all monitoring operations - optimized for Claude Code usage

## Context Required
None - this command handles everything

## Process

When you say "show monitor" or "check system health", Claude Code will:

1. **Update health status**
2. **Refresh dashboard**
3. **Check for issues**
4. **Display summary**

## Quick Commands

### Full Status (Most Common)
```bash
# Updates everything and shows dashboard
python3 .claude/monitor/scripts/quick_status.py
```

### Just View Current Status
```bash
# No updates, just display
cat .claude/monitor/live-dashboard.md
```

### Health Only
```bash
# Quick health check
cat .claude/monitor/health-checks.json | jq '.status, .overall_health_score'
```

## Claude Code Integration

Just say:
- "Show system status" - Full dashboard
- "Check health" - Health metrics
- "Any issues?" - Shows alerts/diagnoses
- "Fix problems" - Applies safe fixes

## Auto-Monitoring

The system can also:
- Auto-check health after task completion
- Update dashboard when viewing
- Run diagnosis on test failures automatically
- Alert on critical issues

## Output
Always returns human-readable summary, not raw JSON