# Template Architecture Map

**Current as of:** v5.1.0

> The line above is machine-read by `scripts/pre-commit-hook.sh` — keep the exact `**Current as of:** v{X.Y.Z}` format. Bump it whenever this map is reconciled against a new template version.

The topology reference for the template repo: the cross-component wiring the shipped files can't state about themselves. This replaces `system-overview.md` as the maintenance-side overview (that file is stale since 2026-04-17 and retained only as the template-repo sentinel — see § Blast radius).

**The layered truth model** (where each kind of truth lives):

- **What the system does** — the shipped files themselves (`.claude/`). There is no prose mirror; command/rule/reference files are self-describing and authoritative.
- **Why and when it changed** — root `decisions/` (rationale), `template-maintenance/ship-log.md` (what/when/file lists), and git tags `v{X.Y.Z}` (one per template version; revert points — `git diff v4.26.0..v5.0.0 -- .claude/`).
- **How components connect** — this file. Update **only when topology changes**: a file added/removed on the shipped surface, a new cross-reference edge, a new state file, a new hidden coupling. Wording, threshold, and bug-fix ships don't touch it.

## Shipped surface at a glance

Everything under `.claude/` ships to downstream projects (see root `CLAUDE.md § File Boundary` for what doesn't). The surface: 14 commands (`commands/`), 3 agent personas (`agents/`), 8 rules (`rules/` — 7 auto-loaded, 1 lazy), ~29 reference docs (`support/reference/`), 4 Python scripts + unittest suite (`scripts/`), 1 hook (`hooks/pre-compact-handoff.sh`), template-owned `settings.json` (base `allow` + DEC-016 `ask` gates), `sync-manifest.json` (sync/customize/ignore categories), `version.json`.

## Load order — what enters context when

- **Every session (auto):** `.claude/CLAUDE.md` + the 7 rules in its `@`-import list: task-management, spec-workflow, decisions, dashboard, agents, archiving, session-management (~54 KB).
- **Lazy by design (read on trigger, stubs say when):** `rules/feature-retirement.md`, `reference/mcp-patterns.md`, `reference/extension-hooks.md`, `reference/claude-code-authoring.md`, most other reference docs. *Caveat (observed 2026-07-19):* at least one harness auto-loads all of `rules/*.md` regardless of the import list — so `feature-retirement.md` may be loaded anyway. Adding a rules file may cost every-session context even if unimported; prefer `support/reference/` for new lazy docs.
- **On command invocation:** the command file itself, then its cited reference docs on demand (edges below).

## Dependency edges — command/agent → reference docs and scripts

Traced from actual citations (2026-07-19). "—" = self-contained.

| Consumer | Reference docs cited | Scripts invoked |
|---|---|---|
| `work.md` | claude-code-authoring, context-transitions, dashboard-regeneration, decomposition, drift-reconciliation, known-issues, parallel-execution, phase-decision-gates, session-recovery, work-procedures, workflow | fingerprint.py (+ dashboard-render.py, persist-friction.py via dashboard-regeneration/friction procedures) |
| `health-check.md` | claude-code-authoring, dashboard-regeneration, decisions, mcp-patterns, paths, root-claude-md-template, shared-definitions, task-schema, workflow | dashboard-render.py, validate-tasks.py |
| `iterate.md` | claude-code-authoring, decisions, desktop-project-prompt, drift-reconciliation, merge-queue, spec-checklist | — |
| `audit-coherence.md` | audit-family-core, audit-fix-workflow | — |
| `audit-ui.md` | audit-family-core, mcp-patterns | — |
| `feedback.md` / `grill.md` / `shakedown.md` | merge-queue (+ shared-definitions for grill) | — |
| `diagnose.md` | friction-register, mcp-patterns | — |
| `breakdown.md` | dashboard-regeneration | — |
| `research.md` | decisions | — |
| `status.md` | — | fingerprint.py |
| `review.md`, `zoom-out.md` | — | — |
| `implement-agent.md` | claude-code-authoring, context-transitions, decisions, friction-register | none (subagents never invoke scripts) |
| `verify-agent.md` | context-transitions, friction-register | none |
| `research-agent.md` | decisions | none |

## State files — writers and readers

All `.claude/` writes are orchestrator-owned (DEC-004); subagents only return reports. "gi" = gitignored/derived.

| State file | Written by | Read by |
|---|---|---|
| `tasks/task-*.json` | `/work` (+ `/breakdown`) | `/work`, `/status`, `/health-check`, dashboard-render.py, both agents |
| `spec_v{N}.md` | `/iterate` (settings `ask`-gated) | everything |
| `spec_v{N}.index.json` (gi) | fingerprint.py `--index` via `/work` Step 1b | `/work`, both agents, spec-workflow rule |
| `verification-result.json` (gi) | `/work` (from verify-agent report) | `/status`, `/health-check`, `/audit-coherence`, dashboard-render.py (AC section, DEC-022) |
| `dashboard.html` (gi) | dashboard-render.py `--html` + orchestrator-filled placeholders | user (read-only) |
| `dashboard-state.json` (gi) | orchestrator (seeds); user content sidecar | dashboard-render.py, `/health-check`, verify-agent |
| `tasks/.handoff.json` (gi) | `/work pause`, `hooks/pre-compact-handoff.sh` | `/work` Step 0 (consumed on read) |
| `tasks/.last-clean-exit.json` (gi) | `/work` | `/work` Step 0 |
| `support/workspace/.session-log.jsonl` (gi) | orchestrator (+ pre-compact hook reads for export) | `/work pause` export, `/audit-coherence` |
| `support/friction.jsonl` (gi) | persist-friction.py (orchestrator-invoked) | `/audit-coherence`, `/audit-ui`, `/diagnose` |
| `drift-deferrals.json` (gi) | `/work` | `/status`, verify-agent, dashboard-render.py |
| `.spec-merge-queue.jsonl` (gi) | `/grill`, `/shakedown`, `/feedback` (producers) | `/iterate` (consumer, DEC-023) |
| `.sync-state.json` (gi) | `/health-check` Part 5 | `/health-check` Part 5 |
| `version.json` | ship process (manual) | `/health-check` sync, pre-commit hook, downstream format-staleness triggers |
| `./CONTEXT.md` (project root) | `/grill` (lazy-created) | `/zoom-out`, `/diagnose`, `/audit-coherence`, both agents |

## Blast radius — if you change X, check Y

The hidden couplings. Each row is a place where an isolated-looking edit silently breaks something else.

| If you change… | Also check… |
|---|---|
| **`system-overview.md` (root) — rename/delete** | It is the **template-repo sentinel** in 4 sites: `health-check.md` Part 5 (§ "Before running any sync step"), Part 5d, Part 7, and `scripts/pre-commit-hook.sh` (top guard). Removing it un-skips self-sync downstream logic and disables the hook. Migrate the sentinel in all 4 sites first. |
| Task JSON fields (`reference/task-schema.md`) | `scripts/validate-tasks.py`, both agents' report envelopes, `reference/work-procedures.md`, dashboard-render.py field reads + its tests |
| dashboard-render.py output shape | Format is pinned by `scripts/tests/test_dashboard_render*.py` (47 tests); prose contracts in `rules/dashboard.md` + `reference/dashboard-regeneration.md`; `/health-check` validates the HTML shape (doctype, `<!-- DASHBOARD META -->`, no CDN deps) |
| `settings.json` `permissions.ask` gates | DEC-016/023 prose in `rules/spec-workflow.md § Direct edits`, `.claude/README.md § Auto Mode`, `sync-manifest.json` notes field |
| `sync-manifest.json` categories | `scripts/pre-commit-hook.sh` `SYNC_PATTERNS` is a **hand-mirrored copy** (noted in its header); `/health-check` Part 5 diff logic |
| fingerprint.py output shapes | Consumers: `/work` Step 1b, `/status`, index readers (agents, spec-workflow rule), `reference/drift-reconciliation.md`. Known trap: `--spec` emits a bare `sha256:` string while `--index`/`--sections` emit JSON (downstream-reported 2026-06-25, unfixed) |
| persist-friction.py / friction schema | `reference/friction-register.md`, `rules/agents.md § Friction Register` kind lists, audit-family consumption |
| Model pin / dispatch value | Single source: `.claude/CLAUDE.md § Model Requirement`. Dispatch sites (work.md ×2, research.md) cite it — never restate IDs. Dispatch convention (`subagent_type: "general-purpose"` + persona-via-prompt) enumerated in `rules/agents.md § Dispatch Convention`; 3 sites must stay uniform |
| Merge-queue shape (`reference/merge-queue.md`) | Producers `/grill` `/shakedown` `/feedback`, consumer `/iterate`, `.gitignore` entry for `.spec-merge-queue.jsonl` |
| `version.json` `template_version` | Pre-commit hook warning, downstream dashboard format-staleness migration, `/health-check` display; **tag the ship commit** (`git tag v{X.Y.Z}`) |
| `disable-model-invocation` frontmatter | Gated set (work, iterate, research, breakdown, feedback) is enumerated in `rules/agents.md § Command Invocation Gates` — keep in sync |
| Adding/removing a `rules/*.md` file | The `@`-import list in `.claude/CLAUDE.md` (unimported ≠ loaded — but see the harness caveat in § Load order), `sync-manifest.json` sync list (rules are enumerated **individually**, not globbed) |
| Acceptance-criteria surfaces | DEC-022 chain: verify-agent `criteria[]` → `verification-result.json` → dashboard AC section → `/audit-coherence` acceptance-reconciliation lens → `rules/spec-workflow.md § Acceptance-criteria authority` |
| FB-NNN IDs (maintenance side) | One ID namespace across **four** files with asymmetric names: `.claude/support/feedback/{feedback,archive}.md` + `template-maintenance/{feedback,feedback-archive}.md` (see root `CLAUDE.md § Feedback`) |

## Ship definition-of-done

Every template ship, in order:

1. Bump `template_version` in `.claude/version.json` (pre-commit hook warns if forgotten)
2. Append the ship entry to `template-maintenance/ship-log.md` (rationale, FB/DEC linkage, file list)
3. Commit, then tag: `git tag v{X.Y.Z}`
4. **If topology changed** (new/removed shipped files, new edges, new state files, new couplings): update this map, including its `Current as of` line (hook reminds on structural changes)
5. If command logic changed: trace the relevant `tests/scenarios/` scenario(s), add one for new behavior
6. Push with tags: `git push --follow-tags`
