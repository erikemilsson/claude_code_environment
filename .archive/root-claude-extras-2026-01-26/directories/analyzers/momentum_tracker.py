#!/usr/bin/env python3
"""
Momentum Tracker Analyzer
Tracks and analyzes task momentum, velocity, and phase transitions.
Adapted from belief_tracker for Claude Code environment.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum


class MomentumPhase(Enum):
    """Momentum phases for tasks."""
    PENDING = "pending"           # Not started
    IGNITION = "ignition"         # Just starting (0-20 velocity)
    BUILDING = "building"         # Accelerating (20-50 velocity)
    CRUISING = "cruising"         # Steady progress (50-80 velocity)
    COASTING = "coasting"         # Slowing down (30-60 velocity)
    STALLING = "stalling"         # Nearly stopped (10-30 velocity)
    STOPPED = "stopped"           # No progress (0 velocity)


class MomentumTracker:
    """Analyzes and tracks task momentum."""

    def __init__(self, tasks_dir: str = ".claude/tasks"):
        """Initialize the momentum tracker.

        Args:
            tasks_dir: Directory containing task JSON files
        """
        self.tasks_dir = Path(tasks_dir)
        self.tasks = {}
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load all task JSON files."""
        if not self.tasks_dir.exists():
            raise ValueError(f"Tasks directory {self.tasks_dir} does not exist")

        for json_file in self.tasks_dir.glob("task-*.json"):
            try:
                with open(json_file, 'r') as f:
                    task = json.load(f)
                    self.tasks[task['id']] = task
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

    def calculate_velocity(self, task: Dict) -> int:
        """Calculate velocity for a task based on activity and progress.

        Args:
            task: Task dictionary

        Returns:
            Velocity score (0-100)
        """
        velocity = 0

        # Base velocity from status
        status_velocity = {
            'Finished': 100,
            'In Progress': 50,
            'Pending': 0,
            'Blocked': 0,
            'Broken Down': 30
        }
        velocity = status_velocity.get(task.get('status', 'Pending'), 0)

        # Adjust for days since last activity
        if 'momentum' in task and 'last_activity' in task['momentum']:
            last_activity = datetime.strptime(
                task['momentum']['last_activity'],
                '%Y-%m-%d'
            )
            days_inactive = (datetime.now() - last_activity).days

            if days_inactive > 7:
                velocity -= 30
            elif days_inactive > 3:
                velocity -= 20
            elif days_inactive > 1:
                velocity -= 10
            elif days_inactive == 0:
                velocity += 10

        # Adjust for blockers
        if task.get('status') == 'Blocked':
            velocity = 0
        elif 'blocked' in task.get('notes', '').lower():
            velocity -= 20

        # Adjust for confidence
        confidence = task.get('confidence', 75)
        if confidence >= 80:
            velocity += 10
        elif confidence < 50:
            velocity -= 15

        # Adjust for assumptions
        if 'assumptions' in task:
            invalidated = sum(1 for a in task['assumptions']
                            if a.get('status') == 'invalidated')
            velocity -= invalidated * 15

        # Adjust for subtask progress
        if task.get('subtasks'):
            completed = sum(1 for sid in task['subtasks']
                          if sid in self.tasks and
                          self.tasks[sid].get('status') == 'Finished')
            total = len(task['subtasks'])
            if total > 0:
                completion_rate = completed / total
                velocity = int(velocity * (0.5 + completion_rate * 0.5))

        # Keep within bounds
        return max(0, min(100, velocity))

    def determine_phase(self, velocity: int, current_phase: str = 'pending') -> str:
        """Determine momentum phase based on velocity.

        Args:
            velocity: Current velocity (0-100)
            current_phase: Current phase for hysteresis

        Returns:
            Phase name
        """
        # Use hysteresis to prevent rapid phase changes
        phase_ranges = {
            MomentumPhase.STOPPED: (0, 5),
            MomentumPhase.STALLING: (5, 30),
            MomentumPhase.IGNITION: (10, 25),
            MomentumPhase.COASTING: (25, 60),
            MomentumPhase.BUILDING: (20, 55),
            MomentumPhase.CRUISING: (45, 100),
            MomentumPhase.PENDING: (0, 0)  # Special case
        }

        # Special handling for status-based phases
        if velocity == 0 and current_phase == 'pending':
            return MomentumPhase.PENDING.value

        # Find best matching phase
        current_enum = MomentumPhase(current_phase) if current_phase else MomentumPhase.PENDING

        # Check if current phase still valid
        min_v, max_v = phase_ranges[current_enum]
        if min_v <= velocity <= max_v and current_phase != 'pending':
            return current_phase

        # Find new phase
        if velocity >= 50:
            return MomentumPhase.CRUISING.value
        elif velocity >= 30:
            if current_enum in [MomentumPhase.CRUISING, MomentumPhase.COASTING]:
                return MomentumPhase.COASTING.value
            else:
                return MomentumPhase.BUILDING.value
        elif velocity >= 15:
            if current_enum == MomentumPhase.BUILDING:
                return MomentumPhase.BUILDING.value
            else:
                return MomentumPhase.IGNITION.value
        elif velocity > 0:
            return MomentumPhase.STALLING.value
        else:
            return MomentumPhase.STOPPED.value

    def detect_momentum_risks(self, task: Dict) -> List[str]:
        """Detect momentum-related risks for a task.

        Args:
            task: Task dictionary

        Returns:
            List of risk descriptions
        """
        risks = []

        # Check velocity
        velocity = self.calculate_velocity(task)
        if velocity < 20 and task.get('status') == 'In Progress':
            risks.append(f"Low velocity ({velocity}) for active task")

        # Check phase
        phase = task.get('momentum', {}).get('phase', 'pending')
        if phase in ['stalling', 'stopped'] and task.get('status') == 'In Progress':
            risks.append(f"Task is {phase} despite being in progress")

        # Check last activity
        if 'momentum' in task and 'last_activity' in task['momentum']:
            last_activity = datetime.strptime(
                task['momentum']['last_activity'],
                '%Y-%m-%d'
            )
            days_inactive = (datetime.now() - last_activity).days
            if days_inactive > 7:
                risks.append(f"No activity for {days_inactive} days")

        # Check confidence decline
        if task.get('confidence', 75) < 50:
            risks.append(f"Low confidence ({task['confidence']})")

        # Check for blockers
        if task.get('status') == 'Blocked':
            risks.append("Task is blocked")

        # Check assumption invalidations
        if 'assumptions' in task:
            invalidated = [a for a in task['assumptions']
                         if a.get('status') == 'invalidated']
            if invalidated:
                risks.append(f"{len(invalidated)} assumptions invalidated")

        return risks

    def detect_momentum_transfer(self) -> List[Dict]:
        """Detect opportunities for momentum transfer between tasks.

        Returns:
            List of transfer opportunities
        """
        transfers = []

        for task_id, task in self.tasks.items():
            velocity = self.calculate_velocity(task)

            # Find related tasks
            related = self.find_related_tasks(task_id)

            for related_id in related:
                related_task = self.tasks.get(related_id)
                if not related_task:
                    continue

                related_velocity = self.calculate_velocity(related_task)

                # High velocity can boost related tasks
                if velocity > 70 and related_velocity < 30:
                    if related_task.get('status') == 'Pending':
                        transfers.append({
                            'from': task_id,
                            'to': related_id,
                            'type': 'boost',
                            'reason': 'High velocity task can energize related pending task',
                            'from_velocity': velocity,
                            'to_velocity': related_velocity
                        })

                # Completing task boosts dependents
                if (task.get('status') == 'Finished' and
                    task_id in related_task.get('dependencies', [])):
                    transfers.append({
                        'from': task_id,
                        'to': related_id,
                        'type': 'unblock',
                        'reason': 'Completed dependency unblocks task',
                        'from_velocity': velocity,
                        'to_velocity': related_velocity
                    })

                # Stalling task may affect dependents
                if (velocity < 20 and
                    related_id in task.get('dependencies', [])):
                    transfers.append({
                        'from': task_id,
                        'to': related_id,
                        'type': 'risk',
                        'reason': 'Stalling task may delay dependent',
                        'from_velocity': velocity,
                        'to_velocity': related_velocity
                    })

        return transfers

    def find_related_tasks(self, task_id: str) -> List[str]:
        """Find tasks related to the given task.

        Args:
            task_id: Task ID to find relations for

        Returns:
            List of related task IDs
        """
        related = set()
        task = self.tasks.get(task_id, {})

        # Direct relations
        related.update(task.get('dependencies', []))
        related.update(task.get('subtasks', []))
        if task.get('parent_task'):
            related.add(task['parent_task'])

        # Reverse relations
        for other_id, other_task in self.tasks.items():
            if other_id == task_id:
                continue

            if task_id in other_task.get('dependencies', []):
                related.add(other_id)
            if task_id in other_task.get('subtasks', []):
                related.add(other_id)
            if other_task.get('parent_task') == task_id:
                related.add(other_id)

        return list(related)

    def update_task_momentum(self, task_id: str) -> Dict:
        """Update momentum information for a task.

        Args:
            task_id: Task ID to update

        Returns:
            Updated momentum data
        """
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        velocity = self.calculate_velocity(task)
        current_phase = task.get('momentum', {}).get('phase', 'pending')
        new_phase = self.determine_phase(velocity, current_phase)

        momentum = {
            'phase': new_phase,
            'velocity': velocity,
            'last_activity': task.get('updated_date', str(datetime.now().date()))
        }

        # Update task
        task['momentum'] = momentum

        # Save to file
        task_file = self.tasks_dir / f"task-{task_id}.json"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)

        return momentum

    def generate_momentum_report(self) -> str:
        """Generate a momentum analysis report.

        Returns:
            Markdown formatted report
        """
        report = ["# Momentum Analysis Report"]
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Phase distribution
        phase_counts = {}
        for task in self.tasks.values():
            phase = task.get('momentum', {}).get('phase', 'pending')
            phase_counts[phase] = phase_counts.get(phase, 0) + 1

        report.append("\n## Phase Distribution")
        for phase, count in sorted(phase_counts.items()):
            report.append(f"- **{phase.title()}**: {count} tasks")

        # Velocity statistics
        velocities = [self.calculate_velocity(t) for t in self.tasks.values()]
        if velocities:
            avg_velocity = sum(velocities) / len(velocities)
            report.append(f"\n## Velocity Statistics")
            report.append(f"- **Average**: {avg_velocity:.1f}")
            report.append(f"- **Highest**: {max(velocities)}")
            report.append(f"- **Lowest**: {min(velocities)}")

        # At-risk tasks
        report.append("\n## At-Risk Tasks")
        at_risk = []
        for task_id, task in self.tasks.items():
            risks = self.detect_momentum_risks(task)
            if risks and task.get('status') == 'In Progress':
                at_risk.append((task_id, task['title'], risks))

        if at_risk:
            for task_id, title, risks in at_risk:
                report.append(f"\n### Task {task_id}: {title}")
                for risk in risks:
                    report.append(f"- ⚠️ {risk}")
        else:
            report.append("No at-risk tasks identified.")

        # Momentum transfer opportunities
        report.append("\n## Momentum Transfer Opportunities")
        transfers = self.detect_momentum_transfer()
        boost_transfers = [t for t in transfers if t['type'] == 'boost']

        if boost_transfers:
            for transfer in boost_transfers[:5]:  # Top 5
                report.append(
                    f"- Task {transfer['from']} (v={transfer['from_velocity']}) → "
                    f"Task {transfer['to']} (v={transfer['to_velocity']}): "
                    f"{transfer['reason']}"
                )
        else:
            report.append("No momentum transfer opportunities identified.")

        # Recommendations
        report.append("\n## Recommendations")
        recommendations = self.generate_recommendations()
        for rec in recommendations:
            report.append(f"- {rec}")

        return "\n".join(report)

    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on momentum analysis.

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Check for stalling tasks
        stalling = [t for t in self.tasks.values()
                   if t.get('momentum', {}).get('phase') == 'stalling'
                   and t.get('status') == 'In Progress']
        if stalling:
            recommendations.append(
                f"Address {len(stalling)} stalling tasks immediately to prevent complete stoppage"
            )

        # Check for blocked tasks
        blocked = [t for t in self.tasks.values()
                  if t.get('status') == 'Blocked']
        if blocked:
            recommendations.append(
                f"Resolve blockers for {len(blocked)} tasks to restore momentum"
            )

        # Check for low confidence tasks
        low_conf = [t for t in self.tasks.values()
                   if t.get('confidence', 75) < 50
                   and t.get('status') in ['Pending', 'In Progress']]
        if low_conf:
            recommendations.append(
                f"Investigate {len(low_conf)} low-confidence tasks for potential issues"
            )

        # Check for inactive tasks
        inactive_threshold = datetime.now() - timedelta(days=7)
        inactive = []
        for task in self.tasks.values():
            if task.get('status') == 'In Progress':
                last_activity = task.get('momentum', {}).get('last_activity')
                if last_activity:
                    activity_date = datetime.strptime(last_activity, '%Y-%m-%d')
                    if activity_date < inactive_threshold:
                        inactive.append(task)

        if inactive:
            recommendations.append(
                f"Review {len(inactive)} tasks with no activity in 7+ days"
            )

        # Suggest momentum boosting
        high_velocity = [t for t in self.tasks.values()
                        if self.calculate_velocity(t) > 70]
        if high_velocity:
            recommendations.append(
                "Leverage high-velocity tasks to energize related work"
            )

        if not recommendations:
            recommendations.append("Momentum is healthy - maintain current pace")

        return recommendations


def main():
    """Main entry point for momentum tracking."""
    tracker = MomentumTracker()

    # Update all task momentum
    print("Updating task momentum...")
    for task_id in tracker.tasks:
        try:
            momentum = tracker.update_task_momentum(task_id)
            print(f"Task {task_id}: phase={momentum['phase']}, velocity={momentum['velocity']}")
        except Exception as e:
            print(f"Error updating task {task_id}: {e}")

    # Generate report
    print("\n" + "=" * 50)
    report = tracker.generate_momentum_report()
    print(report)

    # Save report
    report_file = Path(".claude/reports") / f"momentum-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    report_file.parent.mkdir(exist_ok=True, parents=True)
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()