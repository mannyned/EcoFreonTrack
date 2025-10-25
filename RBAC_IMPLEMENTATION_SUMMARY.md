# Role-Based Access Control (RBAC) Implementation

## Overview

EcoFreonTrack now includes a comprehensive role-based access control system with three user roles:

### User Roles

1. **Technician**
   - Add service logs
   - Record refrigerant additions/removals
   - Upload certificates
   - View own service history

2. **Compliance Manager**
   - View dashboards and analytics
   - Approve/review service logs
   - Generate compliance reports
   - View all compliance alerts
   - Resolve alerts
   - Monitor all equipment and logs

3. **Admin/Owner**
   - All Compliance Manager permissions
   - Manage users (create, edit, deactivate)
   - Manage sites and locations
   - Manage equipment
   - Manage technicians
   - Access billing information
   - Full system access

## What Was Added

### 1. User Model (models.py)

Added `User` model with:
- Username, email, password (hashed)
- Full name, phone
- Role (technician, compliance_manager, admin)
- Link to Technician record (if applicable)
- Active status and verification flags
- Permission checking method

```python
class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='technician')
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'))

    def set_password(self, password)
    def check_password(self, password)
    def has_permission(self, permission)
```

### 2. Authentication Module (auth.py)

Created authentication decorators and helper functions:

**Decorators:**
- `@login_required` - Requires user to be logged in
- `@permission_required(permission)` - Requires specific permission
- `@role_required(*roles)` - Requires specific role(s)

**Helper Functions:**
- `get_current_user()` - Get currently logged-in user
- `is_authenticated()` - Check if user is logged in
- `has_role(*roles)` - Check if user has role
- `has_permission(permission)` - Check if user has permission

### 3. Permission System

Each role has specific permissions defined in the User model:

**Technician Permissions:**
- add_service_log
- add_refrigerant_transaction
- upload_certificate
- view_own_logs

**Compliance Manager Permissions:**
- view_dashboard
- approve_logs
- generate_reports
- view_all_logs
- view_compliance_alerts
- resolve_alerts

**Admin Permissions:**
- All Compliance Manager permissions
- manage_users
- manage_sites
- manage_equipment
- manage_technicians
- manage_billing

## Next Steps to Complete Implementation

### 1. Add Authentication Routes to app.py

Add these routes for login/logout:

```python
from auth import (
    login_required,
    permission_required,
    role_required,
    get_current_user
)
from models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            user.last_login = datetime.utcnow()
            db.session.commit()

            flash(f'Welcome back, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid credentials or inactive account', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))
```

### 2. Protect Existing Routes

Add decorators to existing routes based on required permissions:

```python
# Admin-only routes
@app.route('/equipment/add')
@permission_required('manage_equipment')
def equipment_add():
    ...

# Compliance Manager and Admin
@app.route('/reports')
@permission_required('generate_reports')
def reports():
    ...

# Technician routes
@app.route('/service-logs/add')
@permission_required('add_service_log')
def service_log_add():
    ...
```

### 3. Create Login Template (templates/login.html)

Create a login page for user authentication.

### 4. Create User Management Interface (Admin only)

Create routes and templates for:
- `/users` - List all users
- `/users/add` - Add new user
- `/users/<id>/edit` - Edit user
- `/users/<id>/deactivate` - Deactivate user

### 5. Create Role-Specific Dashboards

Modify dashboard to show different views based on role:
- **Technician**: Own service logs, assigned equipment
- **Compliance Manager**: Compliance overview, alerts, reports
- **Admin**: Full system overview, user management, billing

### 6. Update Navigation

Update base.html template to show/hide menu items based on user role and permissions.

### 7. Create Database Migration Script

Run this to create the user table in Supabase:

```python
# In create_user_table.py
from app import app
from models import db

with app.app_context():
    db.create_all()  # This will create the user table
```

### 8. Create Initial Admin User

Create a script to set up the first admin user:

```python
# In create_admin_user.py
from app import app
from models import db, User

with app.app_context():
    admin = User(
        username='admin',
        email='admin@ecofreontrack.com',
        full_name='System Administrator',
        role='admin',
        is_active=True,
        is_verified=True
    )
    admin.set_password('ChangeMe123!')  # CHANGE THIS!

    db.session.add(admin)
    db.session.commit()

    print(f'Admin user created: {admin.username}')
```

## Security Features

1. **Password Hashing**: Uses Werkzeug's secure password hashing
2. **Session Management**: Flask sessions for user authentication
3. **Permission Checks**: Decorator-based permission checking
4. **Active Account Verification**: Inactive users cannot log in
5. **Role-Based Access**: Fine-grained control over features

## Usage Example

```python
# In app.py, protect a route for admin only:
@app.route('/users/manage')
@role_required('admin')
def user_manage():
    users = User.query.all()
    return render_template('user_manage.html', users=users)

# Protect a route for compliance managers and admins:
@app.route('/alerts/resolve/<int:id>')
@permission_required('resolve_alerts')
def alert_resolve(id):
    alert = ComplianceAlert.query.get_or_404(id)
    # ... resolve logic
```

## Testing

To test the RBAC system:

1. Create users with different roles
2. Log in as each role
3. Verify access to different features
4. Test permission denials work correctly

## Future Enhancements

- Password reset functionality
- Email verification
- Two-factor authentication
- Audit logging (track who did what)
- Site/location-based access control
- API key authentication for integrations
