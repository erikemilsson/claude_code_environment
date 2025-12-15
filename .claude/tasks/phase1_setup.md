# Phase 1: Project Setup (February Weeks 1-2)

## Overview
Initialize all project infrastructure and prepare for data collection.

## Critical Path Tasks

### Week 1: Technical Infrastructure
1. **Setup PostgreSQL Database**
   - Install PostgreSQL 15+
   - Create 'siren' database
   - Run schema creation scripts
   - Test connections
   - Set up backup procedures

2. **Configure Python Environment**
   - Create virtual environment
   - Install required packages
   - Test database connectivity
   - Set up Jupyter (optional)

3. **Microsoft 365 Setup**
   - Create SharePoint site
   - Set up Forms workspace
   - Configure Power BI workspace
   - Test permissions

### Week 2: Documentation & Templates
1. **Create Data Collection Forms**
   - Stakeholder interview form
   - Literature extraction template
   - Workshop feedback forms
   - Test with pilot users

2. **Initialize Git Repository**
   - Create repository structure
   - Add .gitignore
   - Initial commit
   - Set up README

3. **Prepare Project Materials**
   - Consent forms
   - Stakeholder invitation emails
   - Project information sheet
   - Data management plan

## Checklist
- [ ] PostgreSQL running locally
- [ ] Database schema implemented
- [ ] Python environment functional
- [ ] Microsoft Forms created
- [ ] SharePoint site active
- [ ] Power BI workspace ready
- [ ] Git repository initialized
- [ ] All templates created
- [ ] Consent forms prepared
- [ ] Test data loaded

## Dependencies
None - this phase must complete before others begin

## Success Criteria
- All infrastructure operational
- Forms tested with 2-3 pilot users
- Database accepts test data
- Backup procedures verified
- Documentation complete

## Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| PostgreSQL connection fails | Check pg_hba.conf settings |
| Forms not saving to SharePoint | Verify permissions and list setup |
| Python package conflicts | Use virtual environment |
| Power BI connection issues | Check firewall and credentials |

## Files to Reference
- `/technical_architecture.md` - System setup
- `/database_schema.md` - Database structure
- `/data_collection_templates.md` - Form templates

## Commands to Run
```bash
# After setup complete
/setup_database
/create_forms
```

## Time Estimate
- Database setup: 4 hours
- Forms creation: 6 hours
- Testing: 4 hours
- Documentation: 2 hours
- **Total: 16 hours**

## Next Phase Trigger
When all checklist items complete, begin Phase 2: Literature Review & Collection