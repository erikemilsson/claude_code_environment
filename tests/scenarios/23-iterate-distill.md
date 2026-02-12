# Scenario 23: `/iterate distill` — Vision Document to Spec

Verify that `/iterate distill` correctly transforms a vision document into a buildable specification, preserving intent while adding structure.

## Context

Vision documents capture intent and philosophy from ideation sessions (e.g., Claude Desktop brainstorming). They're often conversational, aspirational, and lack the structure needed for task decomposition. `/iterate distill` bridges this gap: it reads the vision, asks clarifying questions, and generates spec content that preserves the original vision's intent while adding buildable structure. The vision doc is preserved — distill produces suggestions, not replacements.

## State (for 23A-23C)

- `.claude/vision/product-vision.md` exists with:
  - Project name and mission statement
  - 3 high-level goals (conversational, not structured as phases)
  - Mentions of "real-time sync", "offline support", "plugin system"
  - A section on "vibes" / design philosophy
  - No frontmatter, no phase structure, no acceptance criteria
- No spec file exists yet (greenfield)
- No tasks exist

---

## Trace 23A: Vision discovery and summarization

- **Path:** /iterate distill process

### Scenario

User runs `/iterate distill`. One vision doc exists in `.claude/vision/`.

### Expected

1. Vision doc located automatically in `.claude/vision/`
2. Claude reads and produces a 2-3 sentence summary + key themes
3. Summary captures the intent faithfully — not just keywords, but the "why"
4. Design philosophy / vibes section acknowledged (not discarded as non-technical)

### Pass criteria

- [ ] Vision doc discovered without user specifying path
- [ ] Summary is concise but captures core intent
- [ ] All major themes identified (real-time sync, offline, plugins)
- [ ] Non-functional aspects (design philosophy) preserved in summary

### Fail indicators

- User must specify exact file path
- Summary is just a list of features (misses the "why")
- Design philosophy section ignored as irrelevant
- Multiple vision docs cause confusion instead of prompting user to choose

---

## Trace 23B: Distillation questions and structure extraction

- **Path:** /iterate distill questions and structure extraction

### Scenario

After summarization, Claude asks the 4 distillation questions and maps vision structure to spec structure.

### Expected

1. Four questions asked:
   - Core value proposition (what makes this worth building?)
   - Essential features for v1 (what's the minimum?)
   - Phase 1 exclusions (what explicitly waits?)
   - First user path (what does a user do first?)
2. User answers inform spec structure
3. Structure carried from vision:
   - Natural boundaries become phases (e.g., "core sync" → Phase 1, "plugins" → Phase 2)
   - Mentioned decisions become placeholder sections noting blocked work
   - Human dependencies flagged (e.g., "need to choose sync protocol")

### Pass criteria

- [ ] All 4 distillation questions asked
- [ ] User answers directly shape the spec output
- [ ] Phase boundaries derived from vision's natural structure, not imposed artificially
- [ ] Decisions and human dependencies identified and flagged
- [ ] Exclusions explicitly listed (not silently dropped)

### Fail indicators

- Generic questions unrelated to the vision content
- Spec structure ignores user's answers
- Everything crammed into one phase (no phase extraction)
- Decisions hidden in prose instead of flagged as blocking items

---

## Trace 23C: Spec generation and handoff

- **Path:** /iterate distill spec generation

### Scenario

Distillation complete. Claude generates spec content.

### Expected

1. Generated spec includes:
   - Frontmatter with `vision_source: .claude/vision/product-vision.md`
   - Phase structure derived from distillation
   - Acceptance criteria for each section (derived from vision goals)
   - Decision placeholders where choices are needed
   - Status: `draft`
2. Content presented as suggestion — user copies/edits into `spec_v1.md`
3. Vision doc preserved unchanged in `.claude/vision/`
4. Next steps listed: review → copy to spec → edit → `/iterate` to refine → `/work`

### Pass criteria

- [ ] `vision_source` in frontmatter links back to origin
- [ ] Spec content is buildable (has acceptance criteria, not just descriptions)
- [ ] User instructed to copy and edit — Claude doesn't write spec directly
- [ ] Vision doc not modified or moved
- [ ] Clear next-step guidance provided

### Fail indicators

- Claude writes directly to `spec_v1.md` (violates suggest-only boundary)
- Generated spec is just the vision doc reformatted (no added structure)
- No acceptance criteria (not decomposable into tasks)
- Vision doc deleted or archived prematurely
- `vision_source` missing from frontmatter

---

## Trace 23D: Re-running distill after vision update

- **Path:** /iterate distill re-run

### Scenario

User updated `product-vision.md` after initial distillation (added a section on accessibility requirements). User runs `/iterate distill` again. `spec_v1.md` already exists with content from the first distillation.

### Expected

1. Claude reads the updated vision doc
2. Detects existing spec — does NOT overwrite or replace
3. Generates new suggestions based on the full updated vision (stateless re-distillation, not incremental diff)
4. User merges manually (no automatic replacement of spec content)

### Pass criteria

- [ ] Existing spec not overwritten or replaced
- [ ] New suggestions generated from the full updated vision
- [ ] User responsible for merging (suggest-only boundary maintained)
- [ ] Stateless design: no dependency on remembering previous distillation output

### Fail indicators

- Existing spec overwritten with new distillation output
- Claude edits spec directly with new content
- Distillation fails because it can't find previous distillation state
- Previous spec content lost during re-distillation
