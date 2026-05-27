---
id: DEC-020
title: Conclude the DEC-007 Skills/reference duplication trial — retire which location, or re-charter
status: implemented
category: architecture
created: 2026-05-27
decided: 2026-05-27
related:
  tasks: []
  decisions: [DEC-007, DEC-004, DEC-017]
  feedback: [FB-094]
implementation_anchors:
  - ".claude/support/reference/decomposition.md (migrated the Test-Protocol Runtime Constraints section from the retired Skill — the only real drift)"
  - ".claude/skills/ deleted (3 SKILLs retired); 3 mirror comments removed from the reference docs"
  - ".claude/sync-manifest.json (dropped skills/*/SKILL.md); .claude/README.md (Skills section + Essential-Files + Where-to-Find rows removed)"
  - ".claude/rules/agents.md + .claude/support/reference/extension-hooks.md (ownership lists updated)"
  - ".claude/support/reference/task-schema.md + .claude/rules/dashboard.md (SKILL-path citations re-pointed to the reference docs)"
  - ".claude/commands/health-check.md (illustrative sync snippet de-skilled); .claude/version.json (4.12.0); .claude/dashboard.md (META bump)"
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Conclude the DEC-007 Skills/reference duplication trial — retire which location, or re-charter

## Select an Option

Mark your selection by checking one box:

- [x] Option A: Conclude — keep the reference docs, retire the 3 Skills
- [ ] Option B: Conclude — keep the 3 Skills, retire the reference docs
- [ ] Option C: Re-charter — reconcile drift now, add a concrete exit criterion + deadline + owner; keep both for now

*Check one box above, then fill in the Decision section below.*

---

## Context

DEC-007 (implemented 2026-04-17, Option B) adopted Claude Code Skills for on-demand reference content, creating three thin-wrapper Skills that **mirror** existing reference docs:

| Skill | Reference companion | Cited from (other files) |
|-------|---------------------|:--:|
| `.claude/skills/decomposition-heuristics/SKILL.md` | `.claude/support/reference/decomposition.md` | 3 |
| `.claude/skills/spec-checklist/SKILL.md` | `.claude/support/reference/spec-checklist.md` | 3 |
| `.claude/skills/dashboard-style/SKILL.md` | `.claude/support/reference/dashboard-regeneration.md` | 9 |

DEC-007 logged the duplication as a **known, deferred cost** (Option B weakness: *"Two copies of the content … unless one is removed — requires a sync decision"*). That sync decision was never made. Each file carries a `<!-- … Update both files in sync until one is retired -->` comment, and `.claude/README.md` tells users *"This duplication is temporary … one of the two locations will be retired once the Skill auto-invocation pattern is validated."*

**The problem this decision closes:** DEC-007 never defined what *"validated"* means, who decides, or a deadline. The trial has therefore run open-ended for ~40 days (2026-04-17 → 2026-05-27) with no mechanism to conclude. Observed costs:

- **Maintenance tax:** ≥5 ships edited both copies "per DEC-007 Option B" (template versions 3.2.0, 3.13.0, 3.16.0, 3.17.0, + the research-spike ship).
- **Drift (the sync discipline has already slipped)** — body-only diff, frontmatter + mirror-comment stripped:
  - `decomposition`: **52 lines only in SKILL, 11 only in ref** — materially diverged (two disagreeing sources of truth).
  - `dashboard`: 1 only in SKILL, 9 only in ref — modest.
  - `spec-checklist`: 1 / 1 — effectively in sync.
  - The drift cuts **both ways**, so there is no clean "delete one" — whichever location is kept needs the other's unique lines merged in first.

## Questions to Research

(Answers in `## Research Findings` below — populated by research-agent.)

1. **Has Skill auto-invocation demonstrated value?** How reliable is description-based auto-invocation in current Claude Code, and is there **any observability** (session logs, telemetry, a way to confirm a given SKILL.md actually loaded) that would let us judge whether these three Skills fire at the intended moments (`/work` decomposition, `/iterate`, dashboard regen)?
2. **What do current Claude Code docs say** about Skills vs. reference docs, the cost of auto-invocation (description-matching token overhead), and the skill content lifecycle? Cross-check against the repo's own `.claude/support/reference/claude-code-authoring.md` (DEC-017) — skill listing 1,536-char cap, auto-compaction 25K re-attachment budget, forked-skill context inheritance.
3. **Given the absence of usage telemetry,** what is the strongest evidentiary basis to choose A vs. B vs. C? Separate *safety/reversibility* confidence from *value* confidence.
4. **Reversibility + ripple cost** of each direction (re-pointing 15 citations for B; deleting `.claude/skills/` for A; drift reconciliation required by all three).

## Option Details

### Option A — Conclude: keep reference docs, retire the 3 Skills

Backport the unique drifted lines into the reference docs, delete `.claude/skills/`, update `.claude/README.md` (Skills section + the duplication note), `/health-check` (drops the skills-sync expectation), and `sync-manifest.json` (remove the 3 `SKILL.md` glob members).

- **For:** Lowest ripple — the 15 citations already point at the reference docs, so nothing re-points. Restores a single source of truth. DEC-007 itself called the on-demand benefit *"small"* and the reversal *"easy (delete `.claude/skills/`, content still lives in `support/reference/`)."* Matches "don't keep a second content location without demonstrated value."
- **Against:** Abandons the documented platform feature (on-demand context loading) that was DEC-007's whole rationale. If the Skills *are* auto-firing usefully, this is a regression.

### Option B — Conclude: keep Skills, retire the reference docs

Backport the lagging lines into the SKILL files, re-point all 15 citations (notably 9 for `dashboard-regeneration.md`) to the SKILL paths, drop the 3 reference docs, update the note + `sync-manifest.json`.

- **For:** Keeps the platform feature and the context-budget benefit. Matches the **practice signal** — maintainers edit the SKILL (the decomposition SKILL leads its ref by 52 lines), so the Skills are the de-facto primary.
- **Against:** Highest ripple (15 citation re-points). Can a cited Skill be referenced by path the same way a reference doc is? (Research Q.) Larger blast radius if a re-point is missed.

### Option C — Re-charter the trial

Reconcile the drift now (stops the active latent-bug), then add a concrete exit criterion + deadline + owner (to DEC-007 or here), and correct the README note. Keep both files for now so the A-vs-B call can be made later on real usage evidence.

- **For:** Stops the active harm (drift) immediately without an evidence-free irreversible direction call. Fits an evidence-first posture — gather the auto-invocation usage data the trial never specified.
- **Against:** The double-edit tax continues (now bounded by a deadline). Re-chartered open-ended trials risk re-stalling. ("Just fix the README note" is a strict subset of C without the criterion — dominated, not listed separately.)

## Options Comparison

| Criterion | **Option A** — keep refs, retire Skills | **Option B** — keep Skills, retire refs | **Option C** — re-charter (keep both) |
|---|---|---|---|
| **Context-discipline value** | Forgoes on-demand loading; but the cited content already loads on-demand via path-Read (not always-on), so the *practical* loss is the auto-fire-when-undirected case only | Preserves the documented on-demand/description-match property — the one genuine platform-feature upside | Preserves it for now; defers the keep/drop call |
| **Ripple / citation cost** | **Lowest** — 0 citations re-point (all real deps already point at ref paths); delete `.claude/skills/`, edit README + sync-manifest | **Highest** — rewrite ~9 dashboard + ~3 others = ~12–15 path citations to SKILL paths; re-key the Part 5 post-sync dashboard check; larger miss-a-reference blast radius | **Lowest now** — no structural change; only the README note correction + drift merge |
| **Reversibility** | **High** (DEC-007's own assessment: "easy — content still lives in support/reference"); re-adding thin Skills later is cheap | **Moderate** — undoing means re-extracting 3 refs + re-pointing 15 citations back | **Highest** (nothing structural changed) — but defers, not resolves |
| **Drift-reconciliation burden** | Must merge unique SKILL lines (incl. the 52-line decomposition delta) into refs **before** deleting Skills — one-time, unavoidable | Must merge unique ref lines into SKILLs before deleting refs — symmetric, same one-time cost | Must reconcile **now** to stop the active two-sources-of-truth bug; then the double-edit tax *continues* for the deadline window |
| **Evidence strength — VALUE** | N/A to keep refs (their value is *observed* via resolving citations). Removing Skills forgoes an upside that is **unmeasured & currently unmeasurable in-session** | **Weak/unproven** — bets the kept location on auto-fire, which is documented-unreliable (#43287) and invisible without OTel; "edits land in SKILL" is a maintenance signal, not a runtime-value signal | **Deferred** — value only becomes evidenceable **if** the re-charter mandates OTel `skill_activated`/`invocation_trigger` capture; a vague "gather evidence" re-charter cannot produce it (in-session UI is aggregate-only, #35319) |
| **Evidence strength — SAFETY** | **High** — reversal pre-judged easy by DEC-007; zero citation churn; failure mode (lose a small unproven benefit) is mild & reversible | **Moderate** — mechanically sound (path-cite works) but largest churn + bets on the weakest-evidence mechanism | **High** — changing nothing structural is the safest *act*; risk is process (re-stall) not correctness |

## Research Findings

### Q1 — Auto-invocation reliability + observability

**Reliability: documented as imperfect**; the docs treat "the model didn't fire the skill" as an expected failure mode. The Skills troubleshooting section: *"If a skill seems to stop influencing behavior after the first response, the content is usually still present and the model is choosing other tools or approaches"* ([skills](https://code.claude.com/docs/en/skills)). The debug page lists the symptom verbatim: *"Skill appears in `/skills` but Claude never invokes it → … its description doesn't match how you phrase the request"* ([debug-your-config](https://code.claude.com/docs/en/debug-your-config)). Still-OPEN bug #43287 (closed only as a duplicate, Apr 2026) describes the model performing a skill's steps manually instead of auto-invoking ([#43287](https://github.com/anthropics/claude-code/issues/43287)). Net: auto-invoke is real but not guaranteed; docs prescribe `hooks` for must-happen behavior.

**Observability — load-bearing, two-tier:**

- **In-session, no external tooling: presence YES, auto-fire NO.** `/context` breaks the window into categories incl. **skills**; `/skills` lists available skills ([debug-your-config](https://code.claude.com/docs/en/debug-your-config)). Invoked SKILL.md "enters the conversation as a single message and stays there for the rest of the session" ([skills](https://code.claude.com/docs/en/skills)), so a post-trigger `/context` can show the body is now resident. BUT per-session metadata tracks only an aggregate `"Skill": N` tool count, not *which* skill — the explicit problem of OPEN issue #35319: *"session metadata tracks `"Skill": 3` … but not which skill was invoked … there is no way to know which skills are actually being used"* ([#35319](https://github.com/anthropics/claude-code/issues/35319)). `/doctor` validates config + budget, not firing. A constructible probe (a skill body logging `${CLAUDE_SESSION_ID}`) is intrusive and still can't capture should-have-fired-but-didn't.
- **With opt-in OpenTelemetry + an external backend: per-skill auto-fire IS precisely observable.** Claude Code emits `claude_code.skill_activated` *"when a skill is invoked, whether Claude calls it through the Skill tool or you run it as a `/` command,"* carrying `skill.name`, `skill.source`, and crucially **`invocation_trigger`: `"user-slash"` | `"claude-proactive"` | `"nested-skill"`** ([monitoring-usage](https://code.claude.com/docs/en/monitoring-usage)). `"claude-proactive"` is exactly the auto-invoke signal the DEC-007 trial needed. Caveats: requires `CLAUDE_CODE_ENABLE_TELEMETRY=1` + an OTLP endpoint, and user-defined skill names are redacted to `"custom_skill"` unless `OTEL_LOG_TOOL_DETAILS=1`.

**Bottom line:** the auto-invoke value question is empirically answerable, but only by standing up OTel infrastructure and running instrumented real sessions — NOT from the in-session UI, and not from anything in this repo today. Absent that, decide on principle.

### Q2 — Current-docs cross-check vs. the repo's `claude-code-authoring.md`

(Footer "Last verified … @ 2026-05-24; against template_version: 4.9.0.") Contradictions/staleness:
1. **Skill-listing cap is now dynamic, not a flat 1,536 chars — FLAG.** Repo doc states a hard "1,536-char cap on `description + when_to_use`." Live: the total listing budget "scales at 1% of the model's context window" (`skillListingBudgetFraction` / `SLASH_COMMAND_TOOL_CHAR_BUDGET`), least-used dropped first; 1,536 is now the PER-ENTRY cap (`maxSkillDescriptionChars`). The repo doc conflates the two ([skills](https://code.claude.com/docs/en/skills)).
2. **`/doctor` now surfaces budget overflow** — additive fact the repo doc lacks.
3. **`/context` + `/skills` presence-inspection** — absent from the repo doc; directly relevant to any "did the Skill load?" question.
4. **Confirmed-consistent:** turn-scoped `model:`/`effort:`; 25K re-attachment budget + first-5,000-tokens-each (live adds most-recent-first fill order); one-message-and-stays lifecycle; `context: fork` inheritance; `disable-model-invocation` (live adds it "removes the skill from Claude's context entirely" + blocks subagent preload).

(These authoring-doc fixes are out of scope for the A/B/C choice — a clean `/health-check` Part 2d `[V]` item.)

### Q3 — Evidentiary basis for A vs B vs C (value vs safety held separate)

Most decision-relevant codebase fact: **the orchestrator never explicitly invokes these three skills — it cites the reference-doc *paths*.** `work.md` ("Read `.claude/support/reference/decomposition.md`"), `iterate.md` ("See `.claude/support/reference/spec-checklist.md`"), and the dashboard pipeline (cites `dashboard-regeneration.md` 9× by path). No skill-tool invocation or auto-invoke trigger appears in `work.md`/`iterate.md`. So the three Skills earn their keep **only** through description-based auto-fire — the mechanism that is (a) documented-unreliable and (b) unobservable without OTel. The reference docs are load-bearing through explicit citations that already work.

- **Value confidence is LOW for B / unmeasured for the Skills generally.** No telemetry in this repo; the only "Skills are primary" signal is that maintainers edited the decomposition SKILL until it leads its ref by 52 lines — a *maintenance-attention* signal, not a *runtime-value* one. Strongest evidence-based statement: the reference docs have observed value (citations resolve); the Skills' incremental value over the docs has not been demonstrated and cannot be from current data.
- **Safety/reversibility:** A high, C high-as-an-act, B moderate. DEC-007 pre-judged the Skills reversal "easy" and the benefit "small."
- **Maintainer posture** (auto-memory "pressure-test value before adopting"; DEC-018 precedent): when value cannot be evidenced and the feature carries an ongoing tax, don't pay the permanent cost — points away from B, toward A or C.

### Q4 — Ripple / reversibility cost

**Can a cited Skill be referenced by path like a reference doc? Yes — mechanically identical** (the docs confirm commands & SKILL.md "work the same way," supporting files referenced by relative path — [skills](https://code.claude.com/docs/en/skills)). The one mechanism difference: a SKILL.md also participates in the auto-invoke/description-budget system. So under **B**, every "Read `…/decomposition.md`" becomes "Read `…/decomposition-heuristics/SKILL.md`" — now both path-citing the body AND paying its description into the listing budget. Under **A**, the SKILL's auto-invoke role disappears and citations don't move.

Real (non-archive, non-illustrative) citation re-points if B: `dashboard-regeneration.md` ~9 (work.md ×4, audit-coherence ×3, audit-ui ×2, + breakdown, rules/dashboard, phase-decision-gates, workflow, extension-patterns, audit-fix-workflow); `decomposition.md` 1 (work.md:635); `spec-checklist.md` 2 (spec-workflow:52, iterate:415). `rules/dashboard.md:21` already names the SKILL path; `health-check.md:551` is an illustrative sync-output snippet, not a dependency. **A re-points none.**

Drift-reconciliation is unavoidable for all three (merge before any delete; C must reconcile now to stop the active two-sources bug): decomposition 52/11 = real semantic merge; dashboard 1/9 light; spec-checklist 1/1 trivial. Sync touch-points (whichever retired): `sync-manifest.json` lists `.claude/skills/*/SKILL.md` (L9) + the 3 ref companions (L24/27/32); `health-check.md` has no dedicated skills-sync check (skills ride the generic Part 5 glob), but B must re-key the Part 5 post-sync dashboard re-check (L610). `.claude/README.md` § Skills (L92–103) + rows L46/L232 need editing under A or B.

## Your Notes & Constraints

**Selected Option A (2026-05-27).** Decided on principle, per the research: Skill auto-invocation value is unobservable without opt-in OpenTelemetry (captured nowhere in this repo), the orchestrator path-cites the reference docs (proven value), and the evidence-first posture (DEC-018) argues against retiring the proven location for the unproven one. Zero *functional* references to the Skills existed — only 2 doc citations + ownership lists, all re-pointed. The one real content drift (the `Test-Protocol Runtime Constraints` section, SKILL-only since v4.5.0/FB-073) was migrated into `decomposition.md` before deletion. Implemented same session.

## Recommendation

*(Evidence only — no selection. Authority to choose remains with the maintainer.)*

**The evidence leans toward Option A, with Option C as the principled alternative *only if* the maintainer wants to make the call on real data and is willing to stand up OTel telemetry to get it.** Option B is the weakest fit for this repo's evidence-first posture — the only option that both bets on the unproven mechanism and pays the highest ripple.

- **Safety/reversibility:** A is the safest direction (high confidence) — zero citation re-points, and DEC-007 already judged reversal "easy." C is the safest *act* (changes nothing structural) but is process-risky (open-ended re-charters re-stall, as this one did). B carries the most churn and the largest miss-a-citation blast radius (moderate confidence).
- **Value:** This is where the decision turns. **The three Skills earn value only through description-based auto-invocation, which is (1) documented-as-unreliable and (2) NOT observable from the in-session UI** — per-session metadata is an aggregate `"Skill": N` count (#35319, OPEN), and `/context`/`/skills`/`/doctor` show presence/budget, not auto-fire. The companion reference docs deliver *observed* value through explicit path citations in `work.md`/`iterate.md`/the dashboard pipeline. So on the only evidence available, the *proven* value sits with the location Option B would delete, and the *unproven* value sits with the location Option B would keep.

**On the maintainer's "pressure-test value before adopting" rule (DEC-018 precedent):** applied here, it says don't retire the proven location (refs) for the unproven one (Skills) without value evidence — and that evidence can't come from current in-session tooling. **That favors A or C over B.** Between A and C: choose **A** if the position is "the on-demand benefit was called *small* and is unproven — stop paying the double-edit tax permanently"; choose **C** if the position is "I'm not ready to foreclose the platform feature and I *will* instrument OTel `skill_activated` capture to settle it" — in which case C must name that mechanism + a deadline + an owner, or it is dominated by A.

**The value question is answerable, but only with opt-in OpenTelemetry capturing `invocation_trigger: "claude-proactive"` across real `/work`/`/iterate`/dashboard-regen sessions.** It is NOT answerable from the in-session UI or anything in this repo today. If the maintainer does not want to stand up that telemetry, decide on principle — and on principle the proven-value location is the reference docs (favoring A).
