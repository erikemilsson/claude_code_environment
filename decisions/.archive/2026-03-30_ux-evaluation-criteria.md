# Research Archive: UX Evaluation Criteria for /health-check

**Decision:** DEC-002 — UX evaluation criteria and methodology for /health-check
**Date:** 2026-03-30
**Researcher:** research-agent (Claude Opus 4.6)

---

## Investigation Methodology

### Scope

Researched how to add a UX evaluation step to `/health-check` that assesses dashboard readability, project structure clarity, interaction flow, and user-input section effectiveness across different project types (software, research, procurement, renovation).

### Sources Consulted

**Academic and industry research:**
- Dowding (2018), "The Development of Heuristics for Evaluation of Dashboard Visualizations" (PMC6041119) — adapted Nielsen's heuristics into 10 principles with 49 usability factors specifically for dashboard evaluation
- Nielsen Norman Group — original 10 usability heuristics, severity rating scales, information scent theory
- Baymard Institute — AI heuristic evaluation methodology achieving 95% accuracy against human expert auditors (UX-Ray)
- UX Magazine — cognitive design guidelines for information dashboards

**Dashboard UX best practices (2025-2026):**
- DesignRush — 9 dashboard design principles (2026)
- UXPin — effective dashboard design principles (2025)
- GammaUX — 6 UX principles for effective dashboard design
- Sanjay Dey — SaaS dashboard information architecture and cognitive overload
- Pencil & Paper — UX pattern analysis for data dashboards

**Mermaid diagram evaluation:**
- MermaidSeqBench (arxiv) — evaluation benchmark for LLM-generated Mermaid diagrams
- Mermaid-Sonar — complexity analyzer using research-backed metrics
- Mermaid GitHub issues — viewport scaling problems (1302px diagram in 800px viewport = 39% smaller text)

**Markdown readability:**
- Google Markdown Style Guide
- MDEval (arxiv) — evaluating Markdown awareness in LLMs
- markdownlint — syntax and readability verification

### Key Constraints from the Decision Record

1. Must work across different project types (software, research, procurement, renovation)
2. Should not enforce one structure — adapt to the project domain
3. Lives as a step in `/health-check`, not a standalone command
4. Must address known issues: mermaid diagrams shrinking, documents buried in workspace, underutilized user-input section
5. The SIREN project is a reference case (7 operational documents in `.claude/support/workspace/` needed daily)

---

## Background: How Existing Systems Handle UX Evaluation

### Baymard/UX-Ray Approach (AI Heuristic Evaluation)

Baymard's UX-Ray achieves 95% accuracy by:
1. Building a curated set of heuristics from 200,000+ hours of human research
2. Only including heuristics where AI achieves >= 95% accuracy against human auditors (tested on 50 sites across ~500 parameters)
3. Prioritizing accuracy over coverage — better to check fewer things correctly than many things poorly
4. Using severity ratings per issue, benchmarked against best-in-class UX

**Key lesson for this template:** Generic AI UX evaluation (e.g., GPT-4 "UX audits") achieves only 50-75% accuracy. High accuracy requires domain-specific heuristics with known-good baselines. This template has an advantage: it controls the dashboard format, so the evaluation criteria can be precisely calibrated to what it generates.

### Nielsen's Heuristics Adapted for Dashboards (Dowding 2018)

The academic study adapted Nielsen's 10 heuristics into 7 general principles and 3 visualization-specific principles with 49 total usability factors for dashboard evaluation:

**General principles retained:**
1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Recognition rather than recall
6. Flexibility and efficiency of use
7. Aesthetic and minimalist design

**Dropped from original 10:** Error prevention, help users recover from errors, help and documentation — deemed irrelevant for passive dashboards.

**Added for visualization:** Data sufficiency, data accuracy/currency, customizability of visualizations.

**Key lesson:** Not all of Nielsen's heuristics apply equally to dashboards. The dashboard in this template is a markdown file (read-only from the user's perspective, except for user-input sections), so interaction-heavy heuristics like "user control and freedom" need reinterpretation as "can the user control what sections are shown" (section toggles) and "can the user add their own content" (Notes, Custom Views, inline feedback).

### Severity Rating Scales

Nielsen's established severity scale:
- 0: Not a usability problem
- 1: Cosmetic — fix if time permits
- 2: Minor — low priority
- 3: Major — high priority
- 4: Catastrophic — must fix before release

Factors determining severity: frequency (how often), impact (how hard to overcome), persistence (one-time vs. recurring).

### Information Density and Cognitive Load Research

Key findings from dashboard UX research:
- Information overload affects 46.7% of dashboard users
- Average SaaS dashboard shows 67 data points on first screen
- Cognitive overload occurs at 7 +/- 2 information chunks (Miller's Law)
- Overview screens with <40% information density correlate with 63% faster pattern recognition
- Progressive disclosure is the primary mitigation: show high-level first, drill on demand

**Key lesson for this template:** The dashboard already uses progressive disclosure (section toggles, phase collapsing, blocked phase collapsing, completed task summarization). The UX evaluation should verify these mechanisms are working correctly, not add new ones.

### Information Scent for Navigation

Information scent theory (Nielsen Norman Group) describes how users decide where to navigate based on their estimate of: (1) how likely a link/path will provide what they need, and (2) how long it will take. Strong information scent means clear, descriptive labels that match user expectations.

**Key lesson:** This directly applies to how the dashboard links to files (task JSONs, decision records, spec), and to how documents are placed in the project structure. A file buried at `.claude/support/workspace/invitation-letter.md` has weak information scent for a user who needs it daily — it should be at `docs/invitation-letter.md` or similar.

---

## Heuristic Categories for This Template's Context

Based on the research, I identified six evaluation dimensions relevant to this template's markdown-based, Claude-generated dashboard operating across different project domains:

### H1. Dashboard Readability
Can the user scan the dashboard and understand project state within 30 seconds?

### H2. Information Density and Progressive Disclosure
Is the right amount of information shown at each level? Are collapsing/summarization rules working?

### H3. Visualization Integrity
Are diagrams (Mermaid, tables) rendering correctly and remaining readable?

### H4. Navigation and Information Scent
Do links, file references, and structural cues help the user find what they need?

### H5. User-Input Section Effectiveness
Are the user-owned areas (Notes, Custom Views, inline feedback, phase gates) accessible and useful?

### H6. Project Structure Clarity
Are files placed where the user would expect to find them? Are operational documents accessible?

---

## Discarded Approaches

### Full Nielsen's 10 applied literally
Rejected because several heuristics (error prevention, error recovery, help/documentation) don't map well to a markdown dashboard. The dashboard is generated, not interactively designed. Error states are handled by `/health-check` itself, not by the dashboard.

### Automated rendering tests (e.g., Playwright screenshot comparison)
Rejected because (1) the dashboard is rendered differently in every markdown viewer (VS Code, GitHub, Obsidian, etc.), (2) this would require a rendering engine dependency, (3) the existing health-check runs as pure text analysis via Claude. However, some rendering-aware heuristics (e.g., "Mermaid diagram has >50 nodes, likely unreadable") can be checked structurally without rendering.

### User testing protocol (think-aloud, task completion)
Rejected as a health-check step because it requires a human to actively participate in a structured test. This could be valuable as a separate `/review ux` command but doesn't fit the automated nature of `/health-check`. However, the severity rating from heuristic evaluation can inform which issues to surface as warnings vs. errors.

### Generic AI UX audit (prompt-based)
Rejected because Baymard's research shows generic AI UX auditing achieves only 50-75% accuracy. The template should use calibrated, domain-specific checks where the expected good state is known.

---

## Options Analysis

### Option A: Heuristic Checklist with Severity Ratings

**Approach:** Define a fixed set of heuristic checks organized by the six categories (H1-H6), each with a pass/warn/fail threshold and a severity rating. Checks are structural — they analyze the markdown content, file structure, and task data without rendering.

**Check examples (illustrative, not exhaustive):**

| Category | Check | Threshold | Severity |
|----------|-------|-----------|----------|
| H1 Readability | Dashboard total lines | >300 = warn, >500 = error | 2 (minor) |
| H1 Readability | Action Required section has items | Error if items exist but section missing | 4 (catastrophic) |
| H2 Density | Completed phase not collapsed | Warn if >3 finished tasks listed individually | 2 (minor) |
| H2 Density | Active phase has >15 uncollapsed task rows | Warn | 2 (minor) |
| H3 Visualization | Mermaid diagram node count | >15 without critical-path-only mode = warn, >50 = error | 3 (major) |
| H3 Visualization | Table column count | >7 columns = warn (horizontal scroll) | 2 (minor) |
| H4 Navigation | Action Required items have links | Error if link missing | 3 (major) |
| H4 Navigation | Workspace files referenced in dashboard | Warn if >3 workspace files linked (suggest graduation) | 2 (minor) |
| H5 User-Input | Notes section is default placeholder | Warn after 5+ tasks completed | 1 (cosmetic) |
| H5 User-Input | Custom Views enabled but empty instructions | Warn | 1 (cosmetic) |
| H6 Structure | Operational documents in workspace | Warn per file if task references it and it's in workspace | 3 (major) |
| H6 Structure | User-facing documents in `.claude/` | Warn if referenced by human tasks | 3 (major) |

**Scoring:** Each check produces pass/warn/fail. Aggregate into category scores (H1-H6) and an overall UX health indicator. Use Nielsen's 0-4 severity scale adapted to three levels for actionability: info (severity 0-1), warning (severity 2), error (severity 3-4).

**Domain adaptation:** Checks are structural, not content-specific. A renovation project with 3 phases and a software project with 5 phases both get the same density checks — the thresholds are about cognitive load, not domain content. Domain-specific language in the dashboard is not evaluated (it's generated by Claude and adapts to the spec).

### Option B: Contextual Scoring Model with Project-Type Profiles

**Approach:** Define project-type profiles (software, research, procurement, renovation, general) that adjust evaluation weights and thresholds. Each profile emphasizes different aspects of the six categories.

**Profile examples:**

| Aspect | Software | Research | Procurement | Renovation |
|--------|----------|----------|-------------|------------|
| Diagram weight | High (architecture diagrams critical) | Medium | Low | Medium |
| Document placement weight | Medium | High (papers, data) | High (contracts, quotes) | High (permits, drawings) |
| Timeline weight | Medium | Low (often open-ended) | High (bid deadlines) | High (inspections, permits) |
| User-input weight | Medium | High (hypotheses, notes) | Medium | Medium |
| Decision complexity | High (technical options) | Medium | High (vendor selection) | Medium |

**How it works:**
1. `/health-check` detects project type from spec frontmatter (`project_type` field, or inferred from spec content)
2. Loads the matching profile (or `general` if unknown)
3. Runs the same structural checks as Option A, but applies profile-specific weights to severity
4. Reports findings grouped by the profile's priority order

**Profile detection heuristic:** If no `project_type` in spec frontmatter, scan spec for keywords: "API", "database", "deploy" = software; "hypothesis", "methodology", "data collection" = research; "vendor", "procurement", "RFP" = procurement; "permit", "inspection", "construction" = renovation. Fallback: `general`.

### Option C: Layered Evaluation with User-Defined Criteria

**Approach:** Three evaluation layers with increasing specificity. Layer 1 is universal (always runs), Layer 2 is structural (checks the template's own formatting rules), Layer 3 is user-defined (optional project-specific criteria).

**Layer 1 — Universal UX checks (always runs):**
- Dashboard exists and has required sections
- Action Required items are actionable (have links, completion commands)
- Mermaid diagram complexity within bounds
- Information density checks (phase collapsing, task summarization)
- User-input markers intact (already partially covered by existing health-check)

**Layer 2 — Template compliance checks (always runs):**
- Dashboard follows the format rules in `dashboard-regeneration.md`
- Section display rules are applied correctly (e.g., completed phases collapsed, blocked phases collapsed when >5 tasks)
- Critical path renders correctly (not >5 steps without truncation)
- Phase naming uses "Phase N -- Descriptive Name" format
- Timeline only renders when tasks have dates
- Status summary table only renders when >20 tasks

**Layer 3 — User-defined criteria (optional, configured in spec frontmatter or root CLAUDE.md):**
- User specifies which files should be easily accessible (e.g., "docs/ folder should be linked from dashboard")
- User specifies navigation preferences (e.g., "decision records should be accessible from Notes section")
- User specifies domain-specific quality criteria (e.g., "all procurement documents should have vendor names in titles")

**Configuration example in root `./CLAUDE.md`:**
```markdown
## UX Preferences

- User-facing documents: `docs/`
- Dashboard should link to: spec, docs/ folder, external vendor portal
- Key navigation: decision records from Notes section
```

### Option D: Minimal Structural Checks (Conservative Approach)

**Approach:** Add only the highest-confidence, lowest-false-positive checks to `/health-check`. Focus exclusively on the three known issues from the feedback item (mermaid readability, buried documents, underutilized user-input) plus a few universal readability checks. No scoring, no profiles, no user configuration.

**Checks (complete list):**

1. **Mermaid diagram node count** — Count nodes in the Mermaid code block. >15 without critical-path-only comment = warn. >50 = error. Rationale: directly addresses the known SIREN mermaid readability issue.

2. **Workspace document reference count** — Count files in `.claude/support/workspace/` that are referenced by dashboard links or task `files_affected`. >3 referenced workspace files = warn with suggestion to graduate them. Rationale: directly addresses the SIREN buried-documents issue.

3. **User Notes section utilization** — Check if Notes section contains only the default placeholder after the project has 5+ completed tasks. Warn with suggestion to add Quick Links. Rationale: directly addresses the underutilized user-input section.

4. **Action Required actionability** — Every item in Action Required has a file link and a completion command (or checkbox). Missing either = warn per item.

5. **Dashboard length** — Total line count. >400 = warn. No error threshold (large projects are legitimately long).

6. **Phase collapsing compliance** — Completed phases that list individual tasks instead of using the summary line = warn.

**No severity scoring** — all findings are either pass or warn. No errors from the UX step (structural integrity errors belong to existing health-check parts).

---

## Evaluation Against Criteria

### Criterion 1: Accuracy (low false-positive rate)

False positives erode trust in `/health-check` output. If the UX step regularly flags things that aren't actually problems, users will ignore it.

- **Option A (Heuristic Checklist):** Moderate risk. Fixed thresholds may not fit all projects — a 500-line dashboard might be appropriate for a 50-task project but excessive for a 10-task project. Severity ratings help but don't eliminate false positives.
- **Option B (Contextual Profiles):** Lower risk for projects that match a profile, but profile detection heuristic adds a new failure mode. Misclassified project type = wrong thresholds.
- **Option C (Layered):** Layer 1-2 have low false-positive risk (checking known format rules). Layer 3 is user-defined so false positives are the user's responsibility.
- **Option D (Minimal):** Lowest risk. Only 6 checks, all targeting known real problems. But may miss emerging issues.

### Criterion 2: Domain adaptability

Must work for software, research, procurement, renovation, and unknown project types.

- **Option A:** Structural checks are inherently domain-agnostic. No domain-specific logic.
- **Option B:** Explicitly domain-aware via profiles. Best adaptation but also most complex. Unknown project types fall back to `general` profile.
- **Option C:** Domain adaptation is opt-in via Layer 3. Universal checks are domain-agnostic.
- **Option D:** Fully domain-agnostic. No domain-specific logic at all.

### Criterion 3: Implementation complexity

This becomes a new Part in `/health-check` (Part 6). How much does it add to the already substantial command definition?

- **Option A:** Moderate. ~20-30 specific checks with thresholds. Requires defining the check catalog and severity mapping. Adds ~100-150 lines to health-check.md.
- **Option B:** High. Everything from Option A plus profile definitions, detection heuristic, and weight adjustment logic. Adds ~200-300 lines.
- **Option C:** Moderate-High. Three layers with different execution paths. Layer 3 requires parsing user configuration. Adds ~150-250 lines.
- **Option D:** Low. 6 checks with simple thresholds. Adds ~40-60 lines to health-check.md.

### Criterion 4: Addresses the known issues

Must fix the three specific problems from the feedback: mermaid shrinking, buried documents, underutilized user-input.

- **Option A:** Yes. All three covered by specific checks in the catalog.
- **Option B:** Yes. All three covered, with domain-adjusted severity.
- **Option C:** Yes. Layer 1 covers all three.
- **Option D:** Yes. Checks 1-3 are explicitly designed for these issues.

### Criterion 5: Extensibility

Can new checks be added later without restructuring?

- **Option A:** Good. Adding a check = adding a row to the catalog.
- **Option B:** Moderate. Adding a check requires updating all profiles.
- **Option C:** Good. Adding a universal check = extending Layer 1. Adding a domain check = documenting it for Layer 3.
- **Option D:** Good but limited. Adding checks is easy, but the "minimal" philosophy may need revisiting if many checks accumulate.

### Criterion 6: Integration with existing health-check

The UX step should complement, not duplicate, existing checks. Existing health-check already validates: dashboard structure (sections exist, correct order), marker integrity, task-dashboard consistency, dashboard staleness, sidecar validity.

- **Option A:** Clear boundary — existing checks handle structural validity, new checks handle UX quality. Some overlap risk with dashboard structure checks.
- **Option B:** Same boundary as A but profiles add a cross-cutting concern.
- **Option C:** Layer 2 has significant overlap with existing Part 1 Check 4 (dashboard consistency). Needs careful deduplication.
- **Option D:** Minimal overlap. Each check targets something the existing health-check doesn't cover.

---

## Comparison Summary

| Criterion | Option A: Heuristic Checklist | Option B: Contextual Profiles | Option C: Layered | Option D: Minimal |
|-----------|------|------|------|------|
| Accuracy | Moderate | Moderate-Good | Good (L1-2), Variable (L3) | Strong |
| Domain adaptability | Good (structural) | Strong (explicit profiles) | Good (opt-in) | Good (structural) |
| Implementation complexity | Moderate (~100-150 lines) | High (~200-300 lines) | Moderate-High (~150-250 lines) | Low (~40-60 lines) |
| Addresses known issues | Yes | Yes | Yes | Yes |
| Extensibility | Good | Moderate | Good | Good (limited scope) |
| Integration fit | Good | Moderate | Needs dedup work | Strong |

---

## Recommendation

**Option A (Heuristic Checklist with Severity Ratings)** provides the best balance of thoroughness, domain adaptability, and implementation feasibility. It addresses all known issues, integrates cleanly with the existing health-check structure, and is extensible.

However, I note a viable hybrid: **start with Option D's minimal checks, then extend to Option A's full catalog over time**. This "Option D-to-A" path would ship a minimal viable UX step quickly (addressing the three known issues immediately) and grow the check catalog based on real usage feedback. The severity rating framework from Option A would be adopted from the start to ensure consistent reporting as checks are added.

**Confidence: Moderate.** The choice between "start minimal and grow" vs. "ship the full checklist" depends on how urgently the broader UX checks are needed vs. the desire to keep the health-check command lean. The user's feedback (FB-015) emphasized the three specific known issues, which supports starting minimal. But the feedback also mentioned "systematic way to evaluate dashboard and project interaction quality," which supports the fuller checklist.

Option B's project-type profiles add real value but at disproportionate complexity. If domain adaptation becomes necessary, it could be added later as an enhancement to Option A without restructuring. Option C's layered approach has merit but the Layer 2 overlap with existing health-check checks creates maintenance burden.

---

## Research Questions for the User

1. **Scope preference:** Should the initial implementation target only the three known issues (mermaid, buried docs, user-input) and grow from there, or should it aim for comprehensive UX coverage from the start?

2. **Severity reporting:** Should UX findings use the same severity indicators as the rest of health-check (pass/warn/error), or should they use a separate "UX quality" indicator that doesn't contribute to the overall HEALTHY/NEEDS ATTENTION/CRITICAL status?

3. **Project-type detection:** Is the spec frontmatter `project_type` field something you want to standardize in the template, or should all UX checks remain purely structural (domain-agnostic)?
