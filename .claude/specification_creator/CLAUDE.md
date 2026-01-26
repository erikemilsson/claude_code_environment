# Specification Creator

## Configuration

```
spec_editing: suggest_only
```

- `suggest_only` - Claude suggests changes, user makes edits (default)
- `with_permission` - Claude may edit spec after explicit user approval

---

Active spec: `../spec_v{N}.md` - this is the source of truth.

## Commands

- `/iterate` - Structured spec review (checks gaps, asks questions, suggests content)
- `/iterate {section}` - Focus on specific section (overview, architecture, requirements, acceptance, questions)

See `commands/iterate.md` for full usage.

## Rules

**Spec editing policy:** Controlled by `spec_editing` in Configuration above.

### If `suggest_only` (default)

**DO NOT edit the specification directly.** Only suggest changes for the user to make.

When suggesting changes:
- Quote the specific section
- Explain what to change and why
- Provide copy-pasteable content
- Let the user make the edit

**Why this mode exists:** The spec is your anchor. If Claude edits freely, it's easy to lose sight of what you originally wanted vs. what Claude decided to build. By requiring you to make edits, you stay in control of scope and intent.

### If `with_permission`

Claude may edit the spec, but **must ask explicit permission before each edit**.

Before editing:
- State the section to be changed
- Explain what will change and why
- Ask "Can I make this edit?" and wait for confirmation
- Only proceed after explicit "yes"

**Why this mode exists:** For users who prefer faster iteration and trust Claude to propose reasonable changes, while maintaining a checkpoint before each modification.

## Spec Readiness

Before a spec can move to task decomposition (`/work`), it must pass the readiness checklist.

See `reference/spec-checklist.md` for:
- Required criteria per section
- Red flags that indicate incomplete sections
- Readiness levels (Not Ready → Minimally Ready → Well-Defined)

## Workflow

### Using /iterate (Recommended)

1. Run `/iterate` to auto-detect the weakest area, or `/iterate {section}` to focus
2. Answer Claude's questions (max 4 at a time)
3. Review Claude's suggested content
4. Edit the spec yourself with the suggestions
5. Run `/iterate` again or specify next section
6. Repeat until checklist passes

### Freeform Discussion

For exploratory conversations:
1. Read the current spec thoroughly
2. Identify one area to discuss
3. Ask clarifying questions (max 4 at a time)
4. Suggest specific, copy-pasteable changes
5. Wait for user to make edits
6. Repeat for next area

## Question Guidelines

When asking questions:
- Maximum 4 questions at a time
- Be specific and answerable
- Build on each other logically
- Extract concrete details, not opinions
- Show example answers when helpful

## Archive

Store research, notes, and planning documents in `.archive/`.

```
.archive/
├── YYYY-MM-DD_topic.md           # General research/notes
├── YYYY-MM-DD_task-name.md       # Task-specific documents
└── YYYY-MM-DD_questions.md       # Question logs
```

**Note:** This `.archive/` is for spec-session working documents. Formal decision records go in `.claude/support/decisions/`.

## Decision Documentation

Significant decisions made during spec creation should be documented:

1. **In the spec** - Key architecture and technology choices belong in the spec itself
2. **In decision records** - For choices that required research or comparison of options

When suggesting spec additions involving technology/architecture decisions:
- Note if a decision record would be valuable
- Reference `.claude/support/reference/decision-guide.md` for when to create records

## Where Decisions Go

| What | Where | Example |
|------|-------|---------|
| **Outcome** (what was chosen + brief rationale) | In the spec | "PostgreSQL for storage (relational model, team familiarity)" |
| **Process** (options compared, research, tradeoffs) | In `../support/decisions/` | Full comparison of Postgres vs. Mongo vs. DynamoDB |

**Rule of thumb:** If you can explain it in one sentence, it stays in the spec. If you researched or compared options, create a decision record.

## Structure

```
specification_creator/
├── CLAUDE.md              # This file (rules for spec sessions)
├── README.md              # How to use this system
├── commands/
│   └── iterate.md         # /iterate command definition
├── reference/
│   └── spec-checklist.md  # Readiness criteria
└── .archive/              # Session working documents
```
