"""
Database models for EPA Section 608 Refrigerant Tracking & Compliance
Manages equipment, refrigerants, technicians, and compliance records per 40 CFR Part 82
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Equipment(db.Model):
    """Equipment containing regulated refrigerants"""
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    equipment_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    equipment_type = db.Column(db.String(100), nullable=False)  # Chiller, AC, Freezer, etc.
    location = db.Column(db.String(200))
    manufacturer = db.Column(db.String(100))
    model_number = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))

    # Refrigerant information
    refrigerant_type = db.Column(db.String(50), nullable=False)  # CFC, HCFC, HFC
    refrigerant_name = db.Column(db.String(50), nullable=False)  # R-22, R-410A, etc.
    full_charge = db.Column(db.Float, nullable=False)  # pounds

    # Status
    status = db.Column(db.String(50), default='Active')  # Active, Retired, Disposed
    install_date = db.Column(db.Date)
    retire_date = db.Column(db.Date)

    # Compliance thresholds
    leak_rate_threshold = db.Column(db.Float, default=10.0)  # percentage per year
    inspection_frequency = db.Column(db.Integer, default=30)  # days

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    service_logs = db.relationship('ServiceLog', backref='equipment', lazy=True, cascade='all, delete-orphan')
    leak_inspections = db.relationship('LeakInspection', backref='equipment', lazy=True, cascade='all, delete-orphan')
    refrigerant_transactions = db.relationship('RefrigerantTransaction', backref='equipment', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='equipment', lazy=True, foreign_keys='Document.equipment_id')

    def __repr__(self):
        return f'<Equipment {self.equipment_id}: {self.name}>'


class Technician(db.Model):
    """EPA Section 608 Certified Technicians"""
    __tablename__ = 'technician'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    certification_number = db.Column(db.String(100), unique=True, nullable=False)
    certification_type = db.Column(db.String(50), nullable=False)  # Type I, II, III, Universal
    certification_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date)

    # Contact info
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    company = db.Column(db.String(200))

    # Certificate file
    certificate_filename = db.Column(db.String(500))  # Stores the uploaded certificate filename

    # Status
    status = db.Column(db.String(50), default='Active')  # Active, Inactive, Expired

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    service_logs = db.relationship('ServiceLog', backref='technician', lazy=True)
    leak_inspections = db.relationship('LeakInspection', backref='technician', lazy=True)
    documents = db.relationship('Document', backref='technician', lazy=True, foreign_keys='Document.technician_id')
    certifications = db.relationship('TechnicianCertification', backref='technician', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Technician {self.name}: {self.certification_type}>'


class ServiceLog(db.Model):
    """Service and repair logs per 40 CFR 82.166"""
    __tablename__ = 'service_log'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=False)

    service_date = db.Column(db.Date, nullable=False)
    service_type = db.Column(db.String(100), nullable=False)  # Repair, Maintenance, Installation, Disposal

    # Refrigerant handling
    refrigerant_added = db.Column(db.Float, default=0.0)  # pounds
    refrigerant_recovered = db.Column(db.Float, default=0.0)  # pounds

    # Service details
    work_performed = db.Column(db.Text)
    leak_found = db.Column(db.Boolean, default=False)
    leak_repaired = db.Column(db.Boolean, default=False)
    leak_location = db.Column(db.String(200))

    # Follow-up
    follow_up_required = db.Column(db.Boolean, default=False)
    follow_up_date = db.Column(db.Date)
    follow_up_notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = db.relationship('Document', backref='service_log', lazy=True, foreign_keys='Document.service_log_id')

    def __repr__(self):
        return f'<ServiceLog {self.id}: {self.service_type} on {self.service_date}>'


class LeakInspection(db.Model):
    """Leak inspection records per 40 CFR 82.157"""
    __tablename__ = 'leak_inspection'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=False)

    inspection_date = db.Column(db.Date, nullable=False)
    inspection_type = db.Column(db.String(50), nullable=False)  # Routine, Post-Repair, Initial

    # Inspection results
    leak_detected = db.Column(db.Boolean, default=False)
    leak_location = db.Column(db.String(200))
    leak_severity = db.Column(db.String(50))  # Minor, Major, Critical

    # Current charge
    current_charge = db.Column(db.Float)  # pounds
    charge_deficit = db.Column(db.Float)  # pounds lost since last inspection

    # Calculated leak rate
    annual_leak_rate = db.Column(db.Float)  # percentage per year
    compliant = db.Column(db.Boolean, default=True)

    # Inspector notes
    notes = db.Column(db.Text)

    # Next inspection
    next_inspection_date = db.Column(db.Date)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = db.relationship('Document', backref='leak_inspection', lazy=True, foreign_keys='Document.leak_inspection_id')

    def __repr__(self):
        return f'<LeakInspection {self.id}: Equipment {self.equipment_id} on {self.inspection_date}>'


class RefrigerantTransaction(db.Model):
    """Refrigerant purchase, usage, recovery, and disposal records"""
    __tablename__ = 'refrigerant_transaction'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)

    transaction_date = db.Column(db.Date, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # Purchase, Added, Recovered, Disposed

    # Refrigerant details
    refrigerant_type = db.Column(db.String(50), nullable=False)  # CFC, HCFC, HFC
    refrigerant_name = db.Column(db.String(50), nullable=False)  # R-22, R-410A, etc.
    quantity = db.Column(db.Float, nullable=False)  # pounds

    # Purchase/disposal info
    supplier_name = db.Column(db.String(200))
    invoice_number = db.Column(db.String(100))
    cost = db.Column(db.Float)

    # Recovery/disposal
    cylinder_number = db.Column(db.String(100))
    disposal_method = db.Column(db.String(100))  # Recycled, Reclaimed, Destroyed
    disposal_facility = db.Column(db.String(200))

    # Notes
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = db.relationship('Document', backref='refrigerant_transaction', lazy=True, foreign_keys='Document.refrigerant_transaction_id')

    def __repr__(self):
        return f'<RefrigerantTransaction {self.id}: {self.transaction_type} - {self.quantity} lbs {self.refrigerant_name}>'


class ComplianceAlert(db.Model):
    """Compliance alerts and notifications"""
    __tablename__ = 'compliance_alert'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=True)

    alert_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    alert_type = db.Column(db.String(100), nullable=False)  # Leak Rate, Inspection Due, Cert Expiring, etc.
    severity = db.Column(db.String(50), nullable=False)  # Info, Warning, Critical

    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # Status
    status = db.Column(db.String(50), default='Active')  # Active, Resolved, Dismissed
    resolved_date = db.Column(db.Date)
    resolved_by = db.Column(db.String(200))
    resolution_notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ComplianceAlert {self.id}: {self.alert_type} - {self.severity}>'


class RefrigerantInventory(db.Model):
    """Current refrigerant inventory tracking"""
    __tablename__ = 'refrigerant_inventory'

    id = db.Column(db.Integer, primary_key=True)
    refrigerant_type = db.Column(db.String(50), nullable=False)  # CFC, HCFC, HFC
    refrigerant_name = db.Column(db.String(50), nullable=False, unique=True)  # R-22, R-410A, etc.

    # Inventory
    quantity_on_hand = db.Column(db.Float, default=0.0)  # pounds
    quantity_recovered = db.Column(db.Float, default=0.0)  # pounds awaiting disposal

    # Thresholds
    reorder_level = db.Column(db.Float, default=50.0)  # pounds
    below_reorder = db.Column(db.Boolean, default=False)

    # Timestamps
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<RefrigerantInventory {self.refrigerant_name}: {self.quantity_on_hand} lbs>'


class Document(db.Model):
    """Document attachments for equipment, service logs, inspections, and certifications"""
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)

    # Document metadata
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)  # Relative path in uploads folder
    file_size = db.Column(db.Integer)  # bytes
    mime_type = db.Column(db.String(100))  # application/pdf, image/jpeg, etc.

    # Document classification
    document_type = db.Column(db.String(100), nullable=False)  # Certification, Invoice, Photo, Report, Manual, etc.
    description = db.Column(db.Text)

    # Relationships - Link to various entities (nullable for flexibility)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=True)
    service_log_id = db.Column(db.Integer, db.ForeignKey('service_log.id'), nullable=True)
    leak_inspection_id = db.Column(db.Integer, db.ForeignKey('leak_inspection.id'), nullable=True)
    refrigerant_transaction_id = db.Column(db.Integer, db.ForeignKey('refrigerant_transaction.id'), nullable=True)

    # Document dates
    document_date = db.Column(db.Date)  # Date on the actual document (e.g., cert issue date)
    expiration_date = db.Column(db.Date)  # For certifications, warranties, etc.

    # Upload info
    uploaded_by = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Status
    status = db.Column(db.String(50), default='Active')  # Active, Archived, Deleted

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Document {self.id}: {self.original_filename} ({self.document_type})>'


class TechnicianCertification(db.Model):
    """EPA Section 608 and other certifications for technicians with document tracking"""
    __tablename__ = 'technician_certification'

    id = db.Column(db.Integer, primary_key=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=False)

    # Certification details
    certification_type = db.Column(db.String(100), nullable=False)  # EPA 608 Type I/II/III/Universal, NATE, etc.
    certification_number = db.Column(db.String(100))
    issuing_organization = db.Column(db.String(200))  # EPA, NATE, HVAC Excellence, etc.

    # Dates
    issue_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date)  # Some certs don't expire

    # Status
    status = db.Column(db.String(50), default='Active')  # Active, Expired, Revoked

    # Notes
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = db.relationship('Document',
                                primaryjoin="and_(Document.technician_id==TechnicianCertification.technician_id, "
                                           "Document.document_type=='Certification')",
                                foreign_keys='Document.technician_id',
                                viewonly=True)

    def __repr__(self):
        return f'<TechnicianCertification {self.certification_type}: {self.certification_number}>'


class User(db.Model):
    """User accounts with role-based access control"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # User profile
    full_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50))

    # Company information
    company_name = db.Column(db.String(200))
    street_address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))

    # Role: technician, compliance_manager, admin, auditor
    role = db.Column(db.String(50), nullable=False, default='technician')

    # Link to technician record if user is a technician
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=True)

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    technician = db.relationship('Technician', backref='user_account', foreign_keys=[technician_id])

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password"""
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        """Check if user has a specific permission based on their role"""
        permissions = {
            'technician': [
                'add_service_log',
                'add_refrigerant_transaction',
                'add_leak_inspection',
                'upload_certificate',
                'view_own_logs',
                'scan_equipment',
                'view_equipment',
            ],
            'compliance_manager': [
                'view_dashboard',
                'approve_logs',
                'generate_reports',
                'view_all_logs',
                'view_compliance_alerts',
                'resolve_alerts',
                'manage_equipment',
                'view_equipment',
                'add_equipment',
                'edit_equipment',
                'view_analytics',
                'export_reports',
            ],
            'admin': [
                'manage_users',
                'manage_sites',
                'manage_equipment',
                'manage_technicians',
                'manage_billing',
                'view_dashboard',
                'approve_logs',
                'generate_reports',
                'add_service_log',
                'add_refrigerant_transaction',
                'add_leak_inspection',
                'upload_certificate',
                'view_all_logs',
                'view_compliance_alerts',
                'resolve_alerts',
                'add_equipment',
                'edit_equipment',
                'delete_equipment',
                'scan_equipment',
                'view_equipment',
                'view_analytics',
                'export_reports',
                'system_settings',
            ],
            'auditor': [
                'view_dashboard',
                'view_all_logs',
                'view_compliance_alerts',
                'view_equipment',
                'generate_reports',
                'export_reports',
                'view_analytics',
            ]
        }
        return permission in permissions.get(self.role, [])

    def __repr__(self):
        return f'<User {self.username}: {self.role}>'


class Customer(db.Model):
    """Customer/Company information with contact details and equipment tracking"""
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)

    # Company information
    company_name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(200))

    # Contact details
    phone = db.Column(db.String(50))
    email = db.Column(db.String(200))

    # Location
    location = db.Column(db.String(300))
    street_address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))

    # Additional information
    notes = db.Column(db.Text)

    # Status
    status = db.Column(db.String(50), default='Active')  # Active, Inactive

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships - Link equipment to customers
    equipment = db.relationship('Equipment', backref='customer', lazy=True, foreign_keys='Equipment.customer_id')

    def __repr__(self):
        return f'<Customer {self.company_name}>'
