# Setup Database Command

## Purpose
Initialize the PostgreSQL database for the SIREN project with all required tables, views, and initial data.

## Usage
`/setup_database`

## Actions
1. Create PostgreSQL database named 'siren'
2. Execute schema creation from `/database_schema.md`
3. Create all 8 core tables:
   - factors
   - evidence
   - sources
   - stakeholders
   - causal_links
   - interventions
   - workshop_sessions
   - workshop_feedback
4. Set up indexes for performance
5. Create analysis views
6. Initialize backup procedures
7. Generate test data for development

## Prerequisites
- PostgreSQL 15+ installed locally
- Database user with creation privileges
- Python environment activated

## Files Used
- `/database_schema.md` - Table definitions
- `/technical_architecture.md` - Connection settings

## Expected Output
- Database 'siren' created
- All tables created with constraints
- Views established
- Test data inserted (if in dev mode)
- Connection test successful

## Error Handling
- Check if database already exists
- Validate PostgreSQL version
- Ensure proper permissions
- Log all operations

## Next Steps
After database setup:
1. Configure Microsoft Forms connection
2. Test data import pipeline
3. Set up Power BI connection