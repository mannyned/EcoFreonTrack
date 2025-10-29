# EcoFreonTrack - 5-Layer UX Architecture

## Overview

EcoFreonTrack follows a clear **5-layer architectural pattern** that organizes all functionality into logical, easy-to-navigate layers. This architecture improves user experience, reduces cognitive load, and ensures compliance workflows are intuitive and efficient.

---

## UX Flow Map

The primary user flow through the application follows this path:

```
Login → Dashboard → Equipment → Logs → Reports → Settings
              ↓
            Alerts
```

### Flow Description:
1. **Login** - User authentication
2. **Dashboard** - Central hub with overview, stats, and quick actions
3. **Equipment** - Manage equipment inventory and compliance status
4. **Logs** - Record service, inspection, and maintenance activities
5. **Reports** - Generate EPA compliance reports
6. **Settings** - Configure preferences and system settings
7. **Alerts** - Branch from Dashboard for compliance alerts and warnings

This flow ensures a logical progression from overview → data entry → reporting → configuration, with alerts accessible at any time from the Dashboard.

---

## The 5 Layers

```
┌─────────────────────────────────────────────┐
│  Layer 1: Dashboard Layer (Blue #0066cc)   │
│  Summary & Alerts                           │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│  Layer 2: Equipment Layer (Green #28a745)   │
│  Equipment detail, leak history, types      │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│  Layer 3: Logs Layer (Orange #ff9800)       │
│  Service, recovery, disposal, certs         │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│  Layer 4: Reports Layer (Purple #673ab7)    │
│  EPA 608/609, CARB, AIM Act reports         │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│  Layer 5: User Layer (Red #dc3545)          │
│  Roles, permissions, certifications         │
└─────────────────────────────────────────────┘
```

---

## Layer 1: Dashboard Layer 🏠

**Color**: Blue (#0066cc)
**Purpose**: Central hub for navigation and system overview

### Key Components:
- **5-Layer Navigation Cards** - Visual gateway to all layers
- **EPA Leak Rate Legend** - Color-coded thresholds
- **Stats Grid** - Equipment, technicians, alerts, inventory
- **Role-Based Quick Actions** - Tailored to user role
- **Active Compliance Alerts** - Pulsing critical warnings
- **Upcoming Inspections** - Next 7 days
- **Recent Service Activity** - Last 5 service logs
- **Low Inventory Warnings** - Below reorder level

### Access:
- URL: `/dashboard`
- Navigation: Always accessible from main nav

### User Roles Access:
- ✓ Technician: Quick actions for service logging
- ✓ Compliance Manager: Focus on alerts and reports
- ✓ Admin: Full system overview + user management
- ✓ Auditor: Read-only view of all activity

---

## Layer 2: Equipment Layer 📦

**Color**: Green (#28a745)
**Purpose**: Manage equipment inventory and compliance status

### Key Components:

#### Equipment List
- Searchable/filterable equipment inventory
- QR/Barcode scanner integration
- Status indicators (Active, Retired, Disposed)
- Quick access to details

#### Equipment Detail
- **Basic Information**
  - Equipment ID, Name, Type
  - Location, Manufacturer, Model, Serial
  - Refrigerant type and name
  - Full charge capacity

- **Compliance Status**
  - Current leak rate (color-coded)
  - Threshold comparison
  - Next inspection date
  - Compliance history

- **Service History**
  - All service logs
  - Refrigerant additions/recoveries
  - Leak repairs
  - Follow-up requirements

- **Leak Inspections**
  - Inspection timeline
  - Leak rate calculations
  - Compliance violations
  - Next inspection scheduling

- **Refrigerant Transactions**
  - Added refrigerant tracking
  - Recovery records
  - Disposal documentation

- **Documents**
  - Equipment photos
  - Manuals
  - Warranty documents
  - Compliance certificates

#### Refrigerant Inventory
- Current stock levels
- Reorder alerts
- Transaction history
- Recovery tracking

### Access:
- URL: `/equipment`
- Scanner: `/equipment/scanner`
- Detail: `/equipment/<id>`
- Add: `/equipment/add`
- Edit: `/equipment/<id>/edit`
- Inventory: `/inventory`

### CSS Classes:
```css
.layer-equipment {
    --layer-color: var(--layer-equipment);
    --layer-color-dark: #218838;
}
```

---

## Layer 3: Logs Layer 📋

**Color**: Orange (#ff9800)
**Purpose**: Record and track all service, maintenance, and compliance activities

### Key Components:

#### Service Logs
- **Service Entry**
  - Date, equipment, technician
  - Service type (Repair, Maintenance, Installation, Disposal)
  - Refrigerant added/recovered
  - Work performed details
  - Leak information (found, repaired, location)
  - Follow-up requirements

- **Wizard-Style Entry** (Future Enhancement)
  - Step 1: Select Equipment
  - Step 2: Service Details
  - Step 3: Refrigerant Handling
  - Step 4: Leak Information
  - Step 5: Review & Submit

#### Leak Inspections
- **Inspection Entry**
  - Date, equipment, technician
  - Inspection type (Routine, Post-Repair, Initial)
  - Leak detection results
  - Current charge measurement
  - Automatic leak rate calculation
  - Compliance determination
  - Next inspection scheduling

#### Refrigerant Transactions
- Purchase records
- Disposal documentation
- Recovery tracking
- Cylinder management

#### Document Management
- Upload capabilities
- Type classification (Certification, Invoice, Photo, Report, Manual)
- Entity linking (equipment, technician, service log, inspection)
- Expiration tracking
- Read-only audit trail

#### Technician Certifications
- EPA 608 certifications (Type I, II, III, Universal)
- Issue and expiration dates
- Document attachments
- Status tracking (Active, Expired, Revoked)

### Access:
- Service Logs: `/service-logs`
- Add Service: `/service-logs/add`
- Leak Inspections: `/leak-inspections`
- Add Inspection: `/leak-inspections/add`
- Documents: `/documents`
- Upload: `/documents/upload`

### CSS Classes:
```css
.layer-logs {
    --layer-color: var(--layer-logs);
    --layer-color-dark: #e68900;
}
```

---

## Layer 4: Reports Layer 📊

**Color**: Purple (#673ab7)
**Purpose**: Generate EPA compliance reports and analytics

### Key Components:

#### EPA 608 Reports
- Equipment summary
- Refrigerant usage by type
- Leak inspection compliance
- Non-compliant equipment list
- Service activity summary

#### EPA 609 Reports (Motor Vehicle AC)
- Vehicle equipment tracking
- R-134a usage
- Technician certifications
- Recovery equipment records

#### CARB Reports (California)
- High-GWP refrigerant tracking
- Phase-out compliance
- Alternative refrigerant adoption

#### AIM Act Reports
- HFC allocation tracking
- Import/export records
- Quarterly reporting
- Annual summaries

#### Report Features
- **Auto-Format Preview**
  - Professional EPA header
  - Structured sections
  - Two-column field layout
  - Print-optimized styles

- **Export Options**
  - PDF generation
  - CSV data export
  - Print-ready format

- **Date Range Selection**
  - Custom date ranges
  - Quarterly reports
  - Annual summaries

### Access:
- Reports Hub: `/reports`
- EPA 608: `/reports/epa608`
- EPA 609: `/reports/epa609`
- CARB: `/reports/carb`
- AIM Act: `/reports/aim-act`

### CSS Classes:
```css
.layer-reports {
    --layer-color: var(--layer-reports);
    --layer-color-dark: #512da8;
}

.epa-report-preview {
    /* Professional report styling */
}
```

---

## Layer 5: User Layer 👥

**Color**: Red (#dc3545)
**Purpose**: Manage users, roles, permissions, and certifications

### Key Components:

#### User Management (Admin Only)
- **User List**
  - All system users
  - Role indicators
  - Active/inactive status
  - Last login tracking

- **User Creation/Editing**
  - Username, email, full name
  - Role assignment (technician, compliance_manager, admin)
  - Password management
  - Technician linking
  - Phone, company info

- **User Roles**
  - **Technician**: Service logging, document upload
  - **Compliance Manager**: Reports, alerts, equipment management
  - **Admin**: Full system access, user management
  - **Auditor**: Read-only access (future)

#### Technician Management
- **Technician List**
  - All certified technicians
  - Certification types
  - Expiration tracking
  - Service history

- **Technician Detail**
  - Contact information
  - EPA 608 certification details
  - Additional certifications
  - Service logs performed
  - Inspection history
  - Attached documents

- **Certification Tracking**
  - Issue dates
  - Expiration dates
  - Auto-alerts for expiring certs
  - Document uploads

#### Permission System
- Role-based access control (RBAC)
- Granular permissions per role
- Read-only vs. edit access
- Audit trail for changes

### Access:
- Users (Admin): `/users`
- Add User: `/users/add`
- Edit User: `/users/<id>/edit`
- Technicians: `/technicians`
- Add Technician: `/technicians/add`
- Edit Technician: `/technicians/<id>/edit`
- Technician Detail: `/technicians/<id>`

### CSS Classes:
```css
.layer-user {
    --layer-color: var(--layer-user);
    --layer-color-dark: #c82333;
}
```

---

## Settings Layer ⚙️

**Color**: Gray (#607d8b)
**Purpose**: System configuration, user preferences, and application settings

### Key Components:

#### User Profile
- **Profile Information**
  - Full name, email, role display
  - Account creation date
  - Profile editing
  - Password management

#### Notification Preferences
- **Alert Notifications**
  - Leak rate alerts (>30% critical threshold)
  - Upcoming inspections (7 days before due)
  - Low refrigerant inventory warnings
  - Certification expiration notices
  - Email digest options

#### Display Preferences
- **Date and Unit Settings**
  - Date format selection (ISO, US, International)
  - Refrigerant unit (lbs/kg)
  - Items per page
  - Layer indicator visibility
  - Compact mode toggle

#### EPA Compliance Configuration (Admin/Manager Only)
- **Threshold Settings**
  - Minor leak threshold configuration (default 10%)
  - Critical leak threshold (EPA 608 default: 30%)
  - Inspection reminder days (default 7)
  - Facility name for reports
  - EPA ID number

#### Quick Links
- Manage Users (Admin)
- Manage Technicians
- Refrigerant Inventory
- Alert Settings
- Documents

#### System Information (Admin Only)
- Application version
- Architecture information
- Database type
- Last backup timestamp
- System logs access
- Cache management

#### Data Export
- Export EPA reports (PDF)
- Export service logs (CSV)
- Export equipment data (JSON)

#### Help & Support
- Documentation links
- EPA 608 compliance guide
- External resources

### Access:
- URL: `/settings`
- Navigation: Main navigation after Reports
- Update Settings: `/settings/update` (POST)

### User Roles Access:
- ✓ All authenticated users can access Settings
- ✓ Admin/Compliance Manager: Additional EPA compliance configuration
- ✓ Admin only: System information and management tools

### CSS Classes:
```css
.layer-settings {
    --layer-color: #607d8b;
    --layer-color-dark: #455a64;
}

.settings-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}

.settings-item {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #607d8b;
}

.settings-label {
    font-size: 0.9rem;
    color: #666;
    font-weight: 600;
}

.settings-value {
    font-size: 1.1rem;
    color: #333;
    font-weight: 500;
}
```

### Implementation Notes:
- Settings is a **supporting layer** that provides configuration for all other layers
- Not part of the primary 5-layer data hierarchy
- Accessible from main navigation for convenience
- Settings updates currently show placeholder message (to be implemented)
- Future enhancement: Persist user preferences in database

---

## Layer Visual Indicators

### Layer Indicator Bar
Every page displays its layer at the top:

```html
<div class="layer-indicator layer-equipment">
    <div class="layer-indicator-content">
        <span class="layer-icon">📦</span>
        <div class="layer-info">
            <h1 class="layer-name">Equipment Layer</h1>
            <p class="layer-description">Equipment detail, leak history, refrigerant types</p>
        </div>
    </div>
</div>
```

### Breadcrumb Navigation
Shows layer context and navigation path:

```html
<div class="breadcrumb layer-equipment">
    <div class="breadcrumb-content">
        <div class="breadcrumb-item">
            <a href="/dashboard">🏠 Dashboard</a>
        </div>
        <span class="breadcrumb-separator">›</span>
        <div class="breadcrumb-item">
            <a href="/equipment">📦 Equipment</a>
        </div>
        <span class="breadcrumb-separator">›</span>
        <div class="breadcrumb-item active">
            HVAC-001
        </div>
    </div>
</div>
```

### Layer Content Container
Consistent content styling per layer:

```html
<div class="layer-content layer-equipment">
    <div class="layer-content-header">
        <h2 class="layer-content-title">
            📦 Equipment Details
        </h2>
        <div class="layer-content-actions">
            <a href="..." class="btn btn-primary">Edit</a>
            <a href="..." class="btn btn-secondary">Back</a>
        </div>
    </div>
    <!-- Content here -->
</div>
```

---

## Layer Tabs (Sub-Navigation)

For pages with multiple sections within a layer:

```html
<div class="layer-tabs layer-equipment">
    <a href="#overview" class="layer-tab active">
        <span class="layer-tab-icon">📋</span>
        Overview
    </a>
    <a href="#service-history" class="layer-tab">
        <span class="layer-tab-icon">🔧</span>
        Service History
    </a>
    <a href="#inspections" class="layer-tab">
        <span class="layer-tab-icon">🔍</span>
        Inspections
    </a>
    <a href="#documents" class="layer-tab">
        <span class="layer-tab-icon">📄</span>
        Documents
    </a>
</div>
```

---

## Layer Navigation Cards

Dashboard displays all 5 layers as interactive cards:

```html
<div class="layer-nav-grid">
    <a href="/equipment" class="layer-nav-card layer-equipment" style="--layer-color: var(--layer-equipment);">
        <div class="layer-nav-card-icon">📦</div>
        <h3 class="layer-nav-card-title">Equipment Layer</h3>
        <p class="layer-nav-card-description">Equipment detail, leak history, refrigerant types</p>
        <div class="layer-nav-card-stats">
            <div class="layer-nav-stat">
                <div class="layer-nav-stat-value">15</div>
                <div class="layer-nav-stat-label">Active</div>
            </div>
            <div class="layer-nav-stat">
                <div class="layer-nav-stat-value">3</div>
                <div class="layer-nav-stat-label">Due Soon</div>
            </div>
        </div>
    </a>
</div>
```

---

## Implementation Guidelines

### Adding a New Page

1. **Determine the Layer** - Which of the 5 layers does this page belong to?
2. **Add Layer Indicator** - Include the colored layer bar at the top
3. **Add Breadcrumbs** - Show navigation context
4. **Use Layer Colors** - Apply the layer's color scheme
5. **Follow Layout Pattern** - Use layer-content container

### Example: New Equipment Sub-Page

```html
{% extends "base.html" %}

{% block content %}
<!-- Layer Indicator -->
<div class="layer-indicator layer-equipment">
    <div class="layer-indicator-content">
        <span class="layer-icon">📦</span>
        <div class="layer-info">
            <h1 class="layer-name">Equipment Layer</h1>
            <p class="layer-description">Equipment detail, leak history, refrigerant types</p>
        </div>
    </div>
</div>

<!-- Breadcrumbs -->
<div class="breadcrumb layer-equipment">
    <div class="breadcrumb-content">
        <div class="breadcrumb-item">
            <a href="{{ url_for('dashboard') }}">🏠 Dashboard</a>
        </div>
        <span class="breadcrumb-separator">›</span>
        <div class="breadcrumb-item">
            <a href="{{ url_for('equipment_list') }}">📦 Equipment</a>
        </div>
        <span class="breadcrumb-separator">›</span>
        <div class="breadcrumb-item active">
            Your Page Name
        </div>
    </div>
</div>

<!-- Content -->
<div class="layer-content layer-equipment">
    <div class="layer-content-header">
        <h2 class="layer-content-title">
            📦 Your Page Title
        </h2>
        <div class="layer-content-actions">
            <a href="..." class="btn btn-primary">Action</a>
        </div>
    </div>

    <!-- Your content here -->
</div>
{% endblock %}
```

---

## Mobile Optimizations

All layer components are mobile-responsive:

- **Layer Indicators**: Stack vertically, reduce font size
- **Breadcrumbs**: Smaller font, wrap on multiple lines
- **Layer Navigation Cards**: Single column layout
- **Layer Tabs**: Horizontal scroll with touch support
- **Content Headers**: Stack actions below title

---

## Color Palette

```css
:root {
    --layer-dashboard: #0066cc;  /* Blue */
    --layer-equipment: #28a745;  /* Green */
    --layer-logs: #ff9800;       /* Orange */
    --layer-reports: #673ab7;    /* Purple */
    --layer-user: #dc3545;       /* Red */
}
```

Each layer has:
- **Primary Color**: Main accent
- **Dark Variant**: Gradients and hover states
- **Light Variant**: Backgrounds (10% opacity)

---

## User Workflows

### Technician Daily Workflow

1. **Dashboard Layer** → Quick Actions
2. **Equipment Layer** → Scan QR code
3. **Logs Layer** → Log service or inspection
4. **Dashboard Layer** → View updated stats

### Compliance Manager Weekly Workflow

1. **Dashboard Layer** → Review alerts
2. **Equipment Layer** → Check non-compliant equipment
3. **Logs Layer** → Review service logs
4. **Reports Layer** → Generate EPA 608 report
5. **User Layer** → Check technician certifications

### Admin Setup Workflow

1. **Settings Layer** → Configure EPA compliance thresholds
2. **Settings Layer** → Set facility name and EPA ID
3. **User Layer** → Add new users/technicians
4. **Equipment Layer** → Register equipment
5. **Equipment Layer** → Set reorder levels for inventory
6. **Dashboard Layer** → Configure alerts
7. **Reports Layer** → Schedule automatic reports

### User Configuration Workflow

1. **Login** → Authentication
2. **Dashboard Layer** → System overview
3. **Settings Layer** → Set personal preferences
4. **Settings Layer** → Configure notifications
5. **Settings Layer** → Adjust display settings
6. **Dashboard Layer** → Return to work

---

## Benefits of Layered Architecture

### For Users:
- ✓ Clear mental model of system organization
- ✓ Reduced cognitive load (know which layer = know what to expect)
- ✓ Consistent navigation patterns
- ✓ Visual color coding for instant recognition
- ✓ Breadcrumbs prevent getting lost

### For Developers:
- ✓ Logical code organization
- ✓ Easier to add new features (just pick a layer)
- ✓ Consistent styling with layer-based classes
- ✓ Maintainable architecture
- ✓ Clear separation of concerns

### For Compliance:
- ✓ Reports layer isolates regulatory requirements
- ✓ Audit trails maintained in logs layer
- ✓ Equipment compliance status clearly visible
- ✓ User permissions enforced at layer level

---

## Future Enhancements

### Layer-Based Features:
1. **Dashboard Layer**
   - Real-time websocket updates
   - Customizable widget layout
   - Layer-specific notifications

2. **Equipment Layer**
   - Equipment health scores
   - Predictive maintenance alerts
   - 3D equipment visualizations

3. **Logs Layer**
   - Voice-to-text service entry
   - Photo annotations
   - Offline-first sync

4. **Reports Layer**
   - Scheduled email reports
   - Interactive charts/graphs
   - Benchmark comparisons

5. **User Layer**
   - Single sign-on (SSO)
   - Two-factor authentication
   - Activity analytics

---

## Testing the Architecture

### Visual Tests:
- [ ] Each layer has correct color indicator
- [ ] Breadcrumbs display proper navigation path
- [ ] Layer cards on dashboard are interactive
- [ ] Layer tabs work on detail pages
- [ ] Mobile view stacks properly

### Navigation Tests:
- [ ] Can navigate from Dashboard → Any Layer
- [ ] Breadcrumbs link back to parent layers
- [ ] Layer indicator shows current location
- [ ] Quick Actions route to correct layers

### Role-Based Tests:
- [ ] Technician sees appropriate quick actions
- [ ] Manager sees compliance-focused actions
- [ ] Admin can access User Layer
- [ ] Non-admin cannot access User Layer

---

## Support & Maintenance

### Adding New Layers (Future):
If you need to add a 6th layer:

1. Add color variable to `:root`
2. Create layer-specific CSS class
3. Add layer card to dashboard
4. Update navigation structure
5. Document in this file

### Modifying Existing Layers:
- Update layer description in dashboard
- Maintain color consistency
- Keep breadcrumb structure
- Test mobile responsiveness

---

## Conclusion

The 5-layer architecture provides:
- **Clarity**: Users always know where they are
- **Consistency**: Predictable patterns across the system
- **Scalability**: Easy to add new features within existing layers
- **Compliance**: Regulatory workflows are clearly organized
- **Mobile-Friendly**: Responsive design throughout

This architecture is the foundation of EcoFreonTrack's superior UX for EPA 608 compliance management.

---

**Version**: 2.0.0
**Last Updated**: October 28, 2025
**Implementation Status**: ✅ Complete
