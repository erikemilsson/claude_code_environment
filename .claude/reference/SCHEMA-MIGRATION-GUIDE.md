# Task Schema Migration Guide

*Created: 2025-12-17*

## Purpose

This document explains the consolidation of three task schema documents into one authoritative reference and how to handle schema evolution going forward.

## Schema Consolidation Summary

### Previous State (3 Documents)

1. **task-schema.md** (Original)
   - Flat belief tracking structure
   - confidence, assumptions, validation_status, momentum, decision_rationale at root level
   - Currently used by all existing task files

2. **task-schema-v2.md** (Progress Extension)
   - Added nested "progress" object
   - Step counter, milestone, percentage tracking
   - Checkpoint management
   - NOT widely adopted yet

3. **enhanced-task-schema.md** (Alternative Format)
   - Nested "belief_tracking" object
   - Same fields as task-schema.md but structured differently
   - NOT used by existing task files

### New State (1 Document)

**task-schema-consolidated.md** - Single authoritative reference combining:
- Flat belief tracking structure (from task-schema.md) - CURRENT STANDARD
- Optional progress tracking (from task-schema-v2.md) - Available for complex tasks
- Dropped nested belief_tracking format (from enhanced-task-schema.md) - Not adopted

## What Changed

### Kept (No Migration Needed)
- Flat belief tracking structure at root level
- All core task fields (id, title, description, etc.)
- Assumption object structure
- Momentum phase system
- All existing task files work without changes

### Added (Opt-in)
- Optional "progress" field for complex tasks
- Progress types: simple, step_counter, milestone, percentage
- Checkpoint management for long-running tasks
- Step history tracking
- Blocking step documentation

### Removed (Never Adopted)
- Nested "belief_tracking" object format
- No migration needed since no tasks used this format

## Migration Actions

### For Template Creators
**Action**: Update references to schema documents
- **OLD**: Link to task-schema.md, task-schema-v2.md, or enhanced-task-schema.md
- **NEW**: Link to task-schema-consolidated.md

**Files to Update**:
- CLAUDE.md: Update schema references
- README.md: Update documentation links
- Template README files: Update schema documentation
- Command files: Update schema references in comments

### For Existing Task Files
**Action**: None required
- All existing task files use the correct flat structure
- No migration script needed
- Files work as-is

### For New Task Files
**Action**: Use consolidated schema
- Follow task-schema-consolidated.md
- Use flat belief tracking (not nested)
- Add "progress" field only if task complexity warrants it (difficulty ≥ 7 or multi-step work)

### For Documentation
**Action**: Deprecate old schema docs

Old files moved to:
- .claude/reference/deprecated/task-schema.md
- .claude/reference/deprecated/task-schema-v2.md
- .claude/reference/deprecated/enhanced-task-schema.md

Add deprecation notice to each:
```markdown
# DEPRECATED

This document has been superseded by task-schema-consolidated.md

See: .claude/reference/task-schema-consolidated.md
```

## When to Use Progress Tracking

### Use Progress Tracking When:
- Task difficulty ≥ 7
- More than 10 discrete steps
- Long-running task (>1 hour estimated)
- Multiple team members involved
- Need to resume from checkpoints
- Stakeholders need visibility into progress

### Skip Progress Tracking When:
- Simple tasks (difficulty 1-4)
- Quick tasks (<30 minutes)
- Single-step implementation
- Standard patterns apply

## Backward Compatibility

### Reading Old Tasks
Tasks without progress field: Treated as simple progress at 0%
```json
{
  "id": "old_task",
  "confidence": 80
  // No progress field - works fine
}
```

### Enhancing Old Tasks
Add progress to existing task:
```json
{
  "id": "old_task",
  "confidence": 80,
  // Add this if needed
  "progress": {
    "type": "simple",
    "completion_percentage": 25
  }
}
```

### Schema Validation
Scripts that validate task JSON should:
1. Require all core fields
2. Require belief tracking fields (flat structure)
3. Allow optional progress field
4. Reject nested belief_tracking format

## Command Updates Needed

### complete-task.md
- Update to optionally manage progress field
- Default to simple progress if not present
- Update step_history when progress exists

### breakdown.md
- Initialize progress field in subtasks if parent difficulty ≥ 7
- Set appropriate progress type based on complexity

### sync-tasks.md
- Display progress metrics when present
- Show completion_percentage in overview table
- Calculate parent progress from subtask completion

### update-tasks.md
- Validate against consolidated schema
- Check progress consistency if present
- Flag deprecated nested belief_tracking format

## Testing the Migration

### Validation Checklist
- [ ] All existing task files still parse correctly
- [ ] Scripts handle tasks with and without progress field
- [ ] Commands reference task-schema-consolidated.md
- [ ] CLAUDE.md points to consolidated schema
- [ ] README.md links to consolidated schema
- [ ] Old schema docs marked deprecated
- [ ] Components/templates use consolidated schema

### Test Cases
1. Read existing task without progress field - should work
2. Create new task with progress field - should work
3. Update task to add progress - should work
4. Validate task with nested belief_tracking - should fail/warn
5. Sync-tasks with mixed progress formats - should handle both

## Timeline

**Immediate (Today)**
- ✅ Create task-schema-consolidated.md
- ✅ Create this migration guide
- ⏸ Mark old schema docs as deprecated
- ⏸ Update CLAUDE.md references

**Short Term (This Week)**
- Update command files to reference new schema
- Update README and template documentation
- Test scripts with mixed task formats
- Create examples in components/task-management/examples/

**Medium Term (This Month)**
- Move deprecated docs to deprecated/ folder
- Update all templates to reference consolidated schema
- Document progress tracking usage in templates
- Create progress tracking examples

**Long Term (Ongoing)**
- Monitor for issues with schema compatibility
- Gather feedback on progress tracking usefulness
- Consider future schema enhancements
- Maintain single source of truth

## Future Schema Changes

### Process for Schema Evolution
1. Propose change in new reference document
2. Discuss impact on existing tasks
3. Create migration plan if breaking change
4. Update consolidated schema
5. Update validation scripts
6. Test with existing task files
7. Document in this guide
8. Roll out to commands and templates

### Versioning Strategy
- Use dates for schema versions: task-schema-consolidated-YYYY-MM-DD.md
- Current version is always task-schema-consolidated.md
- Keep dated snapshots in reference/schema-history/
- Document changes in CHANGELOG section of schema doc

## Questions and Answers

### Why consolidate instead of version?
Three documents created confusion about which to use. Single source of truth is clearer.

### Why keep flat belief tracking instead of nested?
All existing tasks use flat structure. Nesting adds no value, only migration cost.

### Why make progress tracking optional?
Most simple tasks don't need detailed progress. Only complex tasks benefit from tracking.

### What if I need progress tracking for a simple task?
Add it! The "optional" guideline is a recommendation, not a hard rule.

### Can I still use task-schema.md references?
They'll work but should be updated to task-schema-consolidated.md for clarity.

### Will old schema docs be deleted?
No, moved to deprecated/ folder with deprecation notices for reference.

### How do I validate my task files?
Use scripts/schema-validator.py which checks against consolidated schema.

## Related Documents

- task-schema-consolidated.md - Authoritative schema reference
- components/task-management/README.md - Task management system overview
- .claude/commands/complete-task.md - Task execution workflow
- .claude/commands/breakdown.md - Task breakdown process
- .claude/reference/validation-gates.md - Validation rules
