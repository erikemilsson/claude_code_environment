# Mermaid Chart Patterns

Reusable diagram patterns for project documentation. Copy and adapt as needed.

---

## 1. Workflow Phases

Shows sequential phases with sub-steps. Good for documenting development workflows, deployment pipelines, or user journeys.

```mermaid
flowchart TD
    subgraph PHASE1["Phase 1: Planning"]
        P1[Define requirements] --> P2[Create spec]
        P2 --> P3[Review & approve]
    end

    subgraph PHASE2["Phase 2: Implementation"]
        I1[Task decomposition] --> I2[Build features]
        I2 --> I3[Integration]
    end

    subgraph PHASE3["Phase 3: Verification"]
        V1[Test against spec] --> V2[Fix issues]
        V2 --> V3[Final review]
    end

    PHASE1 --> PHASE2
    PHASE2 --> PHASE3
```

**Customization points:**
- Phase names and count
- Steps within each phase
- Arrow labels for conditions (`-->|condition|`)

---

## 2. Decision Dependencies

Shows how choices flow from design to implementation. Good for visualizing the relationship between spec-level and implementation-level decisions.

```mermaid
graph TD
    subgraph Spec["Spec-Level Choices"]
        S1((Auth Strategy))
        S2((Data Model))
        S3((API Design))
    end

    subgraph Impl["Implementation-Level Choices"]
        I1[Auth Library]
        I2[Database Engine]
        I3[API Framework]
        I4[ORM Selection]
    end

    S1 -->|determines| I1
    S2 -->|determines| I2
    S2 -->|determines| I4
    S3 -->|determines| I3

    classDef spec fill:#e1f5fe,stroke:#01579b
    classDef impl fill:#fff3e0,stroke:#e65100
    class S1,S2,S3 spec
    class I1,I2,I3,I4 impl
```

**Customization points:**
- Node shapes: `(( ))` for circles, `[ ]` for rectangles, `{ }` for diamonds
- Colors via `classDef` and `class`
- Relationship labels

---

## 3. Task Status Distribution

Shows task distribution across statuses. Good for quick project health overview.

```mermaid
pie title Task Status
    "Complete" : 15
    "In Progress" : 2
    "Pending" : 8
    "Blocked" : 3
```

**Customization points:**
- Title text
- Category names and values
- Use actual task counts from your project

---

## 4. Component Architecture

Shows system components and their relationships. Good for high-level system overview.

```mermaid
graph LR
    subgraph Frontend
        UI[UI Layer]
        State[State Management]
    end

    subgraph Backend
        API[API Server]
        Auth[Auth Service]
        DB[(Database)]
    end

    subgraph External
        OAuth[OAuth Providers]
        Email[Email Service]
    end

    UI --> State
    State --> API
    API --> Auth
    Auth --> OAuth
    API --> DB
    API --> Email
```

**Customization points:**
- Direction: `graph LR` (left-right), `graph TD` (top-down)
- Subgraph groupings
- Node shapes for different component types
- Bidirectional arrows: `<-->`

---

## 5. Progress Timeline (Gantt)

Shows project timeline with phases and dependencies. Good for planning and status communication.

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Planning
        Spec creation     :done, p1, 2026-01-01, 7d
        Spec review       :done, p2, after p1, 3d
    section Implementation
        Core features     :active, i1, after p2, 14d
        Integration       :i2, after i1, 7d
    section Verification
        Testing           :v1, after i2, 5d
        Release           :v2, after v1, 2d
```

**Customization points:**
- Task status: `done`, `active`, `crit` (critical), or omit for future
- Duration: `7d`, `2w`, or specific dates
- Dependencies: `after taskId`

---

## 6. State Machine

Shows states and transitions. Good for documenting task lifecycles, user flows, or system states.

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> InProgress: Start work
    InProgress --> AwaitingVerification: Complete
    InProgress --> Blocked: Dependency found
    Blocked --> InProgress: Unblocked
    AwaitingVerification --> Finished: Verified
    AwaitingVerification --> InProgress: Failed verification
    Finished --> [*]
```

**Customization points:**
- State names
- Transition labels
- Start `[*]` and end `[*]` markers

---

## 7. Sequence Diagram

Shows interactions over time. Good for API flows, auth sequences, or multi-service interactions.

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Database

    User->>Frontend: Click login
    Frontend->>API: POST /auth/login
    API->>Database: Validate credentials
    Database-->>API: User record
    API-->>Frontend: JWT token
    Frontend-->>User: Redirect to dashboard
```

**Customization points:**
- Participant names
- Arrow types: `->>` (solid), `-->>` (dashed), `-x` (cross)
- Notes: `Note over A,B: text`
- Loops: `loop Every minute`

---

## 8. Entity Relationship

Shows data model relationships. Good for database schema documentation.

```mermaid
erDiagram
    USER ||--o{ POST : creates
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has
    POST }o--|| CATEGORY : belongs_to

    USER {
        int id PK
        string email
        string name
        datetime created_at
    }
    POST {
        int id PK
        int user_id FK
        int category_id FK
        string title
        text content
    }
```

**Customization points:**
- Relationship cardinality: `||` (one), `o{` (many), `|{` (one or more)
- Entity attributes with types
- Primary/foreign key markers

---

## Usage Tips

### Keep Diagrams Focused
One concept per diagram. If a diagram needs extensive explanation, split it.

### Use Subgraphs for Grouping
Group related nodes visually. Helps readers understand boundaries.

### Color-Code Consistently
Pick a color scheme and stick to it:
- Blue tones for spec/design elements
- Orange/yellow for implementation details
- Green for complete/success states
- Red for blocked/error states

### Update When Structure Changes
Diagrams go stale. Update them when the system structure they represent changes significantly.

### Embed or Link
- **Embed** in decision records or spec sections when the diagram is central to understanding
- **Link** from dashboard or overview docs when the diagram is supplementary

---

## Where to Use These Patterns

| Pattern | Good For |
|---------|----------|
| Workflow Phases | Spec overview, README, process docs |
| Decision Dependencies | Decision records, architecture docs |
| Task Status | Dashboard, status updates |
| Component Architecture | System overview, onboarding docs |
| Progress Timeline | Project planning, stakeholder updates |
| State Machine | Task lifecycle docs, workflow specs |
| Sequence Diagram | API documentation, integration specs |
| Entity Relationship | Database design, data model docs |
