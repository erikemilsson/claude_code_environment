# Extras Guide

When and how to use the optional extras.

## Overview

The `extras/` folder contains templates and tools that aren't needed for every project. Copy what you need.

```
extras/
├── development/          # For coding projects
├── project-management/   # For life/PM projects
└── advanced/             # For complex projects
```

## development/

Templates for software development projects.

### source-of-truth-template.md

**Use when:**
- Multiple documentation sources (API docs, specs, etc.)
- Need to clarify which source takes precedence
- Working with regulatory or compliance documents

**Copy to:** `.claude/context/source-of-truth.md`

### assumptions-template.md

**Use when:**
- Making decisions based on incomplete information
- Need to track what needs validation
- Working with external systems you don't control

**Copy to:** `.claude/context/assumptions.md`

### llm-pitfalls-template.md

**Use when:**
- Domain has common LLM mistakes (regulatory, financial, etc.)
- Complex calculations or formulas
- Previous LLM errors you want to prevent

**Copy to:** `.claude/context/llm-pitfalls.md`

## project-management/

Templates for tracking phases, decisions, and handoffs.

### phases-template.md

**Use when:**
- Project has distinct phases (planning, execution, etc.)
- Need to track inputs/outputs between phases
- Multiple stakeholders need visibility

**Copy to:** `.claude/context/phases.md`

### decisions-template.md

**Use when:**
- Multiple important decisions to track
- Need to document rationale for choices
- Want to review decisions later

**Copy to:** `.claude/context/decisions.md`

### mermaid-overview-template.md

**Use when:**
- Need visual architecture diagrams
- Explaining project to stakeholders
- Complex data flows or dependencies

**Copy to:** `.claude/context/overview.md` (integrate diagrams)

### handoff-guide-command.md

**Use when:**
- Tasks split between Claude and human (e.g., Power BI, Excel)
- Need clear handoff points
- Collaborative workflow with dependencies

**Copy to:** `.claude/commands/generate-handoff-guide.md`

## advanced/

For complex projects needing specification development or agent-based routing.

### When to Use Advanced Extras

You probably **need** these if:
- Large project with multiple phases
- Need detailed specification before coding
- Complex features needing architecture design
- Team needs executive summaries

You probably **don't need** these if:
- Solo project
- Clear requirements
- Straightforward implementation

### agents/

Agent configurations for specialized tasks:
- `implementation-architect.md` - Design complex implementations
- `specification-architect.md` - Validate specifications
- `test-generator.md` - Generate test plans

**Use by:** Invoking via Task tool in Claude Code

### planning-workflow/

- `init-specification-command.md` - Set up specification development

**Use when:** Need to iterate on requirements before building

### executive-summaries/

- `update-executive-summary-command.md` - Keep high-level views current

**Use when:** Stakeholders need project status summaries

## How to Add Extras

1. Identify which extra you need
2. Copy the file to your project's `.claude/` folder
3. Customize for your project
4. Reference in CLAUDE.md if needed

Example:
```bash
# Add assumptions tracking
cp extras/development/assumptions-template.md my-project/.claude/context/assumptions.md

# Add phase tracking
cp extras/project-management/phases-template.md my-project/.claude/context/phases.md
```

## Don't Over-Engineer

The base/ template is sufficient for most projects. Only add extras when you actually need them. Each extra adds cognitive overhead.

**Start simple. Add complexity only when needed.**
