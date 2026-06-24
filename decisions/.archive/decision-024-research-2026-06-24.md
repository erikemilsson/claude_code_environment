# Research archive — DEC-024: HTML dashboard render target (2026-06-24)

Detailed findings behind `decisions/decision-024-html-dashboard-render-target.md`. Recommendation: **Option A (Self-contained embed)**; confidence high on the crux + A-vs-B, moderate on the graph sub-decision.

## Methodology

- Read the exploration substrate: `RESEARCH-BRIEF.md`, `FINDINGS.md` (incl. the independent adversarial eval + the user-redirect update), `shakedown-dashboard-console-2026-06-23.md`, and the prototype `viz.py` — all in `.claude/support/workspace/dashboard-html-exploration/`.
- Read the files the change touches: `.claude/scripts/dashboard-render.py` (full) + `test_dashboard_render.py`, `.claude/rules/dashboard.md`, `.claude/support/reference/dashboard-regeneration.md`, `.claude/support/reference/drift-reconciliation.md`, consumer read-sites (`commands/work.md`, `commands/status.md`, `agents/{implement,verify}-agent.md`), and `.claude/settings.json` / `.gitignore` / `version.json`.
- Web research (current-facts questions): `file://` fetch/CORS behavior, ES-module vs classic-script loading under `file://`, stdlib markdown rendering, pure-Python DAG→SVG layout, single-file HTML size ceilings, marked.js size/license.

## The crux, resolved (authoritative)

- **`fetch()`/XHR from `file://` fails.** MDN *Reason: CORS request not HTTP*: "CORS requests may only use the HTTP or HTTPS URL scheme… This often occurs if the URL specifies a local file, using the `file:///` scheme." Local files are **opaque origins** by default (Firefox + Chrome), per **CVE-2019-11730**. → Option B's lazy-fetch-from-siblings is impossible on a double-clicked file.
- **ES-module imports from `file://` fail.** WHATWG **html#8121** (open): module scripts are fetched with CORS; a `file://` page has null origin → blocked ("Cross origin requests are only supported for protocol schemes: http, data, chrome, …, https"). → the prototype's `import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/…esm.min.mjs"` **silently fails on double-click** — which is *also* the mechanism behind FB-007's broken graph.
- **Classic `<script src="CDN">` DOES load from `file://`** (no CORS gate) — but needs network, so not offline-safe; the prototype's classic `marked.min.js` is therefore online-only.
- **Net:** the only design that is simultaneously single-file, offline, and double-click-openable is **everything inline + all rendering at generation time (Python)** = Option A. C is offline-safe only because it embeds raw text and *renders* (not fetches) on expand — and only for markdown; its mermaid is still broken.

## Markdown→HTML in Python

- **No stdlib markdown renderer** (confirmed). Third-party (Python-Markdown, Mistune, Marko) all violate the scripts' stdlib-only invocation contract (`.claude/scripts/README.md`).
- The **curated overview** needs almost no markdown — the prototype's `mdi()` (escape + 3 regexes for links/bold/code) suffices for Action-Required/Recent text.
- A **spec browser** needs a ~120–180-line stdlib converter (headings/lists/tables/fenced-code/links/blockquote), adequate for spec prose. Alternative: inline marked.js (MIT, ~37 KB min / ~14 KB gz, pattern per markedjs#2961) works offline but adds a vendored, version-tracked JS blob — discouraged.

## Dependency graph → SVG without a runtime browser dep

- **mermaid.js: out** (ESM `file://`-broken; classic build needs network; it's the FB-007 root).
- **graphviz `dot`: not assumable** (no install guarantee; would need graceful-skip).
- **Pure-Python:** `grandalf` (Sugiyama hierarchical layout, ~600 lines, no GUI dep) or NetworkX `topological_generations`+`multipartite_layout` — both third-party. **Hand-roll preferred**: the script already computes the topology (`build_graph`, `longest_path`); a layered layout (x = depth, y = index-within-layer) emitting `<rect>`/`<line>`/`<text>` is small + stdlib-only. Given the user's deprioritization, **ship without the graph; FB-007 is fixed by mermaid's absence.**

## Single-file HTML size/perf

- No hard browser byte-limit; pathology starts in the hundreds of MB. Real cost is **DOM node count** + INP/LCP during traversal (Web Performance Calendar 2025; MDN HTML perf). A curated ~25–130 KB file is trivially fast; a ~1 MB spec-embed is loadable but builds a large DOM and is heavier for Claude to re-read → favors **curate + link-out-spec** (≈ the 23 KB v2 prototype) over embedding 884K of spec.

## Repo-specific findings (read directly)

- **`dashboard-render.py` already reads task JSON directly** and builds a structured model — `--html` reuses it; the prototype's regex-scrape-the-MD approach must not ship (independent-eval condition #1).
- **54 tests** in `test_dashboard_render.py` exercise the data layer + MD renderers — **none broken by adding `--html`.** Determinism = byte-identical re-render for fixed `--now`; mirror for HTML.
- **Synthesis-placeholder protocol** (`<!-- CLAUDE: fill … -->` for Action Required + Custom Views) is HTML-comment-based → transfers verbatim; the `dashboard-regeneration.md § Script-First Rendering` division-of-labor carries over.
- **Freshness consumers** (`work.md` Step 1a, `status.md`, `health-check`) string-parse the `<!-- DASHBOARD META -->` comment for `task_hash`/`template_version` → **works unchanged in HTML** (comments valid HTML); only the **filename** flips `.md`→`.html`.
- **`task_hash` split is pre-existing:** dashboard META uses `id:status:difficulty:owner` (`dashboard-render.py --task-hash`); `/status` uses `id:status` (`fingerprint.py --dashboard-rollup`). Unaffected.
- **Agents** reference the dashboard for orientation only — state of record is task JSON; orchestrator owns all writes (DEC-004). A one-line doc update ("read `dashboard.html` or task JSON") suffices. No structural break.
- **Drift detection hashes the spec, not the dashboard** (`drift-reconciliation.md` Step 1b; `fingerprint.py --spec`/`--sections`/`--index`) — **confirmed unaffected**. Single-`spec_v{N}.md` invariant untouched.
- **Git/settings state correction:** `.gitignore` ignores `dashboard-state.json` + `.spec-merge-queue.jsonl` but **NOT `dashboard.md`** (tracked). `permissions.ask` guards only `spec_v*.md` / `decision-*.md` / `vision/**` — **no dashboard guard exists.** So this ship **adds** `.claude/dashboard.html` to `.gitignore`, needs **no** `settings.json` change, and should `git rm --cached .claude/dashboard.md` on the MD-retirement disposition.

## Discarded / not carried forward

- **Dual render target** (FINDINGS' original "keep .md + add .html") — superseded by "one file, not two."
- **In-file searchable decisions browser** — superseded by "decisions are bloat; the win is not showing them."
- **The shakedown's interaction-boundary objection** (read-write control-surface "spine") — explicitly retired by the user ("read-only is what the dashboard IS for me"). Real but non-binding for this workflow.

## Sources

- [MDN — Reason: CORS request not HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS/Errors/CORSRequestNotHttp)
- [WHATWG html#8121 — module scripts under file://](https://github.com/whatwg/html/issues/8121)
- [johnskinnerportfolio.com — XHR blocked by CORS from local file](https://johnskinnerportfolio.com/blog/cors_from_local_file/)
- [Python-Markdown docs (no stdlib renderer)](https://python-markdown.github.io/reference/)
- [grandalf — pure-Python Sugiyama/DAG layout](https://github.com/bdcht/grandalf)
- [NetworkX — DAG topological layout](https://networkx.org/documentation/stable/auto_examples/graph/plot_dag_layout.html)
- [Web Performance Calendar 2025 — Exploring Large HTML Documents](https://calendar.perfplanet.com/2025/exploring-large-html-documents-on-the-web/)
- [markedjs discussion #2961 — offline/no-server use](https://github.com/markedjs/marked/discussions/2961)
- [Marked license (MIT)](https://marked.js.org/license)
