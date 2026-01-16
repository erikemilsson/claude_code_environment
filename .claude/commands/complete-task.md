<!-- Type: Agent-Invoked | Execution Guardian Agent -->
<!-- Template Variables:
{{PROJECT_NAME}} - Filled during bootstrap
{{DOMAIN_CONTEXT}} - From specification
{{VALIDATION_RULES}} - Custom validation if applicable
-->

# Complete Task Command

## Purpose
Start and finish tasks with proper status tracking. This command now uses the **Execution Guardian Agent** to ensure validation gates, checkpoints, and quality standards.

## Agent Integration

**This command invokes the Execution Guardian Agent**:
```markdown
AGENT: Execution Guardian
PHASE: Task Execution
OWNERSHIP: Validation gates, checkpoints, progress tracking, error recovery
```

The Execution Guardian will:
1. Run mandatory pre-execution validation gates
2. Monitor execution progress and confidence
3. Create checkpoints at strategic points
4. Validate completion criteria
5. Hand off to Task Orchestrator for parent checks

## Context Required
- Task ID to work on
- Understanding of task requirements
- `.claude/agents/execution-guardian.md` - Agent definition
- `.claude/agent-config.json` - Agent ownership matrix

## Process (Agent-Driven)

### 1. Invoke Execution Guardian
```markdown
User: "Complete task 003"

System: Task exists with status "Pending"
System: Activating Execution Guardian Agent

Execution Guardian: "Running pre-execution validation gates..."
Execution Guardian: "Checking task readiness and dependencies..."
```

### 2. Agent Performs Pre-Execution Validation
The Execution Guardian will automatically:
- Validate task status is appropriate
- Check all dependencies are met
- Verify resources are available
- Assess initial confidence level
- Create initial checkpoint

### 3. Agent Manages Execution
```markdown
Execution Guardian: "All gates PASSED. Beginning task execution."
Execution Guardian: "Initial confidence: 75%"
Execution Guardian: "Creating checkpoint before starting..."

[Work progresses]

Execution Guardian: "Progress: Step 3 of 7 complete"
Execution Guardian: "Confidence stable at 72%"
Execution Guardian: "Creating checkpoint before risky operation..."
```

### 4. Agent Validates Completion
```markdown
Execution Guardian: "Task work complete. Running post-execution gates..."
Execution Guardian: "Checking acceptance criteria..."
Execution Guardian: "Validating quality standards..."
Execution Guardian: "All gates PASSED. Task marked as Finished."
```

### 5. Agent Handoff (if subtask)
```markdown
Execution Guardian: "Task 003_2 completed successfully."
Execution Guardian: "Handing off to Task Orchestrator for parent check..."

Task Orchestrator: "Received handoff. Checking if parent 003 can be auto-completed..."
```

## Script Integration (If Available)

**The Execution Guardian uses Python scripts for validation:**
```bash
# Pre-execution validation
python scripts/validation-gates.py pre --task-id {ID}

# Progress checkpoints
python scripts/checkpoint-manager.py create --task-id {ID}

# Post-execution validation
python scripts/validation-gates.py post --task-id {ID}

# Metrics update
python scripts/metrics-dashboard.py update --task-id {ID}
```

## Monitoring Integration

**The Execution Guardian triggers monitoring at key points:**

### Pre-Task Monitoring
```bash
# Update health status before starting
python .claude/monitor/scripts/health_checker.py --check-before-task {ID}

# Update dashboard with task start
python .claude/monitor/scripts/dashboard_updater.py --task-start {ID}
```

### During-Task Monitoring
```bash
# Create monitoring checkpoint (every 3 steps or on warnings)
python .claude/monitor/scripts/health_checker.py --checkpoint {ID}

# Update live dashboard with progress
python .claude/monitor/scripts/dashboard_updater.py --progress {ID} --step {STEP}

# If errors occur, trigger diagnosis
python .claude/monitor/scripts/diagnose.py --error "{ERROR_MSG}" --task {ID}
```

### Post-Task Monitoring
```bash
# Final health check after completion
python .claude/monitor/scripts/health_checker.py --check-after-task {ID}

# Update dashboard with completion
python .claude/monitor/scripts/dashboard_updater.py --task-complete {ID}

# Generate performance metrics
python .claude/monitor/scripts/quick_status.py --task-metrics {ID}
```

### Error Recovery Monitoring
```bash
# On task failure or blocking
python .claude/monitor/scripts/diagnose.py --task-failed {ID}
python .claude/monitor/scripts/self_heal.py --recommend-fix {ID}

# Update monitoring with failure
python .claude/monitor/scripts/dashboard_updater.py --task-blocked {ID}
```

## Manual Process (Fallback if agent unavailable)
```
VALIDATION_GATE: task_start_gate
├── CHECK: Task file exists and is readable
├── CHECK: Status is "Pending" or "In Progress"
├── CHECK: Not "Broken Down" (work on subtasks instead)
├── CHECK: Not "Finished" (already complete)
├── CHECK: All dependencies are "Finished"
├── CHECK: No unresolved blockers
├── CHECK: Confidence can be established (>50%)
└── RESULT: PASS → Continue | FAIL → Stop with reason
```

### Starting a Task - EXECUTE EXACTLY

1. **READ** task file `.claude/tasks/task-{id}.json`
2. **TRIGGER** Pre-Task Monitoring:
   ```bash
   python .claude/monitor/scripts/health_checker.py --check-before-task {id}
   python .claude/monitor/scripts/dashboard_updater.py --task-start {id}
   ```
3. **EXECUTE** Pre-Execution Validation Gate (see above)
   ```
   IF gate FAILS →
     TRIGGER monitoring: python .claude/monitor/scripts/diagnose.py --validation-failed {id}
     STOP and report specific failure
   IF gate PASSES → CONTINUE to step 4
   ```
4. **INITIALIZE progress tracking**:
   ```
   IF no progress field exists:
     ADD progress structure based on difficulty:
       1-3: simple progress
       4-6: step_counter with estimated steps
       7+: milestone or percentage based
   SET current_step = 1
   SET completion_percentage = 0
   ```
4. **UPDATE belief tracking IMMEDIATELY**:
   - SET confidence (0-100 based on understanding)
   - ADD discovered assumptions
   - SET momentum.phase = "ignition"
   - SET momentum.velocity = 15
5. **SET status** = "In Progress"
6. **DISPLAY** task details with current confidence
7. **EXECUTE the work** with progress updates

### During Task Execution - TRACK PROGRESS with Validation

**AFTER EACH SIGNIFICANT STEP:**
1. **INCREMENT** progress.current_step
2. **CALCULATE** completion_percentage = (current_step / total_steps) * 100
3. **ADD** to step_history (as before)
4. **UPDATE** Live Monitoring Dashboard:
   ```bash
   python .claude/monitor/scripts/dashboard_updater.py --progress {id} --step {current_step}
   ```

**PROGRESS CHECKPOINT GATE [Every 3 steps]:**
```
VALIDATION_GATE: progress_checkpoint
├── CHECK: Current approach still valid
├── CHECK: No unexpected blockers encountered
├── CHECK: Confidence hasn't dropped >30% from start
├── CHECK: Time spent < 2x original estimate
├── CHECK: Context usage < 70%
└── RESULT:
    ├── PASS → Continue execution
    ├── WARN (1-2 fails) → Adjust approach
    └── FAIL (3+ fails) → Checkpoint & re-evaluate
```

4. **CREATE checkpoint** IF:
   - Gate result is WARN or FAIL
   - Before risky operations
   - Context > 50% of budget
   ```bash
   # Create monitoring checkpoint when needed
   python .claude/monitor/scripts/health_checker.py --checkpoint {id}

   # If issues detected, run diagnosis
   IF gate_result in [WARN, FAIL]:
     python .claude/monitor/scripts/diagnose.py --checkpoint-issue {id}
     python .claude/monitor/scripts/self_heal.py --suggest-recovery {id}
   ```

### Finishing a Task - COMPLETE ALL STEPS with Final Validation

**COMPLETION VALIDATION GATE [MANDATORY before marking finished]:**
```
VALIDATION_GATE: task_completion
├── CHECK: All requirements from description addressed
├── CHECK: Quality standards met (no obvious issues)
├── CHECK: Documentation/comments updated
├── CHECK: No regressions introduced
├── CHECK: Tests pass (if applicable)
├── CHECK: Confidence >= initial level
└── RESULT:
    ├── PASS → Proceed to mark finished
    └── FAIL → Identify gaps & complete missing work
```

1. **EXECUTE** Completion Validation Gate
   ```
   IF gate FAILS:
     LIST specific failures
     COMPLETE missing work
     RE-RUN validation gate
   ```
2. **VERIFY** all work is complete
2. **VALIDATE each assumption**:
   ```
   FOR each assumption:
     TEST validity
     SET status = "validated" | "invalidated"
     ADD validation_method
     SET validated_date = today
   CALCULATE overall validation_status
   ```
3. **FINALIZE belief tracking**:
   - ADJUST confidence based on experience (+/- 10-20)
   - SET momentum.phase = "cruising" if smooth, "coasting" if difficult
   - SET momentum.velocity based on completion speed (0-100)
   - DOCUMENT decision_rationale with specifics
4. **COMPLETE progress tracking**:
   - SET completion_percentage = 100
   - ADD final step to step_history
   - CALCULATE metrics.actual_time_minutes
   - DOCUMENT any skipped steps
5. **DOCUMENT transparently**:
   - STATE what was actually implemented
   - LIST any deviations from plan
   - IDENTIFY follow-up tasks needed
   - REFERENCE created/modified files
6. **SET status** = "Finished"
7. **CHECK parent task**:
   ```
   IF parent_task exists:
     READ all sibling tasks
     IF all siblings.status == "Finished":
       SET parent.status = "Finished"
       CALCULATE parent.completion_percentage = 100
       TRANSFER average momentum to parent
   ```
8. **EXECUTE sync-tasks**:
   ```bash
   # Use script for fast sync (100x faster than manual)
   python scripts/task-manager.py sync
   # Or: python scripts/claude-cli.py task sync
   ```
9. **FINALIZE monitoring**:
   ```bash
   # Update monitoring with task completion
   python .claude/monitor/scripts/health_checker.py --check-after-task {id}
   python .claude/monitor/scripts/dashboard_updater.py --task-complete {id}
   python .claude/monitor/scripts/quick_status.py --task-metrics {id}

   # If parent task auto-completed, update monitoring
   IF parent.status == "Finished":
     python .claude/monitor/scripts/dashboard_updater.py --parent-complete {parent_id}
   ```

## Context-Aware Next Steps

After task completion, provide smart suggestions based on project state:

### Determine Project Context
Check these indicators to provide relevant suggestions:
1. **Template type** (from CLAUDE.md or .claude/context/overview.md)
2. **Remaining tasks** (from task-overview.md)
3. **Parent/sibling tasks** (from current task's parent_task field)
4. **Phase 0 status** (if .claude/tasks/_phase-0-status.md exists)

### Suggestion Logic

**If parent task just auto-completed:**
```
✅ Task [ID] Complete!

🎉 Parent Task [Parent-ID] Auto-Completed!
All subtasks finished. Parent "[Parent Title]" is now complete.

📋 NEXT STEP:
   → Review parent task notes in .claude/tasks/task-[parent-id].json
   → Or: Start next task with /complete-task [next-id]
```

**If sibling tasks remain:**
```
✅ Task [ID] Complete!

Progress: [X] of [Total] subtasks for "[Parent Title]" finished

📋 NEXT STEP (continue parent task):
   → Task [Next-Sibling-ID]: [Title] (difficulty: [N])
   → Run: /complete-task [next-sibling-id]
```

**If this completes Phase 0:**
```
✅ Task [ID] Complete!

🎉 Phase 0 Complete! All initialization tasks finished.

📋 NEXT STEP (begin implementation):
   → Review .claude/tasks/task-overview.md for implementation tasks
   → Start first implementation task: /complete-task [first-impl-id]
   → Estimated time: [X] hours for full implementation
```

**If pending high-difficulty tasks exist (≥7):**
```
✅ Task [ID] Complete!

⚠️  High-difficulty tasks detected ([Count] tasks with difficulty ≥7)

📋 NEXT STEP (break down complex tasks):
   → Task [High-Diff-ID]: [Title] (difficulty: [N])
   → MUST break down before starting: /breakdown [high-diff-id]
   → Or: Continue with easier tasks first
```

**If blocked tasks can now proceed:**
```
✅ Task [ID] Complete!

✓ Unblocked: Task [Blocked-ID] "[Title]" can now proceed
This task was waiting on the task you just completed.

📋 NEXT STEP (unblocked task ready):
   → Run: /complete-task [blocked-id]
   → Or: Review other pending tasks in task-overview.md
```

**If all tasks complete:**
```
✅ Task [ID] Complete!

🎉 PROJECT COMPLETE! All tasks finished.

📋 NEXT STEPS (wrap up):
   □ Review project deliverables
   □ Run validation (if applicable)
   □ Create git commit: All tasks complete
   □ Update README.md with outcomes
```

**If standard continuation (no special cases):**
```
✅ Task [ID] Complete!

Progress: [Finished]/[Total] tasks complete

📋 NEXT STEP:
   → Review: .claude/tasks/task-overview.md
   → Start next task: /complete-task [suggested-next-id]

   Suggested next: Task [ID] - [Title] (difficulty: [N], est. [X]h)
   [Brief reason why this task is suggested - e.g., "Related to completed task", "High priority", "Blocks other tasks"]
```

### Task Suggestion Priority
When multiple pending tasks exist, suggest based on:
1. **Unblocks other tasks** - Dependencies resolved by this task
2. **Same parent** - Sibling tasks to maintain context
3. **Related tags** - Similar to just-completed task
4. **High priority** - Priority field = "high"
5. **Lower difficulty** - Build momentum with easier tasks
6. **Sequential ID** - Natural project flow

## Output Location
- Updated task JSON file
- Updated task-overview.md (via sync-tasks)
- Parent task JSON if applicable

## Critical Rules
- Never mark "Broken Down" tasks as complete (they auto-complete when subtasks finish)
- Always check parent task status when completing subtasks
- Add notes about what was actually done
- **Transparency Requirements**:
  - If implementation deviated from original plan, document why
  - If bugs were fixed during completion, note what was broken
  - If workarounds were needed, explain what didn't work as expected
  - If new tasks were created, reference them in notes
  - Never silently fix issues - always document changes made

## Belief Tracking Integration

### Momentum Phase Transitions
When updating momentum phase during task work:

| Current Phase | Next Phase If... | Velocity Range |
|--------------|------------------|----------------|
| pending | Starting work | ignition (10-20) |
| ignition | Making progress | building (20-50) |
| building | Steady progress | cruising (50-80) |
| cruising | Slowing down | coasting (30-60) |
| coasting | Major slowdown | stalling (10-30) |
| stalling | No progress | stopped (0) |

### Confidence Adjustments
Adjust confidence based on discoveries during task execution:

- **Increase confidence** when:
  - Requirements clearer than expected (+10)
  - Solution simpler than anticipated (+15)
  - Good documentation found (+10)
  - Existing patterns apply (+10)

- **Decrease confidence** when:
  - Hidden complexity discovered (-15)
  - Dependencies not documented (-10)
  - Integration issues found (-20)
  - Performance problems emerge (-15)

### Assumption Validation Process
1. List all assumptions from task
2. For each assumption:
   - Test if still valid
   - Document how validated
   - Update status and date
3. Calculate overall validation_status:
   - All validated → "validated"
   - All invalidated → "invalidated"
   - Mix → "partial"
   - None tested → "pending"

### Decision Rationale Examples

**Good rationale:**
"Chose PostgreSQL over MongoDB because:
1. Strong consistency requirements for financial data
2. Complex relational queries needed
3. Team expertise in SQL
Trade-off: Less flexible schema evolution"

**Poor rationale:**
"Used PostgreSQL because it's better"
