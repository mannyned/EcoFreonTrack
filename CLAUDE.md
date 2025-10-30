# EcoFreonTrack - Claude Code Project Configuration

## Project Overview

**EcoFreonTrack** is an EPA Section 608 Refrigerant Tracking & Compliance System designed for HVAC businesses to maintain compliance with federal regulations (40 CFR Part 82). The system provides role-based access control, comprehensive tracking of equipment, refrigerants, and service activities, automated compliance monitoring, and document management.

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML5, CSS3, JavaScript, Chart.js
- **Template Engine:** Jinja2
- **Authentication:** Flask session-based with werkzeug password hashing
- **File Uploads:** werkzeug secure_filename

## Project Structure

```
EcoFreonTrack/
├── app.py                  # Main Flask application
├── models.py               # SQLAlchemy database models
├── auth.py                 # Authentication and authorization
├── config.py               # Configuration management
├── file_utils.py           # File upload utilities
├── templates/              # Jinja2 HTML templates
├── static/
│   └── css/
│       └── style.css       # Main stylesheet
├── instance/               # Database instance
├── uploads/                # User uploaded files
├── context/                # Design documentation
│   ├── design-principles.md
│   └── style-guide.md
├── .claude/                # Claude Code configuration
│   ├── commands/           # Slash commands
│   └── agents/             # Subagents
└── .github/
    └── workflows/          # GitHub Actions
```

## User Roles

1. **Technician**: Field technicians who log service work
2. **Compliance Manager**: Oversight, reporting, and compliance monitoring
3. **Admin**: Full system access, user management
4. **Auditor**: Read-only compliance review

## Visual Development

### Design Principles
- Comprehensive design checklist in `/context/design-principles.md`
- Brand style guide in `/context/style-guide.md`
- When making visual (front-end, UI/UX) changes, always refer to these files for guidance

### Quick Visual Check
IMMEDIATELY after implementing any front-end change:
1. **Identify what changed** - Review the modified components/pages
2. **Navigate to affected pages** - Use `mcp__playwright__browser_navigate` to visit each changed view
3. **Verify design compliance** - Compare against `/context/design-principles.md` and `/context/style-guide.md`
4. **Validate feature implementation** - Ensure the change fulfills the user's specific request
5. **Check acceptance criteria** - Review any provided context files or requirements
6. **Capture evidence** - Take full page screenshot at desktop viewport (1440px) of each changed view
7. **Check for errors** - Run `mcp__playwright__browser_console_messages`

This verification ensures changes meet design standards and user requirements.

### Comprehensive Design Review
Invoke the `@agent-design-review` subagent for thorough design validation when:
- Completing significant UI/UX features
- Before finalizing PRs with visual changes
- Needing comprehensive accessibility and responsiveness testing

## Code Quality Workflows

### Code Review
- **Slash Command:** `/review` - Review pending changes on current branch
- **Agent:** `@agent-code-reviewer` - Comprehensive code quality review
- **GitHub Action:** Automatic review on all PRs
- **Framework:** Pragmatic Quality - balances rigorous standards with development velocity

### Security Review
- **Slash Command:** `/security-review` - Security vulnerability scanning
- **GitHub Action:** Automatic security scan on all PRs
- **Standards:** OWASP Top 10, Anthropic security best practices
- **Coverage:** Vulnerabilities, exposed secrets, attack vectors

### Design Review
- **Slash Command:** `/design-review` - Comprehensive UI/UX review
- **Agent:** `@agent-design-reviewer` - Automated design quality assessment
- **Tools:** Playwright MCP for live environment testing
- **Standards:** Inspired by Stripe, Airbnb, Linear

## Development Environment

### Running the Application
```bash
cd C:\Users\Manny\EcoFreonTrack
python app.py
```
Application runs on: http://127.0.0.1:3000

### Default Admin Credentials
- Username: `admin`
- Password: `Admin123!`
- **IMPORTANT:** Change on first login

### Database Management
- Database: `instance/epa608_tracker_dev.db`
- Migrations: Manual SQL or Python scripts
- Backup location: `instance/*.db.backup`

## Key Features

1. **Customer Management**: Track customer/company information and link equipment
2. **Equipment Tracking**: Monitor refrigeration equipment and compliance status
3. **Technician Management**: EPA 608 certification tracking with certificate uploads
4. **Service Logging**: Record all refrigerant service work
5. **Leak Inspections**: EPA-required leak inspection documentation
6. **Compliance Alerts**: Automated alerts for threshold violations
7. **Refrigerant Inventory**: Purchase, usage, and recovery tracking
8. **Document Management**: Certificate and compliance document storage
9. **Reports & Analytics**: EPA-compliant reports and dashboards
10. **AI Features**: Leak prediction AI, natural language service entry

## Compliance Requirements

### EPA Section 608 Key Points
- Service records must be maintained for 3 years minimum
- Leak rate thresholds: 10%, 20%, or 30% based on equipment type
- Inspections required within 30 days of threshold exceedance
- All technicians must be EPA 608 certified
- Recovery equipment must be certified
- Proper documentation of all refrigerant transactions

## Brand Guidelines

### Colors
- **Primary:** Teal Green (#00B4A0)
- **Background:** Light Gray (#F9FAFB)
- **Text Primary:** Dark Navy (#111327)
- **Text Secondary:** Medium Gray (#6B7280)
- **Success:** Green (#28a745)
- **Danger:** Red (#dc3545)
- **Warning:** Yellow (#ffc107)

### Typography
- **Font:** Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Body:** 16px, line-height 1.6
- **Headings:** Bold, hierarchical sizing

### Spacing
- **Base unit:** 8px
- **Scale:** 4px, 8px, 16px, 24px, 32px, 48px

## Testing Guidelines

### Manual Testing Checklist
1. Login with different user roles
2. Test CRUD operations for all entities
3. Verify role-based access control
4. Test file uploads (certificates, documents)
5. Verify calculations (leak rates, inventory)
6. Test responsive design on mobile
7. Check accessibility (keyboard navigation, screen readers)

### Important Test Users
- Create test users with Python script: `python create_test_users.py`
- Test with all three roles: technician, compliance_manager, admin

## GitHub Integration

### Repository
https://github.com/mannyned/EcoFreonTrack.git

### Workflows
- **Code Review:** `.github/workflows/code-review.yml`
- **Security Scan:** `.github/workflows/security.yml`

### Commit Guidelines
- Use detailed commit messages
- Reference EPA compliance when applicable
- Include "Generated with Claude Code" footer
- Co-author: Claude <noreply@anthropic.com>

## Documentation

- **USER_GUIDE.md**: Comprehensive user documentation
- **AI_FEATURES_GUIDE.md**: AI feature documentation
- **ENVIRONMENT_GUIDE.md**: Environment setup
- **SUPABASE_SETUP_GUIDE.md**: Cloud database setup

## Common Commands

### Git Operations
```bash
git status
git add .
git commit -m "message"
git push
```

### Database Operations
```bash
# Backup database
copy instance\epa608_tracker_dev.db instance\epa608_tracker_dev.db.backup

# Add column to table
python -c "import sqlite3; conn = sqlite3.connect('instance/epa608_tracker_dev.db'); ..."
```

### File Management
```bash
# View directory structure
dir /s /b

# Find files
find . -name "*.py"
```

## Notes for Claude Code

- Always check `context/design-principles.md` and `context/style-guide.md` before making UI changes
- Use Playwright MCP for visual verification after front-end changes
- Follow EPA compliance requirements for all refrigerant-related features
- Maintain role-based access control in all new features
- Test with multiple user roles before committing
- Use the established color scheme (Teal Green primary)
- Keep code organized and well-commented
- Update USER_GUIDE.md when adding new features
