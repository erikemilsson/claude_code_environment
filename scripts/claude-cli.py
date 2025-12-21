#!/usr/bin/env python3
"""
Claude CLI - Unified command-line interface for all task management scripts

A single entry point for all task operations, validation, bootstrap, and analysis.
"""

import click
import json
import sys
from pathlib import Path
from typing import Optional

# Import all modules
sys.path.insert(0, str(Path(__file__).parent))
from task_manager import TaskManager
from validation_gates import ValidationGates
from schema_validator import SchemaValidator
from bootstrap import BootstrapAutomation
from pattern_matcher import PatternMatcher
from checkpoint_manager import CheckpointManager
from dependency_analyzer import DependencyAnalyzer
from metrics_dashboard import MetricsDashboard
from breakdown_suggester import BreakdownSuggester


@click.group()
@click.version_option(version='1.0.0', prog_name='Claude CLI')
def cli():
    """Claude Task Management System CLI

    A unified interface for managing tasks, validating systems,
    bootstrapping projects, and analyzing metrics.
    """
    pass


@cli.group()
def task():
    """Task management operations"""
    pass


@task.command()
@click.argument('task_id')
@click.option('--json', is_flag=True, help='Output as JSON')
def show(task_id, json):
    """Show task details"""
    manager = TaskManager()
    task_obj = manager.load_task(task_id)

    if not task_obj:
        click.echo(f"Task {task_id} not found", err=True)
        sys.exit(1)

    if json:
        import json as json_lib
        from dataclasses import asdict
        click.echo(json_lib.dumps(asdict(task_obj), indent=2))
    else:
        click.echo(f"Task: {task_obj.id}")
        click.echo(f"Title: {task_obj.title}")
        click.echo(f"Status: {task_obj.status}")
        click.echo(f"Difficulty: {task_obj.difficulty}")
        click.echo(f"Confidence: {task_obj.confidence}%")
        if task_obj.dependencies:
            click.echo(f"Dependencies: {', '.join(task_obj.dependencies)}")
        if task_obj.subtasks:
            click.echo(f"Subtasks: {', '.join(task_obj.subtasks)}")


@task.command()
@click.option('--status', type=click.Choice(['Pending', 'In Progress', 'Finished', 'Blocked']),
              help='Filter by status')
@click.option('--json', is_flag=True, help='Output as JSON')
def list(status, json):
    """List all tasks"""
    manager = TaskManager()
    task_ids = manager.get_all_task_ids()

    tasks = []
    for task_id in task_ids:
        task_obj = manager.load_task(task_id)
        if task_obj:
            if not status or task_obj.status == status:
                tasks.append({
                    "id": task_obj.id,
                    "title": task_obj.title,
                    "status": task_obj.status,
                    "difficulty": task_obj.difficulty
                })

    if json:
        import json as json_lib
        click.echo(json_lib.dumps(tasks, indent=2))
    else:
        for task in tasks:
            click.echo(f"{task['id']}: {task['title']} [{task['status']}]")


@task.command()
def sync():
    """Synchronize task overview"""
    manager = TaskManager()
    if manager.sync_task_overview():
        click.echo("Task overview synchronized successfully")
    else:
        click.echo("Failed to sync task overview", err=True)
        sys.exit(1)


@task.command()
@click.argument('task_id')
@click.argument('subtasks', nargs=-1)
def breakdown(task_id, subtasks):
    """Break down a task into subtasks"""
    manager = TaskManager()

    # Parse subtask definitions
    subtask_defs = []
    for subtask_json in subtasks:
        try:
            import json as json_lib
            subtask_defs.append(json_lib.loads(subtask_json))
        except:
            click.echo(f"Invalid JSON: {subtask_json}", err=True)
            sys.exit(1)

    created = manager.handle_breakdown(task_id, subtask_defs)
    if created:
        click.echo(f"Created {len(created)} subtasks: {', '.join(created)}")
    else:
        click.echo("Failed to create subtasks", err=True)
        sys.exit(1)


@cli.group()
def validate():
    """Validation operations"""
    pass


@validate.command()
@click.argument('task_id')
@click.option('--json', is_flag=True, help='Output as JSON')
def pre(task_id, json):
    """Run pre-execution validation gates"""
    gates = ValidationGates()
    can_proceed, results = gates.run_pre_execution_gates(task_id)

    if json:
        import json as json_lib
        output = {
            "can_proceed": can_proceed,
            "results": [r.to_dict() for r in results]
        }
        click.echo(json_lib.dumps(output, indent=2))
    else:
        click.echo(f"Pre-execution validation for {task_id}:")
        for result in results:
            status = "✓" if result.passed else "✗"
            click.echo(f"  {status} {result.check_name}: {result.message}")

        if can_proceed:
            click.echo(click.style("✅ All gates passed", fg='green'))
        else:
            click.echo(click.style("❌ Blocking gates failed", fg='red'))


@validate.command()
@click.argument('task_id')
@click.option('--json', is_flag=True, help='Output as JSON')
def post(task_id, json):
    """Run post-execution validation gates"""
    gates = ValidationGates()
    all_passed, results = gates.run_post_execution_gates(task_id)

    if json:
        import json as json_lib
        output = {
            "all_passed": all_passed,
            "results": [r.to_dict() for r in results]
        }
        click.echo(json_lib.dumps(output, indent=2))
    else:
        click.echo(f"Post-execution validation for {task_id}:")
        for result in results:
            status = "✓" if result.passed else "✗"
            click.echo(f"  {status} {result.check_name}: {result.message}")

        if all_passed:
            click.echo(click.style("✅ All checks passed", fg='green'))
        else:
            click.echo(click.style("⚠️ Some checks failed", fg='yellow'))


@validate.command()
def all():
    """Validate all tasks"""
    gates = ValidationGates()
    summary = gates.validate_all_tasks()

    click.echo(f"Total tasks: {summary['total_tasks']}")

    if summary['breakdown_required']:
        click.echo(f"Tasks needing breakdown: {', '.join(summary['breakdown_required'])}")

    if summary['pre_execution_failures']:
        click.echo(f"Pre-execution failures: {', '.join(summary['pre_execution_failures'])}")

    if summary['low_confidence']:
        click.echo("Low confidence tasks:")
        for task_id, conf in summary['low_confidence']:
            click.echo(f"  {task_id}: {conf}%")


@cli.group()
def bootstrap():
    """Bootstrap operations"""
    pass


@bootstrap.command()
@click.argument('spec_file', type=click.Path(exists=True))
@click.option('--output', default='.', help='Output directory')
def detect(spec_file, output):
    """Detect template from specification"""
    bootstrap_mgr = BootstrapAutomation(output)

    with open(spec_file, 'r') as f:
        content = f.read()

    template, scores = bootstrap_mgr.detect_template(content, spec_file)

    click.echo(f"Detected template: {click.style(template, fg='green')}")
    click.echo("\nConfidence scores:")
    for tmpl, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]:
        click.echo(f"  {tmpl}: {score:.1f}")


@bootstrap.command()
@click.argument('spec_file', type=click.Path(exists=True))
@click.option('--output', default='.', help='Output directory')
def create(spec_file, output):
    """Bootstrap environment from specification"""
    bootstrap_mgr = BootstrapAutomation()
    results = bootstrap_mgr.bootstrap_environment(spec_file, output)

    if results['errors']:
        for error in results['errors']:
            click.echo(f"Error: {error}", err=True)
        sys.exit(1)

    click.echo(f"Template: {click.style(results['template_detected'], fg='green')}")
    click.echo(f"Files created: {len(results['files_created'])}")
    click.echo(f"Tasks created: {results['tasks_created']}")


@cli.group()
def analyze():
    """Analysis operations"""
    pass


@analyze.command()
def cycles():
    """Detect circular dependencies"""
    analyzer = DependencyAnalyzer()
    cycles = analyzer.detect_circular_dependencies()

    if cycles:
        click.echo(click.style("Circular dependencies detected:", fg='red'))
        for cycle in cycles:
            click.echo(f"  {' -> '.join(cycle)}")
    else:
        click.echo(click.style("No circular dependencies found", fg='green'))


@analyze.command()
def critical():
    """Find critical path"""
    analyzer = DependencyAnalyzer()
    path = analyzer.find_critical_path()

    if path:
        click.echo("Critical path:")
        for task_id in path:
            task = analyzer.task_manager.load_task(task_id)
            if task:
                click.echo(f"  {task_id}: {task.title} (difficulty: {task.difficulty})")
    else:
        click.echo("No critical path found")


@analyze.command()
def parallel():
    """Find parallelizable tasks"""
    analyzer = DependencyAnalyzer()
    groups = analyzer.suggest_parallelizable_tasks()

    click.echo("Parallelizable task groups:")
    for i, group in enumerate(groups):
        click.echo(f"\nLevel {i}:")
        for task_id in group:
            task = analyzer.task_manager.load_task(task_id)
            if task:
                click.echo(f"  {task_id}: {task.title}")


@cli.group()
def metrics():
    """Metrics operations"""
    pass


@metrics.command()
def health():
    """Show health score"""
    dashboard = MetricsDashboard()
    health = dashboard.generate_health_score()

    click.echo(f"Overall health: {click.style(f'{health['overall_score']:.1f}/100', fg='cyan')}")
    click.echo("\nComponents:")
    for component, score in health['components'].items():
        color = 'green' if score >= 70 else 'yellow' if score >= 50 else 'red'
        click.echo(f"  {component}: {click.style(f'{score:.1f}', fg=color)}")

    if health['warnings']:
        click.echo("\nWarnings:")
        for warning in health['warnings']:
            click.echo(f"  ⚠️ {warning}")

    if health['recommendations']:
        click.echo("\nRecommendations:")
        for rec in health['recommendations']:
            click.echo(f"  💡 {rec}")


@metrics.command()
def dashboard():
    """Generate metrics dashboard"""
    dashboard_gen = MetricsDashboard()
    md_dashboard = dashboard_gen.generate_markdown_dashboard()
    click.echo(md_dashboard)


@metrics.command()
@click.option('--output', help='Output file')
def export(output):
    """Export metrics as JSON"""
    dashboard = MetricsDashboard()
    output_file = dashboard.export_metrics_json()
    click.echo(f"Metrics exported to {output_file}")


@cli.group()
def checkpoint():
    """Checkpoint operations"""
    pass


@checkpoint.command()
@click.option('--description', default='', help='Checkpoint description')
def create(description):
    """Create checkpoint"""
    manager = CheckpointManager()
    checkpoint_id = manager.create_checkpoint(description)
    click.echo(f"Created checkpoint: {click.style(checkpoint_id, fg='green')}")


@checkpoint.command()
def list():
    """List checkpoints"""
    manager = CheckpointManager()
    checkpoints = manager.list_checkpoints()

    for cp in checkpoints:
        click.echo(f"{cp['id']}: {cp.get('description', 'No description')} ({cp['files_count']} files)")


@checkpoint.command()
@click.argument('checkpoint_id')
def diff(checkpoint_id):
    """Show diff from checkpoint"""
    manager = CheckpointManager()
    diffs = manager.diff_checkpoint(checkpoint_id)

    click.echo(f"Changes since {checkpoint_id}:")
    if diffs['added']:
        click.echo(f"  Added: {click.style(str(len(diffs['added'])), fg='green')}")
    if diffs['modified']:
        click.echo(f"  Modified: {click.style(str(len(diffs['modified'])), fg='yellow')}")
    if diffs['deleted']:
        click.echo(f"  Deleted: {click.style(str(len(diffs['deleted'])), fg='red')}")


@cli.command()
@click.argument('task_id')
def suggest(task_id):
    """Suggest breakdown strategy for a task"""
    suggester = BreakdownSuggester()
    strategy = suggester.suggest_breakdown_strategy(task_id)

    click.echo(f"Breakdown Strategy for {task_id}")
    click.echo(f"Pattern: {click.style(strategy.get('recommended_pattern'), fg='cyan')}")
    click.echo(f"Confidence: {strategy.get('confidence')}%")
    click.echo(f"Estimated subtasks: {strategy.get('estimated_subtask_count')}")

    click.echo("\nSuggested subtasks:")
    for i, subtask in enumerate(strategy.get('suggested_subtasks', []), 1):
        click.echo(f"  {i}. {subtask}")


@cli.command()
def repair():
    """Repair task schema issues"""
    validator = SchemaValidator()
    results = validator.auto_repair_all()

    click.echo("Auto-repair Results:")
    click.echo(f"  Missing fields fixed: {results['missing_fields_fixed']}")
    click.echo(f"  Date formats fixed: {results['date_formats_fixed']}")

    if results['broken_references']:
        click.echo("  Broken references fixed:")
        for ref_type, task_ids in results['broken_references'].items():
            if task_ids:
                click.echo(f"    {ref_type}: {', '.join(task_ids)}")


if __name__ == '__main__':
    cli()