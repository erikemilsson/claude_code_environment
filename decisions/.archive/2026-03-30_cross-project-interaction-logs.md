# Research Archive: Cross-Project Interaction Log Capture and Processing Pipeline

**Decision:** DEC-001
**Date:** 2026-03-30
**Researcher:** research-agent (Claude Opus 4.6)

---

## Investigation Methodology

### Sources Consulted

1. **Template infrastructure files:**
   - `system-overview.md` -- full lifecycle, features, design principles
   - `.claude/commands/work.md` -- `/work pause`, session boundaries, PreCompact hook, context transitions
   - `.claude/commands/health-check.md` -- template sync mechanism, validation pipeline
   - `.claude/commands/feedback.md` -- feedback capture, triage, and promotion lifecycle
   - `.claude/support/reference/context-transitions.md` -- handoff file schema, PreCompact hook
   - `.claude/hooks/pre-compact-handoff.sh` -- existing hook implementation
   - `.claude/settings.local.json` -- hook configuration and permissions
   - `.claude/version.json` -- template sync configuration
   - `.claude/sync-manifest.json` -- file category definitions

2. **Feedback context:**
   - `FB-011` in `.claude/support/feedback/feedback.md` -- original feedback item with requirements
   - `FB-012` -- source of truth for template repo (related concern)

3. **Related decisions:**
   - `DEC-002` -- UX evaluation criteria (cross-referenced, could benefit from interaction log data)

### Investigation Approach

Analyzed the problem along four dimensions:
1. **Capture mechanism** -- how interaction data leaves source projects and arrives at the template repo
2. **Log format and storage** -- what gets stored, where, and in what structure
3. **Processing pipeline** -- how raw data becomes actionable insights
4. **Integration** -- how this connects with `/feedback`, `/iterate`, `/health-check`

Each option represents a different architectural philosophy for the overall system. Options were evaluated against 8 criteria: capture reliability, data completeness, privacy handling, automation level, integration quality, processing efficiency, storage burden, and implementation complexity.

---

## Key Constraints Identified

1. **Claude Code has no native conversation export API.** There is no built-in mechanism to programmatically export full conversation history from Claude Code sessions. Conversation data exists in Claude Code's internal context management, not as accessible files on disk. This is the single most significant constraint and shapes all viable options.

2. **Hooks have limited context.** The existing PreCompact hook (`pre-compact-handoff.sh`) demonstrates what hooks can and cannot do: they receive stdin JSON with session metadata and have filesystem access, but they cannot access conversation content. The hook reads task JSON files from disk -- it does not see the conversation.

3. **Session boundaries are well-defined.** The template has clear session boundary points: `/work pause` (graceful), PreCompact hook (automatic), and session sentinel (`.last-clean-exit.json`). These are natural trigger points.

4. **The `/feedback` system already handles the insight-to-spec lifecycle.** The 3-phase review pipeline (grouping, refinement, impact assessment) and the promotion path to `/iterate` are mature. Any new system should feed into this pipeline rather than duplicating it.

5. **Template sync is git-based.** The existing template sync mechanism uses a git remote. Interaction logs flowing back to the template repo could use the same transport layer.

6. **Full conversation history size.** Claude Code conversations can be very long (100K+ tokens in extended sessions). Storing full transcripts for multiple projects would create substantial data volume. The user's preference for full history must be balanced against practical storage limits.

7. **Cross-repo data flow.** Source projects and the template repo are separate git repositories. Data must cross this boundary. The template repo URL is already stored in each project's `version.json`.

---

## Options Evaluated

### Option A: Session-End Structured Summary with Friction Markers

**Philosophy:** Rather than exporting raw conversation history (which is inaccessible), instrument the template commands and agents to emit structured annotations during sessions, then export a curated summary at session boundaries.

**Capture Mechanism:**
- **During sessions:** Modify implement-agent and verify-agent to emit "friction markers" to a session log file (`.claude/support/workspace/.session-log.json`) when they encounter situations that suggest template improvement:
  - Verification failures (what failed, why, how many retries)
  - Agent step skips or deviations from prescribed workflow
  - Spec drift reconciliation events (what drifted, user's resolution choice)
  - Decision creation during execution (unplanned decisions)
  - Out-of-spec task creation (user requests beyond spec)
  - Guided testing failures (which steps failed)
  - Recovery events (what states needed recovery, what was stuck)
  - User feedback captured via `/work complete` (`user_feedback` field content)
  - Phase gate conditions that required user override
- **At session end:** `/work pause` and the PreCompact hook already run at session boundaries. Add a step that:
  1. Reads the session log
  2. Reads task completion notes and verification results for tasks touched this session
  3. Compiles a structured export file
  4. Writes it to a designated location

**Export Format:**
```json
{
  "export_version": 1,
  "source_project": "project-name (from git remote or CLAUDE.md)",
  "template_version": "1.5.0",
  "session_date": "2026-03-30",
  "session_duration_estimate": "long|medium|short",
  "friction_events": [
    {
      "type": "verification_failure",
      "task_id": "7",
      "task_title": "Build API layer",
      "details": "Cross-file consistency check failed: modified schema.py but views.py still references old field names",
      "resolution": "fix_and_retry",
      "attempts": 2,
      "template_area": "verify-agent cross-file check"
    },
    {
      "type": "workflow_deviation",
      "step": "implement-agent Step 4",
      "details": "User requested proceeding without spec alignment check",
      "template_area": "/work Step 2 spec check"
    }
  ],
  "session_metrics": {
    "tasks_completed": 3,
    "verification_pass_rate": 0.75,
    "recovery_events": 0,
    "decisions_created": 1,
    "out_of_spec_tasks": 0
  },
  "user_feedback_excerpts": [
    {
      "task_id": "5",
      "feedback": "The verification was too strict about formatting -- flagged whitespace differences as failures"
    }
  ],
  "template_improvement_signals": [
    "Verification cross-file check generated false positive for whitespace-only changes",
    "User bypassed spec check suggesting the friction is too high for minor changes"
  ]
}
```

**Transport to Template Repo:**
- Export file lands in the source project at `.claude/support/workspace/.session-export-YYYY-MM-DD.json`
- A new `/health-check` substep (or standalone command) in the template repo scans a configured inbox directory for these files
- Alternatively: the export file is placed in a shared directory path, or the user manually copies/syncs it (simplest starting point)

**Processing in Template Repo:**
- New folder: `interaction-logs/inbox/` receives raw exports
- New folder: `interaction-logs/processed/` holds analyzed exports
- Processing script (or `/feedback`-adjacent command) parses exports, categorizes friction events by template area, and generates feedback items

**Strengths:**
- Works within Claude Code's actual capabilities (no impossible conversation export)
- Structured data is immediately actionable (no NLP/parsing needed)
- Friction markers are precise -- they capture the exact moment and context of template-relevant events
- Session log file is small (structured JSON, not full conversation)
- Privacy-friendly: captures template-relevant events, not arbitrary project content
- Builds on existing infrastructure (session boundaries, hooks, task JSON)

**Weaknesses:**
- Requires modifying agent definitions and commands to emit friction markers (scattered changes)
- Cannot capture the "full conversation" the user wants -- misses nuanced moments like "Claude should have suggested forking the project" that don't map to a predefined friction type
- The marker taxonomy must be maintained as the template evolves (new commands = new marker types)
- Initial marker coverage will be incomplete; it will improve iteratively
- Transport mechanism (getting exports from source projects to template repo) still needs solving

**Research Notes:**
- The existing PreCompact hook demonstrates the pattern: a shell script that reads task state from disk and writes a structured JSON file. The session log follows this same architecture.
- The `user_feedback` field on task JSON already captures some of this signal. The structured export systematizes what's already partially captured.

---

### Option B: Conversation Checkpoint Export via `/work pause` Enhancement

**Philosophy:** Since full automatic conversation export is not possible, make the session-end handoff richer by having Claude (while it still has conversation context) generate a detailed "interaction report" that captures the reasoning, friction, and user dynamics that disk-only hooks cannot see.

**Capture Mechanism:**
- Enhance the `/work pause` command to add a new step after writing the handoff file:
  1. Claude reviews the current session's conversation (it still has full context at this point)
  2. Generates an "interaction report" summarizing: decisions made (formal and informal), friction moments, user pushback, workflow deviations, places where Claude should have suggested alternatives, user feedback themes
  3. Writes this report to `.claude/support/workspace/.interaction-report-YYYY-MM-DD.md`
- The PreCompact hook adds a minimal version (disk-state-only friction markers, like Option A) as a fallback

**Interaction Report Format:**
```markdown
# Interaction Report — 2026-03-30

## Session Summary
[2-3 sentence overview of what happened]

## Friction Moments
- **[timestamp/context]:** [description of friction and what template change could address it]
- ...

## Workflow Deviations
- [where Claude or user deviated from prescribed flow, and why]

## Design Pushback Opportunities
- **[context]:** User decided X, but Y might have been better because Z. Template could suggest Y when it detects [conditions].

## User Preferences Observed
- [preferences that might inform template defaults or suggestions]

## Template Improvement Signals
- [specific, actionable suggestions for template files/commands/agents]
```

**Transport and Processing:** Same as Option A (inbox directory, processing pipeline, feeding into `/feedback`).

**Strengths:**
- Captures the "why" layer that disk state misses -- closest to "full conversation history" in spirit
- Claude can identify non-obvious friction (like "user should have forked the project") that no predefined marker would catch
- The report is human-readable -- the user can review it before exporting
- Leverages the fact that `/work pause` runs while Claude still has conversation context
- Relatively low implementation complexity -- it's an addendum to an existing command

**Weaknesses:**
- Only works for `/work pause` (graceful exit). Automatic exits (PreCompact, crashes) only get the disk-state fallback
- Claude's self-assessment may have blind spots -- it might not recognize its own failures (the "styler" example: Claude kept building personal profile features instead of suggesting a fork, and might not realize in retrospect that this was wrong)
- The report quality depends on Claude's analytical capability at wind-down time (context window may be getting full)
- Adds session-end latency -- generating the report takes time, which may discourage users from running `/work pause`
- Sensitive project details may leak into the report (user must review before exporting)
- Not automated at the level the user wants -- requires the user to run `/work pause` rather than session-end export happening automatically

**Research Notes:**
- The handoff file's `session_knowledge` field already captures some of this ("User prefers explicit error messages..."). This option expands it into a full report.
- The 32K output token limit means the interaction report must be concise. For very long sessions, Claude may need to prioritize the most actionable friction moments.

---

### Option C: Hybrid Pipeline with Automated Markers + Periodic Claude-Assessed Reports

**Philosophy:** Combine Options A and B: automated friction markers run continuously and capture every session (including crashes), while Claude-generated interaction reports add the nuanced "why" layer at graceful exit points. The processing pipeline normalizes both data sources.

**Capture Mechanism (Dual-Track):**

**Track 1 -- Automated Friction Markers (every session):**
- Agents write friction markers to `.claude/support/workspace/.session-log.json` during execution (same as Option A)
- `/work pause` and PreCompact hook both include the session log in their export
- Covers: verification failures, workflow deviations, recovery events, user feedback, spec drift, decision events
- Always runs, even on crashes (markers are written during execution, not at session end)

**Track 2 -- Claude Interaction Assessment (graceful exits only):**
- `/work pause` includes a step where Claude generates a brief interaction assessment (shorter than Option B's full report):
  ```json
  {
    "design_pushback_opportunities": [
      "User pivoted from personal to public use case in session. Template should detect scope pivots and suggest branch/fork approach."
    ],
    "workflow_friction_notes": [
      "User repeatedly skipped spec check for minor changes. Consider a 'minor change' fast path."
    ],
    "unstructured_observations": "The project's domain (fashion/styling) means visual verification is important but guided testing only supports CLI and web screenshots."
  }
  ```
- This track adds the "things no marker can capture" insights

**Export Format:** Unified export that contains both tracks:
```json
{
  "export_version": 1,
  "source_project": "styler",
  "template_version": "1.5.0",
  "session_date": "2026-03-30",
  "automated_markers": [ /* Track 1 data */ ],
  "session_metrics": { /* aggregated from Track 1 */ },
  "claude_assessment": { /* Track 2 data, null if not available */ },
  "export_quality": "full | markers_only"
}
```

**Transport to Template Repo:**

Three sub-options for getting exports from source projects to the template repo:

**C1: Git-based push (automated).** The export command pushes to a dedicated branch on the template repo (e.g., `interaction-logs/{project-name}`). Uses the `template_repo` URL from `version.json`. Requires write access to the template repo.

**C2: Local filesystem path (semi-automated).** Configure a `template_inbox_path` in `version.json` pointing to a directory in the local template repo clone. The export command copies the file there. Works when both repos are on the same machine (common for solo developers). Simplest, fewest moving parts.

**C3: Manual copy with CLI prompt (manual).** After generating the export, display the file path and suggest: `"Interaction export ready at {path}. Copy to your template repo's interaction-logs/inbox/ when convenient."` Zero configuration needed.

**Processing Pipeline in Template Repo:**

```
interaction-logs/
  inbox/                    # Raw exports land here (any transport method)
  processed/                # Exports that have been analyzed
  insights/                 # Derived insights, grouped by template area
  pipeline.md               # Processing command definition
```

**Processing stages (new command: `/process-logs` or extension to `/feedback`):**

1. **Ingest** -- Read all files in `inbox/`. Validate format. Move invalid files to `inbox/.rejected/` with error notes.

2. **Categorize** -- Group friction events by template area:
   - `verify-agent` -- verification failures, false positives, missing checks
   - `implement-agent` -- workflow deviations, step skips, quality issues
   - `/work` -- routing problems, spec check friction, session recovery
   - `/iterate` -- spec change friction, missed drift
   - `design-guidance` -- pushback opportunities, scope pivot detection
   - `user-experience` -- dashboard confusion, command discoverability, interaction mode mismatches

3. **Aggregate** -- Across multiple sessions/projects, identify patterns:
   - Recurring friction events (same template area, different projects)
   - Trends over template versions (did a change help or hurt?)
   - Project-type correlations (software projects have different friction than non-software)

4. **Generate Insights** -- For each category with significant signal:
   ```markdown
   # Insight: Verify-agent cross-file consistency false positives

   **Evidence:** 3 occurrences across 2 projects (styler, siren)
   **Pattern:** Whitespace-only changes flagged as consistency failures
   **Affected file:** .claude/agents/verify-agent.md (cross-file check)
   **Suggested action:** Add whitespace normalization before comparison
   **Confidence:** High (clear pattern, specific fix)
   ```

5. **Route to `/feedback`** -- Insights above a confidence threshold are automatically captured as feedback items (status: `new`, with the insight markdown as the body). User reviews them through the normal `/feedback review` pipeline.

6. **Archive** -- Move processed exports to `processed/`. Retain for 90 days, then compress/delete.

**Integration with Existing Systems:**

| System | Integration Point |
|--------|------------------|
| `/feedback` | Insights from the pipeline are captured as FB-NNN items. User triages them through the normal 3-phase review. Items that pass impact assessment become `ready` for `/iterate`. |
| `/iterate` | When processing `ready` feedback items from interaction logs, `/iterate` has richer context -- it can reference the specific friction evidence. Spec changes are still propose-approve-apply. |
| `/health-check` | New substep: "Interaction Log Status" -- reports inbox items pending processing, recent insights generated, feedback items promoted from interaction data. Also: when running in the template repo, checks that the processing pipeline is configured and functional. |
| `/work pause` | Extended with Track 2 (Claude assessment). Handoff file now includes an `interaction_export_path` field so the next session knows an export was written. |
| PreCompact hook | Extended to write Track 1 markers to the export file (disk-state-only friction markers). |
| Template sync | When a source project syncs from the template, it gets the updated agent definitions that include friction marker emission. The sync mechanism itself is unchanged. |

**Strengths:**
- Best of both worlds: comprehensive automated coverage + nuanced Claude assessment
- Graceful degradation: crashes get markers only, graceful exits get full assessment
- Processing pipeline produces actionable insights, not raw data dumps
- Feeds into existing `/feedback` lifecycle -- no new decision workflow needed
- Cross-project aggregation reveals patterns invisible from a single project
- Configurable transport (git, filesystem, manual) accommodates different setups
- Privacy: user reviews exports before they leave the source project; processing in template repo works on anonymizable structured data

**Weaknesses:**
- Highest implementation complexity of the three options
- Requires changes across many files: agent definitions, `/work pause`, PreCompact hook, `/health-check`, and a new processing pipeline
- The marker taxonomy needs ongoing maintenance
- Track 2 (Claude assessment) still only fires on graceful exits
- Storage can accumulate if exports are not processed and archived
- The aggregation logic (detecting patterns across projects) is the most complex part and may need iteration to get right

**Research Notes:**
- The marker emission in agents could use a lightweight pattern: a utility function that appends a JSON line to the session log file. Agents already write to task JSON; this is one more structured write per significant event.
- The processing pipeline is most similar to the existing `/feedback review` 3-phase process. It could be a mode of `/feedback` (e.g., `/feedback ingest`) rather than a standalone command, reducing conceptual overhead.
- Transport sub-option C2 (local filesystem path) is the pragmatic starting point for a solo developer. C1 (git push) can be added later without changing the capture or processing sides.

---

### Option D: Lightweight Feedback Bridge (Minimal Viable Pipeline)

**Philosophy:** Minimize new infrastructure. Instead of building a full pipeline, create a lightweight bridge that makes it easy to carry feedback items from source projects to the template repo's existing `/feedback` system.

**Capture Mechanism:**
- No new session logging, no friction markers, no interaction reports
- Instead: rely on the existing `user_feedback` field on tasks, the `/feedback` items in source projects, and manual observation
- Add a new command to source projects: `/feedback export-to-template` that:
  1. Reads `feedback.md` for items tagged with `template-relevant` (new optional tag)
  2. Reads recent task JSONs for `user_feedback` content that mentions template/workflow issues
  3. Bundles these into a single export file
  4. Provides copy instructions (or writes to configured path)

**In the Template Repo:**
- `/feedback import` reads the export file and creates FB-NNN items in the template's `feedback.md`
- Normal `/feedback review` pipeline handles the rest

**Strengths:**
- Minimal implementation: two new command modes, no agent changes, no hooks changes
- Uses existing `/feedback` infrastructure end-to-end
- User explicitly tags what's template-relevant -- no noise, no privacy concerns
- Easy to understand and maintain
- Can be built incrementally: start with manual copy, add automation later

**Weaknesses:**
- Relies heavily on the user remembering to tag feedback as template-relevant
- Misses automated signal entirely: no friction markers, no verification failure patterns, no workflow deviation tracking
- Cannot identify the "styler" scenario -- where Claude should have pushed back but didn't -- because it requires recognizing patterns the user didn't explicitly flag
- Doesn't fulfill the "automated session-end export" requirement from FB-011
- Doesn't capture "full conversation history" -- captures user-authored feedback only
- The value proposition is marginal over just manually creating feedback items in the template repo

**Research Notes:**
- This option is included as the "simpler/cheaper" baseline. It demonstrates the minimum viable integration. However, it fundamentally does not address the core need: automated capture of friction moments the user did not explicitly flag.

---

## Discarded Options

### Full Conversation Transcript Export
**Discarded because:** Claude Code does not expose conversation history as an exportable artifact. There is no API, hook, or filesystem path that provides the raw conversation. The conversation exists in Claude Code's internal context management. Even if it were accessible, storing full transcripts (potentially hundreds of thousands of tokens per session) for multiple projects would create an impractical storage burden. The user's desire for "full conversation history" must be translated into the most complete structured representation achievable within the platform's constraints.

### Real-Time Streaming to Template Repo
**Discarded because:** Streaming interaction data during active sessions would require network connectivity, introduce latency, and create a dependency between source project work and template repo availability. It would also raise significant privacy concerns (all project content flowing to another repo in real time). Session-end export is both the user's stated preference and the technically sound approach.

### Claude Desktop Plugin/Extension
**Discarded because:** The template is for Claude Code (CLI), not Claude Desktop. While Claude Desktop is used for ideation (Phase 0), the execution phase where friction occurs is entirely in Claude Code. Additionally, Claude Code's extension/plugin system does not support this type of instrumentation.

---

## Cross-Cutting Concerns

### Privacy and Sensitivity

All options must handle the fact that interaction data may contain:
- Project-specific business logic, IP, or confidential information
- API keys or credentials mentioned in conversation (even if not committed)
- User personal information
- Client or stakeholder names

**Mitigation strategies (applicable to all options):**
1. **User review before export:** Never auto-push data to the template repo without user confirmation
2. **Structured over raw:** Friction markers and assessments are template-focused, not project-content-focused
3. **Scrubbing step:** The export process should strip or generalize project-specific details (e.g., "API endpoint /users/profile" becomes "API endpoint [redacted]")
4. **Local-first:** Default transport is local filesystem, not network push

### Conversation History Size

Claude Code sessions can exceed 100K tokens. For the "full history" desire:
- Option A captures ~1-5KB per session (structured markers only)
- Option B captures ~2-10KB per session (markers + short report)
- Option C captures ~3-15KB per session (both tracks)
- Option D captures ~0.5-2KB per session (feedback items only)

Even Option C's upper bound (15KB per session, ~50 sessions) is ~750KB -- manageable.

### The "Styler" Scenario

The motivating example: a user pivoted from personal to public use case, but Claude kept building with personal profile data instead of suggesting a fork/branch approach.

- **Option A:** Would not catch this unless "scope pivot" is a predefined friction marker type. Even then, the marker would record the pivot but not the "should have suggested forking" insight.
- **Option B:** Claude might identify this in retrospect during `/work pause`. However, Claude's self-assessment of its own failures is unreliable -- it may not realize the advice was wrong.
- **Option C:** Track 1 captures the scope change event (spec drift, out-of-spec tasks). Track 2 gives Claude a chance to reflect. Combined, they provide the best signal for this scenario.
- **Option D:** Only catches this if the user manually tags feedback about it. The user often doesn't realize the template should have intervened until much later.

### DEC-002 Compatibility

DEC-002 (UX evaluation criteria) is related: interaction logs could inform UX evaluation by showing where users experience friction with the dashboard, commands, and interaction flows. All options are compatible with DEC-002, but Option C's categorized friction data is most directly useful for UX evaluation criteria development.

---

## Evaluation Summary

| Criterion | A: Structured Markers | B: Checkpoint Reports | C: Hybrid Pipeline | D: Feedback Bridge |
|-----------|----------------------|----------------------|-------------------|-------------------|
| Capture reliability | Strong (every session) | Moderate (graceful only) | Strong (both tracks) | Weak (manual) |
| Data completeness | Moderate (predefined types) | Moderate (Claude-assessed) | Strong (both sources) | Weak (user-tagged only) |
| Privacy handling | Strong (structured, no raw content) | Moderate (report may leak) | Strong (structured + review) | Strong (user-controlled) |
| Automation level | Strong (markers auto, export auto) | Moderate (requires /work pause) | Strong (auto + graceful bonus) | Weak (mostly manual) |
| Integration quality | Good (feeds /feedback) | Good (feeds /feedback) | Strong (deep integration) | Good (uses /feedback directly) |
| Processing efficiency | Good (structured, parseable) | Moderate (markdown, needs parsing) | Good (unified format) | Good (already feedback items) |
| Storage burden | Low (~5KB/session) | Low (~10KB/session) | Low-moderate (~15KB/session) | Very low (~2KB/session) |
| Implementation complexity | Moderate (agent changes + pipeline) | Low (command extension) | High (all of the above) | Low (two command modes) |
| Overall | Strong | Moderate | Strong | Weak |

### Recommendation

**Option C (Hybrid Pipeline)** provides the strongest overall solution. It is the only option that addresses both the "automated capture" and "identify non-obvious friction" requirements from FB-011. However, its implementation complexity is the highest.

A pragmatic implementation path would be:
1. **Phase 1:** Implement Option A's friction markers in agents and the session-end export (gets automated capture working)
2. **Phase 2:** Add Option B's Claude assessment to `/work pause` (gets the nuanced insight layer)
3. **Phase 3:** Build the processing pipeline in the template repo (turns raw data into actionable feedback)

This phased approach delivers value at each step and can pause at Phase 1 if the complexity budget is exhausted.

**If implementation complexity is the primary constraint,** Option A (Structured Markers only) is a strong standalone choice that delivers most of the automated capture value without the Claude assessment layer. Option D is insufficient for the stated requirements.

**Confidence:** Moderate. The core constraint (no direct conversation export) is certain. The marker taxonomy and processing pipeline design will need iteration based on real usage data. The transport mechanism (C2: local filesystem) is straightforward, but cross-machine workflows would need C1 (git push), which adds complexity.
