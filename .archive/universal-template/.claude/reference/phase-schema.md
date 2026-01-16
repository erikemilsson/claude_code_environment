# Phase Tracking Schema

This document defines the standard structure for tracking project phases.

## Purpose

Phases represent major stages in the project lifecycle. Each phase has:
- Clear inputs and outputs
- Defined components that implement the phase
- Explicit ordering in the project flow
- Links to related tasks and decisions

## Schema Structure

```yaml
# Project Phases

## Overview
[Brief description of how the project is structured into phases]

## Phase Definitions

### Phase N: [Phase Name]
- **ID**: phase-N (unique identifier, used in task references)
- **Order**: N (numerical order in project flow)
- **Status**: active | pending | completed
- **Inputs**:
  - Input 1 description (what this phase receives)
  - Input 2 description
- **Outputs**:
  - Output 1 description (what this phase produces)
  - Output 2 description
- **Components**:
  - **component-N-1**: Component name and brief description
  - **component-N-2**: Component name and brief description
- **Related Tasks**: [task-XXX, task-YYY] (tasks implementing this phase)
- **Related Decisions**: [decision-XXX] (decisions affecting this phase)

## Phase Flow Diagram
```
phase-1 → phase-2 → phase-3
   ↓         ↓         ↓
output-1  output-2  output-3
```

## Change Log
- YYYY-MM-DD: [Description of change to phase structure]
```

## Field Definitions

### ID
- **Format**: `phase-N` where N is a number
- **Uniqueness**: Must be unique across all phases
- **Usage**: Referenced in task JSON files (`related_phases` field)
- **Immutability**: Should not change once tasks reference it

### Order
- **Format**: Positive integer (1, 2, 3, ...)
- **Purpose**: Defines sequence in project flow
- **Rules**:
  - Can be reordered if phase flow changes
  - Gaps allowed (1, 2, 5, 7 is valid)
  - Used for visualization and dependency understanding

### Status
- **Values**:
  - `pending`: Defined but not yet started
  - `active`: Currently being implemented
  - `completed`: All components finished
- **Auto-Update**: Consider updating when all related tasks are finished

### Inputs
- **Format**: List of descriptions (plain text)
- **Purpose**: Documents what this phase needs to start
- **Sources**: Can reference outputs from previous phases

### Outputs
- **Format**: List of descriptions (plain text)
- **Purpose**: Documents what this phase produces
- **Consumers**: Can be inputs to subsequent phases

### Components
- **Format**: `component-N-M: Description` where N is phase number, M is component number
- **Purpose**: Breaks phase into implementable pieces
- **Granularity**: Each component should be achievable in 1-3 tasks
- **Example**:
  - `component-1-1: CSV parser module`
  - `component-1-2: API authentication handler`

### Related Tasks
- **Format**: Array of task IDs `[task-001, task-002]`
- **Purpose**: Links phase to implementation work
- **Maintenance**: Update when tasks are created/completed
- **Verification**: All tasks should have `related_phases: ["phase-N"]` in their JSON

### Related Decisions
- **Format**: Array of decision IDs `[decision-001, decision-002]`
- **Purpose**: Links phase to architectural decisions that shaped it
- **Usage**: Helps understand why phase is structured this way

## Update Rules

### When to Update
- New phase added to project
- Phase order changes
- Phase components change
- Phase status changes (pending → active → completed)
- New tasks/decisions affect the phase

### How to Update
1. Make changes to `.claude/context/phases.md`
2. Run `/update-executive-summary`
3. Review proposed changes
4. Approve changes (Claude will update change log)
5. Run `/sync-tasks` to update task-overview.md

### Approval Required
Changes to phase structure are significant and require explicit approval:
- Adding/removing phases
- Changing phase order
- Changing inputs/outputs
- Adding/removing components

Status updates can be made without approval if obvious (all related tasks finished).

## Examples

### Example 1: Data Pipeline Project

```yaml
# Project Phases

## Overview
This data pipeline follows a three-phase approach: ingestion, transformation, and serving.

## Phase Definitions

### Phase 1: Data Ingestion
- **ID**: phase-1
- **Order**: 1
- **Status**: completed
- **Inputs**:
  - Raw CSV files from client SFTP server
  - API credentials for third-party data sources
- **Outputs**:
  - Normalized data in PostgreSQL staging schema
  - Ingestion logs in monitoring system
- **Components**:
  - **component-1-1**: CSV file parser with error handling
  - **component-1-2**: API connector for third-party sources
  - **component-1-3**: Data validation module
  - **component-1-4**: Staging database schema
- **Related Tasks**: [task-001, task-002, task-003, task-004]
- **Related Decisions**: [decision-001, decision-003]

### Phase 2: Data Transformation
- **ID**: phase-2
- **Order**: 2
- **Status**: active
- **Inputs**:
  - Normalized data from phase-1 staging schema
  - Business rules configuration
- **Outputs**:
  - Analytics-ready dataset in production schema
  - Data quality reports
- **Components**:
  - **component-2-1**: Business logic transformation layer
  - **component-2-2**: Data quality checks
  - **component-2-3**: Incremental update logic
- **Related Tasks**: [task-005, task-006, task-007]
- **Related Decisions**: [decision-002, decision-004]

### Phase 3: Data Serving
- **ID**: phase-3
- **Order**: 3
- **Status**: pending
- **Inputs**:
  - Analytics-ready dataset from phase-2
  - API request parameters
- **Outputs**:
  - REST API endpoints for data access
  - Dashboard refresh triggers
- **Components**:
  - **component-3-1**: FastAPI service layer
  - **component-3-2**: Query optimization module
  - **component-3-3**: Caching layer
- **Related Tasks**: [task-008, task-009]
- **Related Decisions**: [decision-005]

## Phase Flow Diagram
```
phase-1 (Ingestion) → phase-2 (Transformation) → phase-3 (Serving)
       ↓                       ↓                         ↓
  Staging DB            Production DB              REST API
```

## Change Log
- 2025-12-15: Initial phase structure defined
- 2025-12-20: Phase 1 marked as completed (all tasks finished)
- 2025-12-22: Split component-2-3 from component-2-1 for clarity
```

### Example 2: Web Application Project

```yaml
# Project Phases

## Overview
This web application follows a full-stack approach with separate frontend and backend phases, followed by integration.

## Phase Definitions

### Phase 1: Backend API Development
- **ID**: phase-1
- **Order**: 1
- **Status**: active
- **Inputs**:
  - Database schema design document
  - API specification (OpenAPI)
- **Outputs**:
  - RESTful API with authentication
  - PostgreSQL database with migrations
  - API documentation
- **Components**:
  - **component-1-1**: Express.js API server setup
  - **component-1-2**: Authentication middleware (JWT)
  - **component-1-3**: User management endpoints
  - **component-1-4**: Product catalog endpoints
  - **component-1-5**: Database models and migrations
- **Related Tasks**: [task-010, task-011, task-012, task-013, task-014]
- **Related Decisions**: [decision-006, decision-007, decision-008]

### Phase 2: Frontend Development
- **ID**: phase-2
- **Order**: 2
- **Status**: pending
- **Inputs**:
  - UI/UX design mockups
  - Component library selection
- **Outputs**:
  - React application with routing
  - Responsive UI components
  - State management setup
- **Components**:
  - **component-2-1**: React app scaffolding
  - **component-2-2**: Authentication pages (login, signup)
  - **component-2-3**: Product catalog pages
  - **component-2-4**: User dashboard
  - **component-2-5**: Redux state management
- **Related Tasks**: [task-015, task-016, task-017]
- **Related Decisions**: [decision-009, decision-010]

### Phase 3: Integration & Deployment
- **ID**: phase-3
- **Order**: 3
- **Status**: pending
- **Inputs**:
  - Completed backend API from phase-1
  - Completed frontend app from phase-2
- **Outputs**:
  - Integrated full-stack application
  - CI/CD pipeline
  - Deployed application on cloud platform
- **Components**:
  - **component-3-1**: API integration in frontend
  - **component-3-2**: End-to-end testing suite
  - **component-3-3**: Docker containerization
  - **component-3-4**: GitHub Actions CI/CD
  - **component-3-5**: AWS deployment configuration
- **Related Tasks**: [task-018, task-019, task-020]
- **Related Decisions**: [decision-011, decision-012]

## Phase Flow Diagram
```
        phase-1 (Backend)
               ↓
       Backend API + DB
               ↓
        phase-2 (Frontend) ─────→ React App
               ↓                       ↓
        phase-3 (Integration) ────→ Full-stack App
               ↓
        Deployed Application
```

## Change Log
- 2025-12-10: Initial phase structure defined
- 2025-12-18: Added component-1-5 for database migrations
```

## Common Patterns

### Parallel Phases
Some projects have phases that can run in parallel:

```yaml
### Phase 1: Backend Development
- **Order**: 1
- **Status**: active

### Phase 2: Frontend Development
- **Order**: 1  # Same order = can run in parallel
- **Status**: active

### Phase 3: Integration
- **Order**: 2
- **Inputs**:
  - Completed backend from phase-1
  - Completed frontend from phase-2
```

### Iterative Phases
Some projects repeat phases:

```yaml
### Phase 1: Feature Development (Iteration 1)
- **ID**: phase-1-iter1
- **Order**: 1

### Phase 2: User Testing & Feedback (Iteration 1)
- **ID**: phase-2-iter1
- **Order**: 2

### Phase 3: Feature Development (Iteration 2)
- **ID**: phase-1-iter2
- **Order**: 3
- **Inputs**:
  - Feedback from phase-2-iter1
```

### Conditional Phases
Some phases may be optional:

```yaml
### Phase 2a: Data Migration (if legacy system exists)
- **ID**: phase-2a
- **Order**: 2
- **Status**: pending
- **Note**: Only execute if migrating from legacy system
```

## Troubleshooting

### Problem: Too many components in one phase
**Solution**: Consider splitting into sub-phases (phase-2a, phase-2b)

### Problem: Unclear phase boundaries
**Solution**: Focus on outputs - what does each phase produce that the next phase needs?

### Problem: Tasks don't map to phases
**Solution**: Review component granularity - each component should map to 1-3 tasks

### Problem: Phases keep changing
**Solution**:
1. Expect this during planning phase
2. Once building starts, batch changes and update via `/update-executive-summary`
3. Document why changes were needed in change log
