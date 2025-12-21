# Project-Specific Command Examples

This directory contains command files that were created for specific projects but serve as useful examples for creating custom commands in your own projects.

## Purpose

These commands demonstrate how to create domain-specific workflows for:
- Database setup and schema management
- Form generation and data collection
- Analysis pipelines and reporting
- Project-specific automation

## Files in This Directory

### setup_database.md
**Project**: SIREN (System Innovation Research Evidence Network)
**Purpose**: Initialize PostgreSQL database with project-specific schema
**Key Patterns**:
- Database initialization workflow
- Schema creation from documentation
- Test data generation
- Backup procedure setup

**Useful For**: Data engineering projects requiring database setup automation

### create_forms.md
**Project**: SIREN stakeholder data collection
**Purpose**: Generate Microsoft Forms templates for stakeholder interviews
**Key Patterns**:
- Form structure generation from specifications
- SharePoint integration
- Data validation rules
- Branching logic configuration

**Useful For**: Research projects, stakeholder engagement workflows, data collection automation

### run_analysis.md
**Project**: Theory of Constraints analysis
**Purpose**: Execute analysis pipeline with multiple stages
**Key Patterns**:
- Multi-stage pipeline execution
- Stage selection via command arguments
- Network analysis workflow
- Visualization generation

**Useful For**: Data analysis projects, research workflows, multi-step processing pipelines

### generate_reports.md
**Project**: SIREN project deliverables
**Purpose**: Create scientific publications, technical reports, and datasets
**Key Patterns**:
- Multi-format report generation
- Dashboard updates
- Dataset preparation
- Publication drafting workflow

**Useful For**: Research projects, reporting automation, documentation generation

## How to Use These Examples

### Option 1: Adapt for Your Project
1. Copy relevant command file to your `.claude/commands/` directory
2. Update the Purpose, Actions, and specifications for your project
3. Replace project-specific details (database names, form structures, etc.)
4. Test the command in your project environment

### Option 2: Learn Patterns
Study these examples to understand:
- How to structure multi-step workflows
- How to document prerequisites and dependencies
- How to provide command arguments for flexibility
- How to integrate with external tools (databases, forms, dashboards)

### Option 3: Extract Components
Some patterns are reusable across projects:
- Database initialization workflow
- Report generation pipeline
- Multi-stage processing approach
- Form/template generation logic

## Command File Best Practices

These examples demonstrate key practices:

1. **Clear Purpose Statement**: Each command starts with explicit purpose
2. **Usage Documentation**: Show command syntax with options
3. **Structured Actions**: List all steps the command performs
4. **Prerequisites**: Document required tools, permissions, environment setup
5. **Context Requirements**: Specify which files/data the command needs
6. **Output Documentation**: Describe what the command produces

## Integration with Generic Commands

These project-specific commands often work alongside generic task management commands:

**Workflow Example**:
```
/breakdown "Set up project infrastructure"
  → Creates subtasks including database setup, form creation, etc.

/complete-task 42
  → Marks "Database setup" as in progress

/setup_database
  → Executes project-specific database initialization

/complete-task 42
  → Marks task finished, documents what was done
```

## Template Pattern

Use this template for creating your own project-specific commands:

```markdown
# [Command Name]

## Purpose
[One-sentence description of what this command does]

## Usage
\`/command-name [arguments]\`

Options:
- \`option1\` - Description
- \`option2\` - Description

## Actions
1. [First step]
2. [Second step]
3. [...]

## Prerequisites
- [Required tools]
- [Required permissions]
- [Environment requirements]

## Context Required
- [Files the command needs to read]
- [Data the command needs access to]

## Output Location
- [Where results are saved]
- [What files are created/modified]

## Notes
- [Important warnings]
- [Known limitations]
- [Related commands]
```

## Why These Were Moved

These commands were in `.claude/commands/` but were project-specific rather than template-generic. To avoid confusion about which commands are:
- **Generic** (applicable to any project using the template)
- **Specific** (only useful for particular project types)

...we moved project-specific commands here as examples.

## Creating Generic Versions

If you find a pattern from these examples that would be useful as a generic template command, consider:

1. **Abstracting the specifics**: Replace project names, database schemas, form structures with placeholders
2. **Adding configuration**: Allow customization through command arguments or config files
3. **Documenting variations**: Explain how to adapt for different project types
4. **Contributing back**: Propose adding to template components if widely useful

## Related Resources

- **Generic Commands**: See `.claude/commands/` for template-wide commands
- **Task Management**: See `components/task-management/` for task workflow commands
- **Template Customization**: See `.claude/reference/template-customization-guide.md`
- **Command Patterns**: See `components/pattern-library/` (when populated)

## Questions?

If you're unsure whether a command should be:
- **In `.claude/commands/`**: Generic, reusable across all projects using this template
- **In this examples directory**: Project-specific, useful as reference but not directly applicable
- **In your project only**: Highly specific to one project, not useful as example

...ask yourself: "Would this command need significant changes to work in a different project?" If yes, it's probably project-specific.
