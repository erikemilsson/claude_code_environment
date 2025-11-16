# Power Query Project: [Project Name]

## ⚠️ INITIALIZATION REQUIRED
This project needs Phase 0 initialization before task execution.

**Before starting**: Edit `.claude/context/overview.md` with your project description.

## Phase 0: Ambiguity Resolution & Setup

**Current Status**: Not Started

Run these commands in order:

### 1. Initialize Project
```
@.claude/commands/initialize-project.md
```
- Analyzes calculation documents in `calculation-docs/`
- Extracts all variables, formulas, logic from source documents
- Generates initial ambiguity report in `.claude/reference/ambiguity-report.md`
- Estimates number of ambiguity batches needed

### 2. Resolve Ambiguities (Interactive)
```
@.claude/commands/resolve-ambiguities.md
```
- Presents ambiguities in batches of 5 maximum
- User resolves each batch
- Documents decisions in `.claude/context/assumptions.md`
- **Run multiple times** until all ambiguities resolved

### 3. Generate Artifacts
```
@.claude/commands/generate-artifacts.md
```
- Creates `.claude/context/glossary.md` with all variable definitions
- Generates `.claude/reference/data-contracts.md` with schemas
- Creates `.claude/reference/query-manifest.md` with query descriptions
- Builds `.claude/reference/dependency-graph.md` showing query relationships
- Generates initial tasks in `.claude/tasks/`
- Updates this CLAUDE.md with Phase 1 instructions

### 4. Extract Queries
```
@.claude/commands/extract-queries.md
```
- Instructs on extracting Power Query from Excel files
- Documents watch mode setup
- Prepares for git commit
- Marks Phase 0 as complete

## After Phase 0
This file will be updated with Phase 1 task execution instructions.

## Project Structure
- **Calculation docs**: `calculation-docs/` - Place PDFs, Word docs here
- **Excel files**: `excel-files/` - Place Excel workbooks here
- **Extracted queries**: `power-query/` - Auto-populated after extraction
- **Test data**: `tests/sample-data/` - Sample inputs for validation

## Key Context Files
- **Project description**: `.claude/context/overview.md` ⚠️ **EDIT THIS FIRST**
- **LLM pitfalls**: `.claude/context/llm-pitfalls.md` - Pre-populated checklist
- **Power Query standards**: `.claude/context/power-query.md` - M-code conventions
- **Naming rules**: `.claude/context/naming.md` - Naming conventions
- **Error handling**: `.claude/context/error-handling.md` - Error patterns

## Commands Available
See `.claude/commands/` for all available commands.

---

**Next Step**: Edit `.claude/context/overview.md`, then run `@.claude/commands/initialize-project.md`
