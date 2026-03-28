# Cowork Folder Specification

This document is a specification for setting up a `cowork/` directory inside a Claude Code environment repository. The purpose is to create a structured handoff zone between Claude Code (interactive, terminal-based work) and Cowork Dispatch (long-running, autonomous tasks that run while you're away).

Hand this file to Claude Code and ask it to scaffold the folder structure and populate the initial files.

---

## Context

Cowork Dispatch is a desktop interface for running autonomous Claude tasks. It accesses files through a mounted folder — only the folder you select is visible to it. By placing a `cowork/` directory inside your Claude Code environment repo, you create a controlled workspace where Dispatch tasks can read inputs, follow your conventions, and deliver outputs, without exposing the rest of your project or filesystem.

Claude Code and Cowork are separate runtimes. Cowork does not automatically inherit `.claude/` configuration, slash commands, or MCP servers. The `cowork/` folder bridges this gap by providing explicit instructions and structure that Cowork can read and follow.

---

## Folder Structure

```
your-repo/
├── .claude/                    # Existing Claude Code config (not exposed to Cowork)
├── cowork/                     # Mount this folder in Cowork Dispatch
│   ├── README.md               # Conventions and instructions for Cowork sessions
│   ├── inputs/                 # Task lists, data files, and source material
│   │   └── .gitkeep
│   ├── outputs/                # Deliverables produced by Cowork tasks
│   │   └── .gitkeep
│   ├── templates/              # Reusable templates for reports, analyses, etc.
│   │   └── .gitkeep
│   ├── queue/                  # Individual task definitions (markdown files)
│   │   └── .gitkeep
│   └── archive/                # Completed task definitions moved here for reference
│       └── .gitkeep
```

### Directory purposes

**inputs/** — Place any files here that Cowork tasks should read as source material. This includes tracker spreadsheets (Excel/CSV with lists of items to process), reference documents, datasets, or configuration files. Cowork reads from here but should not modify input files.

**outputs/** — All deliverables produced by Cowork tasks go here. Cowork should create a subfolder per task or per item when processing a batch (e.g., `outputs/2026-03-20_company-research/CompanyA/`). This keeps outputs organized and traceable.

**templates/** — Reusable document structures, report outlines, analysis frameworks, or any standardized format you want Cowork to follow consistently across tasks. Templates should be markdown files describing the structure and expectations, not necessarily final-format files.

**queue/** — Each file here defines a single task or batch of work for Cowork to pick up. Task files are markdown with a specific format (see below). When you want Cowork to do something, you drop a task file here and point Dispatch at it.

**archive/** — After a task is completed, move its queue file here. This preserves a history of what was requested and when, which is useful since the folder is version-controlled.

---

## README.md (for the cowork/ folder)

The README.md inside `cowork/` is the single most important file. When starting any Cowork Dispatch session that uses this folder, the first instruction should be: "Read cowork/README.md and follow its conventions."

The README should contain:

1. **Who you are and what this workspace is for** — A brief description of the kind of work you do and what types of tasks you'll be delegating. Keep it to 2-3 sentences. This gives Cowork enough context to make good judgment calls without over-constraining it.

2. **Output standards** — How you want deliverables structured. For example: naming conventions for files and folders, preferred file formats (markdown, docx, xlsx, etc.), whether to include sources and citations, how to handle uncertainty or gaps in research.

3. **Naming conventions** — How to name output folders and files. A pattern like `YYYY-MM-DD_task-slug/` for task folders keeps things sortable and scannable.

4. **What not to do** — Explicit boundaries. For example: don't modify files in `inputs/`, don't create files outside `cowork/`, don't make assumptions about information not found — flag it instead.

5. **How to report progress** — Whether you want a summary file per task, status updates in the tracker spreadsheet, or some other mechanism for knowing what's done and what's pending.

---

## Task Queue Format

Each file in `queue/` defines a task. Use this format:

```markdown
# Task: [Short descriptive title]

**Created:** YYYY-MM-DD
**Priority:** high | medium | low
**Status:** pending | in-progress | completed
**Type:** research | analysis | document | data-processing | other

## Objective

[One paragraph describing what needs to be done and why.]

## Inputs

- [List of input files or data sources to use, with paths relative to cowork/]
- [e.g., inputs/companies.xlsx — column "Company Name"]

## Expected Outputs

- [Describe what should be produced and where it should go]
- [e.g., outputs/YYYY-MM-DD_task-slug/CompanyA/report.md for each row in the tracker]

## Instructions

[Step-by-step methodology or approach to follow. Be specific about:]
[- What information to gather or analyze]
[- What structure the output should follow (reference a template if applicable)]
[- How to handle missing information or ambiguity]
[- Whether to update the input tracker with status/results]

## Constraints

[Any boundaries: time limits, scope limits, sources to avoid, etc.]
```

---

## Batch Processing Pattern

For iterative work where Cowork processes a list of items (the primary use case for long-running tasks):

1. **Create a tracker file** in `inputs/`. This can be an Excel spreadsheet or CSV with at minimum: an identifier column, a status column (e.g., pending/in-progress/completed/error), and any metadata columns relevant to the task.

2. **Create a task file** in `queue/` that references the tracker and describes what to do for each row.

3. **Instruct Cowork** to: read the queue file, load the tracker, and process each pending row. For each item, create a subfolder under `outputs/`, produce the deliverables, and update the status column in the tracker.

4. **Check in periodically** — the tracker file serves as a progress dashboard. You can open it at any time to see what's done.

This pattern works for any list-based work: researching a list of companies, profiling a set of datasets, generating reports for multiple clients, reviewing a batch of documents, etc.

---

## Integration with Claude Code

Add the following to your `.claude/` configuration (e.g., in CLAUDE.md or equivalent):

```
## Cowork Dispatch Integration

This repository contains a `cowork/` folder for delegating long-running tasks to Cowork Dispatch.

When to suggest using Cowork:
- The task involves processing a list of items iteratively
- The task requires extended web research across multiple topics
- The task will take significant time and doesn't need real-time interaction
- The user mentions wanting to step away or do something else while work runs

When the user wants to set up a Cowork task:
1. Help them create or update the input files in `cowork/inputs/`
2. Help them write a task definition file in `cowork/queue/`
3. Remind them to mount the `cowork/` folder in Dispatch
4. Remind them that Cowork does not inherit this project's .claude/ config —
   all instructions must be in cowork/README.md or the task file itself

The cowork/ folder spec is documented in cowork/README.md.
```

---

## .gitignore Recommendations

```gitignore
# Large generated outputs (optional — include if outputs are bulky)
# cowork/outputs/

# Keep the folder structure
!cowork/outputs/.gitkeep

# OS files
cowork/**/.DS_Store
```

Whether to commit outputs depends on your workflow. If outputs are lightweight (markdown reports, summaries), committing them gives you version history. If they're large (datasets, images, full documents), consider .gitignoring them or using Git LFS.

---

## Use Case Patterns

The cowork/ folder supports any long-running task that benefits from a "set up, walk away, check in" workflow. Below are generic patterns — adapt them to whatever work you're doing.

### 1. Batch Research

**Input:** A spreadsheet listing items to research (companies, technologies, regulations, markets, etc.) with columns defining what angles to investigate.

**Process:** For each row, Cowork searches the web, gathers information, and produces a structured summary following your template.

**Output:** A folder per item containing research notes and a formatted report.

**Best for:** Due diligence, competitive analysis, literature reviews, market scans, regulatory surveys.

### 2. Data Profiling and Exploration

**Input:** One or more datasets (CSV, Excel, database exports) placed in `inputs/`.

**Process:** For each dataset, Cowork profiles the data (schema, distributions, null rates, outliers, quality issues) and produces a summary report with visualizations.

**Output:** A profiling report per dataset with key findings and recommended next steps.

**Best for:** New dataset onboarding, data quality audits, exploratory analysis before deeper work.

### 3. Document Generation

**Input:** A template in `templates/` and a tracker spreadsheet with variable data per item.

**Process:** For each row, Cowork generates a document following the template, populating it with item-specific content (which may involve web research or computation).

**Output:** One document per item (markdown, docx, or other format as specified).

**Best for:** Client reports, standardized assessments, proposal drafts, compliance documentation.

### 4. Comparative Analysis

**Input:** A list of items to compare and the dimensions/criteria for comparison.

**Process:** Cowork researches each item, scores or describes it along each dimension, and produces both individual summaries and a consolidated comparison.

**Output:** Individual item reports plus a comparison matrix or summary document.

**Best for:** Vendor evaluations, technology assessments, policy comparisons, investment screening.

### 5. Content Monitoring and Summarization

**Input:** A list of sources (URLs, publications, topics) to monitor.

**Process:** Cowork checks each source, extracts recent/relevant content, and produces summaries organized by topic or source.

**Output:** A digest document summarizing findings, flagging notable items.

**Best for:** News monitoring, regulatory update tracking, industry trend watching, literature surveillance.

### 6. Data Transformation and Cleanup

**Input:** Raw or messy data files in `inputs/`.

**Process:** Cowork cleans, restructures, and validates the data according to your specifications (handling missing values, standardizing formats, merging sources, etc.).

**Output:** Clean datasets in `outputs/` with a transformation log documenting what was changed and why.

**Best for:** Pre-processing data for analytics pipelines, standardizing data from multiple sources, preparing data for dashboards or reports.

---

## Getting Started

To scaffold this structure, ask Claude Code to:

1. Create the `cowork/` directory with all subdirectories and `.gitkeep` files
2. Generate the `cowork/README.md` based on your specific conventions and work context
3. Create a sample task file in `cowork/queue/` as a reference
4. Create a sample tracker spreadsheet in `cowork/inputs/` as a reference
5. Add the Cowork integration note to your `.claude/` configuration
6. Update `.gitignore` as appropriate

Then test the workflow by mounting `cowork/` in Dispatch and running a small task.
