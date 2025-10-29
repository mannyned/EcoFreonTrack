"""
EPA Section 608 Refrigerant Tracking & Compliance System
Managed under 40 CFR Part 82
Flask web application for tracking refrigerant usage, leakage, recovery, and compliance
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file, session
from models import db, Equipment, Technician, ServiceLog, LeakInspection, RefrigerantTransaction, ComplianceAlert, RefrigerantInventory, Document, TechnicianCertification, User
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from config import get_config
import os
from dotenv import load_dotenv
from file_utils import (
    create_document_record,
    get_document_path,
    delete_document,
    get_documents_by_entity,
    format_file_size,
    get_document_icon,
    ALLOWED_EXTENSIONS
)
from auth import (
    login_required,
    permission_required,
    role_required,
    get_current_user,
    is_authenticated,
    has_permission
)

# Load environment variables from .env file
load_dotenv()

# Import AI features
try:
    from ai_features import (
        get_equipment_at_risk,
        parse_service_nl,
        ask_compliance_question,
        AIConfig
    )
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Create Flask app with environment-based configuration
env = os.environ.get('FLASK_ENV', 'development')
app = Flask(__name__)
app.config.from_object(get_config(env))

db.init_app(app)


# Initialize database
with app.app_context():
    db.create_all()

    # Initialize common refrigerants in inventory if empty
    if RefrigerantInventory.query.count() == 0:
        common_refrigerants = [
            {'type': 'CFC', 'name': 'R-12', 'quantity': 0.0, 'reorder': 25.0},
            {'type': 'HCFC', 'name': 'R-22', 'quantity': 0.0, 'reorder': 100.0},
            {'type': 'HFC', 'name': 'R-134a', 'quantity': 0.0, 'reorder': 100.0},
            {'type': 'HFC', 'name': 'R-410A', 'quantity': 0.0, 'reorder': 150.0},
            {'type': 'HFC', 'name': 'R-404A', 'quantity': 0.0, 'reorder': 75.0},
            {'type': 'HFC', 'name': 'R-407C', 'quantity': 0.0, 'reorder': 75.0},
        ]

        for ref in common_refrigerants:
            inventory = RefrigerantInventory(
                refrigerant_type=ref['type'],
                refrigerant_name=ref['name'],
                quantity_on_hand=ref['quantity'],
                reorder_level=ref['reorder']
            )
            db.session.add(inventory)

        db.session.commit()


# ============================================================================
# PUBLIC LANDING PAGE
# ============================================================================

@app.route('/')
def homepage():
    """Public landing page - accessible without login"""
    return render_template('homepage.html')


# ============================================================================
# AUTHENTICATION & USER MANAGEMENT
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    # Redirect if already logged in
    if is_authenticated():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please provide both username and password', 'danger')
            return render_template('login.html')

        # Try to find user by username or email
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User.query.filter_by(email=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account is inactive. Please contact an administrator.', 'danger')
                return render_template('login.html')

            # Set session
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['full_name'] = user.full_name

            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()

            flash(f'Welcome back, {user.full_name}!', 'success')

            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration/signup"""
    # Redirect if already logged in
    if is_authenticated():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            # Validate all required fields
            required_fields = {
                'full_name': 'Full Name',
                'email': 'Email Address',
                'password': 'Password',
                'company_name': 'Company Name',
                'street_address': 'Street Address',
                'city': 'City',
                'state': 'State',
                'zip_code': 'Zip Code',
                'phone': 'Phone Number'
            }

            missing_fields = []
            for field, label in required_fields.items():
                if not request.form.get(field, '').strip():
                    missing_fields.append(label)

            if missing_fields:
                flash(f'Please provide: {", ".join(missing_fields)}', 'danger')
                return render_template('signup.html')

            # Extract form data
            full_name = request.form['full_name'].strip()
            email = request.form['email'].strip().lower()
            password = request.form['password']
            company_name = request.form['company_name'].strip()
            street_address = request.form['street_address'].strip()
            city = request.form['city'].strip()
            state = request.form['state'].strip()
            zip_code = request.form['zip_code'].strip()
            phone = request.form['phone'].strip()

            # Validate password length
            if len(password) < 6:
                flash('Password must be at least 6 characters long', 'danger')
                return render_template('signup.html')

            # Generate username from email (before @)
            username = email.split('@')[0]

            # Check if email already exists
            if User.query.filter_by(email=email).first():
                flash('An account with this email already exists. Please login instead.', 'danger')
                return render_template('signup.html')

            # Check if username already exists (if so, add a number)
            base_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1

            # Create new user
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                company_name=company_name,
                street_address=street_address,
                city=city,
                state=state,
                zip_code=zip_code,
                role='compliance_manager',  # Default role for new signups
                is_active=True,
                is_verified=False  # Require verification
            )

            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # Auto-login after successful signup
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['full_name'] = user.full_name

            user.last_login = datetime.utcnow()
            db.session.commit()

            flash(f'Welcome, {user.full_name}! Your account has been created successfully.', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'danger')
            return render_template('signup.html')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    """User logout"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/users')
@role_required('admin')
def user_list():
    """List all users (Admin only)"""
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/add', methods=['GET', 'POST'])
@role_required('admin')
def user_add():
    """Add new user (Admin only)"""
    if request.method == 'POST':
        try:
            # Check if username or email already exists
            if User.query.filter_by(username=request.form['username']).first():
                flash('Username already exists', 'danger')
                return redirect(request.url)

            if User.query.filter_by(email=request.form['email']).first():
                flash('Email already exists', 'danger')
                return redirect(request.url)

            user = User(
                username=request.form['username'],
                email=request.form['email'],
                full_name=request.form['full_name'],
                phone=request.form.get('phone', ''),
                role=request.form['role'],
                is_active=True,
                is_verified='is_verified' in request.form
            )

            # Set password
            password = request.form.get('password', '')
            if len(password) < 6:
                flash('Password must be at least 6 characters', 'danger')
                return redirect(request.url)

            user.set_password(password)

            # Link to technician if role is technician and technician_id provided
            if request.form.get('technician_id'):
                user.technician_id = int(request.form['technician_id'])

            db.session.add(user)
            db.session.commit()

            flash(f'User {user.username} created successfully!', 'success')
            return redirect(url_for('user_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'danger')

    # Get technicians for linking
    technicians = Technician.query.filter_by(status='Active').all()
    return render_template('user_form.html', user=None, technicians=technicians)


@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@role_required('admin')
def user_edit(id):
    """Edit user (Admin only)"""
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        try:
            # Check username uniqueness (excluding current user)
            existing = User.query.filter_by(username=request.form['username']).first()
            if existing and existing.id != id:
                flash('Username already exists', 'danger')
                return redirect(request.url)

            # Check email uniqueness (excluding current user)
            existing = User.query.filter_by(email=request.form['email']).first()
            if existing and existing.id != id:
                flash('Email already exists', 'danger')
                return redirect(request.url)

            user.username = request.form['username']
            user.email = request.form['email']
            user.full_name = request.form['full_name']
            user.phone = request.form.get('phone', '')
            user.role = request.form['role']
            user.is_active = 'is_active' in request.form
            user.is_verified = 'is_verified' in request.form

            # Update password if provided
            if request.form.get('password'):
                password = request.form['password']
                if len(password) < 6:
                    flash('Password must be at least 6 characters', 'danger')
                    return redirect(request.url)
                user.set_password(password)

            # Update technician link
            if request.form.get('technician_id'):
                user.technician_id = int(request.form['technician_id'])
            else:
                user.technician_id = None

            db.session.commit()
            flash(f'User {user.username} updated successfully!', 'success')
            return redirect(url_for('user_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'danger')

    technicians = Technician.query.filter_by(status='Active').all()
    return render_template('user_form.html', user=user, technicians=technicians)


@app.route('/users/<int:id>/toggle-active', methods=['POST'])
@role_required('admin')
def user_toggle_active(id):
    """Toggle user active status (Admin only)"""
    try:
        user = User.query.get_or_404(id)

        # Prevent deactivating yourself
        current_user = get_current_user()
        if current_user and current_user.id == id:
            flash('You cannot deactivate your own account', 'danger')
            return redirect(url_for('user_list'))

        user.is_active = not user.is_active
        db.session.commit()

        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {user.username} {status} successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user status: {str(e)}', 'danger')

    return redirect(url_for('user_list'))


# Make current_user available in all templates
@app.context_processor
def inject_user():
    """Make current user available in all templates"""
    return {
        'current_user': get_current_user(),
        'is_authenticated': is_authenticated(),
        'has_permission': has_permission
    }


# ============================================================================
# DASHBOARD
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - requires login"""
    # Get statistics
    total_equipment = Equipment.query.filter_by(status='Active').count()
    total_technicians = Technician.query.filter_by(status='Active').count()
    active_alerts = ComplianceAlert.query.filter_by(status='Active').count()

    # Recent service logs
    recent_services = ServiceLog.query.order_by(desc(ServiceLog.service_date)).limit(5).all()

    # Upcoming inspections
    today = datetime.now().date()
    upcoming_inspections = []
    equipment_list = Equipment.query.filter_by(status='Active').all()
    for equip in equipment_list:
        last_inspection = LeakInspection.query.filter_by(equipment_id=equip.id).order_by(desc(LeakInspection.inspection_date)).first()
        if last_inspection and last_inspection.next_inspection_date:
            if last_inspection.next_inspection_date <= today + timedelta(days=7):
                upcoming_inspections.append({
                    'equipment': equip,
                    'next_date': last_inspection.next_inspection_date
                })

    # Active compliance alerts
    alerts = ComplianceAlert.query.filter_by(status='Active').order_by(desc(ComplianceAlert.alert_date)).limit(10).all()

    # Low inventory warnings
    low_inventory = RefrigerantInventory.query.filter(
        RefrigerantInventory.quantity_on_hand < RefrigerantInventory.reorder_level
    ).all()

    # === COMPLIANCE METRICS (Manager/Auditor View) ===

    # 1. Compliance Percentage - Equipment with leak rate < 30%
    compliant_equipment = 0
    if total_equipment > 0:
        for equip in equipment_list:
            last_inspection = LeakInspection.query.filter_by(equipment_id=equip.id).order_by(desc(LeakInspection.inspection_date)).first()
            if last_inspection:
                # Equipment is compliant if leak rate < 30% (EPA threshold)
                if last_inspection.leak_rate_percent < 30:
                    compliant_equipment += 1
            else:
                # No inspection yet, consider compliant (benefit of doubt)
                compliant_equipment += 1

        compliance_percentage = round((compliant_equipment / total_equipment) * 100, 1)
    else:
        compliance_percentage = 100.0

    # 2. Active Leak Alerts (Critical + Warning)
    critical_alerts = ComplianceAlert.query.filter_by(status='Active', severity='Critical').count()
    warning_alerts = ComplianceAlert.query.filter_by(status='Active', severity='Warning').count()

    # 3. Upcoming EPA Reports (next 30 days)
    # For demo, we'll show inspections due as "reports needed"
    upcoming_reports_count = len(upcoming_inspections)
    # Add equipment that need annual reports
    six_months_ago = today - timedelta(days=180)
    equipment_needing_reports = Equipment.query.filter(
        Equipment.status == 'Active',
        Equipment.install_date <= six_months_ago
    ).count()

    # 4. Refrigerant Recovery Summary (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    recovery_logs = ServiceLog.query.filter(
        ServiceLog.service_date >= thirty_days_ago,
        ServiceLog.refrigerant_recovered > 0
    ).all()

    total_recovered = sum([log.refrigerant_recovered for log in recovery_logs])
    recovery_count = len(recovery_logs)

    # 5. Monthly Refrigerant Usage Trend (last 6 months)
    monthly_usage = []
    monthly_labels = []

    for i in range(5, -1, -1):  # Last 6 months
        month_date = today - timedelta(days=30*i)
        month_start = month_date.replace(day=1)

        # Calculate next month start
        if month_date.month == 12:
            month_end = month_date.replace(year=month_date.year + 1, month=1, day=1)
        else:
            month_end = month_date.replace(month=month_date.month + 1, day=1)

        # Get refrigerant added in this month
        month_logs = ServiceLog.query.filter(
            ServiceLog.service_date >= month_start,
            ServiceLog.service_date < month_end
        ).all()

        month_total = sum([log.refrigerant_added for log in month_logs if log.refrigerant_added])
        monthly_usage.append(round(month_total, 2))
        monthly_labels.append(month_start.strftime('%b %Y'))

    # === TECHNICIAN-SPECIFIC DATA ===
    # Recent service logs (for technicians to track their work)
    technician_recent_logs = ServiceLog.query.order_by(desc(ServiceLog.service_date)).limit(10).all()

    # Recent leak inspections
    recent_leak_inspections = LeakInspection.query.order_by(desc(LeakInspection.inspection_date)).limit(10).all()

    # Equipment needing service soon
    equipment_needing_service = []
    for equip in equipment_list:
        last_service = ServiceLog.query.filter_by(equipment_id=equip.id).order_by(desc(ServiceLog.service_date)).first()
        if last_service:
            days_since_service = (today - last_service.service_date).days
            if days_since_service > 60:  # Equipment not serviced in 60+ days
                equipment_needing_service.append({
                    'equipment': equip,
                    'last_service_date': last_service.service_date,
                    'days_since': days_since_service
                })

    # === AUDITOR-SPECIFIC DATA ===
    # Recent compliance documents
    recent_documents = Document.query.order_by(desc(Document.uploaded_at)).limit(10).all()

    # All active alerts for audit review
    all_active_alerts = ComplianceAlert.query.filter_by(status='Active').order_by(desc(ComplianceAlert.alert_date)).all()

    return render_template('dashboard.html',
                           total_equipment=total_equipment,
                           total_technicians=total_technicians,
                           active_alerts=active_alerts,
                           recent_services=recent_services,
                           upcoming_inspections=upcoming_inspections,
                           alerts=alerts,
                           low_inventory=low_inventory,
                           # Compliance metrics (Manager/Admin)
                           compliance_percentage=compliance_percentage,
                           compliant_equipment=compliant_equipment,
                           critical_alerts=critical_alerts,
                           warning_alerts=warning_alerts,
                           upcoming_reports_count=upcoming_reports_count,
                           total_recovered=round(total_recovered, 2),
                           recovery_count=recovery_count,
                           monthly_usage=monthly_usage,
                           monthly_labels=monthly_labels,
                           # Technician-specific data
                           technician_recent_logs=technician_recent_logs,
                           recent_leak_inspections=recent_leak_inspections,
                           equipment_needing_service=equipment_needing_service,
                           # Auditor-specific data
                           recent_documents=recent_documents,
                           all_active_alerts=all_active_alerts)


# ============================================================================
# EQUIPMENT MANAGEMENT
# ============================================================================

@app.route('/equipment')
def equipment_list():
    """List all equipment"""
    # Get search parameter if provided
    search_query = request.args.get('search', '').strip()

    if search_query:
        # Search by equipment_id or name
        equipment = Equipment.query.filter(
            (Equipment.equipment_id.contains(search_query)) |
            (Equipment.name.contains(search_query))
        ).all()
    else:
        equipment = Equipment.query.all()

    return render_template('equipment_list.html', equipment=equipment, search_query=search_query)


@app.route('/equipment/scanner')
@login_required
def equipment_scanner():
    """QR/Barcode scanner for equipment lookup"""
    return render_template('equipment_scanner.html')


@app.route('/equipment/<int:id>')
def equipment_detail(id):
    """Equipment detail page"""
    equip = Equipment.query.get_or_404(id)

    # Get service history
    services = ServiceLog.query.filter_by(equipment_id=id).order_by(desc(ServiceLog.service_date)).all()

    # Get leak inspections
    inspections = LeakInspection.query.filter_by(equipment_id=id).order_by(desc(LeakInspection.inspection_date)).all()

    # Get refrigerant transactions
    transactions = RefrigerantTransaction.query.filter_by(equipment_id=id).order_by(desc(RefrigerantTransaction.transaction_date)).all()

    # Get documents
    documents = get_documents_by_entity(equipment_id=id)

    # Calculate annual leak rate
    if len(inspections) >= 2:
        latest = inspections[0]
        annual_leak_rate = latest.annual_leak_rate
    else:
        annual_leak_rate = 0.0

    # Check compliance
    compliant = annual_leak_rate <= equip.leak_rate_threshold if annual_leak_rate else True

    return render_template('equipment_detail.html',
                           equipment=equip,
                           services=services,
                           inspections=inspections,
                           transactions=transactions,
                           documents=documents,
                           annual_leak_rate=annual_leak_rate,
                           compliant=compliant,
                           format_file_size=format_file_size,
                           get_document_icon=get_document_icon)


@app.route('/equipment/add', methods=['GET', 'POST'])
def equipment_add():
    """Add new equipment"""
    if request.method == 'POST':
        try:
            equip = Equipment(
                equipment_id=request.form['equipment_id'],
                name=request.form['name'],
                equipment_type=request.form['equipment_type'],
                location=request.form.get('location', ''),
                manufacturer=request.form.get('manufacturer', ''),
                model_number=request.form.get('model_number', ''),
                serial_number=request.form.get('serial_number', ''),
                refrigerant_type=request.form['refrigerant_type'],
                refrigerant_name=request.form['refrigerant_name'],
                full_charge=float(request.form['full_charge']),
                install_date=datetime.strptime(request.form['install_date'], '%Y-%m-%d').date() if request.form.get('install_date') else None,
                leak_rate_threshold=float(request.form.get('leak_rate_threshold', 10.0)),
                inspection_frequency=int(request.form.get('inspection_frequency', 30))
            )

            db.session.add(equip)
            db.session.commit()

            flash(f'Equipment {equip.equipment_id} added successfully!', 'success')
            return redirect(url_for('equipment_detail', id=equip.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding equipment: {str(e)}', 'error')

    return render_template('equipment_form.html', equipment=None)


@app.route('/equipment/<int:id>/edit', methods=['GET', 'POST'])
def equipment_edit(id):
    """Edit equipment"""
    equip = Equipment.query.get_or_404(id)

    if request.method == 'POST':
        try:
            equip.equipment_id = request.form['equipment_id']
            equip.name = request.form['name']
            equip.equipment_type = request.form['equipment_type']
            equip.location = request.form.get('location', '')
            equip.manufacturer = request.form.get('manufacturer', '')
            equip.model_number = request.form.get('model_number', '')
            equip.serial_number = request.form.get('serial_number', '')
            equip.refrigerant_type = request.form['refrigerant_type']
            equip.refrigerant_name = request.form['refrigerant_name']
            equip.full_charge = float(request.form['full_charge'])
            equip.status = request.form['status']
            equip.leak_rate_threshold = float(request.form.get('leak_rate_threshold', 10.0))
            equip.inspection_frequency = int(request.form.get('inspection_frequency', 30))

            if request.form.get('install_date'):
                equip.install_date = datetime.strptime(request.form['install_date'], '%Y-%m-%d').date()

            db.session.commit()
            flash(f'Equipment {equip.equipment_id} updated successfully!', 'success')
            return redirect(url_for('equipment_detail', id=equip.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating equipment: {str(e)}', 'error')

    return render_template('equipment_form.html', equipment=equip)


# ============================================================================
# TECHNICIAN MANAGEMENT
# ============================================================================

@app.route('/technicians')
def technician_list():
    """List all technicians"""
    technicians = Technician.query.all()
    return render_template('technician_list.html', technicians=technicians)


@app.route('/technicians/add', methods=['GET', 'POST'])
def technician_add():
    """Add new technician"""
    if request.method == 'POST':
        try:
            tech = Technician(
                name=request.form['name'],
                certification_number=request.form['certification_number'],
                certification_type=request.form['certification_type'],
                certification_date=datetime.strptime(request.form['certification_date'], '%Y-%m-%d').date(),
                expiration_date=datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date() if request.form.get('expiration_date') else None,
                email=request.form.get('email', ''),
                phone=request.form.get('phone', ''),
                company=request.form.get('company', '')
            )

            db.session.add(tech)
            db.session.commit()

            flash(f'Technician {tech.name} added successfully!', 'success')
            return redirect(url_for('technician_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding technician: {str(e)}', 'error')

    return render_template('technician_form.html', technician=None)


@app.route('/technicians/<int:id>/edit', methods=['GET', 'POST'])
def technician_edit(id):
    """Edit technician"""
    tech = Technician.query.get_or_404(id)

    if request.method == 'POST':
        try:
            tech.name = request.form['name']
            tech.certification_number = request.form['certification_number']
            tech.certification_type = request.form['certification_type']
            tech.certification_date = datetime.strptime(request.form['certification_date'], '%Y-%m-%d').date()
            tech.email = request.form.get('email', '')
            tech.phone = request.form.get('phone', '')
            tech.company = request.form.get('company', '')
            tech.status = request.form['status']

            if request.form.get('expiration_date'):
                tech.expiration_date = datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()

            db.session.commit()
            flash(f'Technician {tech.name} updated successfully!', 'success')
            return redirect(url_for('technician_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating technician: {str(e)}', 'error')

    return render_template('technician_form.html', technician=tech)


# ============================================================================
# SERVICE LOGS
# ============================================================================

@app.route('/service-logs')
def service_log_list():
    """List all service logs"""
    logs = ServiceLog.query.order_by(desc(ServiceLog.service_date)).all()
    return render_template('service_log_list.html', logs=logs)


@app.route('/service-logs/add', methods=['GET', 'POST'])
def service_log_add():
    """Add new service log"""
    if request.method == 'POST':
        try:
            log = ServiceLog(
                equipment_id=int(request.form['equipment_id']),
                technician_id=int(request.form['technician_id']),
                service_date=datetime.strptime(request.form['service_date'], '%Y-%m-%d').date(),
                service_type=request.form['service_type'],
                refrigerant_added=float(request.form.get('refrigerant_added', 0.0)),
                refrigerant_recovered=float(request.form.get('refrigerant_recovered', 0.0)),
                work_performed=request.form.get('work_performed', ''),
                leak_found='leak_found' in request.form,
                leak_repaired='leak_repaired' in request.form,
                leak_location=request.form.get('leak_location', ''),
                follow_up_required='follow_up_required' in request.form,
                follow_up_notes=request.form.get('follow_up_notes', '')
            )

            if request.form.get('follow_up_date'):
                log.follow_up_date = datetime.strptime(request.form['follow_up_date'], '%Y-%m-%d').date()

            db.session.add(log)

            # Update refrigerant inventory
            equipment = Equipment.query.get(log.equipment_id)
            if log.refrigerant_added > 0:
                inventory = RefrigerantInventory.query.filter_by(refrigerant_name=equipment.refrigerant_name).first()
                if inventory:
                    inventory.quantity_on_hand -= log.refrigerant_added

                    # Create transaction record
                    trans = RefrigerantTransaction(
                        equipment_id=log.equipment_id,
                        transaction_date=log.service_date,
                        transaction_type='Added',
                        refrigerant_type=equipment.refrigerant_type,
                        refrigerant_name=equipment.refrigerant_name,
                        quantity=log.refrigerant_added,
                        notes=f'Added during {log.service_type}'
                    )
                    db.session.add(trans)

            if log.refrigerant_recovered > 0:
                inventory = RefrigerantInventory.query.filter_by(refrigerant_name=equipment.refrigerant_name).first()
                if inventory:
                    inventory.quantity_recovered += log.refrigerant_recovered

                    # Create transaction record
                    trans = RefrigerantTransaction(
                        equipment_id=log.equipment_id,
                        transaction_date=log.service_date,
                        transaction_type='Recovered',
                        refrigerant_type=equipment.refrigerant_type,
                        refrigerant_name=equipment.refrigerant_name,
                        quantity=log.refrigerant_recovered,
                        notes=f'Recovered during {log.service_type}'
                    )
                    db.session.add(trans)

            db.session.commit()

            flash('Service log added successfully!', 'success')
            return redirect(url_for('equipment_detail', id=log.equipment_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding service log: {str(e)}', 'error')

    equipment = Equipment.query.filter_by(status='Active').all()
    technicians = Technician.query.filter_by(status='Active').all()

    return render_template('service_log_form.html', log=None, equipment=equipment, technicians=technicians)


# ============================================================================
# LEAK INSPECTIONS
# ============================================================================

@app.route('/leak-inspections')
def leak_inspection_list():
    """List all leak inspections"""
    inspections = LeakInspection.query.order_by(desc(LeakInspection.inspection_date)).all()
    return render_template('leak_inspection_list.html', inspections=inspections)


@app.route('/leak-inspections/add', methods=['GET', 'POST'])
def leak_inspection_add():
    """Add new leak inspection"""
    if request.method == 'POST':
        try:
            inspection = LeakInspection(
                equipment_id=int(request.form['equipment_id']),
                technician_id=int(request.form['technician_id']),
                inspection_date=datetime.strptime(request.form['inspection_date'], '%Y-%m-%d').date(),
                inspection_type=request.form['inspection_type'],
                leak_detected='leak_detected' in request.form,
                leak_location=request.form.get('leak_location', ''),
                leak_severity=request.form.get('leak_severity', ''),
                current_charge=float(request.form.get('current_charge', 0.0)),
                notes=request.form.get('notes', '')
            )

            # Calculate leak rate and next inspection
            equipment = Equipment.query.get(inspection.equipment_id)
            previous_inspection = LeakInspection.query.filter_by(equipment_id=inspection.equipment_id).order_by(desc(LeakInspection.inspection_date)).first()

            if previous_inspection and previous_inspection.current_charge:
                days_between = (inspection.inspection_date - previous_inspection.inspection_date).days
                if days_between > 0:
                    charge_lost = previous_inspection.current_charge - inspection.current_charge
                    inspection.charge_deficit = charge_lost

                    # Calculate annual leak rate
                    annual_loss = (charge_lost / previous_inspection.current_charge) * (365.0 / days_between) * 100
                    inspection.annual_leak_rate = annual_loss

                    # Check compliance
                    inspection.compliant = annual_loss <= equipment.leak_rate_threshold

                    # Create alert if non-compliant
                    if not inspection.compliant:
                        alert = ComplianceAlert(
                            equipment_id=equipment.id,
                            alert_date=inspection.inspection_date,
                            alert_type='Leak Rate Exceeded',
                            severity='Critical',
                            title=f'Equipment {equipment.equipment_id}: Leak Rate Exceeds Threshold',
                            message=f'Annual leak rate of {annual_loss:.2f}% exceeds threshold of {equipment.leak_rate_threshold}%. Immediate repair required per 40 CFR 82.156.'
                        )
                        db.session.add(alert)

            # Set next inspection date
            inspection.next_inspection_date = inspection.inspection_date + timedelta(days=equipment.inspection_frequency)

            db.session.add(inspection)
            db.session.commit()

            flash('Leak inspection added successfully!', 'success')
            return redirect(url_for('equipment_detail', id=inspection.equipment_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding leak inspection: {str(e)}', 'error')

    equipment = Equipment.query.filter_by(status='Active').all()
    technicians = Technician.query.filter_by(status='Active').all()

    return render_template('leak_inspection_form.html', inspection=None, equipment=equipment, technicians=technicians)


# ============================================================================
# REFRIGERANT INVENTORY
# ============================================================================

@app.route('/inventory')
def inventory_list():
    """Refrigerant inventory"""
    inventory = RefrigerantInventory.query.all()

    # Get recent transactions
    transactions = RefrigerantTransaction.query.order_by(desc(RefrigerantTransaction.transaction_date)).limit(20).all()

    return render_template('inventory.html', inventory=inventory, transactions=transactions)


@app.route('/inventory/<int:id>/adjust', methods=['POST'])
def inventory_adjust(id):
    """Adjust inventory quantity"""
    try:
        inventory = RefrigerantInventory.query.get_or_404(id)
        adjustment = float(request.form['adjustment'])
        notes = request.form.get('notes', '')

        inventory.quantity_on_hand += adjustment

        # Create transaction record
        trans = RefrigerantTransaction(
            transaction_date=datetime.now().date(),
            transaction_type='Purchase' if adjustment > 0 else 'Disposed',
            refrigerant_type=inventory.refrigerant_type,
            refrigerant_name=inventory.refrigerant_name,
            quantity=abs(adjustment),
            notes=notes
        )
        db.session.add(trans)

        db.session.commit()

        flash(f'Inventory adjusted: {adjustment:+.2f} lbs of {inventory.refrigerant_name}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adjusting inventory: {str(e)}', 'error')

    return redirect(url_for('inventory_list'))


# ============================================================================
# COMPLIANCE ALERTS
# ============================================================================

@app.route('/alerts')
def alert_list():
    """List all compliance alerts"""
    alerts = ComplianceAlert.query.order_by(desc(ComplianceAlert.alert_date)).all()
    return render_template('alert_list.html', alerts=alerts)


@app.route('/alerts/<int:id>/resolve', methods=['POST'])
def alert_resolve(id):
    """Resolve an alert"""
    try:
        alert = ComplianceAlert.query.get_or_404(id)
        alert.status = 'Resolved'
        alert.resolved_date = datetime.now().date()
        alert.resolved_by = request.form.get('resolved_by', 'System')
        alert.resolution_notes = request.form.get('resolution_notes', '')

        db.session.commit()

        flash('Alert resolved successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error resolving alert: {str(e)}', 'error')

    return redirect(url_for('alert_list'))


# ============================================================================
# REPORTS
# ============================================================================

@app.route('/reports')
def reports():
    """Compliance reports page"""
    # Equipment summary
    equipment_stats = {
        'total': Equipment.query.count(),
        'active': Equipment.query.filter_by(status='Active').count(),
        'retired': Equipment.query.filter_by(status='Retired').count()
    }

    # Refrigerant usage summary
    refrigerant_usage = db.session.query(
        RefrigerantTransaction.refrigerant_name,
        func.sum(RefrigerantTransaction.quantity).label('total')
    ).filter(
        RefrigerantTransaction.transaction_type == 'Added'
    ).group_by(RefrigerantTransaction.refrigerant_name).all()

    # Compliance summary
    total_inspections = LeakInspection.query.count()
    non_compliant = LeakInspection.query.filter_by(compliant=False).count()

    return render_template('reports.html',
                           equipment_stats=equipment_stats,
                           refrigerant_usage=refrigerant_usage,
                           total_inspections=total_inspections,
                           non_compliant=non_compliant)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/equipment', methods=['GET'])
def api_equipment():
    """Get equipment list as JSON"""
    equipment = Equipment.query.all()
    return jsonify([{
        'id': e.id,
        'equipment_id': e.equipment_id,
        'name': e.name,
        'type': e.equipment_type,
        'refrigerant': e.refrigerant_name,
        'status': e.status
    } for e in equipment])


@app.route('/api/compliance-status/<int:equipment_id>', methods=['GET'])
def api_compliance_status(equipment_id):
    """Get compliance status for equipment"""
    equipment = Equipment.query.get_or_404(equipment_id)

    latest_inspection = LeakInspection.query.filter_by(equipment_id=equipment_id).order_by(desc(LeakInspection.inspection_date)).first()

    if latest_inspection:
        return jsonify({
            'equipment_id': equipment.equipment_id,
            'compliant': latest_inspection.compliant,
            'leak_rate': latest_inspection.annual_leak_rate,
            'threshold': equipment.leak_rate_threshold,
            'last_inspection': latest_inspection.inspection_date.isoformat(),
            'next_inspection': latest_inspection.next_inspection_date.isoformat() if latest_inspection.next_inspection_date else None
        })
    else:
        return jsonify({
            'equipment_id': equipment.equipment_id,
            'compliant': True,
            'message': 'No inspections recorded'
        })


# ============================================================================
# AI FEATURES
# ============================================================================

@app.route('/ai/leak-risks')
def ai_leak_risks():
    """AI-powered leak risk analysis page"""
    if not AI_AVAILABLE or not AIConfig.ENABLED:
        flash('AI features not enabled. Set AI_ENABLED=true and ANTHROPIC_API_KEY environment variables.', 'warning')
        return redirect(url_for('dashboard'))

    try:
        risks = get_equipment_at_risk(top_n=20)
        return render_template('ai_leak_risks.html', risks=risks, ai_enabled=AIConfig.ENABLED)
    except Exception as e:
        flash(f'Error getting AI predictions: {str(e)}', 'error')
        return redirect(url_for('dashboard'))


@app.route('/ai/natural-language-service', methods=['GET', 'POST'])
def ai_natural_language_service():
    """Natural language service entry page"""
    if not AI_AVAILABLE or not AIConfig.ENABLED:
        flash('AI features not enabled. Set AI_ENABLED=true and ANTHROPIC_API_KEY environment variables.', 'warning')
        return redirect(url_for('service_log_add'))

    if request.method == 'POST':
        try:
            description = request.form.get('description', '')
            if not description:
                flash('Please enter a service description', 'error')
                return render_template('ai_natural_language_service.html')

            # Parse the natural language description
            parsed = parse_service_nl(description)

            if 'error' in parsed:
                flash(f"AI Parsing Error: {parsed['error']}", 'error')
                return render_template('ai_natural_language_service.html',
                                     description=description,
                                     parsed=None)

            # Return the parsed data for review
            equipment = Equipment.query.filter_by(status='Active').all()
            technicians = Technician.query.filter_by(status='Active').all()

            return render_template('ai_natural_language_service.html',
                                 description=description,
                                 parsed=parsed,
                                 equipment=equipment,
                                 technicians=technicians)

        except Exception as e:
            flash(f'Error processing natural language: {str(e)}', 'error')
            return render_template('ai_natural_language_service.html')

    return render_template('ai_natural_language_service.html')


@app.route('/ai/chatbot', methods=['GET', 'POST'])
def ai_chatbot():
    """EPA Compliance chatbot page"""
    if not AI_AVAILABLE or not AIConfig.ENABLED:
        flash('AI features not enabled. Set AI_ENABLED=true and ANTHROPIC_API_KEY environment variables.', 'warning')
        return redirect(url_for('dashboard'))

    answer_data = None

    if request.method == 'POST':
        try:
            question = request.form.get('question', '')
            if not question:
                flash('Please enter a question', 'error')
                return render_template('ai_chatbot.html')

            # Get context from system
            context = {
                'total_equipment': Equipment.query.filter_by(status='Active').count(),
                'active_alerts': ComplianceAlert.query.filter_by(status='Active').count(),
                'recent_violations': LeakInspection.query.filter_by(compliant=False).count()
            }

            # Ask the chatbot
            answer_data = ask_compliance_question(question, context)

            return render_template('ai_chatbot.html',
                                 question=question,
                                 answer=answer_data)

        except Exception as e:
            flash(f'Error getting chatbot response: {str(e)}', 'error')
            return render_template('ai_chatbot.html')

    return render_template('ai_chatbot.html', answer=answer_data)


@app.route('/api/ai/parse-service', methods=['POST'])
def api_ai_parse_service():
    """API endpoint for natural language service parsing"""
    if not AI_AVAILABLE or not AIConfig.ENABLED:
        return jsonify({'error': 'AI features not enabled'}), 400

    try:
        data = request.get_json()
        description = data.get('description', '')

        if not description:
            return jsonify({'error': 'No description provided'}), 400

        parsed = parse_service_nl(description)
        return jsonify(parsed)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai/equipment-risk/<int:equipment_id>')
def api_ai_equipment_risk(equipment_id):
    """API endpoint for equipment risk analysis"""
    if not AI_AVAILABLE or not AIConfig.ENABLED:
        return jsonify({'error': 'AI features not enabled'}), 400

    try:
        from ai_features import LeakPredictionAI
        risk = LeakPredictionAI.analyze_equipment_risk(equipment_id)
        return jsonify(risk)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai/ask', methods=['POST'])
def api_ai_ask():
    """API endpoint for compliance chatbot"""
    if not AI_AVAILABLE or not AIConfig.ENABLED:
        return jsonify({'error': 'AI features not enabled'}), 400

    try:
        data = request.get_json()
        question = data.get('question', '')

        if not question:
            return jsonify({'error': 'No question provided'}), 400

        context = data.get('context', None)
        answer = ask_compliance_question(question, context)
        return jsonify(answer)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# DOCUMENT MANAGEMENT
# ============================================================================

@app.route('/documents')
def document_list():
    """List all documents"""
    documents = Document.query.filter_by(status='Active').order_by(desc(Document.uploaded_at)).all()
    return render_template('document_list.html', documents=documents, format_file_size=format_file_size, get_document_icon=get_document_icon)


@app.route('/documents/upload', methods=['GET', 'POST'])
def document_upload():
    """Upload a new document"""
    if request.method == 'POST':
        try:
            # Get uploaded file
            if 'file' not in request.files:
                flash('No file selected', 'error')
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(request.url)

            # Get form data
            document_type = request.form.get('document_type', 'Other')
            description = request.form.get('description', '')
            equipment_id = request.form.get('equipment_id')
            technician_id = request.form.get('technician_id')
            service_log_id = request.form.get('service_log_id')
            leak_inspection_id = request.form.get('leak_inspection_id')
            refrigerant_transaction_id = request.form.get('refrigerant_transaction_id')

            # Parse dates
            document_date = None
            if request.form.get('document_date'):
                document_date = datetime.strptime(request.form['document_date'], '%Y-%m-%d').date()

            expiration_date = None
            if request.form.get('expiration_date'):
                expiration_date = datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()

            uploaded_by = request.form.get('uploaded_by', 'System')

            # Determine subfolder based on entity
            subfolder = None
            if technician_id:
                subfolder = 'technicians'
            elif equipment_id:
                subfolder = 'equipment'

            # Create document record
            success, result = create_document_record(
                file=file,
                document_type=document_type,
                description=description,
                equipment_id=int(equipment_id) if equipment_id else None,
                technician_id=int(technician_id) if technician_id else None,
                service_log_id=int(service_log_id) if service_log_id else None,
                leak_inspection_id=int(leak_inspection_id) if leak_inspection_id else None,
                refrigerant_transaction_id=int(refrigerant_transaction_id) if refrigerant_transaction_id else None,
                document_date=document_date,
                expiration_date=expiration_date,
                uploaded_by=uploaded_by,
                subfolder=subfolder
            )

            if success:
                flash(f'Document uploaded successfully (ID: {result})!', 'success')

                # Redirect to appropriate detail page
                if equipment_id:
                    return redirect(url_for('equipment_detail', id=equipment_id))
                elif technician_id:
                    return redirect(url_for('technician_detail', id=technician_id))
                else:
                    return redirect(url_for('document_list'))
            else:
                flash(f'Error uploading document: {result}', 'error')
                return redirect(request.url)

        except Exception as e:
            flash(f'Error uploading document: {str(e)}', 'error')
            return redirect(request.url)

    # GET request - show upload form
    equipment = Equipment.query.filter_by(status='Active').all()
    technicians = Technician.query.filter_by(status='Active').all()
    service_logs = ServiceLog.query.order_by(desc(ServiceLog.service_date)).limit(20).all()
    leak_inspections = LeakInspection.query.order_by(desc(LeakInspection.inspection_date)).limit(20).all()

    return render_template('document_upload.html',
                         equipment=equipment,
                         technicians=technicians,
                         service_logs=service_logs,
                         leak_inspections=leak_inspections,
                         allowed_extensions=ALLOWED_EXTENSIONS)


@app.route('/documents/<int:id>/download')
def document_download(id):
    """Download a document"""
    document = Document.query.get_or_404(id)
    file_path = get_document_path(id)

    if not file_path or not os.path.exists(file_path):
        flash('Document file not found', 'error')
        return redirect(url_for('document_list'))

    return send_file(file_path, as_attachment=True, download_name=document.original_filename)


@app.route('/documents/<int:id>/view')
def document_view(id):
    """View a document (inline)"""
    document = Document.query.get_or_404(id)
    file_path = get_document_path(id)

    if not file_path or not os.path.exists(file_path):
        flash('Document file not found', 'error')
        return redirect(url_for('document_list'))

    # For PDFs and images, view inline
    if document.mime_type in ['application/pdf', 'image/jpeg', 'image/png', 'image/gif']:
        return send_file(file_path, mimetype=document.mime_type)
    else:
        # For other types, download
        return send_file(file_path, as_attachment=True, download_name=document.original_filename)


@app.route('/documents/<int:id>/delete', methods=['POST'])
def document_delete(id):
    """Delete a document"""
    try:
        success, message = delete_document(id)
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
    except Exception as e:
        flash(f'Error deleting document: {str(e)}', 'error')

    return redirect(request.referrer or url_for('document_list'))


@app.route('/technicians/<int:id>')
def technician_detail(id):
    """Technician detail page with documents and certifications"""
    tech = Technician.query.get_or_404(id)

    # Get documents
    documents = get_documents_by_entity(technician_id=id)

    # Get certifications
    certifications = TechnicianCertification.query.filter_by(technician_id=id).all()

    # Get service history
    services = ServiceLog.query.filter_by(technician_id=id).order_by(desc(ServiceLog.service_date)).limit(10).all()

    # Get inspections
    inspections = LeakInspection.query.filter_by(technician_id=id).order_by(desc(LeakInspection.inspection_date)).limit(10).all()

    return render_template('technician_detail.html',
                         technician=tech,
                         documents=documents,
                         certifications=certifications,
                         services=services,
                         inspections=inspections,
                         format_file_size=format_file_size,
                         get_document_icon=get_document_icon)


@app.route('/technicians/<int:id>/certifications/add', methods=['POST'])
def technician_certification_add(id):
    """Add a certification to a technician"""
    try:
        tech = Technician.query.get_or_404(id)

        cert = TechnicianCertification(
            technician_id=id,
            certification_type=request.form['certification_type'],
            certification_number=request.form.get('certification_number', ''),
            issuing_organization=request.form.get('issuing_organization', ''),
            issue_date=datetime.strptime(request.form['issue_date'], '%Y-%m-%d').date(),
            expiration_date=datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date() if request.form.get('expiration_date') else None,
            notes=request.form.get('notes', '')
        )

        db.session.add(cert)
        db.session.commit()

        # Handle file upload if present
        if 'certification_file' in request.files:
            file = request.files['certification_file']
            if file and file.filename != '':
                success, result = create_document_record(
                    file=file,
                    document_type='Certification',
                    description=f"{cert.certification_type} - {cert.certification_number}",
                    technician_id=id,
                    document_date=cert.issue_date,
                    expiration_date=cert.expiration_date,
                    uploaded_by=request.form.get('uploaded_by', 'System'),
                    subfolder='technicians'
                )

                if not success:
                    flash(f'Certification added but file upload failed: {result}', 'warning')
                else:
                    flash('Certification and document added successfully!', 'success')
            else:
                flash('Certification added successfully!', 'success')
        else:
            flash('Certification added successfully!', 'success')

        return redirect(url_for('technician_detail', id=id))

    except Exception as e:
        db.session.rollback()
        flash(f'Error adding certification: {str(e)}', 'error')
        return redirect(url_for('technician_detail', id=id))


# API endpoints for documents
@app.route('/api/documents/equipment/<int:equipment_id>')
def api_documents_equipment(equipment_id):
    """Get documents for equipment"""
    documents = get_documents_by_entity(equipment_id=equipment_id)
    return jsonify([{
        'id': d.id,
        'filename': d.original_filename,
        'type': d.document_type,
        'size': d.file_size,
        'uploaded_at': d.uploaded_at.isoformat()
    } for d in documents])


@app.route('/api/documents/technician/<int:technician_id>')
def api_documents_technician(technician_id):
    """Get documents for technician"""
    documents = get_documents_by_entity(technician_id=technician_id)
    return jsonify([{
        'id': d.id,
        'filename': d.original_filename,
        'type': d.document_type,
        'size': d.file_size,
        'uploaded_at': d.uploaded_at.isoformat()
    } for d in documents])


# ============================================================================
# SETTINGS
# ============================================================================

@app.route('/settings')
@login_required
def settings():
    """User settings and system preferences"""
    # Get technician statistics for managers/admins
    total_technicians = 0
    active_technicians = 0
    expiring_certs = 0

    if get_current_user() and get_current_user().role in ['compliance_manager', 'admin']:
        total_technicians = Technician.query.count()
        active_technicians = Technician.query.filter_by(status='Active').count()

        # Count certifications expiring in next 30 days
        thirty_days_from_now = datetime.now().date() + timedelta(days=30)
        expiring_certs = Technician.query.filter(
            Technician.expiration_date <= thirty_days_from_now,
            Technician.status == 'Active'
        ).count()

    return render_template('settings.html',
                         total_technicians=total_technicians,
                         active_technicians=active_technicians,
                         expiring_certs=expiring_certs)


@app.route('/settings/update', methods=['POST'])
@login_required
def settings_update():
    """Update user settings (placeholder for future implementation)"""
    flash('Settings update functionality coming soon!', 'info')
    return redirect(url_for('settings'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
