# Migration Guide

How to bring an existing project's `.claude/` environment up to date with the current template.

## When to Use This Guide

- Project uses an older version of this template
- Project has a custom `.claude/` structure that predates the template
- Project has no `.claude/` directory at all

This guide is designed to be read by Claude Code when opened at the **target project** root. Claude reads this guide from the template repository, then executes the migration against the target project.

## Prerequisites

- The template repository is available locally (or Claude can access it via a path the user provides)
- The user has confirmed they want to proceed with migration
- Git is initialized in the target project

## Philosophy

The goal is **standardization**: every project should have an identical `.claude/` infrastructure — same commands, agents, reference docs, and schemas. Project-specific content (tasks, decisions, spec, domain commands, domain documents) gets preserved and adapted to fit the standardized structure. Where information doesn't map cleanly, Claude flags it for user review rather than forcing it into an ill-fitting location.

## Step 1: Backup

**Always create a backup before migration.** The backup goes in the user's Developer archive folder, not inside the project.

### Backup Location

```
~/Developer/_archive/backups/{project-name}/{YYYY-MM-DD}/
```

Example:
```
~/Developer/_archive/backups/SIREN/2026-03-05/
```

### What to Back Up

Create a **full project snapshot** — the entire project directory excluding `.git`, caches, and generated artifacts. This ensures the backup captures the complete state of the project at migration time, not just the environment files.

```bash
mkdir -p ~/Developer/_archive/backups/{project-name}/$(date +%Y-%m-%d)
rsync -a --exclude='.git' --exclude='__pycache__' --exclude='.pytest_cache' --exclude='*.pyc' --exclude='.DS_Store' --exclude='node_modules' --exclude='.venv' --exclude='venv' ./ ~/Developer/_archive/backups/{project-name}/$(date +%Y-%m-%d)/
```

### Backup Verification

```bash
# Spot-check key directories exist in the backup
ls ~/Developer/_archive/backups/{project-name}/$(date +%Y-%m-%d)/.claude/
ls ~/Developer/_archive/backups/{project-name}/$(date +%Y-%m-%d)/
```

No output = backup matches. Proceed only after verification.

## Step 2: Inventory

Before changing anything, catalog what exists in the target project. Read through the `.claude/` directory and classify everything.

### Classification Categories

| Category | Description | Migration Action |
|----------|-------------|-----------------|
| **Template infrastructure** | Commands (work, iterate, status, etc.), agents (implement, verify, research), reference docs | Replace with latest template |
| **Project content** | Spec, tasks, decisions, vision docs, workspace files | Preserve |
| **Domain extensions** | Project-specific commands, custom agents, domain documents | Preserve alongside template |
| **Hybrid** | CLAUDE.md, dashboard, settings | Merge (template structure + project data) |
| **Legacy/custom** | Files with no template equivalent | Evaluate and flag for user |
| **Operational docs** | Living documents outside `.claude/` (roadmaps, design systems, etc.) | Leave in place, reference from CLAUDE.md |

### Key Distinctions

**Template commands vs domain commands:** Template commands (`work.md`, `iterate.md`, `status.md`, `research.md`, `feedback.md`, `breakdown.md`, `health-check.md`, `review.md`) get replaced. Any other command in `.claude/commands/` is domain-specific and must be preserved.

**Template agents vs project agents:** The three template agents (`implement-agent.md`, `verify-agent.md`, `research-agent.md`) get replaced. Any other agents are project-specific and must be preserved alongside them.

**Template reference docs vs project reference docs:** Template reference docs (listed in Step 4) get replaced. Any reference doc not in that list is project-specific and must be preserved.

**Gitignored working directories:** If the project has working directories outside `.claude/` (e.g., `.implementation/`), do not touch them. They are outside scope.

## Step 3: Identify Template Changes

Use git to see what has changed in the template since the project's last sync.

### Check for Version Markers

Look for `.claude/version.json` or `.claude/sync-manifest.json` in the target project. These indicate when the last sync happened.

### Compare Against Template History

```bash
# From the template repository
git log --oneline --since="{last-sync-date}"
```

If there are no version markers, treat this as a full migration from scratch.

## Step 4: Replace Template Infrastructure

Copy these files from the current template, replacing what exists. **Only replace the files listed below** — everything else in the project stays.

### Commands (replace only these)

```
.claude/commands/work.md
.claude/commands/iterate.md
.claude/commands/status.md
.claude/commands/research.md
.claude/commands/feedback.md
.claude/commands/breakdown.md
.claude/commands/health-check.md
.claude/commands/review.md
```

All other commands in `.claude/commands/` are domain-specific — preserve them.

### Agents (replace only these)

```
.claude/agents/implement-agent.md
.claude/agents/verify-agent.md
.claude/agents/research-agent.md
```

All other agents in `.claude/agents/` are project-specific — preserve them.

### Reference Docs (replace only these)

```
.claude/support/reference/workflow.md
.claude/support/reference/shared-definitions.md
.claude/support/reference/task-schema.md
.claude/support/reference/decisions.md
.claude/support/reference/extension-patterns.md
.claude/support/reference/parallel-execution.md
.claude/support/reference/decomposition.md
.claude/support/reference/dashboard-regeneration.md
.claude/support/reference/drift-reconciliation.md
.claude/support/reference/session-recovery.md
.claude/support/reference/context-transitions.md
.claude/support/reference/setup-checklist.md
.claude/support/reference/spec-checklist.md
.claude/support/reference/phase-decision-gates.md
.claude/support/reference/paths.md
.claude/support/reference/desktop-project-prompt.md
.claude/support/reference/root-claude-md-template.md
.claude/support/reference/README.md
```

All other files in `.claude/support/reference/` are project-specific — preserve them.

### Rules Files (replace only these)

```
.claude/rules/task-management.md
.claude/rules/spec-workflow.md
.claude/rules/decisions.md
.claude/rules/dashboard.md
.claude/rules/agents.md
.claude/rules/archiving.md
```

User-created rule files (`project-*.md`) in `.claude/rules/` are project-specific — preserve them.

### Other Template Files

```
.claude/README.md
.claude/support/workspace/README.md
.claude/support/documents/README.md
.claude/support/feedback/README.md
.claude/support/learnings/README.md
.claude/support/previous_specifications/README.md
.claude/vision/README.md
.claude/hooks/pre-compact-handoff.sh
```

### Create Missing Directories

Ensure these directories exist (create with `.gitkeep` if empty):
```
.claude/vision/
.claude/rules/
.claude/hooks/
.claude/support/decisions/
.claude/support/decisions/.archive/
.claude/support/documents/
.claude/support/feedback/
.claude/support/learnings/
.claude/support/workspace/
.claude/support/previous_specifications/
.claude/tasks/
.claude/tasks/archive/
```

## Step 5: Migrate Task Schema

Task JSON files may use an older schema. Bring them into the current schema while accepting gaps.

### Philosophy

- **Structure over backfill.** Use the new schema shape, but don't fabricate data that didn't exist.
- **Gaps are acceptable.** A completed task from months ago doesn't need `task_verification` or `spec_fingerprint`.
- **Note the gaps.** Add a `notes` entry: "Pre-migration task — verification predates current schema."
- **Don't lose information.** If old fields have real content with no direct equivalent, capture in `notes` or `description`.
- **Preserve extra structured fields.** If a task has domain-specific structured data (nested objects, arrays of steps, component maps) that would lose value if flattened into a `notes` string, **leave those fields in place**. JSON doesn't break with unrecognized fields — the template commands simply ignore them. This is preferable to destroying structure. See "Rich Domain-Specific Fields" below.

### Field Mapping

| Old Field | New Equivalent | Migration Action |
|-----------|---------------|-----------------|
| `validation.criteria` | `task_verification.checks` | Finished: note in `notes`. Pending: convert if meaningful. |
| `validation.completed` | `task_verification.result` | `true` → `"pass"` |
| `category` | (removed) | Incorporate into `description` or `notes` if useful |
| `deliverables` / `outputs` | `files_affected` | Map paths |
| `related_tasks` | `dependencies` | Move if actual dependencies; otherwise `notes` |
| `user_input_required` | `owner: "human"` + `notes` | Set owner; capture details in `notes` |
| `related_phases` | `phase` | Should already map |
| `created` / `updated` | `created_date` / `updated_date` | Rename |
| `assigned_to` | `owner` | Map value (e.g., "Claude" → "claude") |
| `tags` / `blockers` | (not in schema) | Capture in `notes` if meaningful |

### Rich Domain-Specific Fields

Some projects have tasks with deeply structured domain-specific fields that go beyond the template schema — for example, nested objects describing pipeline components, arrays of implementation steps, evaluation matrices, or success criteria blocks.

**Do not flatten these into `notes`.** Instead:

1. **Rename/add** the fields the new schema expects (e.g., `created` → `created_date`)
2. **Add** any missing required fields (e.g., `difficulty` if absent)
3. **Leave extra fields in place** — they won't break anything
4. **Map what maps** — `deliverables` → `files_affected`, `related_tasks` → `dependencies` where appropriate
5. **Don't strip** fields like `implementation_steps`, `pipeline_components`, `success_criteria`, `documentation_structure`, etc.

The result is a task that conforms to the new schema (all expected fields present) while preserving domain richness (extra fields retained). This is better than a schema-conformant task that lost its most useful content.

### Task Status Mapping

| Current Valid Statuses |
|----------------------|
| `Pending`, `In Progress`, `Awaiting Verification`, `Blocked`, `On Hold`, `Absorbed`, `Broken Down`, `Finished` |

Map old values: `Complete`/`Done` → `Finished`, `Superseded` → `Absorbed` (set `absorbed_into` to the replacing task, or flag for user review if unclear). Preserve `On Hold` as-is — it is a distinct status (user-controlled pause, not auto-routed by `/work`) separate from `Blocked` (impediment that must be cleared).

### Batch Processing (100+ tasks)

1. Read 3-5 sample tasks to understand the old schema
2. Write a conversion approach
3. Process in batches, spot-checking after each
4. Focus attention on active/pending tasks — these matter most

## Step 6: Merge Hybrid Content

### .claude/CLAUDE.md

1. Start with the current template's `.claude/CLAUDE.md` as the base
2. Fill in project-specific sections:
   - **Project Overview** — from existing CLAUDE.md or project docs
   - **Technology Stack** — from existing CLAUDE.md
   - **Conventions** — from existing CLAUDE.md
   - **Specification** — adapt to project's spec structure
3. Preserve project-specific additions (custom commands in the commands list, special rules)
4. Remove template instructions that don't apply

### Context and Standards

If the project has a context directory (`.claude/context/`) or standalone standards files with detailed constraints, framework patterns, or coding standards:

- Create a reference document in `.claude/support/reference/` (e.g., `project-standards.md`) that consolidates this content
- Reference it from `.claude/CLAUDE.md` in the Conventions section
- This avoids bloating CLAUDE.md while keeping the information accessible

### Root CLAUDE.md

Update to match the template's pattern — brief, links to `.claude/CLAUDE.md`, with project-specific quick reference items.

### Operational Documents

Living documents outside `.claude/` (content roadmaps, design systems, etc.) stay where they are. They don't need to be moved into the template structure. Reference them from `.claude/CLAUDE.md` if Claude needs to be aware of them.

### Settings Files

- `.claude/settings.json` — merge template defaults with project overrides. **Preserve project-specific permissions** (e.g., allowed MCP servers, tool permissions, custom `allowedTools` entries) — these reflect the user's trust decisions for their project and should not be dropped during merge.
- `.claude/settings.local.json` — preserve (user-specific)

### Update Internal References

After merging, scan `.claude/CLAUDE.md` and the spec for references to files that moved during migration (e.g., `PROGRESS.md` → dashboard, context files → reference docs). Update these references to point to their new locations. Flag any you're unsure about in the post-migration checklist.

## Step 7: Create Spec (if missing)

If the project has no spec file (`.claude/spec_v*.md`), create one from the project as it currently exists. The spec is the guiding star — every project needs one.

### How to Generate a Spec from an Existing Project

1. Read all project documentation (README, design docs, architecture docs, existing CLAUDE.md)
2. Read the codebase structure and key files
3. Draft a spec that describes what the project **is** and what it **does** — not what to build next, but what exists and what the project's goals are
4. Include any remaining work as future phases or pending items
5. Flag ambiguities — anything unclear goes on the post-migration checklist (Step 10)

### Reference Documents

Large reference documents (design systems, architecture docs, domain glossaries) should live in `.claude/support/documents/`, not in the spec itself. The spec references them.

## Step 8: Consolidate Legacy Dashboard/Progress Documents (if applicable)

If the project has a document like `PROGRESS.md` that serves as the user-facing dashboard, consolidate its content into `.claude/dashboard.md`.

### Section Mapping

| Legacy Section | Dashboard Equivalent |
|---------------|---------------------|
| Critical blockers, immediate actions | Action Required |
| Status overview, completion stats | Progress |
| Task listings by area | Tasks (grouped by phase) |
| Decision tracking | Decisions |
| User notes, ideas, reminders | Notes (USER SECTION) |
| Domain-specific tracking | Custom Views |
| Changelog/update history | Not preserved (git history serves this) |

### Custom Views for Domain Content

Anything that doesn't fit standard dashboard sections becomes a Custom View. Write instructions that tell Claude how to generate them:

```markdown
<!-- CUSTOM VIEWS INSTRUCTIONS -->

**Workshop Management:** Track workshop phases, participant status, and document readiness...

**Publication Progress:** Show publication file checklist by category with completion status...

<!-- END CUSTOM VIEWS INSTRUCTIONS -->
```

### When Domain Content Is Too Large for Custom Views

Some legacy dashboards contain substantial domain-specific content — detailed participant tracking tables, mermaid workflow diagrams, nested document inventories, or multi-page reference sections. Reproducing this inline via Custom Views would bloat the dashboard and exceed what regeneration can maintain reliably.

For these cases, extract the content into a **standalone reference document** in `.claude/support/reference/` or `.claude/support/documents/` rather than forcing it into Custom Views:

1. Create a reference doc (e.g., `.claude/support/reference/workshop-management.md`) with the full detail
2. The dashboard gets a one-line summary row or Custom View instruction that **links to** the reference doc
3. Flag each content-placement decision in `MIGRATION-REVIEW.md` (Step 10) so the user can verify the split was appropriate

**Rule of thumb:** If a legacy section would take more than ~20 lines in the dashboard, it's a candidate for extraction to a reference doc.

### After Consolidation

Archive the legacy document to `.claude/support/workspace/` (e.g., `PROGRESS-pre-migration.md`). Remove it from the project root. Flag this on the post-migration checklist so the user can verify nothing was lost.

## Step 9: Update Version Markers

### version.json

```json
{
  "template_version": "{latest-template-commit-hash}",
  "migrated_at": "{ISO-date}",
  "migrated_from": "{previous-version-or-description}"
}
```

### sync-manifest.json

List all template-managed files so future `/health-check` runs can detect drift.

**Use explicit file lists, not glob patterns.** A glob like `.claude/commands/*.md` will incorrectly flag domain-specific commands as sync targets, causing future health checks to report them as drifted and future migrations to overwrite them.

The `sync` category should list only the template-managed files by name:

```json
{
  "categories": {
    "sync": [
      ".claude/commands/work.md",
      ".claude/commands/iterate.md",
      ".claude/commands/status.md",
      ".claude/commands/research.md",
      ".claude/commands/feedback.md",
      ".claude/commands/breakdown.md",
      ".claude/commands/health-check.md",
      ".claude/commands/review.md",
      ".claude/agents/implement-agent.md",
      ".claude/agents/verify-agent.md",
      ".claude/agents/research-agent.md",
      ".claude/support/reference/workflow.md",
      ".claude/support/reference/shared-definitions.md",
      ".claude/support/reference/task-schema.md"
    ],
    "domain": [
      ".claude/commands/check-approval-status.md",
      ".claude/commands/run-pipeline.md"
    ],
    "ignore": [
      ".claude/tasks/*.json",
      ".claude/dashboard.md"
    ]
  }
}
```

The `domain` category (new) explicitly lists project-specific command and agent files. These are never overwritten by template sync. The `ignore` category can still use globs since those patterns match project-generated content, not named template files.

## Step 10: Post-Migration Checklist

**This is critical.** After completing the migration, generate a checklist file at the project root called `MIGRATION-REVIEW.md`. This file is designed for the user to review at their own pace in a Claude Code conversation.

### Purpose

- Surface everything that needs user attention after migration
- Flag ambiguities and decisions Claude made on the user's behalf
- List files Claude wasn't sure where to place
- Provide a systematic way to verify the migration is complete

### Structure

```markdown
# Migration Review

Migration from: {description of old state}
Migration date: {YYYY-MM-DD}
Backup location: ~/Developer/_archive/backups/{project}/{date}/

## Approval Required

Items where Claude made a judgment call that needs user confirmation.

- [ ] **Spec created from existing docs** — Review `.claude/spec_v1.md` for accuracy
- [ ] **Dashboard consolidated from PROGRESS.md** — Review `.claude/dashboard.md` for completeness
- [ ] **{N} tasks migrated to new schema** — Spot-check active tasks for correctness
- [ ] ...

### Content Placement Decisions

Domain content that was too large for the dashboard and was extracted to reference docs (see Step 8). Compare each pair to verify nothing was lost:

- [ ] **{section name}** — Original: `{legacy file}` § {section} → New: `.claude/support/reference/{file}.md` — Dashboard links to it via {Custom View / summary row}
- [ ] ...

### Schema Judgment Calls

Tasks where migration required a judgment call about field values (e.g., owner assignment, status mapping, priority inference):

- [ ] **Task {id}**: `owner` set to `"{value}"` — original had `{old field/value}`, mapped because {reason}
- [ ] **Task {id}**: `status` mapped from `"{old}"` to `"{new}"` — {reason if non-obvious}
- [ ] ...

### Settings Merge

Project-specific permissions preserved during settings.json merge:

- [ ] **Allowed MCP servers**: {list} — carried from project settings
- [ ] **Custom tool permissions**: {list} — carried from project settings
- [ ] Verify these are still appropriate for the migrated project

### ID Format Note

{If applicable:} Task IDs use non-standard format (`{format}`, e.g., `SIREN-001`). These were preserved as-is — the template accepts any string ID.

## Ambiguities Found

Things Claude encountered that weren't clear-cut.

- [ ] **{file}** — {description of ambiguity and what Claude did}
- [ ] ...

### Orphaned Systems

Features from the old structure that exist but aren't referenced by current template commands. These may be custom tooling the user wants to keep, or may be obsolete:

- [ ] **{file or system}** — {what it appears to do}, not used by any template command. Keep / remove?
- [ ] ...

### Stale References

References in project files that point to locations that changed during migration:

- [ ] **{file}** line {N}: references `{old path}` — {updated to `{new path}` / needs manual update}
- [ ] ...

### Unknown Files

Files Claude encountered but couldn't determine the purpose of:

- [ ] **{file}** — {what Claude observed about it, best guess at purpose}. User should verify placement or remove.
- [ ] ...

## Files Relocated

Files that were moved during migration.

| Original Location | New Location | Reason |
|-------------------|-------------|--------|
| `PROGRESS.md` | `.claude/support/workspace/PROGRESS-pre-migration.md` | Consolidated into dashboard |
| ... | ... | ... |

## Files Left in Place

Files outside `.claude/` that Claude did not move because their placement was unclear. These may need user decision.

- `docs/CONTENT-ROADMAP.md` — Living operational document, referenced from CLAUDE.md
- ...

## Not Migrated

Content from the old structure that was intentionally not carried forward (with reasons).

- {item} — {reason}
- ...

## Verification

- [ ] `.claude/CLAUDE.md` accurately describes the project
- [ ] `.claude/dashboard.md` contains all relevant status information
- [ ] Active/pending tasks are correct and actionable
- [ ] Decision records are intact
- [ ] `/health-check` reports no critical issues
- [ ] `/status` produces a coherent report

## Done

Once all items are checked, delete this file — the migration is complete.
```

### Key Principle

**Don't force decisions.** If Claude isn't sure whether a file should go in `support/documents/` or `support/reference/` or stay where it is, list it in "Files Left in Place" and let the user decide. The checklist is a conversation tool — the user works through it with Claude in a follow-up session.

## Common Migration Scenarios

### Scenario A: Fresh project (no .claude/)

Copy the entire `.claude/` directory from the template. User fills in project-specific sections. Generate spec using `/iterate`.

### Scenario B: Project with old template version (e.g., SIREN, OEMMatInsightBI)

Standard path. Main work: replace infrastructure, migrate task schema, consolidate dashboard. Domain commands, decisions, and project-specific reference docs preserved.

### Scenario C: Project with custom non-template structure (e.g., PortfolioWebsite)

Largest migration effort:
1. Full inventory is essential — the old structure may use different concepts that need mapping
2. Spec must be created from existing project documentation and codebase
3. Tasks may need conversion from a completely different schema
4. Custom commands may overlap with template commands — identify which to keep, which to replace
5. The post-migration checklist will likely be longer

### Scenario D: Project with rich legacy dashboard (e.g., SIREN's PROGRESS.md)

Follow Step 8. Custom Views handle domain-specific sections. The goal is zero information loss with standardized structure.

## Notes

- This guide does not ship to projects — it's template maintenance infrastructure
- The backup strategy uses `~/Developer/_archive/backups/` with ISO-dated folders
- Git history in the template repository serves as the changelog — no separate CHANGELOG.md needed
- Each migration is a one-time operation; `/health-check` handles ongoing drift detection after migration
- The post-migration checklist (`MIGRATION-REVIEW.md`) is temporary — deleted once the user has verified everything
