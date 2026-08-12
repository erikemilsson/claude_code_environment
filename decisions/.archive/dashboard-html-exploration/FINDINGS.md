# Dashboard render-target exploration — HTML vs Markdown

**Date:** 2026-06-23 · **Status:** exploration (pre-decision) · **Trigger:** user question — "can HTML improve how the dashboard displays?"

## The reframe (most important finding)

The dashboard is **not hand-authored** — `.claude/scripts/dashboard-render.py --render` already parses task JSON + the `dashboard-state.json` sidecar and *emits* the Markdown. **Markdown is just the current render target.** So the question is not "rewrite the dashboard in HTML," it's **"what is the right render target, and should there be more than one?"** The data→presentation split already exists; we'd be adding a presentation, not re-architecting.

## What the bloat actually is (and isn't)

The user's "bloated, mostly comments" complaint is about reading the **raw `.md` source** (the 15-line `<!-- DASHBOARD META -->` block, `<!-- USER SECTION -->` / `<!-- FEEDBACK:id -->` / `<!-- SECTION TOGGLES -->` markers). When *rendered* by a Markdown viewer those vanish — so part of the felt problem is that the source doubles as the read surface.

The pain that survives rendering is **scale-dependent**, and it is real:

| Project | Lines | Tasks | Decisions | Markdown verdict |
|---|---|---|---|---|
| styler | 640 | 269 | 141 | breaks down (see below) |
| SIREN_new | 330 | 59 | 10 | strained |
| flirty-gym | 209 | 39 | 8 | fine |
| tinder-streamliner | 199 | 47 | 3 | fine |
| 7 others | 120–186 | small | 0–1 | fine |

**Markdown is fine up to ~150 lines / <20 decisions. It breaks at styler scale.** Any solution should be **scale-aware**, not a forced switch for every project.

## The hard case: styler (the proof)

Rendered as Markdown (GitHub/VS Code preview), styler's dashboard is **28,232 px tall**; the decisions table starts **11,155 px** down — that's the *human-scroll* cost, and it's a legitimate HTML win. (Note the inverse on the *machine* axis — see "raw-input size" below: the rendered HTML browser tree is smaller, but the **raw HTML file Claude reads is 2.5× larger** than the Markdown.) Three structural failures, all visible in the screenshots:

1. **141-decision table = "table hell."** No search, no filter, no collapse. Each "Selected" cell is 50–400 chars; `before-3-longrow.png` shows **one** decision (DEC-078) whose rationale cell fills the entire viewport. Finding DEC-120 means scrolling past ~120 rows.
2. **53 phase headers**, ~50 of them just `✅ N tasks finished`, scrolled one after another.
3. **Notes wall** — retired features, deferred items, follow-ups as one prose block.

## What I built

A Python builder (`build.py`, stdlib only) that reads styler's real `dashboard.md` and emits **two** targets from the **same** data — proving the difference is presentation, not content:

- `before.html` — the `.md` via marked.js + github-markdown-css (status-quo "rendered Markdown")
- `dashboard.html` — an HTML "project console": sticky masthead with live metric chips, a 99% progress bar, sticky section nav, color-coded status stat-cards, **active phases shown with progress bars while the 50 completed phases collapse into one disclosure**, task cards with status/owner/difficulty badges, and the headline: **the 141 decisions as a searchable + status-filterable list of collapsed rows** (type "contrast" → 141 filters to 2 instantly; click to reveal the full rationale). Responsive to 390 px.

Aesthetic: warm-paper editorial console, Fraunces + IBM Plex Sans/Mono, single teal accent + disciplined semantic status colors. Self-contained single file (fonts via CDN).

Screenshots: `dash-1-top`, `dash-2-progress`, `dash-3-decisions`, `dash-4-filter`, `dash-5-mobile`; `before-1-top`, `before-2-decisions`, `before-3-longrow`.

## Verdict

- **HTML wins decisively** on findability, at-a-glance status, scannability, and density **at scale** (collapse + search + filter are things Markdown structurally cannot do).
- **Markdown wins / HTML costs** on (verified against the raw files, not the screenshots):
  - **Raw-input size:** Markdown **64KB** vs generated HTML **162KB — 2.5× heavier** for every Claude re-read (`/work`, audits, drift), for the same data, plus `<details data-search=…>` wrapper tax around each datum. Claude reads the *raw file*, not the rendered tree — so HTML is the *fatter* LLM input, inverting the template's "prefer targeted reads" discipline.
  - **Git diffs:** the emitted `dashboard.html` packs all 141 decisions onto **one 108,578-char line** — any one-word edit diffs the whole line. (Gitignoring the derived HTML moots this.)
  - **Machine markers dropped:** the HTML projection contains **zero** of META / `USER SECTION` / `SECTION TOGGLES` / `task_hash` / `spec_fingerprint` — i.e. it can't be the source of truth; it throws away the state the sidecar/drift system reads back.
  - Plus: drift section-hash instability (cosmetic CSS change mutates the hash), terminal/`git show` unreadability, CDN-font dependency, second-emitter maintenance.
- The win **does not** matter for the 8 small downstream projects; it matters a lot for styler, and styler is where the user actually lives.

## Recommendation — Option B (dual render target, scale-aware)

Keep `dashboard.md` exactly as the authoritative Claude/git surface. **Add** an HTML render target (`dashboard-render.py --html` → a gitignored `dashboard.html`) that the human opens in a browser, auto-emitted only above a size threshold (e.g. >40 tasks or >25 decisions). Additive, reversible, preserves every invariant (single `.md`, markers, drift hashing, Claude-readability). The human gets the console; Claude and git keep the Markdown. *Independent evaluator concurred with B over A/C/D.*

**Conditions for a real build (from the independent eval):**
1. The HTML emitter must read **task JSON directly** (like `dashboard-render.py`), NOT regex-scrape the rendered Markdown the way this prototype's `build.py` does — today it's a renderer-of-a-renderer, structurally behind the real pipeline.
2. **Gitignore** the HTML output — it's a derived artifact; tracking it is what creates the 108K-char-line diff problem.
3. Build it **only if** large (styler-scale) projects are common enough to justify a second, separately-maintained emitter + its tests.

Rejected: **(A) replace `.md` with HTML** — loses Claude-readability, git diffs, marker system (the prototype literally drops all markers). **(C) HTML-primary, MD demoted** — leaves the styler-scale findability problem unsolved on the human side while breaking the "Claude reads the dashboard" assumption.

## Strongest argument against (steelman, sharpened by the independent eval)

**It optimizes the wrong reader.** The dashboard's highest-frequency, highest-stakes consumer is not the human glancing a few times a day — it's **Claude**, re-reading the raw file on every `/work` step, audit, and drift check. On the actual artifacts the HTML is **2.5× larger raw input (162KB vs 64KB)**, wraps every datum in markup, **strips 100% of the machine-markers** the state system reads back, and serializes 141 decisions onto one 108,578-char line. Adopting HTML as anything Claude reads trades the format that is LLM-native, git-native, terminal-native, dependency-free and marker-bearing for a browser-only artifact that is heavier and dumber on every axis the *primary* consumer cares about — to buy polish that materially helps only the minority of projects large enough to need search-and-collapse. This is precisely why, if adopted, HTML must be a **derived view (Option B), never the source of truth**. The cheaper rival to beat: just improve the Markdown (`<details>` around completed phases + a linked `decisions.md`), keeping one plain-text surface.

## UPDATE 2026-06-23 — user redirect (supersedes the Option-B framing above)

The user corrected three premises the analysis above was built on:

1. **Read-only is not a limitation — it's what the dashboard IS for them.** They read it for overview/understanding, then act via CLI conversation with Claude. They don't hand-edit the `.md`. → The entire interaction-boundary objection (the spine of the shakedown) **doesn't bind their workflow.** It's real, but academic for how they use it.
2. **Much of the current content is bloat — including the decisions.** So my "searchable decisions browser" recommendation was **wrong**: the win isn't making 141 decisions findable, it's *not showing them*. The dashboard should be curated to the overview, not an exhaustive dump.
3. **One file, not two.** Kills the dual-target (Option B) and the decisions-slice. And since read-only is fine + they want visualizations Markdown can't render → **the single file becomes HTML** (≈ a curated Option C), generated from task JSON + sidecar like the `.md` is today.

**Revised direction: a single, read-only, visualization-forward, curated HTML dashboard.** State of record stays in task JSON (Claude reads *that*, not the dashboard); a tiny machine-readable header carries the freshness hash; the sidecar holds user notes. No integrity loss.

**v2 prototype (`viz.py` → `dashboard-v2.html`, screenshots `v2-1-top` / `v2-2-polished`):**
- **23 KB** — *smaller than the 64 KB Markdown* (and 1/7th of v1's 161 KB) because it shows less. This dissolves the "Claude reads a 2.5× heavier file" objection too.
- Three visualizations Markdown structurally can't render: a **completion ring**, a **status donut**, and a **53-phase heatmap grid** (one glanceable block replacing the 53-row table + 53 repeated headers). All inline SVG, no libs.
- Curated: decisions demoted to a `125 decided / 16 superseded` stat-bar + "ask Claude to surface any DEC"; full task list not dumped; the 3 active phases expanded; a "Needs you" panel; recent-activity sparkline.
- Whole project ≈ 1.5 viewports vs the Markdown's 28,232 px.

**Iteration 2 (user feedback folded in):** confirmed "I wouldn't even need the Markdown once I have this." Cuts: dropped the explanatory note + bare sparkline. Recent now carries task descriptions. Decisions → fully collapsed-by-default disclosure, openable into a searchable/expandable list (on-hand, zero space until opened). Generator generalized to any project (`viz.py <src> <out>`); rendered a mid-flight project (the renovation example) to exercise the **dependency/critical-path graph** (mermaid.js, themed — task rectangles + decision diamond + gate hexagon + owner emojis + status colors) and the **timeline** (overdue row struck through). Screenshots: `v2-renovation-flow`, `v2-styler-bottom`, `v2-styler-decisions-open`.

**Known polish items (prototype):** (a) Recent leaves a redundant "— Finished:" prefix; (b) the flow graph is degenerate for near-done projects (styler's 4 disconnected nodes) → auto-hide below an edge-count threshold; (c) the renovation "Needs you" is empty because that project formats action items as a table, not `- **T**` bullets → parser needs both; (d) **file size**: embedding all 141 decision rationales for inline search makes styler's file 133 KB — the real version should **link to decision records** (or lazy-load) instead of embedding, keeping it ~25 KB. None are structural.

**Iteration 3 (user idea — fold the spec into the dashboard):** added a collapsible **Specification browser** — the project's `spec_v{N}.md` split into its `## ` sections, each a collapsed `<details>` lazy-rendered to HTML by marked.js on expand, with a section filter. Demoed on styler's **884K-char / 59-section** spec (`viz.py <real styler dashboard path> dashboard-v2-styler-spec.html`; screenshot `v2-spec-browser`). Realizes the "one read surface" goal: project state + spec, all in one rendered HTML page you can browse while Claude works. Also fixed the redundant "— Finished:" prefix in Recent.

**File-size note (important for the real build):** embedding the full spec makes the demo file **~1 MB**. The real version should **lazy-LOAD** sections on expand from the spec file (the template already emits `spec_v{N}.index.json` with per-section line ranges — fetch + render on demand) rather than embedding all 884K. Same for decisions (link to records vs embed). Then the dashboard stays light and the spec/decision files remain the single source.

**User verdict so far:** "wouldn't even need the Markdown once I have this." Design validated; flow-graph deprioritized (low value for his repos); spec browser is the keystone feature. Likely ready to formalize (`/research` → DEC).

**Still unbuilt viz (offered):** click-a-phase-to-expand its tasks; a burn-up / progress-over-time chart.

**Formalization path if the direction holds:** template change → `/research` → DEC. Scope: `dashboard-render.py` emits HTML instead of (or alongside, then replacing) Markdown; freshness header + sidecar contract; `rules/dashboard.md` + `dashboard-regeneration.md` rewritten; drift detection no longer hashes the dashboard (it hashes the spec, unaffected); decide tracked-vs-gitignored. Also fixes the live mermaid-render bug (OEMMatInsightBI FB-007) by dropping broken Markdown-mermaid for real SVG.

## Open questions / next steps

1. **Decide scope** (B vs "improve the Markdown" vs HTML-primary) — user's call.
2. If pursuing: this is a template architectural change → route through `/research` → DEC (touches `dashboard-render.py`, `rules/dashboard.md`, `dashboard-regeneration.md`, `.gitignore`, drift interactions).
3. **`/shakedown` fit:** stress the chosen design against the real downstream corpus (styler's blocked phases, parallel/cross-phase tasks, retired-feature markers, audit-digest section, phase gates) before building — capture the edge cases the prototype hasn't met yet.
4. Prototype gaps not yet handled: Mermaid project-overview diagram, audit-digest section, phase-gate checkboxes, out-of-spec ⚠️ tasks, the section-toggle mechanism.
