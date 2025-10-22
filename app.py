"""
EPA Section 608 Refrigerant Tracking & Compliance System
Managed under 40 CFR Part 82
Flask web application for tracking refrigerant usage, leakage, recovery, and compliance
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import db, Equipment, Technician, ServiceLog, LeakInspection, RefrigerantTransaction, ComplianceAlert, RefrigerantInventory
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'epa-608-compliance-tracker-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epa608_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
# DASHBOARD & HOME
# ============================================================================

@app.route('/')
def index():
    """Main dashboard"""
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

    return render_template('dashboard.html',
                           total_equipment=total_equipment,
                           total_technicians=total_technicians,
                           active_alerts=active_alerts,
                           recent_services=recent_services,
                           upcoming_inspections=upcoming_inspections,
                           alerts=alerts,
                           low_inventory=low_inventory)


# ============================================================================
# EQUIPMENT MANAGEMENT
# ============================================================================

@app.route('/equipment')
def equipment_list():
    """List all equipment"""
    equipment = Equipment.query.all()
    return render_template('equipment_list.html', equipment=equipment)


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
                           annual_leak_rate=annual_leak_rate,
                           compliant=compliant)


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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
