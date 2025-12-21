#!/usr/bin/env python3
"""
Metrics Dashboard Generator - Calculate and visualize task metrics

Features:
- Task velocity calculation
- Confidence trends
- Health score generation
- Breakdown effectiveness metrics
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import sys

sys.path.insert(0, str(Path(__file__).parent))
from task_manager import TaskManager


class MetricsDashboard:
    """Generate task system metrics and dashboards"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.task_manager = TaskManager(base_path)
        self.metrics_dir = self.base_path / ".claude" / "analysis" / "metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

    def calculate_velocity(self) -> Dict[str, Any]:
        """Calculate task completion velocity"""
        velocity_data = {
            "current_velocity": 0,
            "average_velocity": 0,
            "velocity_by_phase": defaultdict(list),
            "trend": "stable"
        }

        all_tasks = self.task_manager.get_all_task_ids()
        velocities = []

        for task_id in all_tasks:
            task = self.task_manager.load_task(task_id)
            if task and task.momentum:
                velocity = task.momentum.get("velocity", 0)
                phase = task.momentum.get("phase", "unknown")
                velocities.append(velocity)
                velocity_data["velocity_by_phase"][phase].append(velocity)

        if velocities:
            velocity_data["current_velocity"] = velocities[-1] if velocities else 0
            velocity_data["average_velocity"] = sum(velocities) / len(velocities)

            # Calculate trend
            if len(velocities) >= 3:
                recent = velocities[-3:]
                if recent[-1] > recent[0]:
                    velocity_data["trend"] = "increasing"
                elif recent[-1] < recent[0]:
                    velocity_data["trend"] = "decreasing"

        # Average by phase
        for phase in velocity_data["velocity_by_phase"]:
            phase_velocities = velocity_data["velocity_by_phase"][phase]
            velocity_data["velocity_by_phase"][phase] = {
                "count": len(phase_velocities),
                "average": sum(phase_velocities) / len(phase_velocities) if phase_velocities else 0
            }

        return velocity_data

    def calculate_confidence_trends(self) -> Dict[str, Any]:
        """Calculate confidence score trends"""
        confidence_data = {
            "current_average": 0,
            "by_status": defaultdict(list),
            "by_difficulty": defaultdict(list),
            "low_confidence_tasks": [],
            "high_confidence_tasks": []
        }

        all_tasks = self.task_manager.get_all_task_ids()
        all_confidences = []

        for task_id in all_tasks:
            task = self.task_manager.load_task(task_id)
            if task:
                confidence = task.confidence
                all_confidences.append(confidence)
                confidence_data["by_status"][task.status].append(confidence)
                confidence_data["by_difficulty"][task.difficulty].append(confidence)

                if confidence < 30:
                    confidence_data["low_confidence_tasks"].append({
                        "id": task_id,
                        "title": task.title,
                        "confidence": confidence
                    })
                elif confidence >= 80:
                    confidence_data["high_confidence_tasks"].append({
                        "id": task_id,
                        "title": task.title,
                        "confidence": confidence
                    })

        if all_confidences:
            confidence_data["current_average"] = sum(all_confidences) / len(all_confidences)

        # Calculate averages
        for status in confidence_data["by_status"]:
            values = confidence_data["by_status"][status]
            confidence_data["by_status"][status] = {
                "count": len(values),
                "average": sum(values) / len(values) if values else 0
            }

        for difficulty in confidence_data["by_difficulty"]:
            values = confidence_data["by_difficulty"][difficulty]
            confidence_data["by_difficulty"][difficulty] = {
                "count": len(values),
                "average": sum(values) / len(values) if values else 0
            }

        return confidence_data

    def generate_health_score(self) -> Dict[str, Any]:
        """Generate overall system health score"""
        health_data = {
            "overall_score": 0,
            "components": {},
            "warnings": [],
            "recommendations": []
        }

        scores = []

        # Task completion rate
        all_tasks = self.task_manager.get_all_task_ids()
        finished_count = 0
        blocked_count = 0
        broken_down_count = 0

        for task_id in all_tasks:
            task = self.task_manager.load_task(task_id)
            if task:
                if task.status == "Finished":
                    finished_count += 1
                elif task.status == "Blocked":
                    blocked_count += 1
                elif task.status == "Broken Down":
                    broken_down_count += 1

        if all_tasks:
            completion_score = (finished_count / len(all_tasks)) * 100
            health_data["components"]["completion"] = completion_score
            scores.append(completion_score)

            if blocked_count > len(all_tasks) * 0.2:
                health_data["warnings"].append(f"High number of blocked tasks: {blocked_count}")

        # Velocity health
        velocity = self.calculate_velocity()
        if velocity["average_velocity"] > 50:
            velocity_score = 80
        elif velocity["average_velocity"] > 20:
            velocity_score = 60
        else:
            velocity_score = 40

        health_data["components"]["velocity"] = velocity_score
        scores.append(velocity_score)

        if velocity["trend"] == "decreasing":
            health_data["warnings"].append("Velocity trending downward")

        # Confidence health
        confidence = self.calculate_confidence_trends()
        confidence_score = confidence["current_average"]
        health_data["components"]["confidence"] = confidence_score
        scores.append(confidence_score)

        if len(confidence["low_confidence_tasks"]) > 5:
            health_data["warnings"].append(f"{len(confidence['low_confidence_tasks'])} low confidence tasks")

        # Breakdown health
        breakdown_metrics = self.analyze_breakdown_effectiveness()
        if breakdown_metrics["breakdown_success_rate"] > 0.8:
            breakdown_score = 90
        elif breakdown_metrics["breakdown_success_rate"] > 0.6:
            breakdown_score = 70
        else:
            breakdown_score = 50

        health_data["components"]["breakdown"] = breakdown_score
        scores.append(breakdown_score)

        # Overall score
        if scores:
            health_data["overall_score"] = sum(scores) / len(scores)

        # Generate recommendations
        if health_data["overall_score"] < 50:
            health_data["recommendations"].append("Consider reviewing blocked tasks")
            health_data["recommendations"].append("Focus on increasing task confidence")

        if velocity["average_velocity"] < 20:
            health_data["recommendations"].append("Review task complexity and breakdown strategy")

        return health_data

    def analyze_breakdown_effectiveness(self) -> Dict[str, Any]:
        """Analyze how effective task breakdowns have been"""
        breakdown_data = {
            "total_breakdowns": 0,
            "successful_breakdowns": 0,
            "breakdown_success_rate": 0,
            "average_subtasks": 0,
            "completion_by_difficulty": defaultdict(dict)
        }

        all_tasks = self.task_manager.get_all_task_ids()
        parent_tasks = []
        all_subtask_counts = []

        for task_id in all_tasks:
            task = self.task_manager.load_task(task_id)
            if task and task.subtasks:
                parent_tasks.append(task)
                breakdown_data["total_breakdowns"] += 1
                all_subtask_counts.append(len(task.subtasks))

                # Check if all subtasks are complete
                all_complete = True
                for subtask_id in task.subtasks:
                    subtask = self.task_manager.load_task(subtask_id)
                    if not subtask or subtask.status != "Finished":
                        all_complete = False
                        break

                if all_complete:
                    breakdown_data["successful_breakdowns"] += 1

                # Track by difficulty
                if task.difficulty not in breakdown_data["completion_by_difficulty"]:
                    breakdown_data["completion_by_difficulty"][task.difficulty] = {
                        "total": 0,
                        "completed": 0
                    }

                breakdown_data["completion_by_difficulty"][task.difficulty]["total"] += 1
                if all_complete:
                    breakdown_data["completion_by_difficulty"][task.difficulty]["completed"] += 1

        if breakdown_data["total_breakdowns"] > 0:
            breakdown_data["breakdown_success_rate"] = (
                breakdown_data["successful_breakdowns"] / breakdown_data["total_breakdowns"]
            )

        if all_subtask_counts:
            breakdown_data["average_subtasks"] = sum(all_subtask_counts) / len(all_subtask_counts)

        return breakdown_data

    def export_metrics_json(self) -> str:
        """Export all metrics as JSON"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "velocity": self.calculate_velocity(),
            "confidence": self.calculate_confidence_trends(),
            "health": self.generate_health_score(),
            "breakdown": self.analyze_breakdown_effectiveness(),
            "summary": self.task_manager.calculate_task_metrics()
        }

        output_file = self.metrics_dir / f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)

        return str(output_file)

    def generate_markdown_dashboard(self) -> str:
        """Generate markdown dashboard"""
        velocity = self.calculate_velocity()
        confidence = self.calculate_confidence_trends()
        health = self.generate_health_score()
        breakdown = self.analyze_breakdown_effectiveness()
        summary = self.task_manager.calculate_task_metrics()

        dashboard = f"""# Task Metrics Dashboard
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

## Health Score: {health['overall_score']:.1f}/100

### Components
- Completion: {health['components'].get('completion', 0):.1f}
- Velocity: {health['components'].get('velocity', 0):.1f}
- Confidence: {health['components'].get('confidence', 0):.1f}
- Breakdown: {health['components'].get('breakdown', 0):.1f}

### Warnings
{chr(10).join('- ' + w for w in health['warnings']) if health['warnings'] else '- None'}

### Recommendations
{chr(10).join('- ' + r for r in health['recommendations']) if health['recommendations'] else '- System healthy'}

## Velocity Metrics
- Current: {velocity['current_velocity']}
- Average: {velocity['average_velocity']:.1f}
- Trend: {velocity['trend']}

## Confidence Analysis
- Average: {confidence['current_average']:.1f}%
- Low confidence tasks: {len(confidence['low_confidence_tasks'])}
- High confidence tasks: {len(confidence['high_confidence_tasks'])}

## Breakdown Effectiveness
- Total breakdowns: {breakdown['total_breakdowns']}
- Success rate: {breakdown['breakdown_success_rate']*100:.1f}%
- Average subtasks: {breakdown['average_subtasks']:.1f}

## Task Summary
- Total tasks: {summary['total_tasks']}
- Tasks broken down: {summary['breakdown_count']}
- Average confidence: {summary['average_confidence']}%
- Average velocity: {summary['average_velocity']}

### Status Distribution
{chr(10).join(f"- {status}: {count}" for status, count in summary['by_status'].items())}

### Difficulty Distribution
{chr(10).join(f"- Level {diff}: {count}" for diff, count in sorted(summary['by_difficulty'].items()))}
"""
        return dashboard


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Metrics Dashboard")
    parser.add_argument("command", choices=["velocity", "confidence", "health",
                                           "breakdown", "dashboard", "export"],
                       help="Metrics command")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    dashboard = MetricsDashboard()

    if args.command == "velocity":
        velocity = dashboard.calculate_velocity()
        if args.json:
            print(json.dumps(velocity, indent=2, default=str))
        else:
            print(f"Current velocity: {velocity['current_velocity']}")
            print(f"Average velocity: {velocity['average_velocity']:.1f}")
            print(f"Trend: {velocity['trend']}")

    elif args.command == "confidence":
        confidence = dashboard.calculate_confidence_trends()
        if args.json:
            print(json.dumps(confidence, indent=2, default=str))
        else:
            print(f"Average confidence: {confidence['current_average']:.1f}%")
            print(f"Low confidence tasks: {len(confidence['low_confidence_tasks'])}")
            print(f"High confidence tasks: {len(confidence['high_confidence_tasks'])}")

    elif args.command == "health":
        health = dashboard.generate_health_score()
        if args.json:
            print(json.dumps(health, indent=2))
        else:
            print(f"Overall health: {health['overall_score']:.1f}/100")
            print("\nComponents:")
            for component, score in health['components'].items():
                print(f"  {component}: {score:.1f}")
            if health['warnings']:
                print("\nWarnings:")
                for warning in health['warnings']:
                    print(f"  - {warning}")

    elif args.command == "breakdown":
        breakdown = dashboard.analyze_breakdown_effectiveness()
        if args.json:
            print(json.dumps(breakdown, indent=2, default=str))
        else:
            print(f"Breakdown success rate: {breakdown['breakdown_success_rate']*100:.1f}%")
            print(f"Average subtasks: {breakdown['average_subtasks']:.1f}")

    elif args.command == "dashboard":
        md_dashboard = dashboard.generate_markdown_dashboard()
        if args.output:
            with open(args.output, 'w') as f:
                f.write(md_dashboard)
            print(f"Dashboard saved to {args.output}")
        else:
            print(md_dashboard)

    elif args.command == "export":
        output_file = dashboard.export_metrics_json()
        print(f"Metrics exported to {output_file}")


if __name__ == "__main__":
    main()