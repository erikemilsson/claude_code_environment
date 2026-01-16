# Breakdown Workflow

## When to Break Down
- Task difficulty >= 7
- Task feels too big for one session
- Requirements are unclear (breaking down clarifies)

## How It Works

### Before
```
Task 1: "Build auth system" (difficulty 8, status: Pending)
```

### After Breakdown
```
Task 1: status = "Broken Down", subtasks = ["1_1", "1_2", "1_3"]
Task 1_1: "Setup OAuth" (difficulty 5, parent: "1")
Task 1_2: "Login flow" (difficulty 4, parent: "1")
Task 1_3: "Sessions" (difficulty 5, parent: "1")
```

### After Completing Subtasks
```
Task 1: status = "Finished" (auto-completed)
Task 1_1: "Finished"
Task 1_2: "Finished"
Task 1_3: "Finished"
```

## Rules

1. **Broken Down tasks are containers** - you can't work on them directly
2. **Subtasks should be difficulty <= 6** - that's the point of breaking down
3. **Auto-completion** - parent finishes when all subtasks finish
4. **One level only** - no subtasks of subtasks

## FAQ

**Can I break down a task that's already In Progress?**
Yes, if you discover it's more complex than expected.

**Can I undo a breakdown?**
Not directly. Either complete the subtasks or delete them and reset the parent.

**How do I track time?**
Track on subtasks, not the parent. Parent time = sum of subtask time.
