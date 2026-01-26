# SIREN Technical Stack

## Core Technologies

### Database
- **PostgreSQL 15+**
  - Primary data storage
  - 8 core tables (factors, evidence, sources, stakeholders, etc.)
  - Views for analysis
  - Daily backups

### Programming
- **Python 3.10+**
  - pandas: Data manipulation
  - networkx: Network analysis for constraint identification
  - psycopg2: PostgreSQL connection
  - scikit-learn: Statistical analysis
  - matplotlib/seaborn: Visualization
  - openpyxl: Excel file handling

### Data Collection
- **Microsoft Forms**
  - Stakeholder surveys
  - Workshop feedback
  - Connected to SharePoint

- **Microsoft SharePoint**
  - Form response storage
  - Document management
  - Team collaboration

### Visualization
- **Power BI**
  - Interactive dashboards
  - Direct query to PostgreSQL
  - Stakeholder-friendly reports

### Version Control
- **Git/GitHub**
  - Code versioning
  - Documentation
  - Future public repository

## Development Environment

### Local Setup Requirements
```bash
# PostgreSQL (without Docker initially)
brew install postgresql@15  # macOS
# or download installer from postgresql.org

# Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Python Dependencies (requirements.txt)
```
pandas>=1.5.0
numpy>=1.23.0
networkx>=2.8
psycopg2-binary>=2.9.0
python-dotenv>=0.21.0
scikit-learn>=1.1.0
matplotlib>=3.5.0
seaborn>=0.12.0
openpyxl>=3.0.0
requests>=2.28.0
```

### Environment Variables (.env)
```
# Database
DB_HOST=localhost
DB_NAME=siren
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_PORT=5432

# Microsoft
SHAREPOINT_URL=https://company.sharepoint.com/sites/SIREN
SHAREPOINT_CLIENT_ID=xxx
SHAREPOINT_SECRET=xxx

# Power BI
POWERBI_WORKSPACE=SIREN_Analysis
```

## File Structure
```
SIREN/
├── .env                    # Environment variables (git-ignored)
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── data/
│   ├── raw/              # Original data files
│   ├── processed/        # Cleaned data
│   └── results/          # Analysis outputs
├── scripts/
│   ├── database/         # SQL scripts
│   ├── data_import/      # Form to database scripts
│   ├── analysis/         # Analysis scripts
│   └── visualization/    # Figure generation
├── notebooks/            # Jupyter notebooks (optional)
├── forms/               # Microsoft Forms templates
├── reports/             # Generated reports
└── docs/                # Documentation
```

## Integration Points

### Microsoft Forms → PostgreSQL
- Power Automate (optional) or Python polling
- Validation before database insert
- Error logging and retry logic

### PostgreSQL → Power BI
- Direct Query connection
- Service account credentials
- Indexed views for performance

### Python → PostgreSQL
- Connection pooling
- Transaction management
- Prepared statements for security

## Security Considerations
- Database passwords in .env file (never committed)
- GDPR compliance for stakeholder data
- Encrypted connections (SSL/TLS)
- Role-based database access

## Performance Requirements
- Support 50 concurrent workshop participants
- Sub-second query response for dashboards
- Batch processing for large imports

## Deployment Phases

### Phase 1: Development (Current)
- Local PostgreSQL
- Manual processes
- Testing and refinement

### Phase 2: Production (Workshop period)
- Consider cloud PostgreSQL if needed
- Automated data collection
- Live dashboards

### Phase 3: Archival (Post-project)
- Static dataset export
- Code repository public
- Documentation complete