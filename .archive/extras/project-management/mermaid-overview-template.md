# Mermaid Overview Template

Use this template to create visual project overviews with Mermaid diagrams.

---

# Project Overview: [Project Name]

**Last Updated:** [Date]

## High-Level Architecture

```mermaid
flowchart TB
    subgraph Input
        A[Data Source 1]
        B[Data Source 2]
    end

    subgraph Processing
        C[Component 1]
        D[Component 2]
    end

    subgraph Output
        E[Result 1]
        F[Result 2]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
```

## Phase Flow

```mermaid
flowchart LR
    P1[Phase 1: Setup] --> P2[Phase 2: Build]
    P2 --> P3[Phase 3: Test]
    P3 --> P4[Phase 4: Deploy]

    style P1 fill:#90EE90
    style P2 fill:#FFD700
    style P3 fill:#E0E0E0
    style P4 fill:#E0E0E0
```

**Legend:**
- Green: Completed
- Yellow: In Progress
- Gray: Pending

## Task Dependencies

```mermaid
flowchart TD
    T1[Task 1: Setup] --> T2[Task 2: Core Feature]
    T1 --> T3[Task 3: Database]
    T2 --> T4[Task 4: Integration]
    T3 --> T4
    T4 --> T5[Task 5: Testing]
    T5 --> T6[Task 6: Deploy]
```

## Component Diagram

```mermaid
flowchart TB
    subgraph Frontend
        UI[User Interface]
        State[State Management]
    end

    subgraph Backend
        API[API Layer]
        Service[Business Logic]
        DB[(Database)]
    end

    UI --> API
    State --> UI
    API --> Service
    Service --> DB
```

## Data Flow

```mermaid
flowchart LR
    Raw[Raw Data] --> Clean[Cleaned Data]
    Clean --> Transform[Transformed Data]
    Transform --> Output[Final Output]
```

## Timeline / Gantt

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1
    Setup           :done,    p1, 2025-01-01, 7d
    Configuration   :done,    p2, after p1, 3d
    section Phase 2
    Development     :active,  p3, after p2, 14d
    Testing         :         p4, after p3, 7d
    section Phase 3
    Deployment      :         p5, after p4, 3d
```

## Sequence Diagram (for workflows)

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Database

    User->>Frontend: Submit Form
    Frontend->>API: POST /data
    API->>Database: INSERT
    Database-->>API: Success
    API-->>Frontend: 200 OK
    Frontend-->>User: Confirmation
```

## Entity Relationship (for data models)

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : includes

    USER {
        int id PK
        string name
        string email
    }
    ORDER {
        int id PK
        int user_id FK
        date created
    }
```

## State Diagram (for status flows)

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> InProgress: Start
    InProgress --> Blocked: Issue Found
    Blocked --> InProgress: Resolved
    InProgress --> Finished: Complete
    Finished --> [*]
```

---

## Usage Notes

1. **Keep diagrams simple** - If it's too complex, break into multiple diagrams
2. **Use subgraphs** to group related components
3. **Add styling** to show status (colors)
4. **Update regularly** - Diagrams should reflect current state
5. **Include legend** when using colors or symbols
