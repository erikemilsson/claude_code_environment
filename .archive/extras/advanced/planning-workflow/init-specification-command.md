# Init Specification Command

Use this command to set up a planning phase for complex projects.

## Purpose

Initialize the specification development phase by:
- Setting up decision tracking categories
- Creating planning folder structure
- Establishing specification templates

## When to Use

- Starting a new project that needs a detailed specification
- Beginning the planning phase before implementation
- Projects where requirements need iterative refinement

## Process

### Step 1: Define Decision Categories

Ask user which decision categories to track. Common examples:
- **architecture**: System design, tech stack, design patterns
- **data**: Database selection, schema design, data modeling
- **integration**: API design, third-party services
- **security**: Authentication, authorization, encryption
- **infrastructure**: Cloud provider, CI/CD, monitoring
- **ux**: User experience, interaction patterns

### Step 2: Create Planning Structure

Create these files:

```
planning/
├── specification.md         # Main specification document
├── CLAUDE.md                # Planning phase instructions
└── .claude/
    └── context/
        ├── decisions.md     # Decision tracking
        └── phases.md        # Phase definitions
```

### Step 3: Specification Template

Create `planning/specification.md` with these sections:

1. **Overview** - Purpose, scope, stakeholders
2. **Architecture** - System overview, phases, tech stack
3. **Requirements** - Functional and non-functional
4. **Data Model** - Data flow, schema design
5. **Integration** - External systems, APIs
6. **User Experience** - User flows, interface requirements
7. **Security** - Auth, data protection
8. **Testing Strategy** - Validation approach
9. **Open Questions** - Items needing clarification

### Step 4: Set Up Decision Tracking

Create `planning/.claude/context/decisions.md`:

```markdown
# Architectural Decisions

## Decision Categories

Categories to track:
- **[category-1]**: [Description]
- **[category-2]**: [Description]

## Decisions

[Decisions will be added as project evolves]

## Decision Matrix

| ID | Category | Question | Chosen | Status | Impacts |
|----|----------|----------|--------|--------|---------|
```

## Next Steps After Initialization

1. Start developing `planning/specification.md`
2. Add decisions to `decisions.md` as they're made
3. Define phases in `phases.md`
4. Run specification validation when ready
5. Complete refinement tasks before implementation

## Notes

- Run once per project at the start of planning phase
- Decision categories can be expanded later
- Specification template sections can be removed if not applicable
