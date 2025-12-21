#!/usr/bin/env python3
"""
Dependency Graph Analyzer - Analyze and visualize task dependencies

Features:
- Detect circular dependencies
- Find critical path
- Suggest parallelizable tasks
- Generate dependency visualizations
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import deque, defaultdict
import sys

# Try to import networkx for advanced graph operations
try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    print("Warning: NetworkX not installed. Some features will be limited.")

# Import task manager
sys.path.insert(0, str(Path(__file__).parent))
from task_manager import TaskManager

# Import conflict detector if available
try:
    from conflict_detector import ConflictDetector, ConflictType
    CONFLICT_DETECTOR_AVAILABLE = True
except ImportError:
    CONFLICT_DETECTOR_AVAILABLE = False

# Import file lock manager if available
try:
    from file_lock_manager import FileLockManager, is_locked
    LOCKS_AVAILABLE = True
except ImportError:
    LOCKS_AVAILABLE = False


class DependencyAnalyzer:
    """Analyze task dependency graphs"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.task_manager = TaskManager(base_path)
        self.graph = None
        self._build_graph()

    def _build_graph(self):
        """Build dependency graph from tasks"""
        if HAS_NETWORKX:
            self.graph = nx.DiGraph()
        else:
            self.graph = {}  # Simple adjacency list

        all_tasks = self.task_manager.get_all_task_ids()

        for task_id in all_tasks:
            task = self.task_manager.load_task(task_id)
            if not task:
                continue

            if HAS_NETWORKX:
                self.graph.add_node(task_id, **{
                    "title": task.title,
                    "difficulty": task.difficulty,
                    "status": task.status
                })

                for dep in task.dependencies:
                    if dep in all_tasks:
                        self.graph.add_edge(dep, task_id)
            else:
                # Simple graph representation
                if task_id not in self.graph:
                    self.graph[task_id] = {
                        "dependencies": task.dependencies,
                        "dependents": [],
                        "data": {
                            "title": task.title,
                            "difficulty": task.difficulty,
                            "status": task.status
                        }
                    }

        # Build reverse dependencies for simple graph
        if not HAS_NETWORKX:
            for task_id, node in self.graph.items():
                for dep in node["dependencies"]:
                    if dep in self.graph:
                        self.graph[dep]["dependents"].append(task_id)

    def detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependency chains"""
        if HAS_NETWORKX:
            try:
                cycles = list(nx.simple_cycles(self.graph))
                return cycles
            except:
                return []
        else:
            # Simple DFS-based cycle detection
            cycles = []
            visited = set()
            rec_stack = set()

            def dfs(node, path):
                visited.add(node)
                rec_stack.add(node)
                path.append(node)

                if node in self.graph:
                    for neighbor in self.graph[node]["dependencies"]:
                        if neighbor not in visited:
                            if dfs(neighbor, path.copy()):
                                return True
                        elif neighbor in rec_stack:
                            # Found cycle
                            cycle_start = path.index(neighbor)
                            cycle = path[cycle_start:] + [neighbor]
                            if cycle not in cycles:
                                cycles.append(cycle)

                rec_stack.remove(node)
                return False

            for node in self.graph:
                if node not in visited:
                    dfs(node, [])

            return cycles

    def find_critical_path(self) -> List[str]:
        """Find the critical path (longest path) through the graph"""
        if HAS_NETWORKX:
            try:
                # For DAG, find longest path
                if nx.is_directed_acyclic_graph(self.graph):
                    return nx.dag_longest_path(self.graph, weight='difficulty')
                else:
                    return []
            except:
                return []
        else:
            # Simple topological sort and dynamic programming
            return self._find_longest_path_simple()

    def _find_longest_path_simple(self) -> List[str]:
        """Find longest path without NetworkX"""
        # Topological sort
        in_degree = defaultdict(int)
        for node in self.graph:
            for dep in self.graph[node]["dependencies"]:
                if dep in self.graph:
                    in_degree[dep] += 1

        queue = deque([node for node in self.graph if in_degree[node] == 0])
        topo_order = []

        while queue:
            node = queue.popleft()
            topo_order.append(node)

            for dependent in self.graph[node].get("dependents", []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Find longest path
        distance = {node: 0 for node in self.graph}
        parent = {node: None for node in self.graph}

        for node in topo_order:
            for dep in self.graph[node]["dependencies"]:
                if dep in self.graph:
                    new_dist = distance[dep] + self.graph[node]["data"]["difficulty"]
                    if new_dist > distance[node]:
                        distance[node] = new_dist
                        parent[node] = dep

        # Reconstruct path
        if not distance:
            return []

        end_node = max(distance, key=distance.get)
        path = []
        current = end_node

        while current:
            path.append(current)
            current = parent[current]

        return list(reversed(path))

    def suggest_parallelizable_tasks(self, check_conflicts: bool = True,
                                    max_group_size: int = 5) -> List[Set[str]]:
        """Find groups of tasks that can be executed in parallel.

        Args:
            check_conflicts: Whether to check for file conflicts
            max_group_size: Maximum tasks per parallel group

        Returns:
            List of task ID sets that can run in parallel
        """
        # Get basic parallel groups from dependency analysis
        if HAS_NETWORKX:
            try:
                # Use topological generations
                if nx.is_directed_acyclic_graph(self.graph):
                    generations = list(nx.topological_generations(self.graph))
                    basic_groups = [set(gen) for gen in generations]
                else:
                    return []
            except:
                return []
        else:
            # Level-based grouping
            basic_groups = self._find_parallel_groups_simple()

        # Refine groups with conflict checking if available
        if check_conflicts and CONFLICT_DETECTOR_AVAILABLE:
            return self._refine_with_conflict_check(basic_groups, max_group_size)
        else:
            # Just apply size limit
            return self._apply_size_limit(basic_groups, max_group_size)

    def _find_parallel_groups_simple(self) -> List[Set[str]]:
        """Find parallel groups without NetworkX"""
        levels = {}
        visited = set()

        def get_level(node):
            if node in levels:
                return levels[node]

            if node not in self.graph:
                levels[node] = 0
                return 0

            max_dep_level = -1
            for dep in self.graph[node]["dependencies"]:
                if dep in self.graph:
                    dep_level = get_level(dep)
                    max_dep_level = max(max_dep_level, dep_level)

            levels[node] = max_dep_level + 1
            return levels[node]

        # Calculate levels for all nodes
        for node in self.graph:
            get_level(node)

        # Group by level
        level_groups = defaultdict(set)
        for node, level in levels.items():
            level_groups[level].add(node)

        return [group for level, group in sorted(level_groups.items())]

    def find_parallel_safe_groups(self, task_ids: Optional[List[str]] = None,
                                 check_all: bool = True) -> List[List[str]]:
        """Find groups of tasks that are safe to execute in parallel.

        This method considers:
        - Dependency graph constraints
        - File conflicts
        - Lock contention
        - Agent capacity

        Args:
            task_ids: Specific tasks to analyze (None = all pending tasks)
            check_all: Whether to check all safety conditions

        Returns:
            List of task groups that can safely run in parallel
        """
        # Get tasks to analyze
        if task_ids is None:
            # Get all pending tasks
            task_ids = []
            for task_id in self.task_manager.get_all_task_ids():
                task = self.task_manager.load_task(task_id)
                if task and task.status in ["Pending", "In Progress"]:
                    task_ids.append(task_id)

        if not task_ids:
            return []

        # Build initial groups from dependency analysis
        initial_groups = self.suggest_parallelizable_tasks(check_conflicts=False)

        # Filter to only include requested task IDs
        task_set = set(task_ids)
        filtered_groups = []
        for group in initial_groups:
            filtered = group & task_set
            if filtered:
                filtered_groups.append(list(filtered))

        if not check_all:
            return filtered_groups

        # Apply safety checks
        safe_groups = []

        for group in filtered_groups:
            # Check file conflicts
            if CONFLICT_DETECTOR_AVAILABLE:
                detector = ConflictDetector()
                can_parallel, blocking = detector.validate_parallel_execution(group)

                if not can_parallel:
                    # Split group to avoid conflicts
                    subgroups = self._split_conflicting_group(group, blocking)
                    safe_groups.extend(subgroups)
                    continue

            # Check lock availability
            if LOCKS_AVAILABLE:
                lock_manager = FileLockManager()
                locked_tasks = []

                for task_id in group:
                    task = self.task_manager.load_task(task_id)
                    if task:
                        for file_path in task.files_affected:
                            if not ('*' in file_path or file_path.endswith('/')):
                                if lock_manager.is_locked(Path(file_path)):
                                    locked_tasks.append(task_id)
                                    break

                # Remove tasks with locked files
                group = [t for t in group if t not in locked_tasks]

            # Apply agent capacity limit
            max_parallel = 5  # Configurable
            if len(group) > max_parallel:
                # Split into smaller batches
                for i in range(0, len(group), max_parallel):
                    safe_groups.append(group[i:i+max_parallel])
            elif group:
                safe_groups.append(group)

        return safe_groups

    def _refine_with_conflict_check(self, basic_groups: List[Set[str]],
                                   max_group_size: int) -> List[Set[str]]:
        """Refine parallel groups by checking for file conflicts."""
        detector = ConflictDetector()
        refined_groups = []

        for group in basic_groups:
            if len(group) <= 1:
                refined_groups.append(group)
                continue

            # Check for conflicts within the group
            group_list = list(group)
            can_parallel, blocking = detector.validate_parallel_execution(group_list)

            if can_parallel:
                # No conflicts, apply size limit
                if len(group) > max_group_size:
                    # Split into smaller groups
                    for i in range(0, len(group_list), max_group_size):
                        refined_groups.append(set(group_list[i:i+max_group_size]))
                else:
                    refined_groups.append(group)
            else:
                # Has conflicts, need to split
                subgroups = self._split_conflicting_group(group_list, blocking)
                for subgroup in subgroups:
                    if len(subgroup) > max_group_size:
                        # Further split by size
                        for i in range(0, len(subgroup), max_group_size):
                            refined_groups.append(set(subgroup[i:i+max_group_size]))
                    else:
                        refined_groups.append(set(subgroup))

        return refined_groups

    def _split_conflicting_group(self, group: List[str],
                                blocking_conflicts: List) -> List[List[str]]:
        """Split a group with conflicts into conflict-free subgroups."""
        # Build conflict graph
        conflict_graph = defaultdict(set)
        for conflict in blocking_conflicts:
            conflict_graph[conflict.task1_id].add(conflict.task2_id)
            conflict_graph[conflict.task2_id].add(conflict.task1_id)

        # Use graph coloring to find conflict-free groups
        colors = {}
        color_groups = defaultdict(list)

        for task in group:
            # Find first available color
            used_colors = {colors[neighbor]
                          for neighbor in conflict_graph[task]
                          if neighbor in colors}

            color = 0
            while color in used_colors:
                color += 1

            colors[task] = color
            color_groups[color].append(task)

        return list(color_groups.values())

    def _apply_size_limit(self, groups: List[Set[str]],
                         max_size: int) -> List[Set[str]]:
        """Apply size limit to parallel groups."""
        limited_groups = []

        for group in groups:
            if len(group) <= max_size:
                limited_groups.append(group)
            else:
                # Split large group
                group_list = list(group)
                for i in range(0, len(group_list), max_size):
                    limited_groups.append(set(group_list[i:i+max_size]))

        return limited_groups

    def visualize_dependency_graph(self) -> str:
        """Generate Mermaid diagram of dependency graph"""
        lines = ["graph TD"]

        all_tasks = self.task_manager.get_all_task_ids()

        for task_id in all_tasks:
            task = self.task_manager.load_task(task_id)
            if not task:
                continue

            # Node definition with styling based on status
            node_label = f"{task_id}: {task.title[:30]}"
            if task.status == "Finished":
                lines.append(f"    {task_id}[\"{node_label}\"]::finished")
            elif task.status == "In Progress":
                lines.append(f"    {task_id}[\"{node_label}\"]::inprogress")
            else:
                lines.append(f"    {task_id}[\"{node_label}\"]")

            # Edges
            for dep in task.dependencies:
                if dep in all_tasks:
                    lines.append(f"    {dep} --> {task_id}")

        # Add styling
        lines.extend([
            "",
            "    classDef finished fill:#90EE90",
            "    classDef inprogress fill:#FFD700"
        ])

        return "\n".join(lines)

    def get_task_impact(self, task_id: str) -> Dict[str, Any]:
        """Analyze impact of a task (what depends on it)"""
        if HAS_NETWORKX and self.graph:
            try:
                descendants = list(nx.descendants(self.graph, task_id))
                ancestors = list(nx.ancestors(self.graph, task_id))
                return {
                    "direct_dependents": list(self.graph.successors(task_id)),
                    "total_dependents": descendants,
                    "depends_on": ancestors,
                    "impact_score": len(descendants)
                }
            except:
                pass

        # Fallback to simple analysis
        if task_id not in self.graph:
            return {"error": "Task not found"}

        return {
            "direct_dependents": self.graph[task_id].get("dependents", []),
            "depends_on": self.graph[task_id].get("dependencies", []),
            "impact_score": len(self.graph[task_id].get("dependents", []))
        }

    def find_blockers(self) -> List[Dict]:
        """Find tasks that are blocking the most other tasks"""
        blockers = []

        for task_id in self.graph:
            task = self.task_manager.load_task(task_id)
            if task and task.status != "Finished":
                impact = self.get_task_impact(task_id)
                if impact.get("impact_score", 0) > 0:
                    blockers.append({
                        "task_id": task_id,
                        "title": task.title,
                        "status": task.status,
                        "blocking_count": impact["impact_score"],
                        "directly_blocking": impact.get("direct_dependents", [])
                    })

        return sorted(blockers, key=lambda x: x["blocking_count"], reverse=True)


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Dependency Analyzer")
    parser.add_argument("command", choices=["cycles", "critical-path", "parallel",
                                           "visualize", "impact", "blockers"],
                       help="Analysis command")
    parser.add_argument("--task-id", help="Task ID for impact analysis")
    parser.add_argument("--output", help="Output file for visualization")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    analyzer = DependencyAnalyzer()

    if args.command == "cycles":
        cycles = analyzer.detect_circular_dependencies()
        if args.json:
            print(json.dumps(cycles, indent=2))
        else:
            if cycles:
                print("Circular dependencies detected:")
                for cycle in cycles:
                    print(f"  {' -> '.join(cycle)}")
            else:
                print("No circular dependencies found")

    elif args.command == "critical-path":
        path = analyzer.find_critical_path()
        if args.json:
            print(json.dumps(path, indent=2))
        else:
            if path:
                print("Critical path:")
                for task_id in path:
                    task = analyzer.task_manager.load_task(task_id)
                    if task:
                        print(f"  {task_id}: {task.title} (difficulty: {task.difficulty})")
            else:
                print("No critical path found")

    elif args.command == "parallel":
        groups = analyzer.suggest_parallelizable_tasks()
        if args.json:
            print(json.dumps([list(g) for g in groups], indent=2))
        else:
            print("Parallelizable task groups:")
            for i, group in enumerate(groups):
                print(f"\nLevel {i}:")
                for task_id in group:
                    task = analyzer.task_manager.load_task(task_id)
                    if task:
                        print(f"  {task_id}: {task.title}")

    elif args.command == "visualize":
        diagram = analyzer.visualize_dependency_graph()
        if args.output:
            with open(args.output, 'w') as f:
                f.write(diagram)
            print(f"Diagram saved to {args.output}")
        else:
            print(diagram)

    elif args.command == "impact":
        if not args.task_id:
            print("Task ID required for impact analysis")
            return

        impact = analyzer.get_task_impact(args.task_id)
        if args.json:
            print(json.dumps(impact, indent=2))
        else:
            print(f"Impact analysis for {args.task_id}:")
            print(f"  Directly blocks: {impact.get('direct_dependents', [])}")
            print(f"  Total impact: {impact.get('impact_score', 0)} tasks")

    elif args.command == "blockers":
        blockers = analyzer.find_blockers()
        if args.json:
            print(json.dumps(blockers, indent=2))
        else:
            print("Top blocking tasks:")
            for blocker in blockers[:10]:
                print(f"\n{blocker['task_id']}: {blocker['title']}")
                print(f"  Status: {blocker['status']}")
                print(f"  Blocking {blocker['blocking_count']} tasks")


if __name__ == "__main__":
    main()