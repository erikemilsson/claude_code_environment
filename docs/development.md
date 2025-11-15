# Development Guide

## Repository Purpose
This repository maintains version-controlled templates for Claude Code project environments. It's both a reference repository and an iteration space for improving template patterns.

## Repository Structure
```
claude_code_environment/
├── templates/              # Copyable project templates
│   ├── base/               # Minimal template
│   ├── data-engineering/   # ETL/pipeline projects
│   ├── bi-dashboard/       # Power BI/reporting
│   ├── hybrid/             # Combined data + BI
│   └── experimental/       # Work-in-progress templates
├── docs/                   # Documentation
│   ├── template-guide.md   # How to use templates
│   ├── template-overview10.md  # Comprehensive reference
│   ├── development.md      # This file
│   └── todo.md             # Development tasks
├── scripts/                # (Future) Automation helpers
├── CLAUDE.md               # AI context for this repo
└── README.md               # Human documentation
```

## Adding New Templates

### 1. Create Template Folder
```bash
# Create new template folder structure
mkdir -p templates/new-template/.claude/{commands,context/standards,tasks,reference}
```

### 2. Copy Base Structure
```bash
# Start with base template
cp -r templates/base/.claude/* templates/new-template/.claude/
cp templates/base/CLAUDE.md templates/new-template/
cp templates/base/README.md templates/new-template/
```

### 3. Add Technology-Specific Standards
Create standards files in `.claude/context/standards/`:
- Coding conventions
- Testing patterns
- Architecture guidelines
- Tool-specific best practices

### 4. Customize Context
Update `.claude/context/overview.md` with:
- Template purpose and use cases
- Typical project structure
- Common workflows
- Example projects that would use this template

### 5. Create Example Tasks
Add 3-5 example tasks in `.claude/tasks/`:
- Representative of typical work for this project type
- Demonstrate difficulty range
- Show dependency patterns
- Include at least one breakdown candidate (difficulty ≥7)

### 6. Document the Template
Add section to `docs/template-overview10.md`:
- When to use this template
- What's included
- Folder structure
- Example initialization questions

### 7. Test the Template
1. Copy to temporary directory
2. Walk through customization checklist
3. Run `@.claude/commands/update-tasks.md`
4. Verify all references work
5. Test task workflow (breakdown, complete)

### 8. Add to Experimental First
- New templates go in `templates/experimental/` initially
- After testing and refinement, promote to top-level `templates/`
- Update `docs/template-guide.md` with new template info

## Modifying Existing Templates

### Process
1. **Make changes** in appropriate template folder
2. **Test changes** by copying to test project
3. **Update documentation** if structure changed
4. **Document in commit** what changed and why
5. **Consider backwards compatibility** - will existing projects break?

### Common Changes
- **Adding standards**: Just add new file, update CLAUDE.md navigation
- **Updating commands**: Modify command file, test workflow
- **Changing task schema**: Update validation-rules.md, all example tasks
- **New reference files**: Add file, document in template-guide.md

## Updating Task Management System

If making changes to task system itself:

### Files to Update
1. `templates/base/.claude/reference/validation-rules.md`
2. `templates/base/.claude/reference/difficulty-guide.md`
3. `templates/base/.claude/reference/breakdown-workflow.md`
4. `templates/base/.claude/commands/breakdown.md`
5. `templates/base/.claude/commands/complete-task.md`
6. `templates/base/.claude/commands/sync-tasks.md`
7. `templates/base/.claude/commands/update-tasks.md`
8. Example task JSON files in all templates
9. `docs/template-overview10.md`

### Propagation
After updating base template:
```bash
# Update all other templates
for template in data-engineering bi-dashboard hybrid; do
  cp templates/base/.claude/commands/* templates/$template/.claude/commands/
  cp templates/base/.claude/reference/* templates/$template/.claude/reference/
done
```

## Standards File Guidelines

When creating standards files:

### Structure
- Start with "General Conventions"
- Include code examples
- Organize by topic/category
- Add "Do's and Don'ts" sections
- Include common patterns
- Add troubleshooting/FAQ if relevant

### Content
- **Be specific**: Not just "use good names" but examples of good vs bad
- **Show examples**: Code snippets demonstrate better than prose
- **Explain why**: Don't just say what to do, explain the reasoning
- **Link to references**: Official docs, style guides, etc.
- **Keep updated**: Standards evolve, keep files current

### File Size
- Aim for 200-400 lines per standards file
- If longer, consider splitting into multiple files
- Use sections and headers for navigation

## Documentation Standards

### CLAUDE.md Files
- Keep under 100 lines
- Router pattern - point to other files
- Quick reference for common operations
- Update "Current Focus" regularly

### README.md Files
- Human-focused documentation
- Installation and usage instructions
- Link to .claude/ folder for AI context
- Keep synchronized with template changes

### docs/ Folder
- `template-guide.md`: User-facing, how to use templates
- `template-overview10.md`: Comprehensive reference
- `development.md`: This file, contributor guide
- `todo.md`: Current development tasks

## Testing Templates

### Manual Testing Checklist
- [ ] Copy template to test directory
- [ ] Run `update-tasks.md` - should show no errors
- [ ] Test `breakdown.md` on high-difficulty task
- [ ] Test `complete-task.md` on simple task
- [ ] Verify `sync-tasks.md` updates overview correctly
- [ ] Check all file references work (@file paths)
- [ ] Validate task JSON against schema
- [ ] Ensure standards files are accessible

### Integration Testing
- [ ] Use template in real project for 1 week
- [ ] Track any issues or confusing points
- [ ] Note any missing standards or patterns
- [ ] Gather feedback on workflow
- [ ] Iterate and improve

## Versioning

### Template Versions
- Template folder names are stable (base, data-engineering, etc.)
- Breaking changes should be documented in commit messages
- Consider keeping archived versions in `templates/archived/`

### Documentation Versions
- `template-overview10.md` uses sequential versioning (v10)
- When making major documentation changes, increment version
- Keep previous version in `docs/archive/` if helpful

## Contributing Workflow

### 1. Local Development
```bash
# Create feature branch
git checkout -b claude/new-template-feature

# Make changes
# Test changes
# Update documentation

# Commit
git add .
git commit -m "Add new template for [purpose]"
```

### 2. Testing
- Test template in isolation
- Test in real project if possible
- Verify documentation accuracy
- Check all links and references

### 3. Documentation
- Update relevant docs files
- Add examples if introducing new patterns
- Update template-guide.md if new template
- Document breaking changes

### 4. Push and Track
```bash
# Push to remote
git push -u origin claude/new-template-feature

# Continue iterating as needed
```

## Common Tasks

### Add New Technology Standards
1. Create `templates/[template]/.claude/context/standards/[tech]-standards.md`
2. Follow standards file guidelines above
3. Add reference in template's CLAUDE.md
4. Update template-guide.md with new capability
5. Test by referencing in actual work

### Update Command Pattern
1. Modify command file in `templates/base/.claude/commands/`
2. Test command workflow
3. Propagate to other templates if applicable
4. Update template-overview10.md if significant change

### Create Experimental Template
1. Copy base to `templates/experimental/[name]/`
2. Add specific standards and context
3. Test thoroughly
4. Document in template-guide.md
5. After validation, promote to `templates/[name]/`

### Archive Old Template
1. Move to `templates/archived/[name]/`
2. Update template-guide.md to mark as archived
3. Document why archived and alternatives
4. Keep for reference but don't promote

## Maintenance

### Regular Updates
- Review templates quarterly
- Update standards as languages/tools evolve
- Incorporate user feedback
- Prune outdated patterns
- Add new common patterns discovered

### Issue Tracking
- Use `docs/todo.md` for development tasks
- Track template improvement ideas
- Note user-reported issues
- Plan major changes

## Best Practices

1. **Start simple**: Base template should be minimal
2. **Specialize deliberately**: Only add to templates what's commonly needed
3. **Document thoroughly**: Templates are teaching tools
4. **Test in practice**: Use templates in real work
5. **Iterate based on feedback**: Real usage reveals improvements
6. **Keep synchronized**: Ensure all templates get critical updates
7. **Version control everything**: Track template evolution over time
