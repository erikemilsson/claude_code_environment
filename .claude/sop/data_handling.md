# Standard Operating Procedure: Data Handling

## Purpose
Ensure consistent, secure, and GDPR-compliant handling of all project data.

## Scope
All data collected, processed, and stored for the SIREN project.

## Data Classification

### Confidential
- Personal stakeholder information
- Email addresses
- Organization affiliations
- Individual responses before anonymization

### Internal
- Raw workshop feedback
- Unpublished analysis results
- Draft reports
- Internal communications

### Public
- Aggregated results
- Anonymized datasets
- Published reports
- Final visualizations

## Data Collection Procedures

### From Literature
1. Record full citation in sources table
2. Extract relevant quotes/data
3. Note page numbers/sections
4. Assign quality score (1-5)
5. Link to evidence and factors

### From Stakeholders
1. Obtain consent before collection
2. Assign anonymous ID
3. Store on work computer/SharePoint only
4. Never share individual responses
5. Aggregate before reporting

### From Workshops
1. Record with permission only
2. Attribute comments by ID not name
3. Summarize rather than quote directly
4. Share aggregate feedback only

## Data Storage Rules

### Location Requirements
- **Primary**: Work computer (encrypted)
- **Backup**: Company SharePoint
- **Never**: Personal devices, external clouds

### File Naming Convention
```
YYYY-MM-DD_DataType_Description_Version
Example: 2025-03-15_Interview_Stakeholder_S001_v1
```

### Version Control
- Save new version for major changes
- Keep last 3 versions minimum
- Archive old versions monthly

## Data Processing Guidelines

### Quality Checks
- Verify data entry accuracy
- Check for duplicates
- Validate against schema
- Document anomalies
- Log all transformations

### Anonymization Process
1. Remove all names
2. Replace with ID codes
3. Generalize organizations
4. Remove identifying details
5. Verify no re-identification possible

## Data Sharing Protocols

### Internal Sharing
- Use company systems only
- Password protect sensitive files
- Track access permissions
- Document sharing log

### External Sharing
- Only aggregated/anonymized data
- Require data use agreement
- Document purpose and recipient
- Set expiration dates

## Security Measures

### Access Control
- Database: Username/password
- Files: Folder permissions
- Forms: Microsoft 365 authentication
- Backups: Encrypted storage

### Incident Response
1. Identify breach/loss
2. Contain immediately
3. Assess impact
4. Notify supervisor
5. Document incident
6. Implement prevention

## GDPR Compliance

### Rights Supported
- Right to access
- Right to rectification
- Right to erasure
- Right to data portability
- Right to object

### Consent Management
- Document consent obtained
- Allow withdrawal anytime
- Track consent versions
- Honor opt-outs immediately

## Retention Schedule

| Data Type | Retention Period | Disposal Method |
|-----------|-----------------|-----------------|
| Raw stakeholder data | Project + 1 year | Secure deletion |
| Anonymized data | Indefinite | N/A |
| Consent records | 5 years | Secure deletion |
| Analysis results | Indefinite | N/A |
| Workshop recordings | 6 months | Secure deletion |

## Backup Procedures

### Daily
- Database incremental backup
- Active document backup
- Form response sync

### Weekly
- Full database backup
- Complete file backup
- Verification test

### Monthly
- Archive to cold storage
- Clean temporary files
- Audit access logs

## Audit Trail

### Required Documentation
- Data source and date
- Processing steps taken
- Transformations applied
- Quality checks performed
- Final destination

### Change Log Format
```
Date | User | Action | Reason | Verification
```

## Common Issues

| Issue | Response |
|-------|----------|
| Duplicate entries | Merge and document |
| Missing consent | Do not use data |
| Corruption detected | Restore from backup |
| Unauthorized access | Reset credentials |
| Lost data | Check backups, document |

## Responsibilities

### Principal Investigator
- Overall compliance
- Policy enforcement
- Incident response
- Audit oversight

### Research Assistant
- Day-to-day handling
- Quality checks
- Documentation
- Backup execution

## Review
This SOP should be reviewed:
- Before project start
- After any incident
- At project completion
- Annually if project extends