"""
Database models for EPA Section 608 Refrigerant Tracking & Compliance
Manages equipment, refrigerants, technicians, and compliance records per 40 CFR Part 82
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Equipment(db.Model):
    """Equipment containing regulated refrigerants"""
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
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

    # Status
    status = db.Column(db.String(50), default='Active')  # Active, Inactive, Expired

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    service_logs = db.relationship('ServiceLog', backref='technician', lazy=True)
    leak_inspections = db.relationship('LeakInspection', backref='technician', lazy=True)

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
