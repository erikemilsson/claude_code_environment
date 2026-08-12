# Template-Maintenance Evidence

Audit-trail artifacts that informed template improvements. Files here are raw evidence (dashboard renders, session snapshots, screenshots) referenced from `feedback.md` or `feedback-archive.md` entries.

## Convention

- **Filename:** `{artifact-type}_{source-project}-{YYYY-MM-DD}.{ext}`
  - Examples: `dashboard_export_styler-2026-04-22.pdf`, `task-list_siren-2026-03-15.png`
- **Lifetime:** keep as long as the originating feedback entry is in `feedback.md` or referenced from `feedback-archive.md`. When neither references the file, archive externally or delete.
- **Not shipped:** this directory is template-maintenance only (template repo only — does not ship to projects).

## Index

| File | Referenced by | Captured |
|------|---------------|----------|
| `dashboard_export_styler-2026-04-22.pdf` | FB-038 (promoted 2026-05-13) — Action Required regression observation that motivated the v3.2.4 summary-shape detection check | 2026-04-22 |
| `dashboard_example_siren-2026-04-10.pdf` | No FB entry — kept as the pre-DEC-024 Markdown-dashboard design reference. Relocated here from the repo root 2026-08-12 (it was an undocumented stray; commit `40f80a5` had deliberately tracked it, so relocated rather than deleted). See lifetime note below. | 2026-04-10 |
| `dashboard_export_siren-2026-03-27.pdf` | No FB entry — same provenance as the row above; the two were the SIREN dashboard renders that informed DEC-002's readability heuristics (DEC-002 cites SIREN in prose, not these files by path). | 2026-03-27 |

**Lifetime note on the two `siren` rows (2026-08-12).** Both predate DEC-024, which retired the Markdown dashboard entirely; the live design reference is now `decisions/.archive/dashboard-html-exploration/`. Under this file's own lifetime rule they are already delete-eligible (no `feedback.md` / `feedback-archive.md` entry references them). They are retained only because an earlier root-cleanup pass chose to track them and nothing since has overturned that judgment. Drop them without ceremony the next time this directory is reviewed — git history holds them either way.
