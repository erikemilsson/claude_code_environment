# Documentation/Content Template

## Overview

The Documentation/Content template provides a structured environment for creating, managing, and maintaining technical documentation, API references, blog posts, user guides, and other written content. It includes writing standards, documentation structure patterns, and content review workflows.

## When to Use This Template

Choose this template for projects focused on:

1. **Technical Documentation Projects**
   - Product documentation sites
   - API reference documentation
   - Developer guides and tutorials
   - Internal knowledge bases

2. **Content Creation Workflows**
   - Technical blog posts
   - White papers and case studies
   - Release notes and changelogs
   - User manuals and help centers

3. **Documentation-as-Code**
   - Markdown-based documentation
   - Version-controlled content
   - Multi-format output (HTML, PDF, etc.)
   - Automated publication pipelines

4. **Multi-Author Content Teams**
   - Collaborative writing environments
   - Content review and approval workflows
   - Style consistency enforcement
   - Publication scheduling

## What This Template Provides

### Core Components

- **Task Management**: Hierarchical task tracking for content planning (from components/task-management/)
- **Writing Standards**: Style guides, voice/tone guidelines, terminology standards
- **Documentation Patterns**: Structural templates for different content types
- **Review Workflows**: Peer review, technical review, and editorial processes
- **Publication Commands**: Automated deployment and publishing workflows

### File Structure

```
project/
├── CLAUDE.md                    # Router file
├── README.md                    # Project overview
├── .claude/
│   ├── commands/
│   │   ├── complete-task.md     # Task management
│   │   ├── breakdown.md         # Task breakdown
│   │   ├── sync-tasks.md        # Task synchronization
│   │   ├── update-tasks.md      # Task validation
│   │   ├── review-content.md    # Content review workflow
│   │   └── publish.md           # Publication/deployment
│   ├── context/
│   │   ├── overview.md          # Project overview
│   │   ├── standards/
│   │   │   ├── writing-style.md       # Writing standards
│   │   │   ├── documentation-structure.md  # Doc patterns
│   │   │   ├── api-documentation.md   # API doc standards
│   │   │   └── terminology.md         # Glossary and terms
│   │   └── validation-rules.md  # Content validation rules
│   ├── tasks/                   # Task tracking
│   │   ├── task-overview.md
│   │   └── task-*.json
│   └── reference/               # Supporting documentation
│       ├── difficulty-guide.md
│       ├── breakdown-workflow.md
│       └── content-review-checklist.md
└── content/                     # Your actual content
    ├── docs/
    ├── blog/
    ├── api-reference/
    └── guides/
```

## Getting Started

### 1. Initialize Project Structure

```bash
# Create the base directories
mkdir -p .claude/{commands,context/standards,tasks,reference}
mkdir -p content/{docs,blog,api-reference,guides}
```

### 2. Copy Template Files

From this template directory, copy:
- Commands from `customizations/commands/` to `.claude/commands/`
- Standards from `customizations/standards/` to `.claude/context/standards/`
- Reference docs from `customizations/reference/` to `.claude/reference/`

### 3. Customize for Your Project

Update `.claude/context/overview.md` with:
- Content scope and goals
- Target audience
- Publication platforms
- Review requirements
- Technology stack (documentation generators, hosting platforms)

Update `.claude/context/standards/writing-style.md` with:
- Organization-specific style preferences
- Voice and tone guidelines
- Formatting conventions
- Examples specific to your domain

### 4. Create Initial Tasks

Create task JSON files for your content work:
- Content planning tasks
- Writing tasks
- Review tasks
- Publication tasks

## Typical Workflows

### Content Creation Workflow

1. **Planning**: Create task for new content piece (e.g., "Write API authentication guide")
2. **Research**: Gather information, review existing documentation
3. **Drafting**: Write initial content following style guide
4. **Review**: Run content review workflow (technical + editorial)
5. **Revision**: Address feedback from reviews
6. **Publication**: Deploy to documentation site or blog

### API Documentation Workflow

1. **Analysis**: Review API endpoints, parameters, responses
2. **Structure**: Follow API documentation pattern template
3. **Examples**: Create code samples for each endpoint
4. **Testing**: Verify all examples work with current API version
5. **Review**: Technical review by API developers
6. **Publication**: Generate API reference docs and deploy

### Multi-Format Publishing Workflow

1. **Source**: Maintain single Markdown source
2. **Build**: Generate HTML, PDF, or other formats
3. **Review**: Preview generated outputs
4. **Deploy**: Push to documentation hosting platform
5. **Validation**: Check links, formatting, search indexing

## Key Features

### 1. Consistency Enforcement

- Style guide templates ensure consistent voice and tone
- Documentation structure patterns provide repeatable templates
- Terminology standards maintain consistent language
- Review checklists catch common issues

### 2. Collaboration Support

- Task management tracks who's writing what
- Review workflows ensure quality control
- Version control integration for content history
- Clear handoff processes between writers and reviewers

### 3. Scalability

- Component-based structure grows with content volume
- Reusable patterns speed up content creation
- Automated publication reduces manual effort
- Search and navigation support for large doc sets

### 4. Quality Assurance

- Multi-stage review process (technical, editorial, legal if needed)
- Validation rules for content structure
- Link checking and broken reference detection
- Readability and accessibility checks

## Customization Points

### Writing Style Guide

Customize `customizations/standards/writing-style.md` to match your organization's preferences:
- Voice: Formal vs. conversational
- Person: First-person vs. second-person vs. third-person
- Active vs. passive voice usage
- Technical jargon policies
- Abbreviation and acronym standards

### Documentation Structure

Customize `customizations/standards/documentation-structure.md` for your content types:
- Tutorial structure (overview → prerequisites → steps → conclusion)
- How-to guide structure (problem → solution → variations)
- Reference structure (purpose → syntax → parameters → examples)
- Conceptual structure (introduction → concepts → relationships)

### Content Review Workflow

Customize `customizations/workflows/content-review.md` for your approval process:
- Review stages (peer, technical, editorial, legal)
- Reviewer assignments
- Approval criteria
- Feedback incorporation process
- Publication approval requirements

### Publication Commands

Customize `customizations/commands/publish.md` for your deployment pipeline:
- Build commands for documentation generators
- Deployment targets (staging, production)
- Pre-publication checks (link validation, spell check)
- Post-publication tasks (sitemap generation, search indexing)

## Integration with Other Components

### Task Management Component

This template uses the task-management component for:
- Breaking down large documentation projects
- Tracking writing progress
- Managing review cycles
- Coordinating multi-author efforts

### Version Control

Documentation projects benefit from:
- Branch-per-document workflow for major rewrites
- PR-based review process
- Commit message standards for content changes
- Changelog generation from commit history

## Common Use Cases

### 1. New Product Documentation Site

**Initial Setup**:
- Create content structure for guides, API reference, tutorials
- Set up documentation generator (e.g., MkDocs, Docusaurus, Sphinx)
- Define writing style guide
- Create task hierarchy for content coverage

**Ongoing Work**:
- Write content by priority (getting started → core features → advanced topics)
- Review and revise based on user feedback
- Update for new product releases
- Maintain search and navigation

### 2. Technical Blog

**Initial Setup**:
- Define blog post structure template
- Set up editorial calendar (task management)
- Create review and publication workflow
- Configure hosting and deployment

**Ongoing Work**:
- Plan topics and schedule writing
- Draft, review, revise cycle
- Publish on schedule
- Cross-post to other platforms

### 3. API Documentation

**Initial Setup**:
- Analyze API structure
- Choose API doc format (OpenAPI, custom)
- Create endpoint documentation template
- Set up code example standards

**Ongoing Work**:
- Document new endpoints
- Update for API changes
- Maintain code examples
- Generate SDK documentation

### 4. Internal Knowledge Base

**Initial Setup**:
- Identify documentation needs
- Create category structure
- Define contribution guidelines
- Set up search and indexing

**Ongoing Work**:
- Capture tribal knowledge
- Document processes and procedures
- Keep content up to date
- Improve based on usage analytics

## Best Practices

1. **Start with Structure**: Define documentation architecture before writing
2. **Write for Scanning**: Use clear headings, bullet points, and visual hierarchy
3. **Show, Don't Tell**: Include code examples, screenshots, diagrams
4. **Keep It Current**: Schedule regular reviews to update outdated content
5. **Test Everything**: Verify all code examples, links, and procedures work
6. **Get Feedback**: Involve actual users in reviewing documentation
7. **Measure Success**: Track metrics (page views, search queries, user feedback)
8. **Version Appropriately**: Match documentation versions to product versions
9. **Make It Searchable**: Optimize for both site search and search engines
10. **Iterate Based on Data**: Use analytics to improve high-traffic pages

## Tools and Technology

Common tools used with this template:

### Documentation Generators
- **MkDocs**: Python-based, Markdown, great for technical docs
- **Docusaurus**: React-based, versioned docs, blogging support
- **Sphinx**: Python-focused, reStructuredText, extensible
- **VuePress**: Vue.js-based, simple and fast
- **Hugo**: Go-based, extremely fast static site generator

### Writing and Editing
- **Markdown editors**: Typora, iA Writer, VS Code
- **Grammar tools**: Grammarly, LanguageTool
- **Diagram tools**: Mermaid, PlantUML, Draw.io
- **Screenshot tools**: Snagit, CloudApp, Lightshot

### Review and Collaboration
- **Git-based workflows**: Pull requests for content review
- **Commenting tools**: Google Docs for drafts, GitHub PR comments
- **Project management**: Task tracking in this repo, or Notion, Linear

### Publishing and Hosting
- **GitHub Pages**: Free hosting for static sites
- **Netlify / Vercel**: Automated builds and deploys
- **Read the Docs**: Documentation hosting with versioning
- **Custom hosting**: AWS S3, DigitalOcean, etc.

## Success Metrics

Track these metrics to measure documentation effectiveness:

1. **Coverage**: Percentage of features documented
2. **Freshness**: Time since last update for each document
3. **Usage**: Page views, time on page, search queries
4. **Quality**: User satisfaction ratings, feedback volume
5. **Effectiveness**: Reduction in support tickets, forum questions
6. **Completion**: Task completion rate for documentation projects
7. **Velocity**: Time from feature release to documentation published

## Getting Help

For questions about this template:
1. Review the customization files in `customizations/`
2. Check the task-management component documentation
3. Consult the reference documentation in `.claude/reference/`
4. Review example projects using this template

## Benefits

1. **Faster Content Creation**: Templates and patterns speed up writing
2. **Higher Quality**: Review workflows and standards ensure consistency
3. **Better Collaboration**: Clear processes for multi-author teams
4. **Easier Maintenance**: Structured approach to keeping content current
5. **Scalable Growth**: Add more content types and writers without chaos
6. **Measurable Impact**: Task tracking and metrics show documentation value
