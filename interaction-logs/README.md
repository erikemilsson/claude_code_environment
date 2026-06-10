# Interaction Logs

Cross-project feedback pipeline for template improvement. Session exports from projects using this template land here for processing.

## Directory Structure

```
interaction-logs/
  inbox/          # Raw session exports from projects (unprocessed)
  processed/      # Exports that have been analyzed and categorized
  insights/       # Derived insights grouped by template area
```

## How Exports Arrive

Projects using this template drop exports into `inbox/`. Two shapes share the directory; `/health-check` Part 7 dispatches by file content.

**Session exports** (from `/work pause` or PreCompact hook — implicit signal):

- **Track 1 (automated markers):** Friction events emitted by agents during execution — verification failures, workflow deviations, spec drift, informal decisions, scope creep, template gaps
- **Track 2 (Claude assessment):** Nuanced observations from Claude's conversation context — design pushback opportunities, workflow friction patterns, unstructured observations. Only available on graceful exits (`/work pause`).
- Shape: `{"export_version": 1, "source_project": "...", "automated_markers": [...], "claude_assessment": {...} | null, "export_quality": "full" | "markers_only"}`

**User-feedback bridges** (from `/feedback template: ...` — explicit user-tagged signal):

- Single FB entry the user marked template-relevant in a downstream project. The downstream `/feedback` writes locally and ALSO writes one of these to the template inbox.
- Shape: `{"export_version": 1, "kind": "user_feedback", "source_project": "...", "feedback": {"title": "...", "body": "...", "source_fb_id": "FB-NNN"}}`
- `/health-check` Part 7 routes these straight into `template-maintenance/feedback.md` (with user confirmation) — no aggregation, since they're already user-curated.

Exports arrive via local filesystem: configure `template_inbox_path` in the downstream project's `.claude/version.json` to point to this repo's `interaction-logs/inbox/` directory.

## Processing Pipeline

Processing is triggered automatically via `/health-check` (when run in the template repo) or can be run manually. The pipeline:

1. **Ingest** — read exports from `inbox/`, validate format
2. **Categorize** — group friction events by template area (verify-agent, implement-agent, /work, /iterate, design-guidance, user-experience)
3. **Aggregate** — detect patterns across projects and sessions
4. **Generate insights** — write insight documents to `insights/`
5. **Route to `/feedback`** — high-confidence insights become feedback items for the normal review pipeline

## Processing Cadence

Run `/health-check` in this repo (Part 7 fires the pipeline) **whenever the inbox reaches ~15 exports, or monthly, whichever comes first**. Rationale: the first aggregation (2026-06-11) ran over a 64-export backlog accumulated since 2026-03-30 — patterns were detectable but much of the evidence had already been independently rediscovered and shipped against in the meantime (FB-058/075/076/086, Family C), which is the cost of letting the backlog grow. ~15 exports is enough for cross-session patterns (the 3-occurrence bar) while keeping insights ahead of the ship loop, and one monthly floor keeps the inbox from silently stalling when export volume dips.

Aggregation (pipeline stage 3) spans `processed/` too, not just the new batch — recurrence counts should reflect the whole corpus, with a version-skew caveat for evidence predating the template fix that covers it.

## Export Format

See `decisions/.archive/2026-03-30_cross-project-interaction-logs.md` for the full export schema and pipeline design (DEC-001).
