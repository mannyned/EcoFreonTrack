# EcoFreonTrack Environment Management Guide

## Overview

EcoFreonTrack supports **three separate environments** to ensure safe development, testing, and production deployment:

1. **Development** - For active development and testing new features
2. **Production** - For live compliance tracking with real data
3. **Testing** - For automated testing (optional)

Each environment uses its own database file to prevent data mixing and ensure regulatory compliance.

---

## Database Files

### Location: `instance/` folder

| Environment | Database File | Purpose |
|-------------|---------------|---------|
| Development | `epa608_tracker_dev.db` | Development and testing |
| Production | `epa608_tracker_prod.db` | Live compliance data |
| Testing | `epa608_tracker_test.db` | Automated tests |

**IMPORTANT**: These database files are **excluded from git** to protect sensitive compliance data.

---

## Running the Application

### Windows Users

#### Development Mode (Recommended for testing)
```batch
run_dev.bat
```
- Database: `instance/epa608_tracker_dev.db`
- Debug mode: ON
- SQL query logging: ON
- Access: http://localhost:5000

#### Production Mode
```batch
run_prod.bat
```
- Database: `instance/epa608_tracker_prod.db`
- Debug mode: OFF
- SQL query logging: OFF
- Access: http://localhost:5000

### Command Line (All Platforms)

#### Development Mode
```bash
# Windows
set FLASK_ENV=development
python app.py

# Linux/Mac
export FLASK_ENV=development
python app.py
```

#### Production Mode
```bash
# Windows
set FLASK_ENV=production
set SECRET_KEY=your-secure-secret-key-here
python app.py

# Linux/Mac
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key-here
python app.py
```

---

## Configuration Details

### Development Configuration
- **Debug mode**: Enabled
- **SQL logging**: Enabled (see all database queries)
- **Database**: `instance/epa608_tracker_dev.db`
- **Secret key**: Uses default (not secure, but OK for dev)
- **Auto-reload**: Server restarts when code changes

**Use for**:
- Testing new features
- Experimenting with data
- Learning the system
- Development workflows

### Production Configuration
- **Debug mode**: Disabled
- **SQL logging**: Disabled
- **Database**: `instance/epa608_tracker_prod.db`
- **Secret key**: MUST be set via environment variable
- **Security**: Enhanced cookie security

**Use for**:
- Live compliance tracking
- Real equipment and service records
- EPA audit preparation
- Official reporting

---

## Best Practices

### 1. **Always Use Development for Testing**
```batch
# Test a new feature in development
run_dev.bat
# Navigate to http://localhost:5000
# Add test equipment, service logs, etc.
```

### 2. **Keep Production Data Safe**
- Never delete or modify production database manually
- Always backup `instance/epa608_tracker_prod.db` before major changes
- Use the database viewer tool to inspect data: `python view_database.py`

### 3. **Set Secret Key in Production**
```batch
# Windows
set SECRET_KEY=generate-a-long-random-string-here-min-32-chars
run_prod.bat

# Linux/Mac
export SECRET_KEY=generate-a-long-random-string-here-min-32-chars
python app.py
```

Generate a secure secret key with Python:
```python
import secrets
print(secrets.token_hex(32))
```

### 4. **Regular Backups (Production)**
```batch
# Windows backup script
xcopy /Y instance\epa608_tracker_prod.db backups\epa608_tracker_prod_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db

# Linux/Mac
cp instance/epa608_tracker_prod.db backups/epa608_tracker_prod_$(date +%Y%m%d).db
```

### 5. **Database Migration Between Environments**

#### Copy Development to Production (when ready)
```batch
# CAUTION: This will REPLACE production data!
copy instance\epa608_tracker_dev.db instance\epa608_tracker_prod.db
```

#### Reset Development Database
```batch
# Delete development database to start fresh
del instance\epa608_tracker_dev.db
# Restart app - it will create new empty database
run_dev.bat
```

---

## Database Viewer Tool

View any database without starting the web app:

```batch
# View development database
python view_database.py
```

By default, it reads `instance/epa608_tracker.db`. To view specific databases:

**Edit `view_database.py` line 8:**
```python
# Development
DB_PATH = 'instance/epa608_tracker_dev.db'

# Production
DB_PATH = 'instance/epa608_tracker_prod.db'
```

**Features**:
1. View all tables and records
2. Export to CSV files
3. Run custom SQL queries

---

## Switching Between Environments

### Scenario 1: Testing a New Feature

1. Start in development:
   ```batch
   run_dev.bat
   ```

2. Test the feature thoroughly

3. If satisfied, switch to production:
   - Stop the dev server (Ctrl+C)
   - Run `run_prod.bat`
   - Or manually migrate data if needed

### Scenario 2: Daily Operations

**Morning (Development)**
```batch
run_dev.bat
# Practice logging service records
# Test leak inspections
# Familiarize team with system
```

**Afternoon (Production)**
```batch
run_prod.bat
# Log actual service work
# Record real inspections
# Generate compliance reports
```

---

## Environment Variables

Create a `.env` file (copy from `.env.example`):

```ini
# .env file
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5000
HOST=0.0.0.0
```

**Note**: `.env` files are NOT committed to git for security.

---

## Security Recommendations

### Development
- ✅ Use default settings
- ✅ Share test data freely
- ✅ SQL logging enabled for debugging

### Production
- ⚠️ **MUST** set SECRET_KEY environment variable
- ⚠️ **MUST** backup database regularly
- ⚠️ **MUST** use HTTPS in deployment (not HTTP)
- ⚠️ **MUST** restrict access to authorized personnel
- ⚠️ **NEVER** commit production database to git
- ⚠️ **NEVER** share production SECRET_KEY

---

## Deployment Checklist

Before deploying to production:

- [ ] Set strong SECRET_KEY environment variable
- [ ] Verify database backups are configured
- [ ] Test all features in development environment
- [ ] Ensure FLASK_ENV=production
- [ ] Document access procedures for team
- [ ] Configure firewall/network security
- [ ] Set up regular backup schedule
- [ ] Train users on production vs development
- [ ] Establish data retention policies (EPA requirements)
- [ ] Test disaster recovery procedures

---

## Troubleshooting

### Problem: App uses wrong database

**Solution**: Check FLASK_ENV variable
```batch
# Windows
echo %FLASK_ENV%

# Set it explicitly
set FLASK_ENV=development
```

### Problem: Production won't start (SECRET_KEY error)

**Solution**: Set SECRET_KEY
```batch
set SECRET_KEY=your-very-long-random-secret-key-minimum-32-characters
run_prod.bat
```

### Problem: Want to reset development database

**Solution**: Delete and restart
```batch
del instance\epa608_tracker_dev.db
run_dev.bat
```

### Problem: Need to view database without starting app

**Solution**: Use database viewer
```batch
python view_database.py
```

---

## EPA Compliance Notes

### Data Retention
- **Service records**: Keep for 3 years (40 CFR 82.166)
- **Disposal records**: Keep for 3 years
- **Leak inspection records**: Keep for 3 years

### Backup Requirements
- Regular backups protect against data loss
- EPA audits may require historical records
- Keep backups for at least 3 years

### Production Database Security
- Contains sensitive business information
- Equipment details may be proprietary
- Technician certification numbers are personal data
- Follow your organization's data protection policies

---

## Quick Reference

| Task | Command |
|------|---------|
| Start development | `run_dev.bat` |
| Start production | `run_prod.bat` |
| View database | `python view_database.py` |
| Backup production | `copy instance\epa608_tracker_prod.db backups\` |
| Reset development | `del instance\epa608_tracker_dev.db` |
| Generate secret key | `python -c "import secrets; print(secrets.token_hex(32))"` |

---

**Remember**: When in doubt, use **Development mode**. It's safe to experiment, test, and learn without risking compliance data!
