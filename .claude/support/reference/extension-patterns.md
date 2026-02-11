# Extension Patterns

Patterns for structuring complex projects. Phases are implicit from spec structure; decisions are always available.

---

## Overview

The core workflow (Spec → Execute → Verify) handles most projects well. These patterns add structure for projects with additional complexity:

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Phases** | Sequential project stages where Phase N+1 can't begin until Phase N completes | Multi-phase projects with natural boundaries |
| **Decisions** | Tracked choices with comparison matrix, option analysis, and optional weighted scoring | Technical or methodological choices that block downstream work |

Both patterns are lightweight. Phases emerge from spec structure; decisions use the existing decision record format.

---

## Phases

Phases structure a project into sequential stages. Work in Phase N+1 cannot begin until all Phase N tasks are complete.

### Purpose

- Enforce natural project boundaries (prototype → production, data pipeline → visualization)
- Prevent premature work on later stages
- Provide clear progress tracking per stage

### How Phases Work

Phases are implicit — they come from the spec structure, not from special configuration.

1. **Spec defines phases:** Sections in the spec naturally group into phases (e.g., "## Phase 1: Data Pipeline", "## Phase 2: Visualization")
2. **Tasks get a `phase` field:** During decomposition, `/work` assigns each task a phase based on its spec section
3. **Phase ordering is enforced:** Tasks in Phase N+1 remain blocked until all Phase N tasks are "Finished"
4. **Dashboard groups by phase:** Tasks section shows tasks under phase headers with per-phase progress; Progress section shows phase breakdown table

### Task Schema

Tasks include a `phase` field:

```json
{
  "id": "11",
  "title": "Chart: enrollment timeline",
  "phase": "2",
  "dependencies": [],
  "decision_dependencies": ["DEC-002"]
}
```

Phase dependencies are checked alongside task dependencies. A task is eligible when:
- All its explicit `dependencies` are "Finished"
- All tasks in earlier phases are "Finished"
- All its `decision_dependencies` are resolved

### Phase Transitions

When all Phase N tasks complete:
- `/work` detects the transition and logs it
- If Phase N+1 needs more detail in the spec, `/work` suggests running `/iterate` to flesh it out
- Dashboard updates to show the new active phase

### No Special Configuration

Unlike the previous stage gates pattern, phases require no frontmatter config, no criteria files, and no folder blocking. Phase membership comes from task metadata, and ordering is enforced through the existing dependency system.

---

## Decisions

Decisions are tracked choices that block downstream work until resolved. They use the existing decision record format with a few additions.

### Purpose

- Document choices with multiple viable options
- Block dependent tasks until a selection is made
- Distinguish between pick-and-go decisions and inflection points

### Decision Records

Decision records live in `.claude/support/decisions/decision-*.md`. They contain:

- **Comparison matrix** — criteria vs options table
- **Option details** — strengths, weaknesses, research notes per option
- **Optional weighted scoring** — for high-stakes decisions
- **Checkbox selection** — user marks their choice directly in the doc

See [decisions.md](decisions.md) for the full format.

### Pick-and-Go vs Inflection Point

| Type | What Happens After Resolution |
|------|-------------------------------|
| **Pick-and-go** | Blocked tasks unblock; `/work` continues normally |
| **Inflection point** | `/work` pauses and suggests running `/iterate` to revisit the spec, because the outcome changes what gets built |

Inflection points are flagged with `inflection_point: true` in the decision frontmatter. Examples:
- "Supervised vs unsupervised analysis" — changes what data you collect, what pipeline you build
- "REST vs GraphQL" might be pick-and-go (same features, different implementation)

### Task Dependencies on Decisions

Tasks can depend on decisions via the `decision_dependencies` field:

```json
{
  "id": "11",
  "title": "Chart: enrollment timeline",
  "decision_dependencies": ["DEC-002"],
  "notes": "Blocked until visualization library is chosen"
}
```

When `/work` detects a task blocked by an unresolved decision:
1. Surfaces the decision: "Decision DEC-002 blocks N tasks. Open the decision doc to make your selection, then run `/work` again."
2. Provides a link to the decision doc
3. Continues with unblocked tasks

### Post-Decision Behavior in `/work`

When `/work` detects a previously-pending decision is now resolved:

1. **Read the decision record** — check `inflection_point` field
2. **If pick-and-go** (`inflection_point: false` or absent):
   - Unblock dependent tasks
   - Continue executing
3. **If inflection point** (`inflection_point: true`):
   - Pause execution
   - Inform user: "Decision DEC-002 was an inflection point. The spec may need updating. Run `/iterate` to review affected sections, then `/work` to continue."
   - Do not proceed until `/iterate` has run

### Dashboard Integration

Decisions appear in the dashboard:

- **Decisions section:** `ID | Decision | Status | Selected` — decided entries show selected option name, pending entries link to doc
- **Action Required → Decisions:** Pending decisions that block tasks appear here with links
- **Blocked tasks:** Show decision IDs in their dependency column (in Tasks section)

---

## Domain-Specific Sub-Dashboards

For projects with complex domain areas (workshop management, inventory, experiment logs), create separate markdown files in `.claude/support/` for domain-specific tracking.

**Enabling:** Check `Sub-Dashboards` in the **Sections** checklist at the top of `dashboard.md`. When enabled, a `## 📑 Sub-Dashboards` section appears in the dashboard as a link collection pointing to your domain-specific tracking files.

**When to use:**
- The main dashboard's Tasks/Progress sections don't capture domain-specific tracking needs
- You need separate tables, checklists, or formats for a specific domain area
- Examples: materials procurement tracker, experiment log, vendor contact sheet

**Convention:**
- Place sub-dashboard files in `.claude/support/` (e.g., `support/materials-tracking.md`)
- Each file is self-contained — it doesn't need to follow dashboard format
- The main dashboard links to them; it doesn't embed their content

---

## Optional Visualizations

For complex projects, create Mermaid diagram files in `.claude/support/visualizations/` and link from the dashboard.

**Enabling:** Check `Visualizations` in the **Sections** checklist at the top of `dashboard.md`. When enabled, a `## 📈 Visualizations` section appears in the dashboard as a link collection pointing to your diagram files.

**When to use:**
- Only when dashboard tables aren't sufficient to convey relationships or flow
- Stale diagrams are worse than none — only create what you'll maintain
- Useful for: workflow phases, decision dependency graphs, system architecture, progress timelines

**Convention:**
- Place diagram files in `.claude/support/visualizations/` (e.g., `support/visualizations/phase-flow.mmd`)
- Use Mermaid (`.mmd`) format for portability
- Keep diagrams focused — one concept per file

---

## Related Files

- [decisions.md](decisions.md) — Decision record format and selection mechanism
- [dashboard.md](../../dashboard.md) — Dashboard template with section toggle checklist and populated example
- [shared-definitions.md](shared-definitions.md) — Vocabulary (Phase, Decision, Inflection Point, Human Task)
- [workflow.md](workflow.md) — Core workflow documentation
