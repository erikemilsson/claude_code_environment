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

## Process

### Step 1: Load Context

Read `../spec_v{N}.md` and assess its current state.

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

4. **Generate spec content:**
   - Include `vision_source:` in frontmatter linking to the vision doc
   - Extract concrete requirements from vision's abstract concepts
   - Add "Deferred to Future Phases" section for items not in Phase 1
   - Format as copy-pasteable content

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
- Acceptance criteria defined: ✓ / ✗
- Blocking questions resolved: ✓ / ✗

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

---

## Rules

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
