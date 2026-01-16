# Task Difficulty Guide (Calibrated for Claude Opus 4.5)

Difficulty reflects task scope and uncertainty, not model capability. Opus 4.5 handles complex reasoning well - breakdown is for managing scope, not preventing errors.

## Scale Overview

| Level | Category | Break Down? |
|-------|----------|-------------|
| 1-2 | Routine | No |
| 3-4 | Standard | No |
| 5-6 | Substantial | No |
| 7-8 | Large scope | Yes |
| 9-10 | Multi-phase | Yes |

## Detailed Examples

### 1-2: Routine
Single-session tasks with clear scope.

- Fix bug with known cause
- Add field to existing form with validation
- Implement CRUD for new entity following existing patterns
- Refactor function for readability
- Add error handling to existing endpoint
- Write tests for existing module
- Update API to add optional parameter
- Add new page following existing layout patterns

### 3-4: Standard
Feature-level work with some decisions to make.

- Implement authentication with OAuth provider (Google, GitHub, etc.)
- Create new API endpoint with validation, error handling, tests
- Build form wizard with multi-step state management
- Add caching layer to existing service
- Implement webhook handler with retry logic
- Database migration adding tables with relationships
- Refactor module to use different state management pattern
- Integrate third-party API with good documentation

### 5-6: Substantial
Significant features requiring architectural decisions.

- Design and implement new service/module from scratch
- Add real-time features (WebSockets, SSE) to existing app
- Implement role-based access control system
- Build data pipeline with transformation and validation
- Create reporting system with aggregations and exports
- Multi-provider authentication with account linking
- Performance optimization with measurable targets
- Database schema redesign for new requirements

### 7-8: Large Scope - BREAK DOWN
Cross-cutting work affecting many parts of the system.

- Migrate monolith module to microservice
- Replace ORM/database layer across application
- Implement multi-tenancy in existing single-tenant app
- Add internationalization (i18n) throughout application
- Major version upgrade of framework with breaking changes
- Implement end-to-end encryption for existing data flows
- Convert REST API to GraphQL (or vice versa)
- Add comprehensive audit logging across all operations
- Integrate with legacy system lacking documentation

### 9-10: Multi-Phase - DEFINITELY BREAK DOWN
Projects requiring discovery, iteration, or coordination.

- Full application architecture redesign
- Data migration with business continuity requirements
- Security overhaul with compliance requirements (SOC2, HIPAA)
- Multi-system integration with inconsistent APIs
- Performance overhaul requiring profiling → optimization → validation cycles
- Distributed system implementation (consensus, eventual consistency)
- Platform migration (cloud provider, infrastructure)
- Implement disaster recovery with tested failover

## What Makes Tasks Hard for Opus 4.5

Not complexity of logic - Opus handles that well. Instead:

1. **Scale**: Changes touching >10-15 files benefit from chunking
2. **Discovery needed**: Can't plan without exploring first
3. **External dependencies**: Waiting on APIs, approvals, or systems you don't control
4. **Iteration required**: Need to measure, adjust, re-measure
5. **Coordination**: Multiple systems that must stay in sync
6. **Rollback complexity**: Changes that are hard to undo if wrong

## When to Break Down

Ask: "Can this be completed in one focused session with clear deliverables?"

- **Yes** → Difficulty 1-6, just do it
- **No, too much scope** → Difficulty 7-8, break into focused chunks
- **No, need to discover/iterate** → Difficulty 9-10, break into phases

## Breakdown Strategy

For 7-8 (scope):
- Split by module/area affected
- Each subtask = one coherent piece
- Subtasks can often run in parallel

For 9-10 (phases):
- Phase 1: Discovery/research
- Phase 2: Design/planning
- Phase 3+: Implementation chunks
- Final phase: Validation/cleanup
