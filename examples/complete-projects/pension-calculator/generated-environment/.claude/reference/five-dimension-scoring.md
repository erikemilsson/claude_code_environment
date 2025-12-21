# Five-Dimension Difficulty Scoring for Power Query Projects

## Overview
Power Query projects require specialized difficulty assessment beyond simple 1-10 scoring. Each task is evaluated on five dimensions, with the overall difficulty being the maximum of all dimensions.

## The Five Dimensions

### 1. M Complexity (Power Query Language)
Score based on language features and logic complexity:

- **1-2**: Simple selections, filters, column operations
- **3-4**: Basic transformations, type conversions, simple merges
- **5-6**: Custom columns with conditions, grouping, pivoting
- **7-8**: Custom functions, recursion, complex iterations
- **9-10**: Advanced patterns, query composition, meta-programming

### 2. DAX Complexity (Measures and Calculations)
Score based on DAX formula complexity:

- **1-2**: Simple SUM, COUNT, AVERAGE
- **3-4**: Basic CALCULATE, simple filters
- **5-6**: Time intelligence, basic context transitions
- **7-8**: Complex context manipulation, iterator functions
- **9-10**: Advanced patterns, complex relationships, optimization

### 3. Data Volume
Score based on data size and refresh requirements:

- **1-2**: <1,000 rows, manual refresh
- **3-4**: 1,000-10,000 rows, daily refresh
- **5-6**: 10,000-100,000 rows, hourly refresh
- **7-8**: 100,000-1M rows, near real-time
- **9-10**: >1M rows, streaming/incremental

### 4. Performance Requirements
Score based on optimization needs:

- **1-2**: No performance constraints
- **3-4**: Basic optimization, <5 minute refresh
- **5-6**: Query folding important, <1 minute refresh
- **7-8**: Critical performance, <30 second refresh
- **9-10**: Real-time performance, complex optimization

### 5. Integration Complexity
Score based on data source and system integration:

- **1-2**: Single Excel/CSV file
- **3-4**: Multiple files, same format
- **5-6**: Mixed sources (files + database)
- **7-8**: APIs, authentication, web services
- **9-10**: Complex systems, real-time feeds, custom connectors

## Calculating Overall Difficulty

```
Overall Difficulty = MAX(M, DAX, Volume, Performance, Integration)
```

If overall difficulty >= 7, the task MUST be broken down.

## Example Scoring

### Task: "Create dynamic pension calculation with real-time data"

```json
{
  "m_complexity": 8,      // Recursive calculations
  "dax_complexity": 6,    // Time intelligence needed
  "data_volume": 7,       // 500,000 records
  "performance": 8,       // <30 second requirement
  "integration": 7,       // Multiple APIs
  "overall": 8           // MAX of all dimensions
}
```

**Result**: Difficulty 8 - Must break down into subtasks

## Breaking Down High-Difficulty Tasks

When overall difficulty >= 7, decompose along the highest-scoring dimensions:

### Example Breakdown
Original Task (Difficulty 8):
- Subtask 1: Build calculation function (M:6, Overall:6)
- Subtask 2: Optimize for volume (Volume:6, Performance:6)
- Subtask 3: Set up API integration (Integration:6)
- Subtask 4: Create DAX measures (DAX:6)

## Red Flags for Power Query Tasks

Watch for these patterns that inflate difficulty:
- Iterative calculations in M (adds +2 to M complexity)
- Query folding breaks (adds +2 to Performance)
- Cross-source joins (adds +2 to Integration)
- Row-level security (adds +2 to DAX)
- Incremental refresh setup (adds +2 to Volume)

## Template Application

When creating tasks from specifications:
1. Identify all five dimensions in requirements
2. Score each dimension independently
3. Calculate overall as maximum
4. Flag tasks >= 7 for breakdown
5. Document rationale for scores