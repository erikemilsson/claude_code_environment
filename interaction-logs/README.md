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

Projects using this template export session data at session boundaries (`/work pause` or PreCompact hook). The export contains:

- **Track 1 (automated markers):** Friction events emitted by agents during execution — verification failures, workflow deviations, spec drift, informal decisions, scope creep, template gaps
- **Track 2 (Claude assessment):** Nuanced observations from Claude's conversation context — design pushback opportunities, workflow friction patterns, unstructured observations. Only available on graceful exits (`/work pause`).

Exports arrive via local filesystem: configure `template_inbox_path` in the project's `.claude/version.json` to point to this repo's `interaction-logs/inbox/` directory.

## Processing Pipeline

Processing is triggered automatically via `/health-check` (when run in the template repo) or can be run manually. The pipeline:

1. **Ingest** — read exports from `inbox/`, validate format
2. **Categorize** — group friction events by template area (verify-agent, implement-agent, /work, /iterate, design-guidance, user-experience)
3. **Aggregate** — detect patterns across projects and sessions
4. **Generate insights** — write insight documents to `insights/`
5. **Route to `/feedback`** — high-confidence insights become feedback items for the normal review pipeline

## Export Format

See `decisions/.archive/2026-03-30_cross-project-interaction-logs.md` for the full export schema and pipeline design (DEC-001).
