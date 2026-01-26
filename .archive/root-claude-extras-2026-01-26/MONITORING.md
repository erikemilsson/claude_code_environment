# 🔍 Monitoring Integration for Claude Code

This file tells Claude Code how to use the monitoring system seamlessly.

## Quick Commands Claude Code Can Run

### When User Says → Claude Code Runs

| User Says | Claude Code Runs | Shows |
|-----------|------------------|-------|
| "Show status" | `python3 .claude/monitor/scripts/quick_status.py` | Complete summary |
| "Check health" | `cat .claude/monitor/health-checks.json \| jq '.status, .overall_health_score'` | Health only |
| "Show dashboard" | `cat .claude/monitor/live-dashboard.md` | Full dashboard |
| "Any problems?" | `cat .claude/monitor/diagnostics.md \| head -30` | Recent issues |
| "Fix issues" | `python3 .claude/monitor/scripts/self_heal.py --all-safe --dry-run` | Proposed fixes |

## Automatic Monitoring

Claude Code automatically runs monitoring when:

1. **After Test Runs** - Check if tests failed, run diagnosis
2. **After Task Completion** - Update health check
3. **On Error** - Capture and diagnose
4. **Periodically** - Every 30 minutes during active work

## Streamlined Workflow

```python
# What happens when user says "check system"
1. Run quick_status.py → Shows everything important
2. If issues found → Automatically show diagnostics
3. If fixes available → Offer to apply them
```

## Even Simpler: Just Read Files

The monitoring system keeps these files always relatively current:

```bash
# Latest status (human-readable)
cat .claude/monitor/live-dashboard.md | head -50

# Just the health score
cat .claude/monitor/health-checks.json | jq '.overall_health_score'

# Any alerts?
cat .claude/monitor/health-checks.json | jq '.alerts'
```

## Smart Integration Examples

### Example 1: User runs tests
```
User: "Run the tests"
Claude Code: [Runs tests]
Claude Code: [Automatically checks if failures]
Claude Code: [If failures, runs diagnosis]
Claude Code: "3 tests failed. I've diagnosed the issues - they appear to be status transition errors. Would you like me to apply the automated fixes?"
```

### Example 2: User asks about system
```
User: "How's the system doing?"
Claude Code: [Runs quick_status.py]
Claude Code: "System is healthy (95/100). Memory at 42%, no alerts, 12 tasks completed. Everything running smoothly."
```

### Example 3: Problem detection
```
User: [Working normally]
Claude Code: [Detects high memory usage]
Claude Code: "⚠️ Memory usage is at 78% and climbing. Should I investigate?"
```

## No Manual Scripts Needed!

When using Claude Code, you never need to manually run scripts. Just ask naturally:

- ✅ "Show me the system status"
- ✅ "Is everything working?"
- ✅ "Check for problems"
- ✅ "Fix any issues"
- ✅ "How's performance?"

Claude Code handles the rest!

## Background Monitoring

If you want continuous monitoring without asking:

```bash
# Start background monitor (runs once)
nohup python3 .claude/monitor/scripts/dashboard_updater.py &

# Then the dashboard auto-updates every 5 seconds
# Claude Code can just read the file anytime
```

## One-Line Status

For the absolute simplest check:

```bash
# Everything in one line
python3 -c "import json; h=json.load(open('.claude/monitor/health-checks.json')); print(f\"{'🟢' if h['status']=='healthy' else '🟡' if h['status']=='warning' else '🔴'} {h['status'].upper()} ({h['overall_health_score']}/100)\")"
```

## Integration Benefits

1. **No manual commands** - Just ask naturally
2. **Automatic diagnosis** - On any failure
3. **Proactive alerts** - Claude Code tells you about issues
4. **Smart context** - Only shows what's relevant
5. **Single command** - `quick_status.py` does everything

The monitoring is now fully integrated with Claude Code - just ask and receive!