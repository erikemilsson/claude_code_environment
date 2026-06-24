---
id: DEC-024
title: HTML dashboard render target — single read-only generated HTML, replacing Markdown dashboard.md
status: implemented
category: architecture
created: 2026-06-24
decided: 2026-06-24
implemented: 2026-06-24
related:
  tasks: []
  decisions: [DEC-004, DEC-016, DEC-021, DEC-022]
  feedback: [FB-096]
implementation_anchors:
  - ".claude/scripts/dashboard-render.py — render_full_html() + inline-SVG charts/heatmap + hand-rolled layered-DAG graph (render_svg_graph) + _html_acceptance; --html CLI mode; MD renderers + --render/--tasks-section deleted (v5.0.0)"
  - ".claude/scripts/tests/test_dashboard_render_html.py — 24 HTML invariants (determinism, META-in-head, placeholders, SVG charts, adaptive graph, acceptance surface, no file://-breakers); test_dashboard_render.py rewritten to 24 data-layer tests; full suite 76 green"
  - ".claude/rules/dashboard.md — read-only HTML single page, full-regen-only, sidecar sole source, SVG/heatmap scaling"
  - ".claude/support/reference/dashboard-regeneration.md — § Script-First Rendering — HTML target; Steps 2–8 reframed; Dependency Graph (SVG) replaces Mermaid; Targeted-Edits path removed"
  - ".claude/CLAUDE.md — Navigation (dashboard.html + sidecar); DEC-022 invariant wording"
  - ".claude/commands/{work,status,health-check}.md — META read from <head>; HTML-integrity/byte-size/offline checks; sidecar single-source"
  - ".claude/agents/{implement,verify}-agent.md — read dashboard.html for orientation only"
  - ".claude/support/reference/{phase-decision-gates,workflow}.md — gate approval via CLI + sidecar phase_gates"
  - ".gitignore — .claude/dashboard.html ignored; git rm .claude/dashboard.md; .claude/version.json → 5.0.0"
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# HTML dashboard render target — single read-only generated HTML, replacing Markdown dashboard.md

## Select an Option

Mark your selection by checking one box:

- [x] Option A — **Self-contained embed.** *(SELECTED 2026-06-24.)* One offline, `file://`-openable HTML file with everything inline; charts + dependency graph rendered **Python-side as inline SVG** (zero runtime CDN deps); gitignored + regenerated. Build scope: **spec linked-out (not embedded), hand-rolled SVG graph in v1, Markdown hard-retired.**
- [ ] Option B — **Served + lazy-load.** Light HTML shell that lazy-fetches spec/decision sections; requires a local server. **Disqualified** — `file://` cannot `fetch()` siblings, so it breaks the settled "open by double-click" requirement.
- [ ] Option C — **Hybrid (embed + lazy-render).** Section text embedded, parsed to HTML only on expand (the current prototype). Offline-safe but pays ~1 MB + duplication for in-file search the user explicitly rejected. (Becomes correct *only* if you reverse the "curate, don't dump" redirect — see Recommendation § flip condition.)

*Check one box, then complete the Decision section. (Research-agent populated evidence; the selection is yours — `/research` authority boundary.)*

---

## Background

**The dashboard is a render target, not a hand-written doc.** `.claude/scripts/dashboard-render.py` (the Family-C script; 54 tests) parses task JSON + the `dashboard-state.json` sidecar and emits `.claude/dashboard.md`. Markdown is just the current target.

**The problem.** As a *read* surface, Markdown breaks down at scale — styler: 640 lines / 28,232 px tall; a 141-row "table hell" decisions section; 53 repeated phase headers — and the user uses the dashboard purely for overview, then acts via the CLI.

**What was explored (2026-06-23/24).** A multi-iteration prototype (`.claude/support/workspace/dashboard-html-exploration/`) built and visually tested an HTML alternative against the 11 real downstream projects, with an independent adversarial evaluation and a `/shakedown` of the design. The user validated the direction ("I wouldn't even need the Markdown once I have this").

**Why a decision record.** Template architectural change with real cost-of-reversal: rewrites the render pipeline (`dashboard-render.py`), `rules/dashboard.md`, `support/reference/dashboard-regeneration.md`, and migrates 11 downstream projects. The *direction* is settled; this DEC scopes the **how**. Full evidence: `.claude/support/workspace/dashboard-html-exploration/{RESEARCH-BRIEF,FINDINGS}.md`; research archive `decisions/.archive/decision-024-research-2026-06-24.md`; auto-memory `project_dashboard_html_redesign`.

## What is settled (NOT under research — user-validated via prototype)

- The human dashboard becomes a **single, read-only, visualization-forward HTML page**, generated from the same source data (task JSON + sidecar). The user reads it for overview and acts via CLI; the interaction features the regeneration spec assumes the user edits in-place (phase-gate checkboxes, inline feedback, section toggles, audit promote/dismiss) **do not bind this user's workflow** — read-only loses nothing.
- **Content is curated, not dumped:** pulse (ring + donut + counts) · 53-phase **heatmap** · active-front · "Needs you" · Recent-with-descriptions · **decisions collapsed → demoted to a stat** · an **adaptive** graph + timeline (only when meaningful) · a collapsible **Specification browser**.
- **State of record stays in task JSON** (Claude reads *that*). **Drift detection is unaffected** (hashes the spec, not the dashboard — confirmed against `drift-reconciliation.md`). **Single `spec_v{N}.md` invariant preserved.**

## Open sub-decisions — resolutions (research-agent)

1. **Asset-loading / `file://` crux → EMBED everything (Option A).** Authoritative (MDN; WHATWG html#8121; CVE-2019-11730): `fetch()` of siblings *and* ES-module CDN imports both fail from a `file://` page (opaque origin). Classic `<script src=CDN>` loads online but not offline. Only design that is single-file + offline + double-click-openable: **zero runtime network deps, everything inline, all rendering Python-side at generation time.** Gates #2/#3/#6.
2. **Markdown→HTML → Python-side, hand-rolled (no JS lib).** stdlib has no markdown renderer; the curated overview needs almost none (the prototype's `mdi()` = 3 regexes); a spec browser needs a ~120–180-line stdlib converter. Reject CDN/bundled marked.js (offline/`file://` or vendored-version liability).
3. **Dependency graph → drop initially; hand-rolled stdlib SVG as a fast-follow.** *(moderate confidence)* mermaid is out (ESM `file://`-broken = the FB-007 root). User deprioritized the graph. **Shipping without it fixes FB-007 by removing broken mermaid entirely.** Re-add later via a layered-DAG→SVG over the script's existing `build_graph`/`longest_path` topology.
4. **Tracked vs gitignored → GITIGNORE.** Derived artifact, regenerated each `/work`; gitignoring moots the 108K-char-line diff + drift-hash-instability objections. *(Correction: `dashboard.md` is currently TRACKED — migration adds `.claude/dashboard.html` to `.gitignore` and `git rm --cached dashboard.md`.)*
5. **Freshness / machine-read → keep the `<!-- DASHBOARD META -->` comment block, relocated to `<head>`.** `/work` Step 1a, `/status`, `/health-check` string-parse `task_hash`/`template_version` from the comment — works byte-identically in HTML; only the filename they read flips `.md`→`.html`.
6. **`dashboard.md` disposition → retire as the rendered surface; keep `--render` (MD) as a maintained no-`python3` fallback mode** (emitted on demand, not by default). De-risks the documented fallback + migration at ~zero cost. (Hard-delete MD is a smaller optional follow-up.)
7. **Render pipeline → EXTEND `dashboard-render.py` with `--html`; do not write a new emitter; keep all 54 tests.** `--html` is a presentation layer over the existing data model (`load_tasks`/`build_phases`/…). The prototype's `viz.py` (regex-scrapes rendered MD) must NOT ship. Add a parallel `test_dashboard_render_html.py` (byte-identical re-render for fixed `--now`; META-in-head; no `<!-- CLAUDE: fill` left; SVG charts present; no `type="module"` script). The `<!-- CLAUDE: fill … -->` synthesis-placeholder protocol (Action Required, Custom Views) transfers verbatim.
8. **Scale-gating → one adaptive file everywhere; auto-hide/auto-collapse degenerate sections.** Ring/donut/heatmap/active-front/Needs-you/Recent at all sizes; auto-hide the graph below an edge threshold; decisions collapsed always (omit at 0–1). The **spec browser is the size-sensitive piece** — default **link-out** keeps every `dashboard.html` light (~25–60 KB) regardless of spec size (see Open Question 1).
9. **Migration → free, via the existing `template_version` format-staleness trigger.** Bumping the template version regenerates all 11 downstream dashboards to HTML on next `/work`, no per-project step. Ship `.gitignore` update; orchestrator stops writing `dashboard.md`.

## Options Comparison

Scoring: ✓✓ strong / ✓ adequate / ⚠ weak / ✗ fails. Weights reflect the user's stated priorities.

| Criteria | Wt | A — Embed | B — Served+lazy | C — Hybrid |
|----------|:--:|:--:|:--:|:--:|
| Offline / `file://` double-click open | ×5 | ✓✓ | ✗ **requires server** | ✓✓ |
| Runtime dependency footprint | ×4 | ✓✓ zero (Python-rendered) | ⚠ serve helper (+marked.js) | ✓/⚠ zero only if Python-side |
| File size / Claude-read cost | ×4 | ✓ ~25–60 KB; ✓✓ if spec linked | ✓✓ smallest shell | ⚠ ~1 MB w/ spec embed |
| Fixes FB-007 mermaid bug | ×3 | ✓✓ no mermaid at all | ✓ | ⚠ only if it drops mermaid too |
| Single-source integrity | ×3 | ✓ overview duplicates nothing | ✓✓ never duplicates | ⚠ embeds full spec/decision text |
| Implementation + maintenance | ×3 | ✓ one emitter, reuses data layer | ⚠ emitter **+ server command** | ⚠ emitter + vendored JS |
| Migration ease (11 downstream) | ×2 | ✓✓ `template_version` auto-regen | ✓ + learn `serve` | ✓✓ |
| **Overall** | | **▲ recommended** | **disqualified (row 1)** | **mid — superseded by user redirect** |

**The matrix is dominated by row 1.** B fails the single settled must-have. Between A and C, the user's redirect ("decisions are bloat; the win is *not showing them*") removes C's reason to embed full text. **A is "C with the embed scoped to the curated overview and the renderer moved to Python."**

## Option Details

### Option A — Self-contained embed  ▲ recommended
**Strengths:** satisfies every settled constraint at once (single file, read-only, offline, double-click); zero runtime deps (inline SVG charts already proven in the prototype; graph→pre-rendered/absent SVG **fixes FB-007**); lightest Claude-read surface (~25–60 KB, ≤ today's 64 KB MD → dissolves the "2.5× heavier" steelman); reuses the tested data layer.
**Weaknesses:** the dependency graph has no trivial stdlib path (→ drop initially per #3); a spec browser needs a hand-rolled md→HTML converter, and offline in-file spec browsing forces *embedding* (→ link-out by default, Open Q1).
**Research Notes:** see archive § "The crux" + "Repo-specific findings".

### Option B — Served + lazy-load  ✗ disqualified
**Strengths:** smallest shell; true single-source; lazy-load via `spec_v{N}.index.json` is elegant.
**Weaknesses (fatal):** `fetch()` from `file://` is blocked (MDN, authoritative) → needs a running server; a `dashboard serve` daemon collides with the "respect prior kills" rule + DEC-005 and is disproportionate for a glance-a-few-times-a-day overview. Keep documented as the escape hatch *if* a served dashboard ever becomes acceptable.
**Research Notes:** archive § "The crux, resolved".

### Option C — Hybrid (embed + lazy-render)  ⚠ superseded by user redirect
**Strengths:** offline + `file://`-safe (lazy *render*, not fetch); instant; it's the literal current prototype (works on double-click for markdown — not its mermaid).
**Weaknesses:** buys in-file searchable spec/decision text the user rejected as bloat (styler → ~1 MB); duplicates source-of-truth text; depends on inlined/CDN marked.js. A ⊃ C.
**Research Notes:** archive § "Option C".

## Recommendation

**Option A — Self-contained embed**, implemented as: extend `dashboard-render.py` with `--html` (reusing the data layer), all visualizations as **inline SVG generated in Python** (zero CDN deps), `<!-- DASHBOARD META -->` carried verbatim in `<head>`, **link out to** the spec (don't embed), **gitignored** + regenerated each `/work`, `--render` (MD) kept as the no-`python3` fallback, synthesis-placeholder protocol preserved.

**Why:** (1) the `file://` crux (×5) is binary and authoritative — only A/C survive, B is out; (2) the user's "curate, don't dump / one file" redirect eliminates C's reason to embed; (3) FB-007 is fixed for free by removing runtime mermaid; (4) lowest Claude-read cost + dependency footprint neutralizes the "optimizes the wrong reader" steelman. **Confidence: high** on the crux and A-vs-B; **moderate** on #3 (graph).

**Flip condition (important):** if you decide you DO want full in-file *searchable* spec/decision text that works offline, the answer becomes **C** (embed + inline renderer, ~1 MB files) — because lazy-fetch (B) is impossible under `file://`. *There is no lazy-load middle ground at `file://`: "browse the whole spec inside the dashboard, offline, by double-click" forces embedding.*

## Your Notes & Constraints

*This section is yours — Claude reads it but never overwrites it.*

**Constraints (captured from the exploration):**
- Dashboard is **read-only** for me; I act via the CLI. One file — no dual Markdown+HTML.
- Current content (incl. the decisions list) is largely **bloat**; curate to the overview.
- Want **HTML visualizations Markdown can't render**; the broken Markdown-mermaid is real pain.
- The spec folded into the dashboard (collapsible, rendered) is the keystone.

**Open questions from the research — RESOLVED 2026-06-24 (see Decision):**
1. **Spec browser → LINK-OUT** (keeps Option A; dashboard stays ~25–60 KB + single-source; browse spec via CLI / the spec file).
2. **Graph → HAND-ROLL the stdlib SVG graph in v1** (pure-Python layered-DAG → SVG over the script's existing topology; no mermaid).
3. **`dashboard.md` → HARD-RETIRE** (delete the Markdown render path entirely; HTML is the only surface).

## Decision

**Selected:** Option A — Self-contained embed (single read-only HTML, Python-rendered, zero runtime deps), with: spec **linked-out** (not embedded), a **hand-rolled stdlib SVG dependency graph in v1**, and **Markdown hard-retired**.

**Rationale:** The `file://` crux is decisive and authoritative — only an all-inline, build-time-rendered file is single-file + offline + double-click-openable, disqualifying B and (with the user's "curate, don't dump" redirect removing its reason to embed) superseding C. A fixes FB-007 for free by removing runtime mermaid, stays lighter than today's Markdown, and reuses the tested data layer. The three forks resolved toward the lightest single-source shape — link-out spec (no ~1 MB embed) — while keeping the graph in v1 (hand-rolled SVG, since mermaid is impossible offline) and fully retiring Markdown (HTML is the sole surface).

## Trade-offs

**Gaining:** a single, glanceable, offline, double-click-openable read surface; visualizations Markdown can't render (inline-SVG ring/donut/heatmap + a real dependency graph); FB-007 fixed (no runtime mermaid); a lighter file than today's Markdown; the spec reachable from the dashboard.

**Giving Up:** the Markdown dashboard as a terminal/`git show`-readable plaintext surface (hard-retired — agents/humans read `dashboard.html` or task JSON); the no-`python3` fallback (HTML requires the script); in-file *searchable* spec/decision text (link-out instead). New build surface: a hand-rolled md→inline-HTML pass + a stdlib DAG→SVG layout.

## Impact

**Implementation Notes (approved build):**
1. Extend `dashboard-render.py` with `--html` (default emit): reuse the data layer (`load_tasks`/`build_phases`/…) — do NOT scrape rendered MD; render the curated sections + inline-SVG charts (port the prototype's ring/donut/heatmap) + a **hand-rolled layered-DAG → SVG** dependency graph over `build_graph`/`longest_path`; carry the `<!-- DASHBOARD META -->` block in `<head>`; a ~120–180-line stdlib md→inline-HTML helper for Action-Required/Recent prose; spec **linked-out** (link to `spec_v{N}.md` / its section index, not embedded).
2. **Hard-retire Markdown:** remove the `--render` (MD) path + its 54 MD-renderer tests; replace with `test_dashboard_render_html.py` (byte-identical re-render for fixed `--now`; META-in-head; no `<!-- CLAUDE: fill` left; SVG charts present; no `type="module"` script).
3. Rewrite `rules/dashboard.md` + `dashboard-regeneration.md` for the HTML target (keep the `<!-- CLAUDE: fill … -->` synthesis-placeholder protocol).
4. `.gitignore` += `.claude/dashboard.html`; `git rm --cached .claude/dashboard.md`; flip freshness consumers' filename (`work.md` Step 1a, `status.md`, `health-check`) `.md`→`.html`; one-line agent-read-path note.
5. Bump `template_version` → 11 downstream dashboards auto-regen to HTML on next `/work`.

**Affected Areas:**
- `.claude/scripts/dashboard-render.py` (+ new HTML tests; 54 existing tests stay green), `.claude/rules/dashboard.md`, `.claude/support/reference/dashboard-regeneration.md`, `.claude/CLAUDE.md` (Navigation + Critical Invariants), `.gitignore` (add `dashboard.html`; un-track `dashboard.md`), the 11 downstream dashboards (auto-regen via `template_version`).
- **Correction (research):** `.claude/settings.json` `permissions.ask` has **no** dashboard guard today (only `spec_v*.md` / `decision-*.md` / `vision/**`) — **no settings.json change needed** for this ship. (The brief's "changes the permissions.ask guard on the dashboard" was inaccurate.)

**Risks:** the hand-rolled md→HTML / SVG paths are new surface (mitigated: link-out spec + drop graph initially keep v1 small); the no-`python3` path relies on the retained MD fallback.
