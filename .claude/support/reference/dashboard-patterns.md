# Dashboard Patterns

Patterns for extending the dashboard with domain-specific tracking.

## Domain-Specific Sub-Dashboards

*Added: 2026-01-27*

**Context:** When a project has a complex domain area that needs dedicated tracking beyond the main task list - such as workshop management, inventory tracking, customer pipelines, or experiment logs.

**Pattern:** Create a separate markdown file in `.claude/support/` for domain-specific tracking, then link to it from the main dashboard's Notes section.

**Structure:**
```markdown
# [Domain] Dashboard

*Last updated: [date]*

## [Key Metric 1]
| Column | Column | Column |
|--------|--------|--------|
| data   | data   | data   |

## [Key Metric 2]
...

## Quick Actions
- [ ] Action item 1
- [ ] Action item 2
```

**Example - Workshop Management:**
```markdown
# Workshop Management Dashboard

## Upcoming Sessions
| Date | Topic | Registered | Capacity | Status |
|------|-------|------------|----------|--------|
| 2026-02-15 | Intro to ML | 23 | 30 | Open |
| 2026-02-22 | Advanced NLP | 30 | 30 | Full |

## Materials Status
| Workshop | Slides | Exercises | Solutions |
|----------|--------|-----------|-----------|
| Intro to ML | ✅ | ✅ | 🔄 |
| Advanced NLP | ✅ | ⏳ | ⏳ |

## Quick Actions
- [ ] Finalize ML solutions
- [ ] Create NLP exercises
```

**Why:** The main dashboard tracks tasks and project progress. Domain-specific dashboards track operational metrics unique to your project's subject matter. Separating them:
- Keeps the main dashboard focused on development progress
- Allows domain tracking to evolve independently
- Provides a single place to check domain-specific status

**When to use:**
- Project has operational concerns beyond code (events, inventory, experiments)
- You find yourself asking "what's the status of X" where X isn't a development task
- Multiple people need to track domain-specific metrics

**Linking from main dashboard:**
Add to the Notes & Ideas section:
```markdown
## 💡 Notes & Ideas

**Quick Links:**
- [Workshop Dashboard](support/workshop-dashboard.md)
- [Experiment Log](support/experiment-log.md)

[Your notes here...]
```

---

## Progress Visualization by Milestone

*Added: 2026-01-27*

**Context:** When you need to communicate project progress to stakeholders in terms they understand (features, phases) rather than raw task counts.

**Pattern:** The Milestones section shows per-phase progress. Populate milestones with meaningful phase names from your spec rather than generic labels.

**Example:**
```markdown
## 🎯 Milestones

| Status | Milestone | Target | Progress | Tasks |
|--------|-----------|--------|----------|-------|
| ✅ | Foundation | Week 1 | 100% | 8/8 |
| 🔄 | Core API | Week 3 | 50% | 6/12 |
| ⏳ | UI Components | Week 5 | 27% | 4/15 |
| ⏳ | Testing | Week 6 | 0% | 0/5 |
```

**Why:** Stakeholders care about "is the API done?" not "are 18 of 40 tasks done?" The Milestones section bridges that gap, while Quick Status provides the overall completion percentage.

---

## Critical Path Clarity

*Added: 2026-01-27*

**Context:** When multiple people (or Claude and human) are working on a project and need to know what's blocking progress.

**Pattern:** The Critical Path section shows the sequence of dependent tasks that must complete for the project to finish. Each step indicates who owns it, making handoff points clear.

**Reading the critical path:**
- ❗ **You**: Human action required - Claude is waiting
- 🤖 **Claude**: Claude can proceed - human doesn't need to act
- 👥 **Both**: Collaborative task - coordinate timing

**Example:**
```markdown
## 🛤️ Critical Path

**Next steps to completion:**

1. ❗ **You**: Review API design doc - *blocks step 2*
2. 🤖 **Claude**: Implement API endpoints - *blocks step 3*
3. 👥 **Both**: Integration testing
4. ❗ **You**: Production deployment approval

*4 steps remaining on critical path*
```

**Why:** Without this view, it's easy to lose track of what's actually blocking progress vs. what's parallel work that can wait.
