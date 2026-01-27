# Decision Documentation Guide

Philosophy and practices for documenting project decisions.

---

## Why Document Decisions?

### The Problem

Without decision records:
- Future developers ask "why is it built this way?"
- Same debates recur with each new team member
- Context is lost when people leave or forget
- Reversing decisions happens without understanding costs

### The Solution

Decision records capture:
- **What** was decided
- **Why** it was chosen (over alternatives)
- **What** we traded away
- **When** circumstances might warrant revisiting

---

## When to Create a Decision Record

### Create a Record For

- Technology choices (libraries, frameworks, services)
- Architectural patterns (how components connect)
- Scope decisions (what's in/out of MVP)
- Process changes (how work gets done)
- Anything that took significant discussion to resolve

### Skip Records For

- Obvious choices with no real alternatives
- Trivial implementation details
- Decisions already documented elsewhere (e.g., in specs)
- Temporary workarounds (use code comments instead)

### Rule of Thumb

> If someone might reasonably ask "why did we do it this way?" in 3 months, create a record.

---

## Decision Lifecycle

```
draft → proposed → approved → implemented
                      ↓
                 superseded
```

### draft
Research phase. Gathering options, running experiments. Not ready for review.

### proposed
Options documented, recommendation made. Ready for stakeholder input.

### approved
Decision finalized. May await implementation.

### implemented
Decision reflected in codebase. This is the common end state.

### superseded
Replaced by a newer decision. Link to replacement in Impact section.

---

## Comparison Tables

The options comparison table is the core of a decision record. It forces structured evaluation.

### Good Criteria

- **Performance**: Speed, resource usage
- **Complexity**: Learning curve, maintenance burden
- **Cost**: Licensing, infrastructure, time
- **Ecosystem**: Community, documentation, longevity
- **Fit**: How well it matches our constraints
- **Risk**: Unknowns, potential failure modes

### Table Format

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Performance | Fast | Moderate | Slow |
| Complexity | High | Low | Medium |
| Cost | Free | $500/mo | Free |
| **Overall** | Good for perf | Good for simplicity | Not recommended |

Use qualitative ratings (Good/Moderate/Poor) or quantitative when available.

---

## Research Archives

Sometimes decisions require significant research: benchmarks, proof-of-concepts, vendor evaluations.

Store research in `.claude/support/decisions/.archive/`:
- `YYYY-MM-DD_topic.md` - Research notes, findings
- Link from the decision record's Research Notes

This keeps decision records focused while preserving detailed findings.

---

## Decision Tracking

The **project dashboard** (`.claude/dashboard.md`) serves as the decision index. All decisions appear in the dashboard's "All Decisions" section, which is regenerated automatically after task and decision changes.

Pending decisions that need human input are surfaced in the dashboard's "Needs Your Attention" section.

---

## Integration with Workflow

### During Spec Creation

The specification phase (via `/iterate`) is where key decisions are made:
- Technology selections
- Architectural approaches
- Scope boundaries

These should be documented in the spec and as decision records when significant.

Reference: `.claude/commands/iterate.md`

### During Execution

The implement-agent references decisions when:
- Implementing the chosen approach
- Encountering edge cases the decision anticipated

### During Health Checks

`/health-check` validates:
- Frontmatter completeness
- Staleness (drafts/proposals too old)

---

## Anti-Patterns

### Decision Theater
Creating elaborate records for trivial choices. Keep small decisions in code comments or task notes.

### Analysis Paralysis
Researching endlessly without deciding. Set time limits for draft status.

### Orphan Records
Decisions referenced nowhere, never implemented. Either implement or mark superseded.

### Missing Trade-offs
Every choice has costs. "No downsides" means incomplete analysis.

### Invisible Rationale
"We chose X" without explaining why. The rationale is the most valuable part.

---

## Revisiting Decisions

Decisions aren't permanent. Revisit when:

- Circumstances change (new requirements, technology shifts)
- Trade-offs prove worse than expected
- Better options become available

When superseding a decision:
1. Create a new decision record
2. Reference the old decision in Related
3. Mark old decision as `superseded`
4. Note the replacement in old decision's Impact

---

## Templates and References

- **Template**: `.claude/support/reference/decision-template.md`
- **Archive**: `.claude/support/decisions/.archive/`
