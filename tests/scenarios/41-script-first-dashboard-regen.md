# Scenario 41: Script-First Dashboard Regeneration (Family C full port)

Verify the v4.22.0 division of labor: `dashboard-render.py --render` produces every structural section deterministically; the LLM writes the output and fills ONLY the synthesis placeholders; the canonical `task_hash` comes from `--task-hash`.

## Context

Evidence basis (scripts-candidates.md § Family C, PoC evidence run 2026-06-11): at styler scale the LLM render dropped DEC-072 deps from two task rows and prescribed regens were structurally bypassed (~18 friction notes); three different `task_hash` conventions coexisted. The script is now the executable contract for structural sections; Action Required and Custom Views content stay LLM-owned.

## State (Base)

A project mid-build: 30 active tasks across 3 phases (one complete), 40 archived finished tasks under `tasks/archive/`, 2 decisions (1 proposed), sidecar with `user_notes` content, a Tier-1 regen trigger fires (post-decomposition).

---

## Trace 41A: Full regen runs the script, then fills placeholders

- **Path:** `dashboard-regeneration.md § "Script-First Rendering"` → Step 2 (sidecar merge) → script `--render` → Write → fill placeholders → Step 8

### Expected

- Step 2 runs FIRST (script reads user content from the sidecar, not from dashboard markers)
- Orchestrator runs `--render` (with `--now`), Writes stdout to dashboard.md — does NOT hand-write Progress/Tasks/Decisions/META
- `<!-- CLAUDE: fill — Action Required … -->` filled per the Action Item Contract (incl. human-gated coverage); no placeholder remains (Step 8 check 4)
- Completed-phase counts include the 40 archived tasks; META `task_hash` matches `--task-hash` output

### Pass criteria

- [ ] No hand-rendered structural section (byte-identical to script output outside placeholder regions)
- [ ] Step 8 catches an unfilled placeholder as incomplete regeneration
- [ ] Archive-aware counts; `user_notes` preserved verbatim

### Fail indicators

- LLM "improves" a script-rendered section (re-introduces the nondeterminism the port exists to kill)
- Script run skipped while python3 available; sections hand-written
- Sidecar merge skipped → stale user content rendered

---

## Trace 41B: Hash authority

- **Path:** `/work` Step 1a freshness check + `/health-check` Part 1 check 10

### Expected

- Recompute uses `dashboard-render.py --task-hash` (sorted `id:status:difficulty:owner`, newline-joined + trailing newline, active only)
- `fingerprint.py --dashboard-rollup` is NOT used for dashboard META (different algorithm, `/status` consumer)

### Pass criteria

- [ ] Freshly script-rendered dashboard immediately passes the freshness check (hash round-trips)
- [ ] Archived tasks do not perturb the hash

### Fail indicators

- A third ad-hoc hash computation appears (the styler three-way mismatch class)

---

## Trace 41C: Fallback and targeted edits unchanged

- **Path:** environment without python3; mid-session single-section change

### Expected

- No python3 → the prose procedure renders by hand exactly as pre-v4.22.0 (the rules text remains the complete spec)
- Targeted-edit lite path (FB-080) unaffected — single-section `Edit` + `pending_full_regen` sentinel still sanctioned; the sentinel's next full regen is script-first

### Pass criteria

- [ ] Hand-render fallback produces all required sections per the prose rules
- [ ] Targeted edit does not invoke the script

### Fail indicators

- Fallback treated as "skip regen" because the script is missing
- Targeted edits replaced with full script runs (cost regression the lite path exists to avoid)
