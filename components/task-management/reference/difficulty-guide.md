# Task Difficulty Guide

## Scoring Criteria (LLM Error Probability)

### Low Risk (1-6)
- 1: Single word/character change
- 2: Simple UI text update
- 3: Basic CRUD following pattern
- 4: Standard form with validation
- 5: API integration with docs
- 6: Component with state logic

### High Risk (7-10) - REQUIRES BREAKDOWN
- 7: Multi-provider auth setup
- 8: Database migration with backfill
- 9: Architectural refactoring
- 10: Distributed system implementation

## Breakdown Strategy

When difficulty ≥7:
1. Identify independent components
2. Create logical sequence
3. Each subtask should be ≤6
4. Add clear dependencies
5. Test each subtask independently

## Why Breakdown Matters

**Without Breakdown:**
- Task: "Implement OAuth2 authentication" (difficulty: 8)
- Status: "In Progress" (ambiguous - what part is being worked on?)
- Risk: High error probability, unclear progress

**With Breakdown**
- Parent: "Implement OAuth2 authentication" (difficulty: 8, status: "Broken Down (2/4 done)")
- Subtask 1: "Create OAuth config structure" (difficulty: 3) ✅ Finished
- Subtask 2: "Implement Google provider" (difficulty: 5) ✅ Finished
- Subtask 3: "Implement GitHub provider" (difficulty: 5) 🔄 In Progress
- Subtask 4: "Add session management" (difficulty: 4) ⏳ Pending

Result: Clear progress (50% complete), lower error risk per subtask, parent auto-completes when done.
