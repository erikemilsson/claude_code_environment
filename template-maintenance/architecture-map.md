# Template Architecture Map

**Current as of:** v5.14.3

> The line above is machine-read by `scripts/pre-commit-hook.sh` — keep the exact `**Current as of:** v{X.Y.Z}` format. Bump it whenever this map is reconciled against a new template version.

The topology reference for the template repo: the cross-component wiring the shipped files can't state about themselves. This replaces the former `system-overview.md` (stale since 2026-04-17; deleted 2026-07-19 in v5.1.1 — historical content via `git show v5.1.0:system-overview.md`).

**The layered truth model** (where each kind of truth lives):

- **What the system does** — the shipped files themselves (`.claude/`). There is no prose mirror; command/rule/reference files are self-describing and authoritative.
- **Why and when it changed** — root `decisions/` (rationale), `template-maintenance/ship-log.md` (what/when/file lists), and git tags `v{X.Y.Z}` (one per template version; revert points — `git diff v4.26.0..v5.0.0 -- .claude/`).
- **How components connect** — this file. Update **only when topology changes**: a file added/removed on the shipped surface, a new cross-reference edge, a new state file, a new hidden coupling. Wording, threshold, and bug-fix ships don't touch it.

## Shipped surface at a glance

Everything under `.claude/` ships to downstream projects (see root `CLAUDE.md § File Boundary` for what doesn't). The surface: 14 commands (`commands/`), 3 agent personas (`agents/`), 8 rules (`rules/` — 7 auto-loaded, 1 lazy), 33 reference docs (`support/reference/`), 7 Python scripts + a unittest suite of 10 files (`scripts/`, `scripts/tests/`), 1 hook (`hooks/pre-compact-handoff.sh`), template-owned `settings.json` (base `allow` + DEC-016 `ask` gates), `sync-manifest.json` (sync/customize/ignore categories), `version.json`.

## Load order — what enters context when

- **Every session (auto):** `.claude/CLAUDE.md` + the 7 rules in its `@`-import list: task-management, spec-workflow, decisions, dashboard, agents, archiving, session-management (~54 KB).
- **Path-scoped:** `rules/feature-retirement.md` (`paths:` frontmatter since v5.10.0: loads when Read/Write/Edit touches `.claude/support/retired/**`; before that it loaded every session, because Claude Code loads every rule file without `paths:` at launch).
- **Lazy by design (read on trigger, stubs say when):** `reference/mcp-patterns.md`, `reference/extension-hooks.md`, `reference/claude-code-authoring.md`, most other reference docs. Claude Code loads every `rules/*.md` without `paths:` at launch (`claude-code-authoring.md § "Rules loading"`); for a new lazy doc, prefer `support/reference/`, or give the rule `paths:` frontmatter.
- **On command invocation:** the command file itself, then its cited reference docs on demand (edges below).

## Dependency edges — command/agent → reference docs and scripts

Traced from actual citations (2026-10-07, v5.14.1: a `name.md` or script-name match in each file). "—" = self-contained.

| Consumer | Reference docs cited | Scripts invoked |
|---|---|---|
| `work.md` | claude-code-authoring, context-transitions, dashboard-regeneration, decisions, decomposition, drift-reconciliation, known-issues, parallel-execution, phase-decision-gates, session-recovery, task-schema, work-procedures, work-recovery (on trigger), work-user-flows (on trigger), work-web-evidence (on trigger), workflow | fingerprint.py, dashboard-render.py, persist-session-export.py (pause export); persist-friction.py via work-procedures |
| `health-check.md` | claude-code-authoring, context-transitions, dashboard-regeneration, decisions, mcp-patterns, parallel-execution, paths, root-claude-md-template, shared-definitions, task-schema, workflow | dashboard-render.py, validate-tasks.py, sync-check.py (Part 5, v5.10.0), sync-apply.py (Part 5 Step 4 writer, v5.12.0; behind `permissions.ask`), fingerprint.py `--baseline [--write]` (Part 1 check 11, v5.13.0; `--write` edits provenance keys in task files) |
| `iterate.md` | claude-code-authoring, decisions, desktop-project-prompt, drift-reconciliation, merge-queue, phase-decision-gates, spec-checklist | fingerprint.py |
| `audit-coherence.md` | audit-family-core, audit-fix-workflow, dashboard-regeneration, friction-register | — |
| `audit-ui.md` | audit-family-core, audit-fix-workflow, dashboard-regeneration, mcp-patterns | — |
| `feedback.md` / `shakedown.md` | merge-queue | — |
| `grill.md` | decisions, merge-queue, shared-definitions | — |
| `diagnose.md` | decisions, friction-register, mcp-patterns | — |
| `breakdown.md` | dashboard-regeneration, task-schema | — |
| `research.md` | decisions | — |
| `status.md` | drift-reconciliation, shared-definitions | fingerprint.py, dashboard-render.py |
| `review.md`, `zoom-out.md` | — | — |
| `implement-agent.md` | claude-code-authoring, context-transitions, decisions, friction-register | none (subagents never invoke scripts) |
| `verify-agent.md` | context-transitions, friction-register, negative-findings, task-schema | none |
| `research-agent.md` | decisions | none |
| `rules/agents.md` (auto-loaded) | claude-code-authoring, extension-hooks, friction-register, mcp-patterns, negative-findings (v5.8.0), shared-definitions, work-procedures | names sync-apply.py (the one script that asks) |
| other auto-loaded rules | archiving → paths; dashboard → dashboard-regeneration, workflow; decisions → decisions, extension-patterns; session-management → parallel-execution; spec-workflow → drift-reconciliation, merge-queue, spec-checklist, workflow; task-management → parallel-execution, shared-definitions, task-schema | dashboard → dashboard-render.py; spec-workflow, task-management → fingerprint.py |
| `hooks/pre-compact-handoff.sh` | context-transitions (handoff schema it writes) | none (copies its export to the inbox itself; FB-127 (b)) |

**Script → script (loaded by path):** `dashboard-render.py` loads `fingerprint.py` (`compute_drift()`, v5.9.0); `sync-apply.py` loads `sync-check.py` (v5.12.0). **Reference docs that name a script** (the prose procedure a script mirrors): fingerprint.py in dashboard-regeneration, decomposition, drift-reconciliation, paths, phase-decision-gates, shared-definitions, task-schema, work-procedures, workflow; dashboard-render.py in dashboard-regeneration, drift-reconciliation, extension-patterns; persist-friction.py in merge-queue, work-procedures; persist-session-export.py in context-transitions, work-recovery; validate-tasks.py in task-schema; sync-check.py and sync-apply.py in workflow.

## State files — writers and readers

All `.claude/` writes are orchestrator-owned (DEC-004); subagents only return reports. "gi" = gitignored/derived.

| State file | Written by | Read by |
|---|---|---|
| `tasks/task-*.json` | `/work` (+ `/breakdown`); fingerprint.py `--baseline --write` (provenance keys only, v5.13.0). Carries `decisions_pending` (agent choices held until the verify pass, v5.11.0) and `pending_decomposition[]` (v5.4.0) | `/work`, `/status`, `/health-check`, dashboard-render.py, validate-tasks.py, fingerprint.py `--drift`, both agents |
| `spec_v{N}.md` | `/iterate` (settings `ask`-gated) | everything |
| `spec_v{N}.index.json` (gi) | fingerprint.py `--index` via `/work` Step 1b | `/work`, both agents, spec-workflow rule |
| `verification-result.json` (gi) | `/work` (from verify-agent report) | `/status`, `/health-check`, `/audit-coherence`, dashboard-render.py (AC section, DEC-022) |
| `dashboard.html` (gi) | dashboard-render.py `--html` + orchestrator-filled placeholders | user (read-only) |
| `dashboard-state.json` (gi) | orchestrator (seeds); user content sidecar: `section_toggles`, `user_notes`, `augment_rows[]` (v5.8.0), plus `phase_gates` and `audit_digest` | dashboard-render.py (the Needs-you card also reads `drift-deferrals.json`, decision records and `support/feedback/feedback.md`, v5.4.0), `/health-check`, verify-agent |
| `tasks/.handoff.json` (gi) | `/work pause`, `hooks/pre-compact-handoff.sh` (cut to 2560 bytes, `truncated`, v5.14.1) | `/work` Step 0 (consumed on read) |
| `support/workspace/handoff-overflow-*.md` (gi) | `/work pause` when the handoff is over its bound (named in the handoff's `overflow_ref`, v5.14.0) | `/work` Step 0a (read, then deleted with the consumed or stale handoff, v5.14.1) |
| `tasks/.last-clean-exit.json` (gi) | `/work`: marked `"open": true` at "Before Any Dispatch", written closed at Step 5 and pause (v5.14.1) | `/work` Step 0 (`session-recovery.md`: open means full scan) |
| `{scratch}/residue-baseline.txt` (outside `.claude/`) | `/work` "Before Any Dispatch" (v5.14.1) | the Residue check in `work-procedures.md` after compaction |
| `support/workspace/.pending-markers.jsonl` (gi) | orchestrator dual-write of friction markers (DEC-011; persist-friction.py emits the lines to append) | pre-compact hook, `/work` startup catchup (`work-recovery.md`) |
| `support/workspace/.session-log.jsonl` (gi) | orchestrator (+ pre-compact hook reads for export) | `/work pause` export, `/audit-coherence` |
| `support/friction.jsonl` (gi) | persist-friction.py (orchestrator-invoked); status updates by the audit family, `/iterate`, and `/work` when a task with `resolves_friction` finishes (v5.10.0) | `/audit-coherence`, `/audit-ui`, `/diagnose` |
| `drift-deferrals.json` (gi) | `/work` | `/status`, verify-agent, dashboard-render.py |
| `support/decisions/decision-*.md` | `/research`, `/work` (Step 2b fills `## Decision`; "Persist decisions" writes `recorded` agent records; `/work ratify` and `reconsider`; the Post-Decision Check appends a follow-up task id to `related.tasks`, v5.14.2), settings `ask`-gated | `/work`, `/review`, `/health-check` Part 3, `/audit-coherence`, dashboard-render.py |
| `support/audits/{kind}-{ts}/digest.json` (gi) | `/audit-coherence`, `/audit-ui` | `/health-check`, audit triage and `[Fix it]`; summarised into sidecar `audit_digest` |
| `.spec-merge-queue.jsonl` (gi) | `/grill`, `/shakedown`, `/feedback` (producers) | `/iterate` (consumer, DEC-023) |
| `.sync-state.json` (gi) | sync-apply.py (`/health-check` Part 5 Step 4) | sync-check.py |
| `sync-manifest.json` | template (shipped lists); sync-apply.py updates a project's `sync`, `customize` and `ignore` lists | sync-check.py, sync-apply.py, pre-commit hook (hand-mirrored) |
| `version.json` | ship process (manual); sync-apply.py in a project (`template_version`, `template_release_date` only) | `/health-check` sync, pre-commit hook, downstream format-staleness triggers |
| `./CONTEXT.md` (project root) | `/grill` (lazy-created) | `/zoom-out`, `/diagnose`, `/audit-coherence`, both agents |

## Blast radius — if you change X, check Y

The hidden couplings. Each row is a place where an isolated-looking edit silently breaks something else.

| If you change… | Also check… |
|---|---|
| **`template-maintenance/` (root dir) — rename/delete** | It is the **template-repo sentinel** in 4 sites: `health-check.md` Part 5 (§ "Repo-type skip"), Part 5d, Part 7, and `scripts/pre-commit-hook.sh` (top guard). Renaming it makes downstream-sync logic run inside the template repo and silently disables the hook. Migrate all 4 sites together. (Migrated from `system-overview.md` in v5.1.1.) |
| Decision record `related.tasks` order | First id = the task that produced an agent record (`work-procedures.md` "If an agent record for this task already exists"); last id on a reconsidered record = the follow-up task (`phase-decision-gates.md § "Post-Decision Check"` writes it, `/review`'s Decision Implementation Audit reads it). Anything else that appends to or reorders the list breaks both (v5.14.2) |
| Task JSON fields (`reference/task-schema.md`) | `scripts/validate-tasks.py`, both agents' report envelopes, `reference/work-procedures.md`, dashboard-render.py field reads + its tests |
| dashboard-render.py output shape | Depends on `fingerprint.py` `compute_drift()` (loaded by path, v5.9.0) for the drift footer/rows. Format is pinned by `scripts/tests/test_dashboard_render*.py` (164 tests at v5.14.3: 26 + 138); prose contracts in `rules/dashboard.md` + `reference/dashboard-regeneration.md`; `/health-check` validates the HTML shape (doctype, `<!-- DASHBOARD META -->`, no CDN deps) |
| `settings.json` `permissions.ask` gates | DEC-016/023 prose in `rules/spec-workflow.md § Direct edits`, `.claude/README.md § Auto Mode`, `sync-manifest.json` notes field |
| `sync-manifest.json` categories | `scripts/pre-commit-hook.sh` `SYNC_PATTERNS` is a **hand-mirrored copy** (noted in its header); `/health-check` Part 5 diff logic; `sync-check.py` reads every historical manifest version (a file counts as template-owned when it was in `sync` at deletion), so category moves change what Part 5 offers to remove |
| sync-check.py output shape (v5.10.0, FB-126; `files[]`/`manifest`/`sidecar`/`history_complete` v5.12.0, FB-136) | Consumers: `/health-check` Part 5 Steps 2–5 and `sync-apply.py` (imports it; writes `.claude/` files, `version.json`, `sync-manifest.json`, `.sync-state.json`; pinned by `scripts/tests/test_sync_apply.py`); its rules are restated as the prose fallback in Part 5 Step 2 (dual location); pinned by `scripts/tests/test_sync_check.py` |
| fingerprint.py output shapes | Consumers: `/work` Step 1b, `/status`, index readers (agents, spec-workflow rule), `reference/drift-reconciliation.md`. **`compute_drift()` / `--drift` (v5.9.0, FB-128)** is also loaded by `dashboard-render.py` by path (META `drift_sections`, footer, Needs-you drift rows; degrades to "drift unchecked"), and its rules are restated as the prose fallback in `drift-reconciliation.md` § "Spec Drift Detection" (dual location); pinned by `scripts/tests/test_fingerprint.py` + the renderer tests. Known trap: `--spec` emits a bare `sha256:` string while `--index`/`--sections` emit JSON (downstream-reported 2026-06-25, unfixed) |
| `hooks/pre-compact-handoff.sh` handoff shape | `reference/context-transitions.md` (schema, `truncated`, reduced entries), `/work` Step 0a's required-fields check and its `truncated` exemption, `scripts/tests/test_pre_compact_hook.py` (19 tests; byte bound 2560) |
| persist-session-export.py | Callers: `/work pause` export (`work.md`, `context-transitions.md`, `work-recovery.md`); writes to the external `template_inbox_path` from `version.json`, never under `.claude/`; pinned by `scripts/tests/test_persist_session_export.py`. The pre-compact hook copies its own export without it |
| `scripts/tests/test_python_floor.py` `SHIPPED` tuple | Add every new shipped script to it (in the template repo the test asserts it equals the glob, v5.14.0) |
| persist-friction.py / friction schema | `reference/friction-register.md`, `rules/agents.md § Friction Register` kind lists, audit-family consumption |
| Model pin / dispatch value | Single source: `.claude/CLAUDE.md § Model Requirement`. Dispatch sites (`work.md`, `research.md`, `reference/parallel-execution.md`) cite it — never restate IDs. Dispatch convention (`subagent_type: "general-purpose"` + persona-via-prompt) enumerated in `rules/agents.md § Dispatch Convention`; all sites must stay uniform |
| Merge-queue shape (`reference/merge-queue.md`) | Producers `/grill` `/shakedown` `/feedback`, consumer `/iterate`, `.gitignore` entry for `.spec-merge-queue.jsonl` |
| `version.json` `template_version` | Pre-commit hook warning, downstream dashboard format-staleness migration, `/health-check` display; **tag the ship commit** (`git tag v{X.Y.Z}`) |
| `disable-model-invocation` frontmatter | Gated set (work, iterate, research, breakdown, feedback, zoom-out) is enumerated in `rules/agents.md § Command Invocation Gates` — keep in sync |
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
