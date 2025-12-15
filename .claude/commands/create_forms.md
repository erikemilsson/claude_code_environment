# Create Forms Command

## Purpose
Generate Microsoft Forms templates for stakeholder data collection based on the project specifications.

## Usage
`/create_forms`

## Actions
1. Generate form structures from `/data_collection_templates.md`
2. Create the following forms:
   - Stakeholder Interview Form
   - Literature Extraction Form
   - Workshop Voting Form
   - Real-time Feedback Form
   - Post-Workshop Evaluation Form
3. Set up SharePoint lists for responses
4. Configure data validation rules
5. Enable branching logic where needed
6. Set up automated response notifications

## Form Specifications

### Stakeholder Interview Form
- 25 questions across 6 sections
- PESTLE categorization
- Consent tracking
- Long-form text for barriers

### Workshop Forms
- Real-time voting capability
- Quick feedback options
- Ranking mechanisms
- Consensus tracking

## Prerequisites
- Microsoft 365 account access
- SharePoint site created
- Forms permissions configured

## Files Used
- `/data_collection_templates.md` - All form templates
- `/database_schema.md` - Field mapping reference

## Expected Output
- 5 Microsoft Forms created
- SharePoint lists configured
- Form URLs generated
- Test responses validated
- Database field mapping documented

## Integration Points
- Forms → SharePoint Lists
- SharePoint → Python scripts
- Python → PostgreSQL database

## Next Steps
1. Test each form with sample data
2. Set up Power Automate flows (optional)
3. Create Python import scripts
4. Document form URLs for participants