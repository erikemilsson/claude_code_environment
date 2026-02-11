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

**Spec editing policy:** `suggest_only` — Claude suggests content, the user decides what goes in.

**DO NOT author spec content directly.** Only suggest changes for the user to make. This means Claude does not write requirements, acceptance criteria, scope definitions, or architecture decisions into the spec.

Claude **CAN** perform spec infrastructure operations: archiving, copying during version transitions, updating frontmatter metadata (version number, dates, status). See "Suggest-Only Boundary" in the Spec Versioning section below for the full distinction.

When suggesting content changes:
- Quote the specific section
- Explain what to change and why
- Provide copy-pasteable content
- Let the user make the edit

**Why this mode exists:** The spec is your anchor. If Claude authors content freely, it's easy to lose sight of what you originally wanted vs. what Claude decided to build. By requiring you to make content edits, you stay in control of scope and intent.

**Claude MUST NOT:**
- Author spec content (requirements, criteria, scope) directly
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

Determine the current spec version using the same version discovery as `/work`: glob for `.claude/spec_v*.md`, use the highest N. Read `.claude/spec_v{N}.md` and assess its current state.

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

**Implicit decision detection:** When assessing "Key decisions documented," don't just count existing decision records — scan the spec for language that implies unresolved choices. Look for:
- Vague method references ("appropriate methods," "a suitable library," "the chosen approach")
- Unnamed technology choices ("a database," "a charting library," "an auth provider")
- Conditional language ("depending on the analysis method," "if we use X")
- Alternatives mentioned without resolution ("could use X or Y")

For each implicit decision found:
1. Flag it in the readiness check (contributes to `Key decisions documented: ✗`)
2. In Step 3, ask questions that surface whether it's an inflection point or pick-and-go
3. In Step 4, suggest creating a decision record (see `support/reference/decisions.md`) rather than filling in the choice inline — decisions need to be trackable so `/work` can gate dependent tasks

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

### Core Invariant: One Spec File at a Time

There must always be exactly **one** `spec_v{N}.md` file in `.claude/`. Not two during a transition, not zero. One. This is enforced by `/health-check` and validated by `/work` on every run.

### Direct Edits Are Always Safe

You can edit the spec file directly at any time. The system handles this gracefully:

- **The decomposed snapshot** (`spec_v{N}_decomposed.md` in `previous_specifications/`) preserves the state when tasks were created
- **Drift detection** in `/work` compares the current spec against the snapshot and shows exactly what changed
- **No data loss is possible** — the "before" state is always available for comparison

You never need to version before editing. If your edits turn out to be substantial enough for a new version, `/work` will suggest it (see "Substantial Change Detection" in `work.md`).

### Suggest-Only Boundary: Content vs Infrastructure

The `suggest_only` policy applies to **spec content authorship** — Claude does not decide what to build.

**Claude CAN perform structural file operations:**
- Copy a spec to the archive (preserving content the user wrote)
- Create a new version file as a copy of the current one
- Update the frontmatter version number and dates
- Delete the old version file after archiving

**Claude CANNOT:**
- Write new spec sections or requirements
- Modify acceptance criteria, scope, or architecture decisions
- Remove sections the user wrote

This is the distinction between **infrastructure** (moving files, updating metadata) and **authorship** (deciding what gets built). The user controls what the spec says; Claude manages the filing system.

### Version Transition Procedure

When a version bump is warranted, Claude executes this 5-step procedure:

```
1. CONFIRM: "Suggest creating spec v{N+1}. Reason: {reason}. Proceed? [Y/N]"
   → User must approve — this is a checkpoint, not automatic

2. ARCHIVE: Copy .claude/spec_v{N}.md → .claude/support/previous_specifications/spec_v{N}.md

3. CREATE: Copy .claude/spec_v{N}.md → .claude/spec_v{N+1}.md
   → Bump frontmatter: version: {N+1}, status: draft, updated: {today}
   → New version starts in "draft" because new content needs review

4. REMOVE: Delete .claude/spec_v{N}.md
   → Single-spec invariant maintained

5. REPORT:
   "spec_v{N} archived → previous_specifications/spec_v{N}.md
    spec_v{N+1} is now the active spec (status: draft).
    Edit it with your changes, then run /iterate to review or /work to continue."
```

**After the transition:** The user edits `spec_v{N+1}.md` with their changes (or uses `/iterate` to refine). When they run `/work`, task migration handles the transition (see "Task Migration on Version Transition" in `work.md`).

### When to Create a New Version

| Trigger | Version bump? | Why |
|---------|:---:|-----|
| Phase transition (Phase N complete → N+1) | **Yes** | New work scope, clean baseline |
| Inflection point resolved, major scope change | **Yes** | What gets built changed fundamentally |
| User explicitly requests it | **Yes** | User authority |
| `/work` detects substantial changes (see work.md) | **Suggested** | System offers the choice; user decides |
| Adding detail to existing sections | No | Same scope, more precision |
| Minor clarifications, typos | No | Not substantive |
| Adding a new feature section | Maybe | Claude asks user if scope expansion warrants it |

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
   - spec_revised is NOT true (spec hasn't been updated for this decision yet)
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

4. After presenting spec suggestions, also suggest updating the decision record:
   │
   │  Also update the decision record frontmatter:
   │  Add `spec_revised: true` and `spec_revised_date: YYYY-MM-DD`
   │
   │  This tells `/work` that the spec now reflects this decision.
```

**Why `spec_revised` instead of time-based detection:** The previous approach used `decided date is recent (within last 7 days)` which breaks across long session gaps and has no durable record of when `/iterate` last ran. The `spec_revised` field is a state-based signal — both `/work` and `/iterate` check it, and it persists until the user explicitly marks the spec as updated. This makes inflection point handling reliable across any number of sessions.

This auto-detection means the user doesn't need to remember which decisions were inflection points or manually trigger a review. Running `/iterate` after `/work` suggests it is sufficient.

---

## Spec Versioning at Phase Transitions

When Phase 1 completes and Phase 2 begins, Claude executes the Version Transition Procedure (above) to create `spec_v{N+1}.md`. Phase transitions always warrant a new version — they represent a clean baseline for new work.

**After the version transition**, `/iterate` should suggest a spec revision if:

- Phase 2 sections are vague or placeholder-level
- Decisions resolved during Phase 1 affect Phase 2 scope
- Phase 1 learnings suggest Phase 2 adjustments

**Process:**
1. `/work` detects Phase 1 completion → executes Version Transition Procedure → suggests running `/iterate`
2. `/iterate` reads the new spec version, focuses on Phase 2 sections
3. Asks targeted questions about Phase 2 scope (now informed by Phase 1 results)
4. Suggests spec content for the user to add to `spec_v{N+1}.md`
5. User edits spec, then runs `/work` to decompose Phase 2 and continue
