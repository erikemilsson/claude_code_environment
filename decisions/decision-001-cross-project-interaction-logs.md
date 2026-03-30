---
id: DEC-001
title: Cross-project interaction log capture and processing pipeline
status: approved
category: process
created: 2026-03-30
decided:
related:
  tasks: []
  decisions: [DEC-002]
  feedback: [FB-011]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Cross-project interaction log capture and processing pipeline

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Session-End Structured Markers
- [ ] Option B: Conversation Checkpoint Reports
- [x] Option C: Hybrid Pipeline (Markers + Reports)
- [ ] Option D: Lightweight Feedback Bridge

*Check one box above, then fill in the Decision section below.*

## Background

Projects using this template generate valuable interaction data -- friction moments where Claude skipped steps, mishandled workflows, or failed to push back on user design choices that led to problems downstream (e.g., a project trying to serve both personal and public use cases simultaneously when it should have been forked).

Currently, there's no mechanism to feed this data back into the template repo for improvement. The user must manually remember and report issues, which means most insights are lost.

The goal is an automated session-end export of conversation history from projects back to this repo, with a processing pipeline that surfaces actionable insights. Full conversation history (not just summaries) is preferred for pinpointing exactly where template improvements should intervene.

**Critical constraint discovered during research:** Claude Code does not expose conversation history as an exportable artifact. There is no API, hook, or filesystem path to access raw conversation transcripts. All options must work within this constraint. The user's preference for "full conversation history" is best served by capturing the most complete structured representation achievable within the platform's limits.

Key design questions:
- **Capture mechanism:** What triggers the export and what format does it use?
- **Storage:** Where do logs land in this repo and how are they organized?
- **Processing pipeline:** How are logs parsed, categorized, and turned into actionable feedback?
- **Integration:** How does this connect with existing `/feedback`, `/iterate`, and `/health-check` systems?
- **Automation level:** Most of the pipeline should be automated, with user review only at decision points.

## Options Comparison

| Criteria | A: Structured Markers | B: Checkpoint Reports | C: Hybrid Pipeline | D: Feedback Bridge |
|----------|----------------------|----------------------|-------------------|-------------------|
| Capture reliability | Strong (every session via hooks) | Moderate (graceful exits only) | Strong (both tracks) | Weak (manual tagging) |
| Data completeness | Moderate (predefined types only) | Moderate (Claude-assessed, may miss own blind spots) | Strong (automated + nuanced) | Weak (user-tagged only) |
| Privacy handling | Strong (structured, no raw content) | Moderate (report may contain project details) | Strong (structured + user review) | Strong (user-controlled) |
| Automation level | Strong (markers + export auto) | Moderate (requires /work pause) | Strong (auto baseline + graceful bonus) | Weak (mostly manual) |
| Integration quality | Good (feeds /feedback) | Good (feeds /feedback) | Strong (deep integration across commands) | Good (uses /feedback directly) |
| Processing efficiency | Good (structured JSON, parseable) | Moderate (markdown needs parsing) | Good (unified JSON format) | Good (already feedback items) |
| Storage burden | Low (~5KB/session) | Low (~10KB/session) | Low-moderate (~15KB/session) | Very low (~2KB/session) |
| Implementation complexity | Moderate | Low | High | Low |
| Overall | Strong | Moderate | Strong | Weak |

**Recommendation:** Option C provides the most comprehensive solution. A phased rollout (Phase 1: markers, Phase 2: assessment, Phase 3: processing pipeline) makes the complexity manageable and delivers value at each step. If complexity is the primary constraint, Option A is a strong standalone choice.

## Option Details

### Option A: Session-End Structured Markers

**Description:** Instrument agents (implement-agent, verify-agent) to emit "friction markers" to a session log file during execution. At session boundaries (`/work pause`, PreCompact hook), compile markers into a structured JSON export. No conversation access needed -- markers capture specific events (verification failures, workflow deviations, recovery events, user feedback, spec drift) as they occur on disk.

**Strengths:**
- Works within Claude Code's actual capabilities (no impossible conversation export)
- Captures every session, including crashes (markers written during execution, not at end)
- Structured data is immediately actionable -- no NLP or transcript parsing needed
- Privacy-friendly: captures template-relevant events, not project content
- Builds on existing infrastructure (session boundaries, hooks, task JSON patterns)

**Weaknesses:**
- Cannot capture nuanced friction like "Claude should have suggested forking" -- only predefined marker types
- Requires modifying agent definitions to emit markers (scattered changes across files)
- The marker taxonomy must be maintained as the template evolves
- Initial coverage will be incomplete; improves iteratively

**Research Notes:** The existing PreCompact hook (`pre-compact-handoff.sh`) demonstrates the pattern: reads disk state, writes structured JSON. Session markers follow this same architecture. See `decisions/.archive/2026-03-30_cross-project-interaction-logs.md` for full analysis.

### Option B: Conversation Checkpoint Reports

**Description:** Enhance `/work pause` so that Claude, while it still has conversation context, generates a brief "interaction report" covering friction moments, pushback opportunities, workflow deviations, and design observations. The PreCompact hook provides a disk-state-only fallback for non-graceful exits.

**Strengths:**
- Captures the "why" layer that automated markers miss -- closest to "full history" in spirit
- Can identify non-obvious friction (like the styler scenario) through Claude's retrospective analysis
- Low implementation complexity -- addendum to an existing command
- Human-readable reports that users can review before exporting

**Weaknesses:**
- Only produces full reports for graceful exits (`/work pause`). Crashes and auto-compaction get minimal data.
- Claude's self-assessment may have blind spots -- it might not recognize its own failures
- Adds session-end latency (report generation takes time)
- Not truly "automated session-end export" -- requires user to run `/work pause`
- Sensitive project details may leak into the report

**Research Notes:** The handoff file's `session_knowledge` field already captures some of this. This option expands it into a structured assessment. The 32K output token limit constrains report length for very long sessions. See full archive for details.

### Option C: Hybrid Pipeline (Markers + Reports)

**Description:** Combines Options A and B. Track 1: automated friction markers run continuously and capture every session. Track 2: Claude-generated interaction assessment adds the nuanced "why" layer at graceful exit points. Both tracks feed into a unified export format. A processing pipeline in the template repo categorizes, aggregates across projects, generates insights, and routes actionable items to `/feedback`.

**Full pipeline:**
1. **Capture** -- Markers during execution (Track 1) + Claude assessment at `/work pause` (Track 2)
2. **Export** -- Unified JSON written at session end, containing both tracks
3. **Transport** -- Local filesystem path (default), git push (advanced), or manual copy
4. **Ingest** -- Template repo reads exports from `interaction-logs/inbox/`
5. **Categorize** -- Group friction by template area (verify-agent, implement-agent, /work, design-guidance, etc.)
6. **Aggregate** -- Detect patterns across sessions and projects
7. **Generate insights** -- Produce specific, evidence-backed improvement suggestions
8. **Route to /feedback** -- Insights become FB-NNN items for the normal 3-phase review pipeline

**Strengths:**
- Best of both worlds: comprehensive automated coverage + nuanced assessment
- Graceful degradation: crashes get markers only, graceful exits get full data
- Cross-project aggregation reveals patterns invisible from a single project
- Deep integration with existing systems (`/feedback`, `/iterate`, `/health-check`)
- Configurable transport accommodates different developer setups
- Phased implementation path: deliver value at each phase

**Weaknesses:**
- Highest implementation complexity (changes across agents, commands, hooks, and new processing pipeline)
- Requires changes to many template files (agent definitions, `/work pause`, PreCompact hook, `/health-check`)
- Track 2 still only fires on graceful exits
- Marker taxonomy and processing logic need ongoing maintenance
- Aggregation logic (cross-project pattern detection) is complex and may need iteration

**Research Notes:** Pragmatic implementation phases: (1) friction markers + export, (2) Claude assessment in `/work pause`, (3) processing pipeline in template repo. Each phase is independently valuable. Transport sub-option C2 (local filesystem path, configured via `version.json`) is the pragmatic starting point. See full archive for export format specification, processing pipeline details, and transport sub-options.

### Option D: Lightweight Feedback Bridge

**Description:** Minimal new infrastructure. Add `/feedback export-to-template` to source projects (exports template-tagged feedback items and task user_feedback) and `/feedback import` to the template repo. Relies on user explicitly tagging feedback as template-relevant. No automated capture, no friction markers, no interaction reports.

**Strengths:**
- Minimal implementation: two new command modes, no agent changes
- Uses existing `/feedback` infrastructure end-to-end
- User controls exactly what gets exported -- no privacy concerns
- Easy to understand and maintain

**Weaknesses:**
- Relies on user remembering to tag feedback -- most insights are still lost
- Cannot identify friction the user did not explicitly flag (the core problem FB-011 describes)
- Does not fulfill the "automated session-end export" requirement
- Marginal value over manually creating feedback items in the template repo
- Cannot handle the "styler" scenario where Claude should have pushed back

**Research Notes:** Included as the baseline "simpler/cheaper" option per research methodology. Does not address the core need identified in FB-011. See full archive for analysis.

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision. This section is yours -- Claude reads it but never overwrites it.*

**Constraints:**
- Full conversation history preferred over summaries -- need to pinpoint exact intervention points
- Most of the pipeline should be automated, with user review only at decision points
- Must integrate with existing `/feedback`, `/iterate`, and `/health-check` rather than duplicating
- Session-end export is the preferred trigger point
- Template repo is at `/Users/erikemilsson/Developer/claude_code_environment`

**Questions:**
- What are the practical limits on conversation history size?
- How should sensitive project data in logs be handled?

**Research Questions:**
- Given that full conversation export is technically impossible in Claude Code, does the "structured markers + Claude assessment" approach in Option C provide sufficient signal for the two stated use cases (friction identification and design pushback)?
- For the transport mechanism: is local filesystem path (both repos on the same machine) the expected setup, or do you need cross-machine support from the start?
- What is the acceptable implementation timeline? Option C's phased approach can start delivering value quickly (Phase 1) but full pipeline completion is substantial work.
- Should the processing pipeline be a new command (`/process-logs`) or a mode of the existing `/feedback` command (`/feedback ingest`)?

## Decision

**Selected:** Option C: Hybrid Pipeline (Markers + Reports)
**Decided:** 2026-03-30

**Rationale:**
Only option that addresses both core use cases — automated friction capture (Track 1 markers) and non-obvious design pushback identification (Track 2 Claude assessment). The phased rollout (markers → assessment → pipeline) makes the complexity manageable. Structured markers + Claude assessment provides sufficient signal given that raw conversation export is impossible.

**Transport:** Local filesystem (C2) — both repos on the same machine. Configure `template_inbox_path` in `version.json`.

**Processing automation:** Prefer a hook-based trigger (e.g., processing fires automatically when new files appear in `interaction-logs/inbox/`). Second choice: integrate processing into an existing command like `/health-check` or `/work` rather than a standalone manual command. The user should never need to remember to run a separate processing step.

## Trade-offs

**Gaining:**
- Automated capture of friction moments across all sessions (including crashes via Track 1)
- Nuanced "why" insights from Claude assessment at graceful exits (Track 2)
- Cross-project pattern detection (recurring friction = high-confidence template fix)
- Direct integration with existing `/feedback` lifecycle for insight-to-spec pipeline

**Giving Up:**
- Implementation complexity is the highest of all options — requires changes across agent definitions, `/work pause`, PreCompact hook, and a new processing pipeline
- Marker taxonomy needs ongoing maintenance as the template evolves
- Track 2 only fires on graceful exits (`/work pause`), not crashes or auto-compaction

## Impact

**Implementation Notes:**
Phased rollout:
- Phase 1: Friction markers in agents + session-end export (gets automated capture working)
- Phase 2: Claude interaction assessment in `/work pause` (adds nuanced insight layer)
- Phase 3: Processing pipeline in template repo (turns raw data into `/feedback` items)

**Affected Areas:**
- `.claude/agents/implement-agent.md` — add friction marker emission
- `.claude/agents/verify-agent.md` — add friction marker emission
- `.claude/commands/work.md` — `/work pause` extended with Track 2 assessment and export
- `.claude/hooks/pre-compact-handoff.sh` — extended to include Track 1 markers in export
- `.claude/version.json` — add `template_inbox_path` field
- `interaction-logs/` — new directory structure in template repo (inbox, processed, insights)
- `.claude/commands/health-check.md` or hook — processing pipeline trigger

**Risks:**
- Marker taxonomy may be incomplete initially — improves iteratively with real usage
- Claude's self-assessment (Track 2) may have blind spots about its own failures
- Storage accumulation if exports are not processed and archived regularly
