# Scenario 41: Script-First Dashboard Regeneration (Family C full port)

Verify the division of labor (v4.22.0, HTML target since DEC-024): `dashboard-render.py --html` renders the whole dashboard deterministically, including every mechanical "Needs you" row and the sidecar's `augment_rows`; the LLM writes judgment rows to the sidecar and fills only the Custom Views placeholder; the canonical `task_hash` comes from `--task-hash`.

## Context

Evidence basis (scripts-candidates.md § Family C, PoC evidence run 2026-06-11): at styler scale the LLM render dropped DEC-072 deps from two task rows and prescribed regens were structurally bypassed (~18 friction notes); three different `task_hash` conventions coexisted. The script is the executable contract for structural sections. Since FB-105 it also owns the mechanical Action Required rows; since FB-118 judgment rows live in sidecar `augment_rows[]`, because rows hand-inserted into the HTML were wiped by every regen.

## State (Base)

A project mid-build: 30 active tasks across 3 phases (one complete), 40 archived finished tasks under `tasks/archive/`, 2 decisions (1 proposed). One active task is Finished with `user_review_pending: true`. The sidecar has `user_notes` content and two `augment_rows`: an unlinked action row, and a row whose `task_id` names an archived (Finished, no review flag) task. A Tier-1 regen trigger fires (post-decomposition).

---

## Trace 41A: Full regen runs the script; only Custom Views is filled

- **Path:** `dashboard-regeneration.md § "Script-First Rendering — HTML target"` → Step 2 (sidecar merge) → `--html` → Write → Custom Views fill (when on) → Step 8

### Expected

- Step 2 runs FIRST (the script reads user content and `augment_rows` from the sidecar)
- Orchestrator runs `--html` (with `--now`) and Writes stdout to `dashboard.html` — it does NOT hand-write any section or row
- The card's Your Tasks lists the review-pending task (`/work complete {id}`); "Also Needs You" comes last and shows the unlinked row but not the expired one
- The only edit after the Write is the Custom Views `<!-- CLAUDE: fill … -->` region, when that section is on; Step 8 finds no `<!-- CLAUDE: fill` left
- Completed-phase counts include the 40 archived tasks; META `task_hash` matches `--task-hash` output

### Pass criteria

- [ ] Byte-identical to script output outside the Custom Views region
- [ ] Step 8 catches an unfilled Custom Views placeholder as incomplete regeneration
- [ ] Archive-aware counts; `user_notes` preserved verbatim; the expired augment row not rendered

### Fail indicators

- LLM "improves" a script-rendered section (re-introduces the nondeterminism the port exists to kill)
- Script run skipped while python3 available; sections hand-written
- Sidecar merge skipped → stale user content rendered
- A judgment row edited into the card instead of written to `augment_rows[]`

---

## Trace 41B: Hash authority

- **Path:** `/work` Step 1a freshness check + `/health-check` Part 1 check 10 + `/status` freshness check

### Expected

- Recompute uses `dashboard-render.py --task-hash` (sorted `id:status:difficulty:owner:review`, `review` = 1 when `user_review_pending`, else 0; newline-joined + trailing newline, active only)
- `fingerprint.py --dashboard-rollup` (`id:status`) is never compared with dashboard META
- Clearing only the review flag on the review-pending task changes the hash; a dashboard rendered before the `review` field reads stale once and regenerates

### Pass criteria

- [ ] Freshly script-rendered dashboard immediately passes the freshness check (hash round-trips)
- [ ] Archived tasks do not perturb the hash
- [ ] A review-flag-only change reads as stale

### Fail indicators

- A third ad-hoc hash computation appears (the styler three-way mismatch class)
- `/status` reports a fresh dashboard as stale (rollup hash compared with META)

---

## Trace 41C: No fallback, no hand edits; judgment rows persist

- **Path:** environment without python3; a mid-session judgment row followed by two more Tier-1 regens

### Expected

- No python3 → no regeneration (there is no Markdown fallback); the previously rendered `dashboard.html` stays readable
- A new judgment row goes into sidecar `augment_rows[]`, then a full regen renders it; there is no targeted-edit path and no `pending_full_regen` sentinel
- Each later regen re-renders the row from the sidecar, unchanged, until the orchestrator prunes it

### Pass criteria

- [ ] Script absent → nothing hand-rendered
- [ ] The row survives both later regens with no re-authoring

### Fail indicators

- HTML sections hand-rendered because the script is missing
- A row `Edit`ed into `dashboard.html` (gone at the next regen)
- Rows re-extracted from the previous HTML and re-injected after each regen
