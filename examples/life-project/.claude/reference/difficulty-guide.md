# Task Difficulty Guide

Difficulty reflects task scope and complexity. Break down tasks with difficulty >= 7.

## Scale Overview

| Level | Category | Break Down? |
|-------|----------|-------------|
| 1-2 | Routine | No |
| 3-4 | Standard | No |
| 5-6 | Substantial | No |
| 7-8 | Large scope | Yes |
| 9-10 | Multi-phase | Yes |

## Examples

### 1-2: Routine
Single-step tasks with clear scope.

- Fix bug with known cause
- Add field to existing form
- Update configuration value
- Write docstring for function
- Add error handling to endpoint

### 3-4: Standard
Feature-level work with some decisions.

- Implement CRUD for new entity
- Create API endpoint with validation
- Add authentication with OAuth provider
- Database migration adding new table
- Integrate third-party API with docs

### 5-6: Substantial
Significant features requiring design decisions.

- Build new service/module from scratch
- Add real-time features (WebSockets)
- Implement role-based access control
- Create data pipeline with transformations
- Performance optimization with targets

### 7-8: Large Scope - BREAK DOWN
Cross-cutting work affecting many parts.

- Migrate module to microservice
- Replace database layer
- Add multi-tenancy support
- Implement i18n throughout app
- Major framework version upgrade

### 9-10: Multi-Phase - DEFINITELY BREAK DOWN
Projects requiring discovery and iteration.

- Full architecture redesign
- Security overhaul with compliance
- Multi-system integration
- Platform migration
- Disaster recovery implementation

## When to Break Down

Ask: "Can this be completed in one focused session?"

- **Yes** -> Difficulty 1-6, just do it
- **No, too much scope** -> Difficulty 7-8, break into chunks
- **No, need discovery** -> Difficulty 9-10, break into phases

## Breakdown Strategy

For 7-8 (scope):
- Split by module/area affected
- Each subtask = one coherent piece
- Subtasks can run in parallel

For 9-10 (phases):
- Phase 1: Discovery/research
- Phase 2: Design/planning
- Phase 3+: Implementation chunks
- Final: Validation/cleanup
