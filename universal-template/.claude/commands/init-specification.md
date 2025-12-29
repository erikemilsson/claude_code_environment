# Command: init-specification

## Purpose
Initialize the specification development phase by setting up decision tracking categories, creating planning folder structure, and establishing templates.

## When to Use
- Starting a new project that needs a detailed specification
- Beginning the planning phase before implementation
- Setting up decision tracking framework

## Prerequisites
- Project folder exists with universal template copied
- planning/ folder exists (should be part of template)

## Process

### Step 1: Welcome and Explain
Explain to user:
- This command sets up the planning phase
- We'll define which types of decisions to track
- Templates will be created for specification development

### Step 2: Define Decision Categories
Ask user: "Which decision categories should we track for this project?"

Provide examples:
- **architecture**: System design, tech stack, design patterns
- **data**: Database selection, schema design, data modeling
- **integration**: API design, third-party services, message queues
- **security**: Authentication, authorization, encryption, compliance
- **infrastructure**: Cloud provider, CI/CD, monitoring
- **ux**: User experience, interaction patterns, accessibility
- **[custom]**: User can define custom categories

Iterate with user:
1. User selects from examples or proposes custom categories
2. For each category, ask: "What types of decisions belong in [category]?"
3. Confirm final list
4. Example final list:
   - architecture
   - data
   - integration
   - security

### Step 3: Create Planning Structure
Create the following files:

#### planning/.claude/context/decisions.md
```yaml
# Architectural Decisions

## Decision Categories

Categories to track for this project:
- **[category-1]**: [Description of what decisions belong here]
- **[category-2]**: [Description]
- **[category-3]**: [Description]

## Decisions

[No decisions yet - will be added as project evolves]

## Decision Matrix
| ID | Category | Question | Chosen | Status | Impacts |
|----|----------|----------|--------|--------|---------|
| [Empty - will be populated] |

## Change Log
- [Date]: Decision tracking categories defined during initialization
```

#### planning/.claude/context/phases.md
```yaml
# Project Phases

## Overview
[To be defined during specification development]

## Phase Definitions

[No phases yet - will be defined as specification evolves]

### Phase 1: [Phase Name - TBD]
- **ID**: phase-1
- **Order**: 1
- **Status**: pending
- **Inputs**: [TBD]
- **Outputs**: [TBD]
- **Components**: [TBD]
- **Related Tasks**: []
- **Related Decisions**: []

## Phase Flow Diagram
```
[To be defined]
```

## Change Log
- [Date]: Initial phase structure template created
```

#### planning/specification.md
```markdown
# [Project Name] Specification

## Document Information
- **Version**: 0.1.0
- **Created**: [Date]
- **Last Updated**: [Date]
- **Status**: Draft

## 1. Overview

### 1.1 Purpose
[What is this project trying to achieve?]

### 1.2 Scope
[What's included and what's not?]

### 1.3 Stakeholders
[Who is involved or affected?]

## 2. Architecture

### 2.1 System Overview
[High-level description of how the system works]

### 2.2 Phase Breakdown
[Reference to planning/.claude/context/phases.md]

### 2.3 Technology Stack
[Technologies being considered or chosen - link to decisions]

## 3. Requirements

### 3.1 Functional Requirements
[What must the system do?]

### 3.2 Non-Functional Requirements
[Performance, security, scalability, etc.]

## 4. Data Model

### 4.1 Data Flow
[How data moves through the system]

### 4.2 Schema Design
[Database/storage structure]

## 5. Integration

### 5.1 External Systems
[Third-party services, APIs]

### 5.2 API Design
[If applicable - how this system exposes data/functionality]

## 6. User Experience

### 6.1 User Flows
[Key user journeys]

### 6.2 Interface Requirements
[If applicable - UI/UX requirements]

## 7. Security & Compliance

### 7.1 Authentication & Authorization
[How users are identified and what they can access]

### 7.2 Data Protection
[Encryption, privacy, compliance requirements]

## 8. Testing Strategy

### 8.1 Validation Approach
[How will we verify this specification is complete?]

### 8.2 Test Coverage
[What aspects need testing?]

## 9. Open Questions
[Items that need clarification or decision]

- [ ] Question 1
- [ ] Question 2

## 10. References
[Related documents, external resources]

---

## Specification Change Log
- [Date]: Initial specification created
```

#### planning/CLAUDE.md
```markdown
# Planning Phase Instructions

This folder contains specification development and planning artifacts.

## Purpose
Iteratively develop the project specification before implementation begins.

## Key Files
- `specification.md` - The main specification document
- `.claude/context/decisions.md` - Track architectural decisions
- `.claude/context/phases.md` - Define project phase structure
- `tests/spec-test-*.md` - Specification validation tests

## Workflow
1. Develop specification.md iteratively
2. Document major decisions in .claude/context/decisions.md
3. Define phases in .claude/context/phases.md
4. Run /test-specification when ready to validate
5. Complete generated tasks to refine specification
6. Run /sync-from-planning to pull to main .claude/ when done

## Decision Categories
[Categories defined during initialization - reference .claude/context/decisions.md]

## Status
Phase: Planning (not yet building)
```

### Step 4: Confirm Completion
Show user what was created:
```
Created planning structure:
- planning/.claude/context/decisions.md (with [N] categories)
- planning/.claude/context/phases.md (template)
- planning/specification.md (template)
- planning/CLAUDE.md (instructions)
```

Ask: "Would you like to start developing the specification now?"

## Output Location
- `planning/.claude/context/decisions.md`
- `planning/.claude/context/phases.md`
- `planning/specification.md`
- `planning/CLAUDE.md`

## Post-Command Actions
User can now:
1. Start editing `planning/specification.md`
2. Add decisions to `planning/.claude/context/decisions.md`
3. Define phases in `planning/.claude/context/phases.md`
4. Run `/test-specification` when ready to validate

## Example Interaction

```
User: /init-specification

Claude: I'll help you set up the specification development phase.

This command will:
1. Define decision tracking categories
2. Create planning folder structure
3. Set up specification template

Which decision categories should we track? Here are common examples:
- architecture (system design, tech stack, patterns)
- data (databases, schemas, modeling)
- integration (APIs, third-party services)
- security (auth, encryption, compliance)
- infrastructure (cloud, CI/CD, monitoring)

You can choose from these or define your own. What categories make sense for your project?

User: Let's use architecture, data, and integration

Claude: Great! For each category:

**Architecture**: System design decisions, technology stack, design patterns
**Data**: Database selection, schema design, data modeling
**Integration**: API design, third-party service integration, messaging

Is this correct?

User: Yes

Claude: Perfect. I'll create the planning structure now.

[Creates files]

Created planning structure:
✓ planning/.claude/context/decisions.md (with 3 categories: architecture, data, integration)
✓ planning/.claude/context/phases.md (template)
✓ planning/specification.md (template with standard sections)
✓ planning/CLAUDE.md (planning phase instructions)

Your planning phase is ready!

Next steps:
1. Start developing planning/specification.md
2. Document decisions in planning/.claude/context/decisions.md
3. Define phases in planning/.claude/context/phases.md
4. Run /test-specification when you're ready to validate

Would you like to start working on the specification now?
```

## Notes
- This command only runs once per project (at the start)
- If planning/ already has content, ask user if they want to overwrite
- Decision categories can be expanded later, but should be thoughtfully chosen upfront
- The specification template is comprehensive - user can remove sections that don't apply
