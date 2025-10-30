# EcoFreonTrack User Guide

**Version 2.0.0** | EPA Section 608 Refrigerant Tracking & Compliance System

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [User Roles and Permissions](#user-roles-and-permissions)
4. [Logging In](#logging-in)
5. [Dashboard Overview](#dashboard-overview)
6. [User Management (Admin Only)](#user-management-admin-only)
7. [Equipment Management](#equipment-management)
8. [Technician Management](#technician-management)
9. [Customer Management](#customer-management)
10. [Service Logging](#service-logging)
11. [Leak Inspections](#leak-inspections)
12. [Refrigerant Inventory](#refrigerant-inventory)
13. [Document Management](#document-management)
14. [Compliance Alerts](#compliance-alerts)
15. [Reports and Analytics](#reports-and-analytics)
16. [EPA Compliance Guidelines](#epa-compliance-guidelines)
17. [Troubleshooting](#troubleshooting)
18. [Best Practices](#best-practices)

---

## Introduction

EcoFreonTrack is designed to help businesses maintain compliance with EPA Section 608 regulations (40 CFR Part 82) for refrigerant management. This system provides:

- **Role-based access control** for secure, organized workflows
- **Comprehensive tracking** of equipment, refrigerants, and service activities
- **Automated compliance monitoring** with proactive alerts
- **Document management** for certificates and compliance records
- **Cloud database integration** for reliable data storage

### Who Should Use This Guide?

- **Administrators/Owners** - System setup, user management, full access
- **Compliance Managers** - Dashboard monitoring, report generation, log approval
- **Technicians** - Service logging, certificate uploads, daily operations

---

## Getting Started

### Initial Setup

1. **Install EcoFreonTrack** (see README.md for installation instructions)

2. **Run the RBAC setup script**:
   ```bash
   python setup_rbac.py
   ```

   This creates the initial admin account:
   - Username: `admin`
   - Password: `Admin123!`

3. **Start the application**:
   ```bash
   python app.py
   ```

4. **Access the system**:
   - Open your browser to `http://localhost:5000/login`

5. **First Login**:
   - Log in with admin credentials
   - **IMMEDIATELY change your password** (see User Management section)
   - Create additional user accounts as needed

### System Requirements

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for cloud database features)

---

## User Roles and Permissions

EcoFreonTrack implements a three-tier role-based access control system:

### 1. Technician

**Purpose**: Field technicians who perform service work

**Permissions**:
- Add service logs
- Record refrigerant transactions
- Upload EPA 608 certificates
- View their own service history
- Access limited compliance data

**Cannot**:
- View all system data
- Approve logs
- Generate reports
- Manage users or equipment

**Use Case**: John is a field technician with EPA 608 Type II certification. He logs into EcoFreonTrack at each job site to record refrigerant added, leaks found, and work performed.

### 2. Compliance Manager

**Purpose**: Oversight and compliance monitoring

**Permissions**:
- View comprehensive dashboards
- Approve and review service logs
- Generate compliance reports
- Monitor all compliance alerts
- Resolve compliance issues
- View all logs and equipment data

**Cannot**:
- Manage users
- Manage sites and equipment
- Access billing features

**Use Case**: Sarah is the compliance manager who reviews all service logs weekly, generates monthly EPA reports, and monitors leak rate thresholds across all equipment.

### 3. Admin/Owner

**Purpose**: Full system administration

**Permissions**:
- **All permissions** (complete system access)
- Manage users and roles
- Manage sites and equipment
- Manage technicians
- Configure system settings
- Access billing features

**Use Case**: Mike is the business owner who manages the entire system, creates user accounts for new employees, adds new equipment locations, and configures compliance thresholds.

---

## Logging In

### First-Time Login (Admin)

1. Navigate to `http://localhost:5000/login`

2. Enter default credentials:
   - Username: `admin`
   - Password: `Admin123!`

3. Click **Log In**

4. You will see a welcome message and be directed to the dashboard

5. **IMPORTANT**: Change your password immediately:
   - Navigate to **User Management**
   - Click **Edit** next to your admin user
   - Enter a new secure password
   - Click **Update User**

### Standard Login

1. Navigate to the login page

2. Enter your username and password

3. Click **Log In**

4. Upon successful login:
   - You'll see a welcome message with your name
   - You'll be directed to the main dashboard
   - Your last login time is recorded

### Login Errors

**"Invalid username or password"**
- Check that your credentials are correct
- Passwords are case-sensitive
- Contact your administrator if you've forgotten your password

**"Your account is inactive"**
- Your account has been deactivated
- Contact your administrator to reactivate it

### Logout

- Click the **Logout** button in the navigation menu
- You'll be returned to the login page
- Your session will be cleared

---

## Dashboard Overview

The dashboard is your home screen after logging in. Content varies by user role:

### All Users See:

- **Active Equipment Count** - Total number of active refrigeration systems
- **Total Technicians** - Number of registered EPA-certified technicians
- **Active Alerts** - Current compliance issues requiring attention
- **Recent Activity** - Latest service logs and inspections

### Compliance Managers and Admins Also See:

- **Upcoming Inspections** - Equipment due for leak inspections
- **Low Inventory Warnings** - Refrigerants below reorder levels
- **Certification Expiration Alerts** - Technicians with expiring certifications
- **Compliance Status Summary** - Overall system compliance health

### Navigation Menu

The navigation menu provides access to all system features based on your role:

- **Dashboard** - Return to home screen
- **Equipment** - Manage refrigeration equipment
- **Technicians** - Manage EPA-certified technicians
- **Service Logs** - Record and view service work
- **Leak Inspections** - Conduct and track inspections
- **Inventory** - Manage refrigerant stock
- **Alerts** - View compliance alerts
- **Documents** - Upload and manage files
- **Reports** - Generate compliance reports (Manager/Admin only)
- **User Management** - Manage users (Admin only)
- **Logout** - Exit the system

---

## User Management (Admin Only)

Admins can create and manage user accounts for the entire organization.

### Viewing Users

1. Navigate to **User Management** from the menu

2. You'll see a table with all users showing:
   - Username
   - Full Name
   - Email
   - Role (with colored badge)
   - Status (Active/Inactive)
   - Last Login

3. Users are listed with color-coded role badges:
   - **Blue (Admin)** - Full system access
   - **Green (Compliance Manager)** - Oversight and reporting
   - **Cyan (Technician)** - Service logging only

### Adding a New User

1. Click **Add New User** button

2. Fill in the required information:

   **Basic Information:**
   - Username (unique, used for login)
   - Email (unique)
   - Full Name
   - Phone (optional)

   **Role Selection:**
   - Choose **Technician**, **Compliance Manager**, or **Admin**
   - Role descriptions are shown to help you decide

   **Technician Linking (Optional):**
   - Link this user account to an existing technician record
   - Useful for technicians who need system access

   **Security:**
   - Set initial password (minimum 6 characters)
   - Check **Account Active** to enable login
   - Check **Email Verified** if email is confirmed

3. Click **Create User**

4. The user can now log in with their username and password

### Editing a User

1. Click **Edit** next to the user you want to modify

2. Update any information:
   - Change role
   - Update contact information
   - Reset password (leave blank to keep current)
   - Change active/verified status

3. Click **Update User**

### Activating/Deactivating Users

**To Deactivate:**
1. Click **Deactivate** next to an active user
2. Confirm the action
3. The user will no longer be able to log in

**To Reactivate:**
1. Click **Activate** next to an inactive user
2. The user can now log in again

**Use Cases:**
- Deactivate employees who leave the company
- Temporarily disable access during investigations
- Reactivate seasonal workers

### Password Management

**Resetting User Passwords:**
1. Edit the user account
2. Enter a new password in the password field
3. Leave blank to keep the current password
4. Click **Update User**
5. Inform the user of their new password securely

**Best Practices:**
- Use strong passwords (mix of letters, numbers, symbols)
- Change default passwords immediately
- Never share passwords between users
- Change passwords if compromised

---

## Equipment Management

Track all refrigeration equipment and their refrigerant charges.

### Viewing Equipment

1. Navigate to **Equipment** from the menu

2. View equipment list with:
   - Equipment ID
   - Name and type
   - Location
   - Refrigerant type and charge
   - Status (Active, Retired, Disposed)
   - Compliance status indicator

3. Click on any equipment to view detailed information

### Adding New Equipment

1. Click **Add New Equipment**

2. Fill in equipment details:

   **Identification:**
   - Equipment ID (unique identifier)
   - Equipment Name
   - Type (e.g., Chiller, HVAC Unit, Walk-in Cooler)

   **Location:**
   - Site location
   - Building
   - Room or area

   **Specifications:**
   - Manufacturer
   - Model Number
   - Serial Number
   - Year Manufactured

   **Refrigerant Information:**
   - Refrigerant Type (CFC, HCFC, HFC)
   - Refrigerant Name (R-22, R-410A, R-134a, etc.)
   - Full Charge (pounds)

   **Compliance Settings:**
   - Leak Rate Threshold (default 10%, 20%, or 30% based on equipment type)
   - Inspection Frequency (default 30 days)

   **Dates:**
   - Installation Date
   - Last Service Date (if applicable)

3. Click **Save Equipment**

### Editing Equipment

1. Click **Edit** on the equipment detail page

2. Update any information

3. Click **Update Equipment**

### Equipment Detail Page

The detail page shows comprehensive equipment information:

**Overview:**
- All equipment specifications
- Current charge vs. full charge
- Compliance status
- Annual leak rate

**Service History:**
- All service logs for this equipment
- Refrigerant added and recovered
- Work performed
- Technician details

**Leak Inspections:**
- Inspection dates and results
- Leak rate calculations
- Compliance status over time

**Compliance Alerts:**
- Active alerts for this equipment
- Alert history
- Resolution status

**Documents:**
- Installation certificates
- Service invoices
- Photos
- Compliance documentation

### Equipment Status

**Active:**
- Equipment is in service
- Requires compliance monitoring
- Appears in reports and dashboards

**Retired:**
- Equipment removed from service
- No longer monitored for compliance
- Historical data retained

**Disposed:**
- Equipment properly disposed
- Refrigerant recovered and documented
- Kept for EPA recordkeeping

---

## Technician Management

Track EPA 608 certified technicians and their qualifications.

### Viewing Technicians

1. Navigate to **Technicians** from the menu

2. View all registered technicians with:
   - Name
   - Certification number
   - Certification type
   - Expiration date
   - Status

### Adding a Technician

1. Click **Add New Technician**

2. Enter technician information:

   **Personal Information:**
   - Full Name
   - Email
   - Phone

   **EPA 608 Certification:**
   - Certification Number (unique)
   - Certification Type:
     - **Type I**: Small appliances (< 5 lbs)
     - **Type II**: High-pressure equipment
     - **Type III**: Low-pressure equipment
     - **Universal**: All equipment types
   - Certification Date
   - Expiration Date (if applicable)

   **Employment:**
   - Company Name
   - Status (Active/Inactive)

3. Click **Save Technician**

### Certification Types Explained

**Type I:**
- Small appliances
- Refrigerators, freezers, window AC units
- Systems with < 5 lbs refrigerant charge

**Type II:**
- High-pressure systems
- Most commercial and residential AC
- Refrigeration systems > 5 lbs

**Type III:**
- Low-pressure systems
- Centrifugal chillers
- Low-pressure refrigeration

**Universal:**
- All equipment types
- Combines Types I, II, and III
- Most comprehensive certification

### Linking Technicians to User Accounts

Technicians who need system access should have both:
1. A **Technician record** (for EPA compliance)
2. A **User account** (for system login)

To link them:
1. Create the technician record first
2. Create or edit their user account
3. Select their technician record in the "Link to Technician" dropdown
4. Save the user account

**Benefits:**
- Service logs automatically link to technician
- Certification tracking for logged-in users
- Better audit trail

---

## Customer Management

Track customer/company information and associate equipment with specific customers.

### Overview

The Customer Management system allows you to:
- Store customer/company information and contact details
- Track multiple locations for each customer
- Associate equipment with customers
- View all equipment for a specific customer
- Maintain organized customer records for billing and reporting

**Who Can Access:**
- **Managers**: Full access (view, add, edit, delete)
- **Technicians**: Full access (view, add, edit, delete)
- **Admins**: Full access (view, add, edit, delete)

### Viewing Customers

1. Navigate to **Customers** from the menu

2. View customer list with:
   - Company name
   - Contact person
   - Phone number
   - Email address
   - Location
   - Equipment count (number of units associated)
   - Status (Active/Inactive)

3. Click **Edit** to view and modify customer details

### Adding a New Customer

1. Click **Add Customer** button

2. Fill in customer information:

   **Company Information:**
   - Company Name * (required)
   - Contact Person (primary contact at the company)

   **Contact Details:**
   - Phone number
   - Email address

   **Location:**
   - Location/Site Name (e.g., "Main Building", "Warehouse #2")
   - Street Address
   - City
   - State (select from dropdown)
   - ZIP Code

   **Additional Information:**
   - Notes field for any additional details

3. Click **Save Customer**

4. Customer is now available for equipment assignment

### Editing a Customer

1. Click **Edit** next to the customer

2. Update any information:
   - Company details
   - Contact information
   - Location
   - Notes
   - Status (Active/Inactive)

3. View associated equipment:
   - Shows list of equipment linked to this customer
   - Click equipment names to view details

4. Click **Save Customer**

### Linking Equipment to Customers

**When Adding New Equipment:**

1. Navigate to **Equipment** → **Add New Equipment**

2. In the equipment form, find the **Customer/Company** dropdown

3. Select the customer from the list (or leave blank if not applicable)

4. Complete the rest of the equipment details

5. Click **Save Equipment**

**When Editing Existing Equipment:**

1. Navigate to the equipment detail page

2. Click **Edit**

3. Select or change the customer in the **Customer/Company** dropdown

4. Click **Update Equipment**

### Customer Status

**Active:**
- Customer is currently using your services
- Equipment is being monitored
- Appears in customer list by default

**Inactive:**
- Former customer or inactive account
- Equipment may be retired
- Retained for historical records

### Deleting a Customer

**Important**: Only delete customers if they have no associated equipment and no historical data.

1. Click **Delete** next to the customer

2. Confirm deletion

3. Customer record is removed from the system

**Best Practice:**
- Use "Inactive" status instead of deleting
- Keeps historical records intact
- Better for audit trail and reporting

### Customer Use Cases

**Scenario 1: Multi-Site Customer**

*ABC Restaurant Group has 5 locations, each with multiple refrigeration units*

1. Create customer: "ABC Restaurant Group"
2. Add equipment for each location:
   - Set Customer to "ABC Restaurant Group"
   - Use Location field to specify which restaurant (e.g., "Downtown Location", "Airport Location")
3. View all ABC equipment from the customer record
4. Generate reports filtered by this customer

**Scenario 2: Property Management**

*Managing HVAC for multiple building owners*

1. Create separate customer for each building owner
2. Link all equipment in their buildings to their customer record
3. Generate customer-specific compliance reports
4. Track service history per customer for billing

**Scenario 3: Commercial Complex**

*Large shopping center with multiple tenants*

1. Create customer: "Westfield Shopping Center"
2. Contact: Property Manager details
3. Add all HVAC equipment with location details (store numbers)
4. Track all equipment under one customer account

### Customer Reports

**View Equipment by Customer:**
1. Go to customer detail page
2. See all associated equipment
3. View total equipment count
4. Check compliance status across all units

**Generate Customer-Specific Reports:**
1. Navigate to **Reports**
2. Select report type
3. Filter by customer
4. Generate for billing or compliance purposes

### Best Practices for Customer Management

**Data Entry:**
- Use consistent naming (e.g., "ABC Corp" not "ABC Corporation" elsewhere)
- Keep contact information current
- Update status when customers become inactive
- Use notes field for special instructions or billing details

**Organization:**
- Create customer before adding equipment
- Link all equipment to customers for better tracking
- Use location field to differentiate multiple sites
- Keep email addresses current for automated reports

**For Service Technicians:**
- Check customer information before service calls
- Verify contact person and phone number
- Update notes if you learn new information
- Report any changes to office staff

**For Compliance Managers:**
- Review customer records quarterly
- Ensure all equipment is properly assigned
- Generate customer-specific compliance reports
- Keep customer contacts updated for alert notifications

---

## Service Logging

Record all refrigerant service work for EPA compliance.

### Adding a Service Log

1. Navigate to **Service Logs** → **Add Service Log**

2. Fill in service details:

   **Service Information:**
   - Service Date
   - Equipment (select from dropdown)
   - Technician (select from dropdown)
   - Service Type:
     - Routine Maintenance
     - Repair
     - Installation
     - Leak Repair
     - Recovery
     - Disposal
     - Other

   **Refrigerant Usage:**
   - Refrigerant Added (pounds)
   - Refrigerant Recovered (pounds)
   - Recovery Cylinder Number

   **Work Performed:**
   - Detailed description of work
   - Parts replaced
   - Issues found
   - Repairs made

   **Leak Information:**
   - Leak Detected? (Yes/No)
   - If yes:
     - Leak Location
     - Leak Severity (Minor/Moderate/Major)
     - Leak Repaired? (Yes/No)

   **Follow-up:**
   - Follow-up Required? (Yes/No)
   - If yes:
     - Follow-up Date
     - Follow-up Notes

3. Click **Save Service Log**

### Best Practices for Service Logging

**Be Specific:**
- Describe exact work performed
- Note specific components serviced
- Record meter readings if applicable

**Document Everything:**
- All refrigerant added or recovered
- Every leak found (even if repaired)
- Parts replaced with part numbers
- Time spent on site

**Record Immediately:**
- Log service while at job site
- Don't wait until returning to office
- Fresh details are more accurate

**Include Photos:**
- Take photos of equipment
- Document leak locations
- Show repair work completed
- Upload to Document Management

### Viewing Service Logs

**All Logs:**
1. Navigate to **Service Logs**
2. View complete service history
3. Filter by equipment, technician, or date

**By Equipment:**
1. Go to Equipment detail page
2. Scroll to "Service History" section
3. View all logs for that equipment

**By Technician:**
1. Go to Technician detail page
2. View all logs by that technician

---

## Leak Inspections

Conduct and document EPA-required leak inspections.

### When Inspections Are Required

**EPA Triggers:**
- Equipment exceeds leak rate threshold (10%, 20%, or 30%)
- Within 30 days of threshold exceedance
- After repairs (verification inspection)
- Regular scheduled inspections (as configured)

**System Alerts:**
- EcoFreonTrack automatically generates alerts
- Dashboard shows upcoming inspections
- Email notifications (if configured)

### Conducting a Leak Inspection

1. Navigate to **Leak Inspections** → **Add Inspection**

2. Fill in inspection details:

   **Inspection Information:**
   - Inspection Date
   - Equipment (select from dropdown)
   - Technician (select from dropdown)
   - Inspection Type:
     - Initial (first inspection)
     - Follow-up (after repairs)
     - Verification (confirm repairs)
     - Required (scheduled)
     - Routine (preventive)

   **Leak Detection:**
   - Leak Detected? (Yes/No)
   - If yes:
     - Leak Location (describe precisely)
     - Leak Severity:
       - **Minor**: Small, slow leak
       - **Moderate**: Noticeable refrigerant loss
       - **Major**: Significant leak, immediate action required
     - Estimated Leak Rate (if known)

   **Refrigerant Measurement:**
   - Current Charge (pounds) - measure with scales
   - Charge Deficit (calculated automatically)

   **Inspector Notes:**
   - Detailed findings
   - Areas inspected
   - Equipment condition
   - Recommendations

3. Click **Save Inspection**

### System Calculations

EcoFreonTrack automatically calculates:

**Annual Leak Rate:**
```
Annual Leak Rate = (Refrigerant Lost / Full Charge) × 100%
```

**Compliance Status:**
- Compliant: Leak rate below threshold
- Non-Compliant: Leak rate exceeds threshold

**Next Inspection Date:**
- Based on equipment inspection frequency
- Adjusts for failed inspections

### Leak Inspection Results

After saving an inspection:

1. **System Updates:**
   - Equipment compliance status
   - Annual leak rate calculation
   - Next inspection date scheduled

2. **Alerts Generated (if applicable):**
   - Leak threshold exceeded
   - Inspection overdue
   - Follow-up required

3. **Equipment Page Updates:**
   - Latest inspection results shown
   - Compliance status badge updated
   - Inspection history added

---

## Refrigerant Inventory

Track refrigerant purchases, usage, and stock levels.

### Viewing Inventory

1. Navigate to **Inventory** from the menu

2. View all refrigerant types with:
   - Refrigerant name (R-22, R-410A, etc.)
   - Quantity on hand (pounds)
   - Quantity recovered (pounds)
   - Reorder level
   - Below reorder status

### Managing Inventory

**Purchase Refrigerant:**
1. Click **Adjust** next to refrigerant type
2. Select transaction type: **Purchase**
3. Enter positive quantity (e.g., +30 for 30 lbs purchased)
4. Enter supplier information
5. Enter invoice number and cost
6. Add notes if needed
7. Click **Save Transaction**

**Record Usage:**
1. Usage is automatically recorded from service logs
2. When technicians log refrigerant added, inventory decreases
3. Manual adjustments available if needed

**Record Recovery:**
1. Click **Adjust** next to refrigerant type
2. Select transaction type: **Recovered**
3. Enter quantity recovered
4. Enter cylinder number
5. Note source equipment or job
6. Click **Save Transaction**

**Record Disposal:**
1. Click **Adjust** next to refrigerant type
2. Select transaction type: **Disposed**
3. Enter quantity disposed
4. Enter disposal facility information
5. Enter disposal certificate number
6. Click **Save Transaction**

### Inventory Alerts

**Low Stock Alert:**
- Triggered when quantity falls below reorder level
- Appears on dashboard
- Allows proactive ordering

**Setting Reorder Levels:**
1. Click **Edit** next to refrigerant
2. Set reorder level based on:
   - Average monthly usage
   - Lead time for ordering
   - Number of systems using this refrigerant
3. Recommended: 2-3 months of typical usage

### Recovered Refrigerant

**Tracking:**
- Separate column for recovered refrigerant
- Tracked by cylinder number
- Awaiting reclamation or reuse

**EPA Requirements:**
- Must use certified recovery equipment
- Must document all recovered refrigerant
- Must send to certified reclamation facility
- Keep certificates of reclamation

---

## Document Management

Upload and organize compliance documents, certificates, and photos.

### Document Types

**EPA 608 Certificates:**
- Technician certification documents
- Upload when adding new technicians
- Store renewals and updates

**Service Invoices:**
- Attach to service logs
- Provide proof of work
- Required for EPA audits

**Equipment Photos:**
- Installation photos
- Leak location photos
- Repair work documentation
- Before and after comparisons

**Compliance Reports:**
- Generated reports
- EPA submissions
- Audit documentation

**Other:**
- Equipment manuals
- Refrigerant purchase receipts
- Disposal certificates
- Insurance documents

### Uploading Documents

1. Navigate to **Documents** from the menu

2. Click **Upload Document**

3. Fill in document information:
   - Document Type (select from dropdown)
   - Description (what this document is)
   - Link to Equipment (optional)
   - Link to Service Log (optional)
   - Link to Technician (optional)

4. Click **Choose File** and select document

5. Click **Upload**

**Supported File Types:**
- PDF (.pdf)
- Images (.jpg, .png, .gif)
- Microsoft Office (.doc, .docx, .xls, .xlsx)
- Text files (.txt)

**File Size Limit:**
- Maximum 10 MB per file
- Contact admin to increase if needed

### Viewing Documents

**All Documents:**
1. Navigate to **Documents**
2. Browse all uploaded files
3. Filter by type, date, or equipment
4. Click to download or view

**By Equipment:**
1. Go to Equipment detail page
2. Scroll to "Documents" section
3. View all files for that equipment

**By Service Log:**
1. Go to Service Log detail page
2. View attached documents

**By Technician:**
1. Go to Technician detail page
2. View uploaded certificates

### Organizing Documents

**Best Practices:**
- Use descriptive file names
- Add detailed descriptions
- Link to relevant equipment or logs
- Upload documents immediately after service
- Keep digital copies of all EPA-required documents

**Folder Structure (recommended):**
- Certificates/
  - Technician_Name_EPA608.pdf
- Equipment/
  - EquipmentID_Install.pdf
  - EquipmentID_Photos/
- Service_Logs/
  - YYYY-MM-DD_EquipmentID_Invoice.pdf
- Reports/
  - YYYY-MM_Monthly_Compliance.pdf

---

## Compliance Alerts

Monitor and resolve compliance issues.

### Alert Types

**Leak Threshold Exceeded:**
- Equipment's annual leak rate exceeds threshold
- **Action Required**: Schedule inspection within 30 days
- **Resolution**: Conduct inspection, repair leaks, verify repairs

**Inspection Overdue:**
- Required inspection not conducted on time
- **Action Required**: Conduct inspection immediately
- **Resolution**: Complete and log inspection

**Certification Expiring:**
- Technician's EPA 608 certification expires soon
- **Action Required**: Schedule recertification
- **Resolution**: Update technician record with new certification

**Low Refrigerant Inventory:**
- Stock below reorder level
- **Action Required**: Order more refrigerant
- **Resolution**: Purchase refrigerant, log transaction

**Follow-up Required:**
- Service log indicates follow-up needed
- **Action Required**: Schedule follow-up service
- **Resolution**: Complete follow-up, log service

### Viewing Alerts

**Dashboard:**
- Shows count of active alerts
- Click to view alert list

**Alerts Page:**
1. Navigate to **Alerts** from menu
2. View all alerts with:
   - Alert type
   - Severity (Critical, Warning, Info)
   - Equipment or technician affected
   - Date created
   - Status (Active, Resolved, Dismissed)

**By Equipment:**
- Equipment detail page shows equipment-specific alerts

### Resolving Alerts

**For Compliance Managers and Admins:**

1. Click on alert to view details

2. Review alert information:
   - What triggered the alert
   - EPA requirement
   - Recommended action

3. Take appropriate action:
   - Conduct required inspection
   - Schedule service
   - Update records
   - Order supplies

4. Mark alert as resolved:
   - Click **Resolve** button
   - Enter resolution notes
   - Click **Save**

5. Alert moves to resolved status:
   - No longer appears in active alerts
   - Retained for audit trail
   - Can be viewed in alert history

### Alert Severity Levels

**Critical (Red):**
- EPA violation
- Immediate action required
- Risk of penalties

**Warning (Yellow):**
- Approaching non-compliance
- Action needed soon
- Preventive measure

**Info (Blue):**
- Informational notice
- No immediate action required
- Awareness item

---

## Reports and Analytics

Generate compliance reports and analyze system data.

**Note**: Report generation is available to **Compliance Managers** and **Admins** only.

### Report Types

**Equipment Compliance Summary:**
- All equipment with compliance status
- Leak rates vs. thresholds
- Next inspection dates
- Non-compliant equipment highlighted

**Refrigerant Usage Report:**
- Total refrigerant purchased
- Total refrigerant added to equipment
- Total refrigerant recovered
- Net refrigerant usage
- By refrigerant type
- By time period

**Service History Report:**
- All service logs for date range
- By equipment or technician
- Work performed summary
- Refrigerant transactions

**Inspection Report:**
- All leak inspections
- Compliance status over time
- Leak detection rate
- Inspection frequency analysis

**Technician Activity Report:**
- Service logs by technician
- Hours worked
- Equipment serviced
- Certification status

**EPA Compliance Report:**
- Comprehensive EPA-ready report
- All required data elements
- Suitable for EPA audits
- Export as PDF

### Generating Reports

1. Navigate to **Reports** from the menu

2. Select report type

3. Configure report parameters:
   - Date range
   - Equipment filter
   - Technician filter
   - Report format (PDF, Excel, CSV)

4. Click **Generate Report**

5. Report is generated and displayed:
   - View in browser
   - Download to computer
   - Print for records

### Report Best Practices

**Regular Reporting:**
- Generate monthly compliance reports
- Review quarterly for trends
- Annual EPA compliance summary

**Audit Preparation:**
- Generate comprehensive report
- Review for any gaps
- Address issues before EPA visits
- Keep printed copies on-site

**Data Analysis:**
- Track leak rate trends
- Identify problem equipment
- Monitor refrigerant costs
- Evaluate technician performance

---

## EPA Compliance Guidelines

### EPA Section 608 Key Requirements

**Service Records (40 CFR 82.166):**

Must maintain records for each service event including:
- Date of service
- Name and address of facility
- Type and serial number of equipment
- Quantity of refrigerant added (pounds)
- Quantity of refrigerant recovered (pounds)
- Reason for refrigerant charge change
- Technician name and certification number

**Recordkeeping Period**: 3 years minimum

**Leak Rate Thresholds:**

| Equipment Type | Threshold | Action Required |
|---------------|-----------|-----------------|
| Commercial refrigeration | 10% | Inspection within 30 days |
| Industrial process | 10% | Inspection within 30 days |
| Comfort cooling | 20% | Inspection within 30 days |
| Appliances < 50 lbs | 30% | Inspection within 30 days |

**Leak Rate Calculation:**
```
Annual Leak Rate = (Refrigerant Lost / Full Charge) × 100%
```

**Leak Repair Timeline:**
- **Within 30 days** of discovery for most equipment
- **Within 14 days** for some industrial process equipment
- **Verification** required after repairs

**Technician Certification:**
- All technicians must be EPA 608 certified
- Certification type must match equipment
- Keep copies of certificates on file

**Recovery Requirements:**
- Use certified recovery equipment
- Meet EPA purity standards
- Document all recovered refrigerant
- Proper disposal through certified facility

### Using EcoFreonTrack for EPA Compliance

**EcoFreonTrack helps you comply by:**

1. **Automatic Record Keeping**
   - All service logs include required data
   - 3-year retention built-in
   - Searchable and exportable

2. **Leak Rate Monitoring**
   - Automatic calculations
   - Threshold alerts
   - Inspection scheduling

3. **Certification Tracking**
   - Verify technician qualifications
   - Expiration alerts
   - Certificate storage

4. **Recovery Documentation**
   - Track all recovered refrigerant
   - Cylinder tracking
   - Disposal records

5. **Audit-Ready Reports**
   - EPA-compliant format
   - Complete documentation
   - Easy PDF export

**EPA Audit Preparation:**

1. Generate comprehensive compliance report
2. Review for any missing data
3. Ensure all technician certifications current
4. Verify all leak inspections conducted on time
5. Print and organize by equipment
6. Keep both digital and paper copies

---

## Troubleshooting

### Login Issues

**Problem**: Can't log in
- Verify username and password are correct
- Check that account is active (contact admin)
- Clear browser cache and try again
- Try a different browser

**Problem**: Forgot password
- Contact your administrator
- Admin can reset your password
- You'll receive new temporary credentials

### Data Entry Issues

**Problem**: Can't add service log
- Verify equipment exists in system
- Verify technician is registered
- Ensure all required fields filled
- Check that you have permission (Technician or Admin)

**Problem**: Equipment not showing in dropdown
- Verify equipment status is "Active"
- Refresh the page
- Check that equipment was saved properly

**Problem**: Refrigerant inventory not updating
- Verify service log was saved successfully
- Check refrigerant type matches between equipment and log
- Manual adjustment available in Inventory section

### Compliance Alert Issues

**Problem**: Alert not clearing after resolution
- Verify you clicked "Resolve" and entered notes
- Refresh the alerts page
- Check that underlying issue is actually resolved

**Problem**: Not receiving alerts
- Check your user role (Technicians don't see all alerts)
- Verify alert type is enabled
- Contact admin to check alert settings

### Performance Issues

**Problem**: System running slowly
- Clear browser cache
- Close unnecessary browser tabs
- Check internet connection
- Contact admin if issue persists

**Problem**: Large reports timing out
- Reduce date range
- Apply filters to limit data
- Generate report during off-peak hours

### Document Upload Issues

**Problem**: Can't upload document
- Check file size (max 10 MB)
- Verify file type is supported
- Ensure stable internet connection
- Try different browser

**Problem**: Uploaded document not appearing
- Refresh the page
- Check Documents section directly
- Verify upload completed successfully

### Getting Help

**For Technical Issues:**
1. Check this User Guide first
2. Contact your system administrator
3. Check README.md for installation issues
4. Open GitHub issue for bugs

**For EPA Compliance Questions:**
1. Review [EPA Section 608 website](https://www.epa.gov/section608)
2. Consult EPA compliance specialist
3. Contact EPA regional office

---

## Best Practices

### For Administrators

**User Management:**
- Review user accounts quarterly
- Deactivate former employees immediately
- Enforce strong password policies
- Create users with least privilege (start with Technician, promote as needed)
- Keep admin accounts to minimum

**System Maintenance:**
- Back up database weekly
- Review system logs monthly
- Update software as patches released
- Test recovery procedures
- Monitor disk space

**Data Quality:**
- Audit service logs monthly
- Verify equipment data accuracy
- Review technician certifications quarterly
- Clean up old alerts
- Archive old reports

### For Compliance Managers

**Daily Tasks:**
- Review new service logs
- Check active alerts
- Monitor upcoming inspections

**Weekly Tasks:**
- Review leak rate trends
- Approve service logs
- Generate activity report
- Address compliance issues

**Monthly Tasks:**
- Generate comprehensive compliance report
- Review with management
- Update procedures as needed
- Train staff on any changes

**Quarterly Tasks:**
- EPA compliance audit
- Refrigerant usage analysis
- Equipment performance review
- Technician certification check

### For Technicians

**At Each Job:**
- Log service immediately
- Record exact refrigerant quantities
- Document all work performed
- Note any leaks found
- Take photos of repairs
- Upload documents before leaving site

**End of Day:**
- Review all logs entered
- Verify data accuracy
- Complete any missing information
- Upload any remaining photos

**Weekly:**
- Review your service history
- Ensure all jobs logged
- Check for follow-ups required
- Update personal contact info

### General Best Practices

**Data Entry:**
- Be specific and detailed
- Use consistent terminology
- Include units (pounds, PSI, etc.)
- Note meter readings
- Timestamp everything

**Documentation:**
- Upload supporting documents
- Link documents to equipment/logs
- Use descriptive file names
- Keep EPA-required records for 3+ years

**Communication:**
- Report issues immediately
- Document conversations
- Follow up on open items
- Update stakeholders regularly

**Compliance:**
- Know your responsibilities
- Stay current on EPA regulations
- Attend training sessions
- Ask questions when unsure

**Security:**
- Never share passwords
- Log out when finished
- Don't access from public computers
- Report suspicious activity

---

## Appendix A: Quick Reference

### User Role Permissions Matrix

| Feature | Technician | Compliance Manager | Admin |
|---------|-----------|-------------------|-------|
| Add Service Logs | ✓ | ✓ | ✓ |
| View Own Logs | ✓ | ✓ | ✓ |
| View All Logs | ✗ | ✓ | ✓ |
| Approve Logs | ✗ | ✓ | ✓ |
| Add Equipment | ✗ | ✗ | ✓ |
| Edit Equipment | ✗ | ✗ | ✓ |
| View Dashboard | ✓ | ✓ | ✓ |
| Generate Reports | ✗ | ✓ | ✓ |
| Manage Users | ✗ | ✗ | ✓ |
| Upload Documents | ✓ | ✓ | ✓ |
| Resolve Alerts | ✗ | ✓ | ✓ |
| Manage Inventory | ✗ | ✓ | ✓ |

### EPA 608 Certification Types

| Type | Equipment Covered | Notes |
|------|------------------|-------|
| Type I | Small appliances (< 5 lbs) | Refrigerators, freezers, window units |
| Type II | High-pressure (> 5 lbs) | Most commercial AC and refrigeration |
| Type III | Low-pressure | Centrifugal chillers |
| Universal | All types | Most comprehensive |

### Common Refrigerants

| Name | Type | Common Use | Status |
|------|------|-----------|--------|
| R-22 | HCFC | Older AC systems | Being phased out |
| R-410A | HFC | Modern AC systems | Current standard |
| R-134a | HFC | Automotive, refrigeration | Current standard |
| R-404A | HFC | Commercial refrigeration | Current standard |
| R-407C | HFC | AC systems | R-22 replacement |

### Default Leak Rate Thresholds

| Equipment Type | Threshold | Inspection Frequency |
|---------------|-----------|---------------------|
| Commercial refrigeration | 10% | 30 days |
| Industrial process | 10% | 30 days |
| Comfort cooling | 20% | 30 days |
| Appliances < 50 lbs | 30% | 30 days |

### Support Contacts

**System Issues:**
- Administrator: [Contact Info]
- Technical Support: [Contact Info]

**EPA Compliance:**
- EPA Hotline: 1-800-EPA-SAVE
- EPA Website: https://www.epa.gov/section608
- Regional EPA Office: [Contact Info]

---

## Document Information

**Document**: EcoFreonTrack User Guide
**Version**: 2.0.0
**Last Updated**: October 2025
**Maintained By**: EcoFreonTrack Development Team

**Related Documents:**
- README.md - Installation and setup
- RBAC_IMPLEMENTATION_SUMMARY.md - Technical documentation
- SUPABASE_SETUP_GUIDE.md - Cloud database setup

---

**For additional help or to report issues, visit:**
https://github.com/[your-repo]/EcoFreonTrack
