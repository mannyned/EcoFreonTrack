# EcoFreonTrack


A comprehensive web application for tracking refrigerant usage, leakage, recovery, and disposal in compliance with **EPA Section 608** (40 CFR Part 82).

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## Overview

This application helps businesses and technicians maintain compliance with EPA regulations for handling refrigerants (CFCs, HCFCs, HFCs). It provides comprehensive tracking for:

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

### Refrigerant Inventory
- Real-time inventory tracking
- Purchase and usage records
- Recovery cylinder management
- Low-stock alerts
- Disposal documentation

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

### Setup

1. **Clone or download** this repository:
   ```bash
   cd EcoFreonTrack
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database** (automatic on first run):
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser to `http://localhost:5000`

## Usage

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
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── templates/               # HTML templates
│   ├── dashboard.html       # Main dashboard
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
│   └── reports.html         # Compliance reports
├── static/
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       └── main.js         # JavaScript functions
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

### v1.0.0 (Current)
- Initial release
- Equipment management and tracking
- Leak inspection and monitoring
- Service log management
- Technician certification tracking
- Refrigerant inventory management
- Compliance alerts and reporting
- Full EPA Section 608 compliance features

## Future Enhancements

- Multi-user authentication and roles
- Email notifications for alerts
- PDF report generation
- Mobile app integration
- Cloud database support
- Advanced analytics and trends
- Integration with refrigerant suppliers
- Barcode/QR code scanning
- Photo attachments for service logs

---

**Developed for EPA Section 608 Compliance**
**Version 1.0.0**
**Last Updated: October 2025**
