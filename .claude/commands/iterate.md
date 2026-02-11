# Iterate Command

Structured spec review that identifies gaps, asks focused questions, and suggests content for you to add.

## Usage

```
/iterate                    # Continue building the spec (auto-detects what's needed)
/iterate {topic}            # Focus on a specific area
/iterate distill            # Extract buildable spec from vision document
```

## What It Does

1. **Reads current spec** and assesses completeness
2. **Determines mode:**
   - Empty/placeholder spec → Bootstrap mode (foundational questions)
   - Partial spec → Identify weakest area and improve it
3. **Asks up to 4 questions** about the focus area
4. **Generates suggested content** based on your answers
5. **You edit the spec** with the suggestions
6. **Repeat** until spec is ready

---

## Rules

**Spec editing policy:** `suggest_only` — Claude suggests changes, the user makes edits.

**DO NOT edit the specification directly.** Only suggest changes for the user to make.

When suggesting changes:
- Quote the specific section
- Explain what to change and why
- Provide copy-pasteable content
- Let the user make the edit

**Why this mode exists:** The spec is your anchor. If Claude edits freely, it's easy to lose sight of what you originally wanted vs. what Claude decided to build. By requiring you to make edits, you stay in control of scope and intent.

**Claude MUST NOT:**
- Edit the spec file directly
- Skip the question step and jump to suggestions
- Ask more than 4 questions at once
- Generate suggestions before receiving answers

**Claude MUST:**
- Assess spec state before diving into questions
- Match rigor to stated project seriousness
- Format suggestions as copy-pasteable content
- Report readiness status when spec has substance

---

## Process

### Step 1: Load Context

Read `.claude/spec_v{N}.md` and assess its current state.

### Step 2: Determine Mode

**If user specified `/iterate distill`:**

Enter distill mode. Extract buildable spec from a vision document.

1. **Locate vision doc:**
   - Check `.claude/vision/` for existing documents
   - If multiple exist, list them and ask which to use
   - If none exist, ask user to provide the document (paste or file path)

2. **Read and summarize the vision:**
   ```
   I've read your vision document: [filename]

   Summary: [2-3 sentence summary of core concept]

   Key themes I see:
   - [theme 1]
   - [theme 2]
   - [theme 3]
   ```

3. **Ask distillation questions:**
   ```
   Let's extract a buildable Phase 1 spec.

   1. What's the core value proposition in one sentence?
      (From your vision, I see: "[extracted summary]" - confirm or refine?)

   2. What must be working for this to be useful at all?
      (Your vision mentions several features - which are essential vs. nice-to-have for Phase 1?)

   3. What's explicitly NOT in Phase 1?
      (Your vision has ambitious ideas - which do we defer?)

   4. Who's the first user and what's their critical path?
   ```

4. **Carry structure through from vision doc:**

   When reading the vision document, recognize and preserve these structures:

   - **Phases:** If the vision describes natural boundaries ("build the pipeline first, then the dashboard"), structure the spec with phase sections (e.g., `## Phase 1: Data Pipeline`, `## Phase 2: Visualization`). Phases become the grouping mechanism for tasks during decomposition.
   - **Key Decisions:** If the vision identifies choices with multiple options, create placeholder sections in the spec noting work is blocked until the decision is resolved. For each decision, note:
     - What options are being considered
     - What depends on this decision
     - Whether it's an **inflection point** (outcome changes what gets built) — if so, don't add premature detail for dependent work
   - **Human Dependencies:** If the vision identifies things only the user can do (set up accounts, configure hosting, get API keys), flag these as human tasks in the spec.

5. **Generate spec content:**
   - Include `vision_source:` in frontmatter linking to the vision doc
   - Extract concrete requirements from vision's abstract concepts
   - Structure spec sections by phase when phases were identified
   - Add decision placeholders where unresolved choices block work
   - Add "Deferred to Future Phases" section for items not in Phase 1
   - Format as copy-pasteable content for the user to add to the spec

5. **Post-distill next steps:**
   ```
   Distillation complete. Here's what to do next:

   1. Review the suggested content above
   2. Copy it into your spec file (.claude/spec_v{N}.md)
   3. Edit to match your intent — the suggestions are a starting point
   4. Run /iterate to refine specific sections
   5. When the spec passes readiness checks, run /work
   ```

**Output handling:** Distill generates suggested content for you to paste into the spec. It does not auto-create or edit spec files (respects `spec_editing: suggest_only`).

**Re-running distill:** If the vision document is updated:
- Run `/iterate distill` again
- Claude reads the updated vision doc and generates new suggestions
- You merge the new suggestions into the existing spec manually
- No automatic replacement or versioning occurs — you stay in control

**Multiple vision documents:** If `.claude/vision/` contains multiple files, Claude lists them and asks which to use. To combine multiple vision docs, run distill once per document and merge the suggestions.

---

**If spec is empty or only has placeholders:**

Enter bootstrap mode. Start with foundational questions:

```
The spec is empty. Let's build it from the ground up.

1. In one sentence, what does this project do?

2. Who will use this? (Be specific - role or persona, not just "users")

3. What's the core problem this solves?

4. How serious/complete does this project need to be?
   (Quick prototype, MVP for real users, production-grade system, etc.)
```

The answer to #4 calibrates the entire spec process - a prototype needs less rigor than a production system.

**If spec has content:**

Assess readiness and identify the weakest area. Report:

```
Checking spec readiness...

Current state:
- Has clear problem statement: ✓ / ✗
- Users identified: ✓ / ✗
- Core components described: ✓ / ✗
- Key decisions documented: ✓ / ✗
  - Resolved decisions: N (no blocker)
  - Pending decisions not blocking Phase 1: N (noted, not urgent)
  - Pending decisions blocking Phase 1: N ⚠️ (must resolve before /work)
  - Unresolved inflection points: N 🔴 (spec sections may be premature)
- Acceptance criteria defined: ✓ / ✗
- Blocking questions resolved: ✓ / ✗
- Phase boundaries clear: ✓ / ✗ / N/A
  - Phase dependencies make sense: ✓ / ✗
  - No Phase 2 content mixed into Phase 1: ✓ / ✗

Overall: Ready for /work | Needs more detail | Major gaps

Focusing on: [weakest area]
```

### Step 3: Ask Questions (max 4)

Generate focused questions for the target area. Questions should:
- Be specific and answerable
- Build on each other logically
- Extract concrete details, not opinions
- Include example answers when helpful

**Wait for user responses before proceeding.**

### Step 4: Generate Suggestions

Based on answers, generate spec-ready content:

```
## Suggested Content

Based on your answers, here's what to add to the spec:

---

[Copy-pasteable content formatted for the spec]

---

Copy the above into your spec, then modify as needed.
```

### Step 5: Continue or Finish

After presenting suggestions:

```
Edit the spec with these suggestions (modify as needed).

When ready, run /iterate again to continue, or focus on a specific area.
```

---

## Principles for Good Questions

Rather than following a script, Claude should:

1. **Establish fundamentals first** - Who uses it, what problem it solves, before diving into technical details
2. **Match depth to project seriousness** - A prototype doesn't need the same rigor as a production system
3. **Uncover constraints early** - Technology limits, timeline, dependencies shape everything
4. **Push for specificity** - "Users can log in" → "Users log in with email/password; errors shown within 2s"
5. **Identify the critical path** - What must work for this to be useful at all?

---

## Readiness Indicators

A spec is ready for `/work` when:

- [ ] The core problem and users are clear
- [ ] You could explain the system to someone in 2 minutes
- [ ] Key technical decisions are made (not deferred)
- [ ] You know what "done" looks like (acceptance criteria)
- [ ] Remaining questions won't block starting work

The threshold depends on project seriousness:
- **Prototype:** Problem and basic approach clear
- **MVP:** Above + key decisions made, acceptance criteria exist
- **Production:** Above + non-functional requirements, constraints documented

See `.claude/support/reference/spec-checklist.md` for full readiness criteria.

---

## When to Use Each Mode

| Situation | Command | Why |
|-----------|---------|-----|
| Starting from scratch, no docs | `/iterate` | Bootstrap mode asks foundational questions |
| Have a vision/design document | `/iterate distill` | Extracts buildable scope from abstract ideas |
| Spec exists, want to improve | `/iterate` | Auto-detects weakest area |
| Spec exists, specific gap known | `/iterate {topic}` | Focuses on that area |
| Adding a new feature to existing spec | `/iterate {feature}` | Targets the new section |
| Vision doc updated after initial distill | `/iterate distill` | Re-read vision and suggest updates |

**Note on distill questions:** The four distillation questions are intentionally fixed (core value, essential features, Phase 1 exclusions, first user path). These cover the minimum information needed to convert abstract vision into buildable scope. The answers are what vary — Claude adapts its generated content based on your responses.

---

## Spec Versioning

When changes are significant enough to warrant a new spec version (major scope changes, phase transitions, substantial rewrites), follow this process:

### Before Creating New Version

1. **Archive current spec**: Copy `.claude/spec_v{N}.md` to `.claude/support/previous_specifications/spec_v{N}.md`
2. **Create new spec**: Write the new version as `.claude/spec_v{N+1}.md`
3. **Update references**: Dashboard and tasks will reference the new version

**When to create a new version:**
- Major scope changes or pivots
- Transitioning between project phases
- Substantial rewrites that change multiple sections
- User explicitly requests a new version

**When NOT to create a new version:**
- Minor clarifications or fixes
- Adding details to existing sections
- Typo corrections

**Note:** Since spec editing is `suggest_only`, Claude suggests the new version content; the user creates and saves the files. When suggesting a new version, remind the user to archive the current spec first.

---

## Working with Vision Documents

Vision documents capture ideation, design philosophy, and future thinking. Common sources:
- Brainstorming sessions in Claude Desktop
- Product thinking documents
- Technical architecture explorations

**Distillation workflow:**
1. Save vision doc to `.claude/vision/`
2. Run `/iterate distill`
3. Answer questions to extract Phase 1 scope
4. Spec links to vision via `vision_source:` frontmatter

**Once a spec exists, the spec is the single source of truth.** Vision docs become historical context only—useful for understanding original intent or planning future phases, but not consulted during implementation.

---

## Post-Inflection-Point Re-Entry

When `/iterate` runs, it automatically checks for recently resolved inflection point decisions. No special subcommand is needed — `/iterate` just notices.

**Detection logic:**
```
1. Read all decision-*.md files in .claude/support/decisions/
2. Find decisions where:
   - inflection_point: true in frontmatter
   - status is "approved" or "implemented"
   - decided date is recent (within last 7 days or since last /iterate run)
3. IF any found:
   │
   │  Inflection point resolved: {decision_title}
   │  Selected: {chosen_option}
   │
   │  This decision changes what gets built. Let me review
   │  the spec sections affected by this choice.
   │
   │  Affected sections:
   │  - {section 1} — {how it's affected}
   │  - {section 2} — {how it's affected}
   │
   │  Suggested adjustments:
   │  [Copy-pasteable content reflecting the decision outcome]
```

This auto-detection means the user doesn't need to remember which decisions were inflection points or manually trigger a review. Running `/iterate` after `/work` suggests it is sufficient.

---

## Spec Versioning at Phase Transitions

When Phase 1 completes and Phase 2 begins, the spec may need additional detail for Phase 2 work. `/iterate` should suggest a spec revision if:

- Phase 2 sections are vague or placeholder-level
- Decisions resolved during Phase 1 affect Phase 2 scope
- Phase 1 learnings suggest Phase 2 adjustments

**Process:**
1. `/work` detects Phase 1 completion → suggests running `/iterate`
2. `/iterate` reads the spec, focuses on Phase 2 sections
3. Asks targeted questions about Phase 2 scope (now informed by Phase 1 results)
4. Suggests spec updates, potentially as a new spec version if changes are substantial
5. User edits spec, then runs `/work` to continue into Phase 2
