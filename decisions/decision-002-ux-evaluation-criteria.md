---
id: DEC-002
title: UX evaluation criteria and methodology for /health-check
status: approved
category: methodology
created: 2026-03-30
decided:
related:
  tasks: []
  decisions: [DEC-001]
  feedback: [FB-015]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# UX evaluation criteria and methodology for /health-check

## Select an Option

Mark your selection by checking one box:

- [x] Option A: Heuristic Checklist with Severity Ratings (D-to-A hybrid path)
- [ ] Option B: Contextual Scoring Model with Project-Type Profiles
- [ ] Option C: Layered Evaluation with User-Defined Criteria
- [ ] Option D: Minimal Structural Checks (Conservative)

*Check one box above, then fill in the Decision section below.*

## Background

There's no systematic way to evaluate dashboard and project interaction quality across projects using this template. `/health-check` validates structural integrity (task schema, instruction files, decisions, archives, template sync) but doesn't assess whether the project is actually usable from the user's perspective.

Observed problems include: mermaid diagrams shrinking to unreadable sizes, operational documents buried in `.claude/support/workspace/`, and the user-input section of the dashboard being underutilized.

The goal is to add a UX evaluation step to `/health-check` that covers:
- Dashboard readability (layout, diagrams, information density)
- Project structure clarity (file placement, navigation)
- Interaction flow (are the right things surfaced at the right time?)
- User-input section effectiveness

This must accommodate different project types (software, research, procurement, renovation) rather than enforcing one structure. The evaluation needs defined criteria — what constitutes "good" UX across these varied domains?

### Research Foundation

Research drew on Nielsen's usability heuristics adapted for dashboard evaluation (Dowding 2018 — 10 principles, 49 factors), Baymard Institute's AI heuristic evaluation methodology (95% accuracy by using domain-specific calibrated checks rather than generic AI auditing), cognitive load research (information overload affects 46.7% of dashboard users; cognitive overload at 7 +/- 2 chunks), information scent theory for navigation (strong scent = clear labels matching user expectations), and Mermaid diagram scaling research (viewport compression makes text 39% smaller than intended when diagrams exceed container width).

Key insight: Generic AI UX auditing achieves only 50-75% accuracy. High accuracy requires domain-specific heuristics with known-good baselines. This template controls the dashboard format, so evaluation criteria can be precisely calibrated to what it generates.

Six evaluation dimensions were identified:
- **H1. Dashboard Readability** — can the user scan and understand project state within 30 seconds?
- **H2. Information Density** — is progressive disclosure working (phase collapsing, task summarization)?
- **H3. Visualization Integrity** — are Mermaid diagrams and tables rendering readably?
- **H4. Navigation and Information Scent** — do links and file references help users find what they need?
- **H5. User-Input Section Effectiveness** — are Notes, Custom Views, inline feedback accessible and useful?
- **H6. Project Structure Clarity** — are files placed where users expect them?

## Options Comparison

| Criteria | Option A: Heuristic Checklist | Option B: Contextual Profiles | Option C: Layered | Option D: Minimal |
|----------|------|------|------|------|
| Accuracy (low false-positive rate) | Moderate | Moderate-Good | Good (L1-2), Variable (L3) | Strong |
| Domain adaptability | Good (structural) | Strong (explicit profiles) | Good (opt-in) | Good (structural) |
| Implementation complexity | Moderate (~100-150 lines) | High (~200-300 lines) | Moderate-High (~150-250 lines) | Low (~40-60 lines) |
| Addresses known issues | Yes | Yes | Yes | Yes |
| Extensibility | Good | Moderate (new checks need all profiles updated) | Good | Good (limited scope) |
| Integration with existing health-check | Good | Moderate (cross-cutting profiles) | Needs dedup with Part 1 | Strong |
| Overall | Recommended | Overkill for now | Overlap risk | Good starting point |

**Recommendation:** Option A provides the best balance. A viable hybrid path: start with Option D's checks, adopt Option A's severity framework from day one, extend the check catalog over time based on real usage.

## Option Details

### Option A: Heuristic Checklist with Severity Ratings

**Description:** Define a fixed catalog of ~20-30 structural checks organized by the six heuristic categories (H1-H6). Each check has a pass/warn/fail threshold and a severity rating (Nielsen's 0-4 scale mapped to info/warning/error). Checks analyze markdown content, file structure, and task data without rendering. All checks are domain-agnostic — they target cognitive load and structural patterns, not domain-specific content.

**Example checks:**

| Category | Check | Threshold | Severity |
|----------|-------|-----------|----------|
| H1 Readability | Dashboard total lines | >300 warn, >500 error | 2 |
| H2 Density | Completed phase not collapsed | Warn if >3 finished tasks listed | 2 |
| H3 Visualization | Mermaid node count | >15 without critical-path mode = warn | 3 |
| H4 Navigation | Action Required items missing links | Error per item | 3 |
| H4 Navigation | Workspace files referenced in dashboard | >3 = warn, suggest graduation | 2 |
| H5 User-Input | Notes section still default placeholder | Warn after 5+ tasks done | 1 |
| H6 Structure | Operational docs in `.claude/support/workspace/` | Warn per file referenced by human tasks | 3 |

**Strengths:**
- Comprehensive coverage of all six evaluation dimensions
- Clear severity ratings help users prioritize fixes
- Domain-agnostic by design — structural checks apply to any project type
- Extensible: adding a check = adding a row to the catalog
- Integrates cleanly as a new Part 6 in health-check

**Weaknesses:**
- Fixed thresholds may not fit all project scales (500-line dashboard is fine for 50 tasks, excessive for 10)
- ~20-30 checks add meaningful complexity to an already substantial command definition
- Some thresholds require tuning based on real-world usage (risk of false positives initially)

**Research Notes:** Inspired by Baymard's approach of domain-specific calibrated checks over generic AI auditing. Severity scale from Nielsen (1994). Dashboard-specific heuristic categories from Dowding (2018). See `decisions/.archive/2026-03-30_ux-evaluation-criteria.md`.

### Option B: Contextual Scoring Model with Project-Type Profiles

**Description:** Everything from Option A, plus project-type profiles (software, research, procurement, renovation, general) that adjust evaluation weights and thresholds. Profile detected from spec frontmatter `project_type` field or inferred from spec keywords.

**Profile weight adjustments (example):**

| Aspect | Software | Research | Procurement | Renovation |
|--------|----------|----------|-------------|------------|
| Diagram weight | High | Medium | Low | Medium |
| Document placement | Medium | High | High | High |
| Timeline weight | Medium | Low | High | High |
| User-input weight | Medium | High | Medium | Medium |

**Strengths:**
- Best domain adaptation — different project types get tailored evaluation
- Acknowledges that a research project values Notes section more than a software project values diagrams
- Profile detection heuristic provides reasonable defaults

**Weaknesses:**
- Highest implementation complexity (~200-300 lines added to health-check)
- Profile detection heuristic adds a failure mode (misclassification)
- Every new check requires updating all profiles — maintenance burden scales
- Profile definitions are subjective — what weights are "right" for procurement?
- Premature optimization: insufficient real-world data to calibrate profiles accurately

**Research Notes:** Inspired by cognitive load research showing strategic variance in information density based on user intent. Profile concept from SaaS dashboard design literature. See `decisions/.archive/2026-03-30_ux-evaluation-criteria.md`.

### Option C: Layered Evaluation with User-Defined Criteria

**Description:** Three evaluation layers. Layer 1: universal UX checks (always runs, similar to Option D). Layer 2: template compliance checks (verifies dashboard follows `dashboard-regeneration.md` format rules). Layer 3: user-defined criteria (optional, configured in root `./CLAUDE.md` under `## UX Preferences`).

**Layer configuration example:**
```markdown
## UX Preferences
- User-facing documents: `docs/`
- Dashboard should link to: spec, docs/ folder, external portal
```

**Strengths:**
- Progressive adoption: Layer 1 works out of the box, Layer 3 lets power users customize
- User-defined criteria enable domain-specific checks without template hardcoding profiles
- Clear separation of concerns between universal, template, and project-specific checks

**Weaknesses:**
- Layer 2 overlaps significantly with existing health-check Part 1 Check 4 (dashboard consistency) — requires careful deduplication
- Layer 3 adds configuration parsing complexity (reading UX Preferences from root CLAUDE.md)
- Three evaluation layers with different execution paths increase cognitive load for both the command definition and the user reading the report
- User-defined criteria may go stale as the project evolves

**Research Notes:** Layered concept from progressive disclosure research. Layer 3 inspired by customizable evaluation frameworks. See `decisions/.archive/2026-03-30_ux-evaluation-criteria.md`.

### Option D: Minimal Structural Checks (Conservative)

**Description:** Only 6 high-confidence, low-false-positive checks targeting the three known issues (mermaid readability, buried documents, underutilized user-input) plus basic readability. No scoring system, no profiles, no user configuration. All findings reported as warnings (no errors from the UX step).

**Complete check list:**
1. Mermaid diagram node count (>15 without critical-path-only = warn, >50 = error)
2. Workspace document reference count (>3 referenced workspace files = warn, suggest graduation)
3. User Notes section utilization (default placeholder after 5+ completed tasks = warn)
4. Action Required actionability (every item must have link + completion command)
5. Dashboard length (>400 lines = warn)
6. Phase collapsing compliance (completed phases listing individual tasks = warn)

**Strengths:**
- Lowest implementation complexity (~40-60 lines in health-check)
- Lowest false-positive risk (each check targets a known real problem)
- Strongest integration fit (no overlap with existing checks)
- Can be implemented and shipped immediately
- Clear, predictable behavior — users always understand why a finding was reported

**Weaknesses:**
- Limited scope — misses emerging UX issues not yet observed
- No severity differentiation (all warnings treated equally)
- No systematic framework for adding checks later (risk of ad hoc growth)
- Does not provide the "systematic way to evaluate dashboard and project interaction quality" that FB-015 requested

**Research Notes:** Directly maps to the three specific issues cited in FB-015. Conservative approach inspired by Baymard's "accuracy over coverage" principle. See `decisions/.archive/2026-03-30_ux-evaluation-criteria.md`.

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision. This section is yours — Claude reads it but never overwrites it.*

**Constraints:**
- Must work across different project types (software, research, procurement, renovation, etc.)
- Should not enforce one structure — adapt to the project domain
- Lives as a step in `/health-check`, not a standalone command
- The user-input section of the dashboard is an area with particular potential for improvement
- Observed issue: SIREN project had mermaid diagrams shrinking to unreadable sizes

**Questions:**
- How do other dashboard-driven Claude workflows handle UX evaluation?
- What are the minimum viable checks that would catch the most common UX problems?

**Research Questions (from investigation):**
- Should the initial implementation target only the three known issues and grow from there, or aim for comprehensive UX coverage from the start?
- Should UX findings use the same severity indicators as the rest of health-check (pass/warn/error), or a separate "UX quality" indicator that doesn't contribute to the overall HEALTHY/NEEDS ATTENTION/CRITICAL status?
- Is the spec frontmatter `project_type` field something to standardize in the template (needed for Option B), or should all UX checks remain purely structural?

## Decision

**Selected:** Option A: Heuristic Checklist with Severity Ratings (D-to-A hybrid path)
**Decided:** 2026-03-30

**Rationale:**
Option A provides the best balance of thoroughness, domain adaptability, and extensibility. The D-to-A hybrid path starts with Option D's 6 high-confidence checks targeting the 3 known issues (mermaid readability, buried documents, underutilized user-input) while adopting Option A's severity rating framework from day one. The check catalog grows over time based on real usage feedback. This avoids false positives from untested thresholds while immediately addressing observed problems.

UX findings contribute to the overall health-check status (HEALTHY/NEEDS ATTENTION/CRITICAL) rather than using a separate indicator. `project_type` field left open for now — all checks remain structural and domain-agnostic.

## Trade-offs

**Gaining:**
- Immediate coverage of the 3 known UX issues (mermaid, buried docs, user-input)
- Consistent severity framework (Nielsen's 0-4 scale) ready for catalog growth
- Domain-agnostic structural checks work for any project type
- Clean integration as Part 6 of `/health-check`
- Extensible: adding a check = adding a row to the catalog

**Giving Up:**
- Initial coverage is limited to 6 checks (comprehensive coverage comes later)
- Fixed thresholds may need tuning for edge cases (very large/small projects)
- No domain-specific adaptation (Option B's profiles deferred unless needed)

## Impact

**Implementation Notes:**
Start with 6 checks from Option D, using Option A's severity framework:
1. Mermaid diagram node count (severity 3)
2. Workspace document reference count (severity 3)
3. User Notes section utilization (severity 1)
4. Action Required actionability (severity 3)
5. Dashboard length (severity 2)
6. Phase collapsing compliance (severity 2)

Extend the catalog as real usage reveals additional UX patterns. DEC-001's interaction logs will be a source of new check candidates.

**Affected Areas:**
- `.claude/commands/health-check.md` — new Part 6: UX Evaluation
- `.claude/support/reference/workflow.md` — document the UX evaluation step
- `system-overview.md` — update `/health-check` description and feature catalog

**Risks:**
- Thresholds for the initial 6 checks may need adjustment based on real projects
- Risk of threshold creep as catalog grows — need discipline to only add high-confidence checks
