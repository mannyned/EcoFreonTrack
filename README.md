# EcoFreonTrack


A comprehensive web application for tracking refrigerant usage, leakage, recovery, and disposal in compliance with **EPA Section 608** (40 CFR Part 82).

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Database](https://img.shields.io/badge/database-Supabase-green.svg)

## Overview

EcoFreonTrack is an enterprise-grade web application that helps businesses and technicians maintain compliance with EPA regulations for handling refrigerants (CFCs, HCFCs, HFCs). Features include:

- **Role-Based Access Control** - Three-tier user system (Technician, Compliance Manager, Admin)
- **Cloud Database Integration** - Supabase PostgreSQL or local SQLite
- **Document Management** - Upload and organize certificates, compliance documents, and photos
- **AI-Powered Compliance** - Automated alerts and intelligent monitoring
- Equipment inventory and refrigerant charges
- Leak rate monitoring and inspection schedules
- Service and repair logs with refrigerant usage
- Technician EPA 608 certification tracking
- Recovery and disposal records
- Refrigerant purchase and inventory management
- Automated compliance alerts

## Key Compliance Requirements (40 CFR Part 82)

### Equipment Leak Rate Monitoring
- **10% Threshold**: Commercial refrigeration and industrial process equipment
- **20% Threshold**: Comfort cooling equipment
- **30% Threshold**: Appliances with full charge < 50 lbs

### Leak Inspection Requirements
- **Within 30 days** of exceeding leak rate threshold
- **Follow-up verification** after repairs
- **Documentation** of all inspections and findings

### Service Records (40 CFR 82.166)
- Date of service
- Technician EPA 608 certification
- Refrigerant added/recovered (in pounds)
- Work performed
- Leak detection and repair details

### Technician Certification
- **Type I**: Small appliances
- **Type II**: High-pressure systems
- **Type III**: Low-pressure systems
- **Universal**: All types

### Recovery & Disposal
- Required for all servicing and disposal
- Certified recovery equipment
- Proper documentation of recovered refrigerant
- Tracking to approved reclamation facilities

## Features

### Role-Based Access Control (RBAC)

**Three User Roles:**

1. **Technician**
   - Add service logs and refrigerant transactions
   - Upload EPA 608 certificates
   - View their own service history
   - Limited access to compliance data

2. **Compliance Manager**
   - View comprehensive dashboards
   - Approve and review service logs
   - Generate compliance reports
   - Monitor all compliance alerts
   - Resolve compliance issues

3. **Admin/Owner**
   - Full system access
   - Manage users and roles
   - Manage sites and equipment
   - Configure system settings
   - Access all features

**Security Features:**
- Password hashing with Werkzeug (scrypt algorithm)
- Session-based authentication
- Permission-based authorization
- Account activation controls
- Last login tracking

### Equipment Management
- Track all equipment containing refrigerants
- Record equipment specifications (type, location, charge size)
- Monitor equipment status (Active, Retired, Disposed)
- Set custom leak rate thresholds and inspection frequencies

### Leak Monitoring
- Automatic leak rate calculations
- Inspection scheduling and tracking
- Compliance status monitoring
- Alert system for exceeded thresholds

### Service Logging
- Comprehensive service record keeping
- Refrigerant usage tracking (added/recovered)
- Leak detection and repair documentation
- Follow-up scheduling

### Technician Management
- EPA 608 certification tracking
- Certification expiration alerts
- Service history per technician
- Link user accounts to technician records

### Refrigerant Inventory
- Real-time inventory tracking
- Purchase and usage records
- Recovery cylinder management
- Low-stock alerts
- Disposal documentation

### Document Management
- Upload EPA 608 certificates
- Store service documentation
- Attach photos to service logs
- Organize compliance documents
- Secure file storage

### Cloud Database Integration
- **Supabase PostgreSQL** for production (cloud-hosted)
- **SQLite** for local development and testing
- Automatic schema migration
- Secure connection with environment variables
- Real-time data synchronization

### Compliance Alerts
- Leak rate threshold exceeded
- Inspection overdue
- Certification expiring
- Inventory low
- Follow-up service required

### Reporting
- Equipment compliance summary
- Refrigerant usage reports
- Service history
- Inspection records
- Regulatory compliance status

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Supabase account for cloud database

### Setup

1. **Clone or download** this repository:
   ```bash
   cd EcoFreonTrack
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Configure Supabase**:

   For cloud database, create a `.env` file:
   ```bash
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   DATABASE_URL=postgresql://postgres:[password]@[host]/postgres
   ```

   See `SUPABASE_SETUP_GUIDE.md` for detailed instructions.

4. **Set up Role-Based Access Control**:
   ```bash
   python setup_rbac.py
   ```

   This creates the user table and initial admin account:
   - **Username:** admin
   - **Password:** Admin123!

   **IMPORTANT:** Change the admin password immediately after first login!

5. **Start the application**:
   ```bash
   python app.py
   ```

6. **Log in**:
   - Open your browser to `http://localhost:5000/login`
   - Use the admin credentials from step 4
   - Change your password in user settings
   - Create additional users as needed

## Usage

### 0. User Management (Admin Only)

**Create Users:**
1. Log in as admin
2. Navigate to **User Management**
3. Click **Add New User**
4. Fill in user details:
   - Username, email, full name
   - Select role (Technician, Compliance Manager, or Admin)
   - Optionally link to technician record
   - Set password and account status
5. Click **Create User**

**Manage Users:**
- View all users and their status
- Edit user details and roles
- Activate/Deactivate accounts
- Reset passwords

### 1. Add Equipment

1. Navigate to **Equipment** → **Add New Equipment**
2. Enter equipment details:
   - Equipment ID (unique identifier)
   - Name and type
   - Location
   - Refrigerant type (CFC, HCFC, HFC)
   - Refrigerant name (R-22, R-410A, etc.)
   - Full charge (pounds)
   - Leak rate threshold (default: 10%)
   - Inspection frequency (default: 30 days)
3. Click **Save Equipment**

### 2. Register Technicians

1. Navigate to **Technicians** → **Add New Technician**
2. Enter technician details:
   - Name
   - EPA 608 Certification Number
   - Certification Type (Type I, II, III, or Universal)
   - Certification date
   - Expiration date (if applicable)
   - Contact information
3. Click **Save Technician**

### 3. Log Service Work

1. Navigate to **Service Logs** → **Add Service Log**
2. Select equipment and technician
3. Enter service details:
   - Service date and type
   - Refrigerant added (lbs)
   - Refrigerant recovered (lbs)
   - Work performed
   - Leak information (if found/repaired)
   - Follow-up requirements
4. Click **Save Service Log**

### 4. Conduct Leak Inspections

1. Navigate to **Leak Inspections** → **Add Inspection**
2. Select equipment and technician
3. Enter inspection details:
   - Inspection date and type
   - Leak detected (yes/no)
   - Current charge (lbs)
   - Leak location and severity
   - Inspector notes
4. System automatically calculates:
   - Annual leak rate
   - Compliance status
   - Next inspection date
5. Click **Save Inspection**

### 5. Manage Refrigerant Inventory

1. Navigate to **Inventory**
2. View current stock levels
3. Adjust inventory:
   - Click **Adjust** next to refrigerant
   - Enter positive (purchase) or negative (usage) amount
   - Add notes
   - Click **Save Adjustment**

### 6. Monitor Compliance

1. **Dashboard** shows:
   - Active equipment count
   - Technician count
   - Active compliance alerts
   - Upcoming inspections
   - Low inventory warnings
   - Recent service activity

2. **Alerts** page shows:
   - Leak rate threshold exceeded
   - Inspection overdue
   - Certification expiring
   - Other compliance issues

3. **Equipment Detail** page shows:
   - Current compliance status
   - Annual leak rate vs. threshold
   - Service history
   - Inspection records
   - Refrigerant usage

## Database Schema

### Equipment
- ID, Equipment ID (unique), Name, Type, Location
- Manufacturer, Model, Serial Number
- Refrigerant Type/Name, Full Charge
- Status, Install Date, Retire Date
- Leak Rate Threshold, Inspection Frequency

### Technician
- ID, Name, Certification Number (unique)
- Certification Type, Dates
- Email, Phone, Company
- Status

### ServiceLog
- ID, Equipment, Technician
- Service Date, Service Type
- Refrigerant Added/Recovered
- Work Performed
- Leak Information
- Follow-up Requirements

### LeakInspection
- ID, Equipment, Technician
- Inspection Date, Type
- Leak Detected, Location, Severity
- Current Charge, Charge Deficit
- Annual Leak Rate, Compliant Status
- Next Inspection Date

### RefrigerantTransaction
- ID, Equipment (optional)
- Transaction Date, Type (Purchase/Added/Recovered/Disposed)
- Refrigerant Type/Name, Quantity
- Supplier, Invoice, Cost
- Cylinder Number, Disposal Method/Facility

### ComplianceAlert
- ID, Equipment/Technician (optional)
- Alert Date, Type, Severity
- Title, Message
- Status, Resolution Details

### RefrigerantInventory
- ID, Refrigerant Type/Name
- Quantity On Hand, Quantity Recovered
- Reorder Level, Below Reorder Status

### User
- ID, Username (unique), Email (unique)
- Password Hash, Full Name, Phone
- Role (technician/compliance_manager/admin)
- Technician ID (optional link to Technician table)
- Is Active, Is Verified
- Created At, Updated At, Last Login

### Document
- ID, Equipment/Service Log/Technician (optional links)
- Document Type (certificate, invoice, photo, report, other)
- File Name, File Path, File Size, MIME Type
- Description, Uploaded At

## API Endpoints

### Equipment
- `GET /api/equipment` - Get all equipment (JSON)
- `GET /api/compliance-status/<equipment_id>` - Get compliance status

## Compliance Best Practices

### 1. Regular Inspections
- Schedule inspections based on equipment type and history
- Document all findings thoroughly
- Address leaks promptly

### 2. Accurate Record Keeping
- Log all refrigerant usage immediately
- Maintain detailed service records
- Track technician certifications

### 3. Proactive Monitoring
- Review compliance dashboard regularly
- Respond to alerts promptly
- Schedule follow-ups on time

### 4. Proper Recovery
- Use certified recovery equipment
- Document all recovered refrigerant
- Arrange proper disposal/reclamation

### 5. Technician Compliance
- Verify certifications before service
- Track certification expiration dates
- Ensure proper training

## EPA Section 608 Penalties

Non-compliance can result in significant penalties:
- **Civil penalties**: Up to $44,539 per day per violation
- **Criminal penalties**: Up to $25,000 per day and/or imprisonment

## EPA Resources

- [EPA Section 608 Overview](https://www.epa.gov/section608)
- [40 CFR Part 82](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-82)
- [EPA Technician Certification](https://www.epa.gov/section608/technician-certification)
- [Leak Repair Requirements](https://www.epa.gov/section608/leak-repair-requirements)

## Project Structure

```
EcoFreonTrack/
├── app.py                    # Flask application with routes
├── models.py                 # Database models (SQLAlchemy)
├── auth.py                   # Authentication and authorization module
├── setup_rbac.py             # RBAC setup script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── USER_GUIDE.md             # Comprehensive user guide
├── RBAC_IMPLEMENTATION_SUMMARY.md # RBAC documentation
├── SUPABASE_SETUP_GUIDE.md   # Cloud database setup guide
├── .env                      # Environment variables (create this)
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── login.html           # Login page
│   ├── dashboard.html       # Main dashboard
│   ├── user_list.html       # User management (admin)
│   ├── user_form.html       # Add/edit user (admin)
│   ├── equipment_list.html  # Equipment listing
│   ├── equipment_detail.html # Equipment detail page
│   ├── equipment_form.html  # Add/edit equipment
│   ├── technician_list.html # Technician listing
│   ├── technician_form.html # Add/edit technician
│   ├── service_log_list.html # Service logs
│   ├── service_log_form.html # Add service log
│   ├── leak_inspection_list.html # Inspection listing
│   ├── leak_inspection_form.html # Add inspection
│   ├── inventory.html       # Refrigerant inventory
│   ├── alert_list.html      # Compliance alerts
│   ├── document_list.html   # Document management
│   └── reports.html         # Compliance reports
├── static/
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       └── main.js         # JavaScript functions
├── uploads/                 # Uploaded documents (created automatically)
└── epa608_tracker.db       # SQLite database (created on first run)
```

## Disclaimer

**IMPORTANT**: This application is a tool to help track and manage EPA Section 608 compliance. It does NOT:

- Replace professional legal advice
- Guarantee EPA compliance
- Substitute for proper technician training
- Eliminate the need for certified recovery equipment
- Replace official EPA reporting requirements

Users are responsible for:
- Ensuring accurate data entry
- Following all EPA regulations
- Maintaining proper certifications
- Using approved equipment and procedures
- Consulting with EPA compliance experts

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Contact: [Your Contact Information]

## Version History

### v2.0.0 (Current - October 2025)
- **Role-Based Access Control (RBAC)** - Three-tier user system
- **User Authentication** - Secure login with password hashing
- **User Management** - Admin interface for managing users
- **Supabase Integration** - Cloud PostgreSQL database support
- **Document Management** - Upload and organize compliance documents
- **Enhanced Security** - Session-based auth, permission decorators
- Technician-User account linking
- Last login tracking
- Account activation controls

### v1.0.0 (September 2025)
- Initial release
- Equipment management and tracking
- Leak inspection and monitoring
- Service log management
- Technician certification tracking
- Refrigerant inventory management
- Compliance alerts and reporting
- Full EPA Section 608 compliance features

## Future Enhancements

- Email notifications for alerts
- PDF report generation with digital signatures
- Mobile app integration
- Advanced analytics and trends
- Integration with refrigerant suppliers
- Barcode/QR code scanning for equipment
- Two-factor authentication (2FA)
- Audit logs for compliance tracking
- Multi-site management
- Custom report builder

---

**Developed for EPA Section 608 Compliance**
**Version 2.0.0**
**Last Updated: October 2025**

## Additional Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Comprehensive user guide with step-by-step instructions
- **[RBAC_IMPLEMENTATION_SUMMARY.md](RBAC_IMPLEMENTATION_SUMMARY.md)** - Detailed RBAC system documentation
- **[SUPABASE_SETUP_GUIDE.md](SUPABASE_SETUP_GUIDE.md)** - Cloud database configuration guide
