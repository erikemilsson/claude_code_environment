# Template Maintenance

Working documents for maintaining the template itself. **None of this ships to downstream projects** — it's deleted alongside `README.md`, `CLAUDE.md`, `system-overview.md`, `tests/`, `decisions/`, and `scripts/` when someone clones the template to start a real project.

## Contents

| File | Purpose |
|------|---------|
| `feedback.md` | Template-maintenance feedback log (FB-NNN items about template improvements) |
| `feedback-archive.md` | Resolved / absorbed / closed feedback items |
| `scripts-candidates.md` | Inventory for FB-011 staged script extractions (Families A/B landed v3.0.0; C/D/E tiered for later) |

## Routing

**When capturing template-maintenance feedback — append to `template-maintenance/feedback.md` manually. Do NOT use `/feedback` in the template repo**: that slash command writes to `.claude/support/feedback/feedback.md`, which is the shipped location for downstream projects using the template.

For formal decisions about template direction, use `/research` or write to root `decisions/` directly (per root `CLAUDE.md` § "Template Maintenance Workflow").

## Why this folder exists

The `.claude/` tree is the environment that ships. Root-level artifacts (`decisions/`, `tests/`, `scripts/`, `system-overview.md`, this folder) are template-maintenance — they don't ship because they'd be noise in a new project's workspace. Keeping maintenance content physically separate from ship content makes "can I copy `.claude/` wholesale into a new project?" answerable as "yes."
