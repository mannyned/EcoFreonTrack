# EcoFreonTrack - Role-Based Optimization Guide

## Overview

EcoFreonTrack implements a comprehensive role-based access control (RBAC) system optimized for three primary user types:

1. **Technicians** - Field workers focused on quick data entry, scanning, and status updates
2. **Compliance Managers** - Office staff focused on monitoring, reports, and analytics
3. **Auditors** - External reviewers with read-only access to logs and certifications
4. **Administrators** - System managers with full access to all features

This document outlines how each layer of the application is optimized for specific user roles.

---

## User Roles & Permissions

### Role Definitions

#### 1. Technician
**Primary Tasks**: Service logging, equipment scanning, status updates

**Permissions**:
- ✓ Add service logs
- ✓ Add refrigerant transactions
- ✓ Add leak inspections
- ✓ Upload certificates/documents
- ✓ View own service logs
- ✓ Scan equipment QR codes
- ✓ View equipment details
- ✗ Cannot add/edit equipment
- ✗ Cannot manage users
- ✗ Cannot resolve alerts

**Color Theme**: Green (#28a745)
**Icon**: 🔧

#### 2. Compliance Manager
**Primary Tasks**: Monitoring, reporting, analytics

**Permissions**:
- ✓ View dashboard analytics
- ✓ Approve service logs
- ✓ Generate EPA reports
- ✓ View all logs (not just own)
- ✓ View compliance alerts
- ✓ Resolve alerts
- ✓ Manage equipment (add/edit)
- ✓ View equipment details
- ✓ Export reports
- ✓ View analytics
- ✗ Cannot manage users
- ✗ Cannot access system settings

**Color Theme**: Blue (#0066cc)
**Icon**: 📊

#### 3. Auditor
**Primary Tasks**: Read-only review of compliance records

**Permissions**:
- ✓ View dashboard (read-only)
- ✓ View all logs (read-only)
- ✓ View compliance alerts (read-only)
- ✓ View equipment (read-only)
- ✓ Generate reports (view/export only)
- ✓ Export reports
- ✓ View analytics
- ✗ Cannot add/edit any data
- ✗ Cannot resolve alerts
- ✗ Cannot upload documents
- ✗ Cannot manage anything

**Color Theme**: Orange (#ff9800)
**Icon**: 📋

#### 4. Administrator
**Primary Tasks**: Full system management

**Permissions**:
- ✓ ALL permissions from all other roles
- ✓ Manage users (add/edit/delete)
- ✓ Manage sites
- ✓ Manage equipment (full CRUD)
- ✓ Manage technicians
- ✓ System settings access
- ✓ Delete operations
- ✓ Access all layers

**Color Theme**: Purple (#673ab7)
**Icon**: ⚙️

---

## Layer-by-Layer Role Optimization

### Dashboard Layer 🏠

#### **Technician View**
- **Quick Actions** (4 large buttons):
  1. 📝 **Log Service** - Direct link to service log entry
  2. 🔍 **Leak Inspection** - Quick leak test logging
  3. 📦 **Scan Equipment** - QR/barcode scanner
  4. 📄 **Upload Document** - Certificate upload

- **Simplified Stats**:
  - Recent service activity (last 5 logs)
  - Upcoming inspections assigned to them
  - Equipment assigned to them

- **Hidden Elements**:
  - Add Equipment button
  - Alert resolution buttons
  - User management links
  - Inventory management

#### **Compliance Manager View**
- **Quick Actions** (4 large buttons):
  1. 📊 **EPA Reports** - Generate compliance reports
  2. 🚨 **Review Alerts** - Manage compliance violations
  3. ➕ **Add Equipment** - Register new systems
  4. 📦 **Inventory** - Refrigerant stock management

- **Enhanced Stats**:
  - Total equipment count
  - Active alerts (with severity)
  - Compliance rate percentage
  - Low inventory warnings
  - Upcoming inspections (all)

- **Analytics Dashboard**:
  - Leak rate trends
  - Service frequency graphs
  - Technician performance metrics
  - Compliance score over time

#### **Auditor View**
- **Read-Only Banner**:
  - Yellow warning banner: "Auditor Mode - Read-Only Access"
  - Clear indication of no editing capabilities

- **Quick Actions** (6 view-only buttons):
  1. 📋 **View Service Logs** - Audit trail
  2. 🔍 **View Inspections** - Compliance records
  3. 📊 **EPA Reports** - View & export
  4. 📦 **View Equipment** - Compliance status
  5. 🔧 **View Certifications** - Technician records
  6. 📄 **View Documents** - Certificates & reports

- **Stats Display**:
  - All statistics visible (read-only)
  - No "Add" or "Edit" buttons anywhere
  - Export buttons prominently displayed

#### **Administrator View**
- **Full Access**:
  - Same as Compliance Manager view
  - Additional user management link
  - System settings access
  - All CRUD operations available

---

### Equipment Layer 📦

#### **Technician View**
- **Primary Actions**:
  - 📱 **QR Scanner** - Quick equipment lookup (prominent)
  - 🔍 **Search** - Find by equipment ID
  - 👁️ **View Details** - Read equipment info

- **Equipment Detail Page**:
  - Basic information display
  - Service history (own logs only)
  - Next inspection date
  - Current leak rate status
  - **Quick Log Service** button (large, prominent)

- **Hidden Elements**:
  - Add Equipment button
  - Edit Equipment button
  - Delete Equipment button
  - Refrigerant inventory access

#### **Compliance Manager View**
- **Primary Actions**:
  - ➕ **Add Equipment** - Register new systems
  - ✏️ **Edit Equipment** - Update details
  - 📦 **Inventory Management** - Stock levels
  - 📊 **Compliance Overview** - Equipment status grid

- **Equipment Detail Page**:
  - Full edit capabilities
  - All service history
  - All leak inspections
  - Refrigerant transaction history
  - Compliance alerts for this equipment
  - **Resolve Alert** buttons

- **Equipment List Enhancements**:
  - Sortable columns
  - Filter by compliance status
  - Filter by leak rate threshold
  - Export to CSV/Excel

#### **Auditor View**
- **Primary Actions**:
  - 👁️ **View Only** - All equipment visible
  - 📊 **Export** - Download equipment list

- **Equipment Detail Page**:
  - All information visible (read-only)
  - No edit/delete buttons
  - **Export Equipment Report** button
  - Service history (all logs, read-only)
  - Leak inspection history (read-only)

- **Visual Indicators**:
  - **"Read-Only"** badge on every page
  - Disabled form fields (grayed out)
  - No hover effects on interactive elements

#### **Administrator View**
- **Full Access**:
  - Same as Compliance Manager
  - Additional delete capabilities
  - Bulk operations
  - QR code generation/printing

---

### Logs Layer 📋

#### **Technician View**
- **Primary Actions**:
  - 📝 **Log Service** (prominent, large button)
  - 🔍 **Log Leak Inspection** (prominent)
  - 📄 **Upload Document** (certificate upload)

- **Service Log Entry**:
  - **Step-by-step wizard** (multi-step form)
  - Step 1: Select Equipment (with QR scan option)
  - Step 2: Service Details (dropdowns, not free text)
  - Step 3: Refrigerant Added (numeric input)
  - Step 4: Notes & Photos (optional)
  - **Large Submit Button**: "Complete Service Log"

- **My Logs View**:
  - Filter: "My Logs Only" (default)
  - Recent 20 logs
  - Quick edit (within 24 hours)
  - Status indicators (Pending/Approved)

- **Hidden Elements**:
  - Other technicians' logs
  - Approve/Reject buttons
  - Delete buttons

#### **Compliance Manager View**
- **Primary Actions**:
  - 📊 **Review All Logs** - Approval workflow
  - 🔍 **Audit Trail** - Full history view
  - 📈 **Analytics** - Service patterns

- **Service Log List**:
  - **All logs visible** (all technicians)
  - Filter by technician
  - Filter by date range
  - Filter by status (Pending/Approved)
  - **Approve/Reject buttons**

- **Log Detail Page**:
  - Full details
  - Technician info
  - Equipment info
  - **Approval workflow**:
    - Approve button
    - Reject button (with reason)
    - Request modification

- **Analytics Dashboard**:
  - Service frequency by technician
  - Average refrigerant usage
  - Leak repair effectiveness
  - Compliance trend over time

#### **Auditor View**
- **Primary Actions**:
  - 📋 **View Audit Trail** - Chronological log
  - 🔍 **Search Logs** - Filter by criteria
  - 📊 **Export Logs** - Download for review

- **Service Log List**:
  - All logs visible (read-only)
  - Advanced filtering
  - Sort by any column
  - **Export to PDF/CSV** (prominent)

- **Log Detail Page**:
  - All details visible (read-only)
  - Change history/audit trail visible
  - Timestamps for all actions
  - User attribution for all changes
  - **No edit/approve buttons**

- **Visual Features**:
  - **Audit Trail styling** - Gray border, read-only badges
  - Timestamps prominent
  - User attribution visible

#### **Administrator View**
- **Full Access**:
  - Same as Compliance Manager
  - Additional delete capabilities
  - Bulk approve/reject
  - Reassign logs to different technicians

---

### Reports Layer 📊

#### **Technician View**
- **Limited Access**:
  - **My Performance Report** - Personal metrics
  - **My Service Summary** - Own logs summary
  - **View only** - Cannot generate EPA reports

- **Hidden Elements**:
  - EPA 608/609 reports
  - Facility-wide reports
  - Compliance analytics

#### **Compliance Manager View**
- **Primary Actions**:
  - 📊 **Generate EPA 608 Report**
  - 📊 **Generate EPA 609 Report**
  - 📊 **CARB Report**
  - 📊 **AIM Act Report**
  - 📈 **Custom Analytics**

- **Report Generation Wizard**:
  - Step 1: Select Report Type
  - Step 2: Date Range
  - Step 3: Filter Equipment
  - Step 4: Preview
  - Step 5: Generate PDF/Export

- **Report Features**:
  - **Auto-formatted** EPA templates
  - Professional header/footer
  - Compliance stamps
  - Digital signature field
  - Export to PDF (print-ready)
  - Export to Excel (data analysis)

- **Analytics Dashboard**:
  - Leak rate trends
  - Refrigerant usage by type
  - Compliance score over time
  - Equipment at risk
  - Predictive alerts

#### **Auditor View**
- **Primary Actions**:
  - 📊 **View EPA Reports** (read-only)
  - 📥 **Export Reports** (PDF/Excel)
  - 📈 **View Analytics** (read-only)

- **Report Access**:
  - All generated reports visible
  - **Cannot generate new reports**
  - Can export existing reports
  - Can view historical reports

- **Audit Trail View**:
  - Report generation history
  - Who generated what report when
  - Export/download history

#### **Administrator View**
- **Full Access**:
  - Same as Compliance Manager
  - Schedule automated reports
  - Email report distribution
  - Custom report templates
  - Bulk export capabilities

---

### User Layer 👥

#### **Technician View**
- **Limited Access**:
  - **My Profile** - View/edit own profile
  - **My Certifications** - View/upload own certs
  - **Other Technicians** - View directory (read-only)

- **Hidden Elements**:
  - User management
  - Role assignment
  - Delete users
  - Other users' personal info

#### **Compliance Manager View**
- **Access**:
  - **Technician Management**:
    - View all technicians
    - View certifications
    - Track certification expirations
    - View service history per technician

  - **Technician Detail Page**:
    - Contact information
    - Certification status
    - Service log count
    - Performance metrics
    - Expiration alerts

- **Hidden Elements**:
  - User account management (admin only)
  - Role changes (admin only)
  - Delete users (admin only)

#### **Auditor View**
- **Access**:
  - **View Technicians** (read-only)
  - **View Certifications** (read-only)
  - **Export Certification List**

- **No Access**:
  - Cannot edit technician info
  - Cannot upload certifications
  - Cannot view personal contact info (privacy)

#### **Administrator View**
- **Full User Management**:
  - ➕ **Add User** - Create new accounts
  - ✏️ **Edit User** - Modify any user
  - 🗑️ **Delete User** - Remove accounts
  - 🔐 **Reset Password** - Security management
  - 👥 **Assign Roles** - Change user roles

- **Technician Management**:
  - Link users to technician records
  - Manage certifications
  - Track performance
  - Bulk operations

- **Access Control**:
  - View login history
  - View audit trail
  - Manage permissions
  - Configure roles

---

### Settings Layer ⚙️

#### **All Users**
- **Personal Settings**:
  - Edit profile
  - Change password
  - Notification preferences
  - Display preferences

#### **Compliance Manager**
- **EPA Compliance Settings**:
  - Leak rate thresholds
  - Inspection reminder days
  - Facility name
  - EPA ID number

#### **Auditor**
- **Limited Access**:
  - View-only personal settings
  - Cannot change system settings
  - Cannot export system data

#### **Administrator**
- **Full System Configuration**:
  - All compliance settings
  - System information
  - Database backup
  - Cache management
  - Data export (all)

---

## Implementation Guide

### Using Template Macros

EcoFreonTrack includes `templates/macros.html` with helper functions for role-based UI:

```jinja2
{% import "macros.html" as macros %}

{# Show role info banner #}
{{ macros.role_info_box() }}

{# Show button only if user has permission #}
{{ macros.button_if_permitted(url_for('equipment_add'), 'Add Equipment', 'btn-primary', 'add_equipment') }}

{# Show edit/delete buttons (hidden for auditors) #}
{{ macros.edit_delete_buttons(
    url_for('equipment_edit', id=equipment.id),
    url_for('equipment_delete', id=equipment.id),
    equipment.id
) }}

{# Show form submit button (disabled for auditors) #}
{{ macros.submit_button_if_not_auditor('Save Equipment') }}

{# Table actions column #}
{{ macros.table_row_actions(
    url_for('equipment_detail', id=item.id),
    url_for('equipment_edit', id=item.id),
    url_for('equipment_delete', id=item.id)
) }}
```

### Backend Permission Checks

Always verify permissions in routes:

```python
from auth import login_required, permission_required, role_required

# Require specific permission
@app.route('/equipment/add', methods=['GET', 'POST'])
@login_required
@permission_required('add_equipment')
def equipment_add():
    # Only users with add_equipment permission can access
    pass

# Require specific role
@app.route('/users', methods=['GET'])
@login_required
@role_required('admin')
def user_list():
    # Only admins can access
    pass

# Multiple roles allowed
@app.route('/reports', methods=['GET'])
@login_required
@role_required('admin', 'compliance_manager', 'auditor')
def reports():
    # Admins, managers, and auditors can access
    pass
```

### Frontend Permission Checks

Check permissions in templates:

```jinja2
{% if current_user and current_user.has_permission('add_equipment') %}
<a href="{{ url_for('equipment_add') }}" class="btn btn-primary">Add Equipment</a>
{% endif %}

{% if current_user and current_user.role != 'auditor' %}
<button type="submit" class="btn btn-primary">Save</button>
{% else %}
<div class="alert alert-warning">Read-Only Access</div>
{% endif %}
```

---

## Visual Design for Roles

### Color Coding

Each role has a distinct color for visual identification:

- **Technician**: Green (#28a745) - Action/Field work
- **Compliance Manager**: Blue (#0066cc) - Analysis/Reports
- **Auditor**: Orange (#ff9800) - Caution/Read-only
- **Administrator**: Purple (#673ab7) - Authority/Control

### Role Badges

Display role badges prominently:

```html
<span class="badge badge-success">🔧 Technician</span>
<span class="badge badge-info">📊 Compliance Manager</span>
<span class="badge badge-warning">📋 Auditor</span>
<span class="badge badge-primary">⚙️ Administrator</span>
```

### Read-Only Indicators

For auditors, show clear read-only indicators:

```html
<div class="audit-trail-readonly">READ-ONLY</div>
<span class="badge badge-warning">📋 Read-Only Mode</span>
```

---

## Best Practices

### 1. **Always Check Permissions Twice**
- Check in backend route (security)
- Check in frontend template (UX)

### 2. **Fail Securely**
- Default to no access
- Show error message on unauthorized access
- Log unauthorized attempts

### 3. **Provide Clear Feedback**
- Show role badge on dashboard
- Show permission denial messages
- Show read-only indicators for auditors

### 4. **Optimize for Primary Use Case**
- Technicians: Quick entry, scanning
- Managers: Analytics, reports
- Auditors: Viewing, exporting

### 5. **Mobile Optimization**
- Technicians primarily use mobile
- Large touch targets (50-80px)
- QR scanner optimized for mobile camera

### 6. **Audit Trail Everything**
- Log all actions with user attribution
- Timestamp all changes
- Show change history to auditors

---

## Testing Checklist

### Technician Role
- [ ] Can add service logs
- [ ] Can scan QR codes
- [ ] Can view own logs
- [ ] Cannot add equipment
- [ ] Cannot edit others' logs
- [ ] Cannot access user management

### Compliance Manager Role
- [ ] Can generate EPA reports
- [ ] Can view all logs
- [ ] Can resolve alerts
- [ ] Can add/edit equipment
- [ ] Cannot access user management
- [ ] Cannot delete users

### Auditor Role
- [ ] Can view all data
- [ ] Cannot edit anything
- [ ] Cannot add anything
- [ ] Cannot delete anything
- [ ] Can export reports
- [ ] See "Read-Only" badges everywhere

### Administrator Role
- [ ] Can access everything
- [ ] Can manage users
- [ ] Can delete data
- [ ] Can access system settings
- [ ] Can perform bulk operations

---

## Future Enhancements

### Phase 2
1. **Custom Roles**
   - Define custom roles beyond the 4 default
   - Granular permission assignment per role

2. **Field-Level Permissions**
   - Hide/show specific fields based on role
   - Example: Technicians can't see cost data

3. **Time-Based Access**
   - Temporary role elevation
   - Example: Technician becomes manager for 1 week

4. **Multi-Tenant Support**
   - Different companies
   - Cross-company auditing

5. **Approval Workflows**
   - Multi-level approval for critical actions
   - Example: Equipment deletion requires 2 approvals

---

## Support & Documentation

### Resources
- **User Manual**: See `/docs/USER_MANUAL.md`
- **API Reference**: See `/docs/API_REFERENCE.md`
- **EPA Compliance Guide**: See `/docs/EPA_COMPLIANCE.md`

### Role-Specific Training
- **Technicians**: 30-minute quick start guide
- **Compliance Managers**: 2-hour full system training
- **Auditors**: 1-hour read-only access training
- **Administrators**: 4-hour comprehensive training

---

**Document Version**: 1.0.0
**Last Updated**: October 28, 2025
**Status**: ✅ Complete
