# Spec Merge Queue (DEC-023)

The **re-entry transport** for the spec-shaping workflow. When `/grill`, `/shakedown`, or `/feedback` surface a finding in one conversation that belongs in a vision or the spec, the finding is appended here so it is **surfaced on return** instead of being re-stated from memory. This is the mechanism that fixes the "I take an excursion, then can't get the output back into the flow" friction (DEC-023 § Background).

This is a sibling register to `.claude/support/friction.jsonl` (see `friction-register.md`) — same JSONL-append discipline, different purpose: friction tracks *template/coherence* signals; the merge queue tracks *findings to fold into a vision or the spec*.

## Location

`.claude/support/.spec-merge-queue.jsonl` — one JSON object per line, append-only. **Project-generated state** (like `friction.jsonl` and `.claude/tasks/*.json`), not template-shipped content: this reference doc ships; the `.jsonl` is created on first append and is gitignored project-side. A missing file means an empty queue.

## What it is NOT — relationship to the vision's in-doc fork-tracker

A feature vision already carries an **Open-forks tracker** (the scaffold's canonical fork table) that accumulates findings *in the vision document*. The merge queue does **not** replace it — they compose:

| | Vision Open-forks tracker | Merge queue |
|---|---|---|
| Lives in | the vision doc (durable, in-context) | `.spec-merge-queue.jsonl` (transport) |
| Role | the **accumulation surface** — the canonical record of a feature's open questions + resolutions | the **transport / notification** — ensures a finding from a *separate conversation* isn't stranded before it reaches the vision or spec |
| When used | folding findings into a vision you're actively developing **in-session** | findings produced when the destination doc is **not open in this session**, and all **spec-target** refinements (no vision to hold them) |

**Rule of thumb:** if you're developing a vision *in this conversation*, fold findings straight into its fork-tracker (no queue entry needed). If the excursion is a separate conversation, or targets a spec section directly, emit a queue entry so `/iterate` (or your next vision session) surfaces it.

## Schema

One object per line:

| Field | Type | Notes |
|---|---|---|
| `id` | string | `MQ-NNN`, zero-padded, monotonic. Collision-safe: `max(existing MQ ids) + 1` (see Write protocol). |
| `source` | enum | `grill` \| `shakedown` \| `feedback` — which command produced it. |
| `target` | enum | `vision` \| `spec` — the altitude the finding belongs to (DEC-023 "the target sets the altitude"). |
| `target_ref` | string | where it lands: a vision path + fork id (`vision/<slug>.md#F3`) or a spec section (`spec_v{N} § 12.4`). |
| `origin_ref` | string | where it came from: a shakedown corpus + entry (`shakedowns/<slug>-YYYY-MM-DD.md#R-07`), a `CONTEXT.md` term, or an `FB-NNN`. |
| `kind` | enum | `gap` (a ⚠ capability gap) \| `term` (a sharpened glossary term) \| `decision` (a fork needing `/research`) \| `delta` (a drafted spec/vision change ready to apply). |
| `summary` | string | one line — what the finding is, human-readable for the re-entry prompt. |
| `drafted_delta` | string \| null | for `kind: delta` — the proposed text (a *proposal*; never written to spec/vision directly — DEC-016). |
| `needs_impact_assessment` | bool | `true` when a mature-project feature delta must route through `/feedback`'s impact assessment before `/iterate` (DEC-023 G2). `false` for initial-spec / small refinements. |
| `status` | enum | `open` → `merged` \| `dismissed`. |
| `created` | string | ISO date (pass the date in; do not call `Date.now()` in scripts). |

Example:
```json
{"id":"MQ-003","source":"shakedown","target":"vision","target_ref":"vision/outfit-scoring.md#F2","origin_ref":"shakedowns/outfit-scoring-2026-06-22.md#R-09","kind":"gap","summary":"Engine can't express a rule relating two items (binary relation); mechanism is a per-item predicate.","drafted_delta":null,"needs_impact_assessment":false,"status":"open","created":"2026-06-22"}
```

## Write protocol (producers)

`/grill`, `/shakedown`, `/feedback` are **main-thread, user-driven commands** — they may write `.claude/` (unlike subagents, which cannot per DEC-004). The producing command:

1. Computes `id = MQ-` + zero-padded `(max existing MQ-NNN in the file) + 1` (empty/missing file → `MQ-001`). A future helper `persist-merge-item.py` may mechanize this collision-safe step (mirrors `persist-friction.py`, FB-098); until then it is a prose step the orchestrator performs.
2. Appends one line per finding with `status: open`.
3. Skips the queue entirely when folding directly into an in-session vision fork-tracker (see the composition table above).

Append-only: never rewrite prior lines except the status update below.

## Drain protocol (consumers)

`/iterate` (and `/iterate distill`) **drain the queue on entry**: read all `status: open` items, group by `target_ref`, and surface them as the re-entry prompt — e.g.:

> *Excursion findings since last spec update:*
> *— 2 ⚠ gaps + 1 drafted delta from `shakedown outfit-scoring-2026-06-22` (target: vision/outfit-scoring.md)*
> *Fold in? [Y] all · [R] review each · [S] skip*

On resolution:
- **Folded in** → set `status: merged` (the change lands via `/iterate`'s normal propose-approve-apply for spec, or an in-place vision edit for `target: vision` per the DEC-016 vision carve-out).
- **Declined** → set `status: dismissed`.
- A `needs_impact_assessment: true` item is **not** applied by `/iterate` directly — it is routed to `/feedback` for impact assessment first (DEC-023 G2), then returns as an ordinary item once assessed.

A vision session (developing a vision doc) may likewise drain `target: vision` items for that doc and fold them into its fork-tracker.

## Status lifecycle

```
open ──fold──▶ merged
   └─decline─▶ dismissed
```

`merged`/`dismissed` rows are retained (audit trail), not deleted. Periodic compaction (drop resolved rows older than N) is optional and project-side, mirroring friction-register hygiene.

## See also

- `.claude/support/reference/friction-register.md` — sibling JSONL register (template/coherence signals).
- `.claude/rules/spec-workflow.md § "Vision Documents"` — the vision lifecycle + target-awareness this transport serves.
- `.claude/vision/_feature-vision-template.md` — the in-doc Open-forks tracker the queue composes with.
- `decisions/decision-023-vision-hub-and-spec-shaping-workflow.md` — the decision establishing this transport (F1, G2, G4).
