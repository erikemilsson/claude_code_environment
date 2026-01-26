#!/usr/bin/env python3
"""
Quick Status - Streamlined monitoring for Claude Code
One command to update and display everything important
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from health_checker import HealthChecker
from dashboard_updater import DashboardUpdater
from diagnose import DiagnosisEngine

def get_emoji(status):
    """Get status emoji"""
    return {
        "healthy": "🟢",
        "warning": "🟡",
        "critical": "🔴",
        "unknown": "⚪"
    }.get(status.lower(), "⚪")

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def quick_status():
    """Run quick status check and display summary"""

    # Update health
    print("Checking system health...", end=" ")
    checker = HealthChecker()
    health = checker.run_health_check()
    checker.save_results(health)
    print("✓")

    # Update dashboard
    print("Updating dashboard...", end=" ")
    updater = DashboardUpdater()
    updater.update_dashboard()
    print("✓")

    # Check for recent failures
    print("Checking for issues...", end=" ")
    test_results_path = Path(__file__).parents[3] / "test" / "test_results.json"
    has_failures = False
    if test_results_path.exists():
        with open(test_results_path) as f:
            results = json.load(f)
            has_failures = results.get("failed", 0) > 0 or results.get("errors", 0) > 0
    print("✓")

    # Display summary
    print_header("🏥 SYSTEM STATUS")

    # Overall health
    status_emoji = get_emoji(health["status"])
    print(f"\n{status_emoji} Overall Status: {health['status'].upper()}")
    print(f"📊 Health Score: {health['overall_health_score']}/100")

    # Key metrics
    print("\n📈 Key Metrics:")
    metrics = health["metrics"]
    system_metrics = metrics.get('system', {})
    perf_metrics = metrics.get('performance', {}).get('file_operations', {})
    task_metrics = metrics.get('task_system', {})
    obs_metrics = metrics.get('observability', {})

    if system_metrics.get('memory_usage_percent') is not None:
        print(f"  • Memory: {system_metrics['memory_usage_percent']:.0f}%")
    if system_metrics.get('cpu_usage_percent') is not None:
        print(f"  • CPU: {system_metrics['cpu_usage_percent']:.0f}%")
    print(f"  • File Ops: {perf_metrics.get('average_ms', 0):.1f}ms")
    print(f"  • Task Queue: {task_metrics.get('queue_depth', 0)} pending")
    print(f"  • Monitor Overhead: {obs_metrics.get('monitoring_overhead_percent', 0):.1f}%")

    # Alerts
    if health["alerts"]:
        print(f"\n🚨 ALERTS ({len(health['alerts'])}):")
        for alert in health["alerts"][:3]:  # Show top 3
            print(f"  • {alert['message']}")
    else:
        print("\n✅ No alerts - system healthy")

    # Recent issues
    if has_failures:
        print("\n⚠️ Recent Test Failures Detected")
        print("  Run 'python3 .claude/monitor/scripts/diagnose.py --test-results' to analyze")
        print("  Then 'python3 .claude/monitor/scripts/self_heal.py --all-safe' to fix")

    # Task summary
    task_metrics = metrics["task_system"]
    total = task_metrics.get("total_tasks", 0)
    if total > 0:
        print(f"\n📋 Tasks: {task_metrics.get('completed', 0)}/{total} completed")
        print(f"  • In Progress: {task_metrics.get('in_progress', 0)}")
        print(f"  • Pending: {task_metrics.get('pending', 0)}")

    # Recommendations
    if health.get("recommendations"):
        print("\n💡 Recommendations:")
        for rec in health["recommendations"][:2]:  # Show top 2
            print(f"  • {rec}")

    # View commands
    print("\n📄 For Details:")
    print("  • Full Dashboard: cat .claude/monitor/live-dashboard.md")
    print("  • Diagnostics: cat .claude/monitor/diagnostics.md")
    print("  • Fixes: cat .claude/monitor/self-heal.md")

    print(f"\n⏰ Last Updated: {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)

    # Return status code
    if health["status"] == "critical":
        return 2
    elif health["status"] == "warning":
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(quick_status())