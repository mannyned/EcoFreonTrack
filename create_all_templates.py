"""Create all remaining HTML templates"""
import os

# All template files needed
TEMPLATES = {
    'service_log_list.html': '''{% extends "base.html" %}
{% block title %}Service Logs{% endblock %}
{% block content %}
<div class="d-flex justify-between align-center mb-3">
    <h1>Service & Repair Logs</h1>
    <a href="{{ url_for('service_log_add') }}" class="btn btn-primary">Add Service Log</a>
</div>
<div class="card">
    <table>
        <thead>
            <tr><th>Date</th><th>Equipment</th><th>Type</th><th>Technician</th><th>Added</th><th>Recovered</th><th>Leak</th></tr>
        </thead>
        <tbody>
            {% for log in logs %}
            <tr>
                <td>{{ log.service_date }}</td>
                <td><a href="{{ url_for('equipment_detail', id=log.equipment_id) }}">{{ log.equipment.equipment_id }}</a></td>
                <td>{{ log.service_type }}</td>
                <td>{{ log.technician.name }}</td>
                <td>{{ log.refrigerant_added }} lbs</td>
                <td>{{ log.refrigerant_recovered }} lbs</td>
                <td><span class="badge badge-{{ 'warning' if log.leak_found else 'success' }}">{{ 'Yes' if log.leak_found else 'No' }}</span></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'service_log_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>Add Service Log</h1>
<div class="card"><form method="POST">
<div class="form-row">
<div class="form-group"><label>Equipment *</label><select name="equipment_id" required>
<option value="">Select equipment...</option>
{% for e in equipment %}<option value="{{ e.id }}">{{ e.equipment_id }} - {{ e.name }}</option>{% endfor %}
</select></div>
<div class="form-group"><label>Technician *</label><select name="technician_id" required>
<option value="">Select technician...</option>
{% for t in technicians %}<option value="{{ t.id }}">{{ t.name }} ({{ t.certification_type }})</option>{% endfor %}
</select></div>
</div>
<div class="form-row">
<div class="form-group"><label>Service Date *</label><input type="date" name="service_date" required></div>
<div class="form-group"><label>Service Type *</label><select name="service_type" required>
<option value="Repair">Repair</option><option value="Maintenance">Maintenance</option>
<option value="Installation">Installation</option><option value="Disposal">Disposal</option>
</select></div>
</div>
<div class="form-row">
<div class="form-group"><label>Refrigerant Added (lbs)</label><input type="number" step="0.1" name="refrigerant_added" value="0"></div>
<div class="form-group"><label>Refrigerant Recovered (lbs)</label><input type="number" step="0.1" name="refrigerant_recovered" value="0"></div>
</div>
<div class="form-group"><label>Work Performed</label><textarea name="work_performed"></textarea></div>
<div class="form-group"><label><input type="checkbox" name="leak_found"> Leak Found</label></div>
<div class="form-group"><label><input type="checkbox" name="leak_repaired"> Leak Repaired</label></div>
<div class="form-group"><label>Leak Location</label><input type="text" name="leak_location"></div>
<div class="mt-3">
<button type="submit" class="btn btn-primary">Save Log</button>
<a href="{{ url_for('service_log_list') }}" class="btn btn-secondary">Cancel</a>
</div>
</form></div>
{% endblock %}''',

    'leak_inspection_list.html': '''{% extends "base.html" %}
{% block title %}Leak Inspections{% endblock %}
{% block content %}
<div class="d-flex justify-between align-center mb-3">
    <h1>Leak Inspections</h1>
    <a href="{{ url_for('leak_inspection_add') }}" class="btn btn-primary">Add Inspection</a>
</div>
<div class="card">
    <table>
        <thead>
            <tr><th>Date</th><th>Equipment</th><th>Type</th><th>Leak</th><th>Leak Rate</th><th>Compliant</th><th>Technician</th></tr>
        </thead>
        <tbody>
            {% for i in inspections %}
            <tr>
                <td>{{ i.inspection_date }}</td>
                <td><a href="{{ url_for('equipment_detail', id=i.equipment_id) }}">{{ i.equipment.equipment_id }}</a></td>
                <td>{{ i.inspection_type }}</td>
                <td><span class="badge badge-{{ 'danger' if i.leak_detected else 'success' }}">{{ 'Yes' if i.leak_detected else 'No' }}</span></td>
                <td>{{ i.annual_leak_rate|round(2) if i.annual_leak_rate else 'N/A' }}%</td>
                <td><span class="badge badge-{{ 'success' if i.compliant else 'danger' }}">{{ 'Yes' if i.compliant else 'No' }}</span></td>
                <td>{{ i.technician.name }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'leak_inspection_form.html': '''{% extends "base.html" %}
{% block content %}
<h1>Add Leak Inspection</h1>
<div class="card"><form method="POST">
<div class="form-row">
<div class="form-group"><label>Equipment *</label><select name="equipment_id" required>
<option value="">Select equipment...</option>
{% for e in equipment %}<option value="{{ e.id }}">{{ e.equipment_id }} - {{ e.name }}</option>{% endfor %}
</select></div>
<div class="form-group"><label>Technician *</label><select name="technician_id" required>
<option value="">Select technician...</option>
{% for t in technicians %}<option value="{{ t.id }}">{{ t.name }} ({{ t.certification_type }})</option>{% endfor %}
</select></div>
</div>
<div class="form-row">
<div class="form-group"><label>Inspection Date *</label><input type="date" name="inspection_date" required></div>
<div class="form-group"><label>Inspection Type *</label><select name="inspection_type" required>
<option value="Routine">Routine</option><option value="Post-Repair">Post-Repair</option>
<option value="Initial">Initial</option>
</select></div>
<div class="form-group"><label>Current Charge (lbs) *</label><input type="number" step="0.1" name="current_charge" required></div>
</div>
<div class="form-group"><label><input type="checkbox" name="leak_detected"> Leak Detected</label></div>
<div class="form-group"><label>Leak Location</label><input type="text" name="leak_location"></div>
<div class="form-group"><label>Leak Severity</label><select name="leak_severity">
<option value="">None</option><option value="Minor">Minor</option>
<option value="Major">Major</option><option value="Critical">Critical</option>
</select></div>
<div class="form-group"><label>Notes</label><textarea name="notes"></textarea></div>
<div class="mt-3">
<button type="submit" class="btn btn-primary">Save Inspection</button>
<a href="{{ url_for('leak_inspection_list') }}" class="btn btn-secondary">Cancel</a>
</div>
</form></div>
{% endblock %}''',

    'inventory.html': '''{% extends "base.html" %}
{% block title %}Refrigerant Inventory{% endblock %}
{% block content %}
<h1>Refrigerant Inventory</h1>
<div class="card">
    <h2>Current Stock</h2>
    <table>
        <thead>
            <tr><th>Refrigerant</th><th>Type</th><th>On Hand</th><th>Recovered</th><th>Reorder Level</th><th>Status</th><th>Action</th></tr>
        </thead>
        <tbody>
            {% for item in inventory %}
            <tr>
                <td><strong>{{ item.refrigerant_name }}</strong></td>
                <td>{{ item.refrigerant_type }}</td>
                <td>{{ item.quantity_on_hand }} lbs</td>
                <td>{{ item.quantity_recovered }} lbs</td>
                <td>{{ item.reorder_level }} lbs</td>
                <td><span class="badge badge-{{ 'success' if item.quantity_on_hand >= item.reorder_level else 'warning' }}">
                    {{ 'OK' if item.quantity_on_hand >= item.reorder_level else 'Low' }}</span></td>
                <td>
                    <form method="POST" action="{{ url_for('inventory_adjust', id=item.id) }}" class="d-flex gap-1">
                        <input type="number" step="0.1" name="adjustment" placeholder="±" style="width:80px" required>
                        <button type="submit" class="btn btn-sm btn-primary">Adjust</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
<div class="card">
    <h2>Recent Transactions</h2>
    <table>
        <thead>
            <tr><th>Date</th><th>Type</th><th>Refrigerant</th><th>Quantity</th><th>Equipment</th></tr>
        </thead>
        <tbody>
            {% for t in transactions %}
            <tr>
                <td>{{ t.transaction_date }}</td>
                <td><span class="badge badge-{{ 'success' if t.transaction_type == 'Purchase' else 'info' }}">{{ t.transaction_type }}</span></td>
                <td>{{ t.refrigerant_name }}</td>
                <td>{{ t.quantity }} lbs</td>
                <td>{{ t.equipment.equipment_id if t.equipment else 'N/A' }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'alert_list.html': '''{% extends "base.html" %}
{% block title %}Compliance Alerts{% endblock %}
{% block content %}
<h1>Compliance Alerts</h1>
<div class="card">
    <table>
        <thead>
            <tr><th>Date</th><th>Type</th><th>Severity</th><th>Title</th><th>Status</th><th>Action</th></tr>
        </thead>
        <tbody>
            {% for alert in alerts %}
            <tr>
                <td>{{ alert.alert_date }}</td>
                <td>{{ alert.alert_type }}</td>
                <td><span class="badge badge-{{ 'danger' if alert.severity == 'Critical' else 'warning' }}">{{ alert.severity }}</span></td>
                <td>{{ alert.title }}</td>
                <td><span class="badge badge-{{ 'secondary' if alert.status == 'Resolved' else 'danger' }}">{{ alert.status }}</span></td>
                <td>
                    {% if alert.status == 'Active' %}
                    <form method="POST" action="{{ url_for('alert_resolve', id=alert.id) }}">
                        <button type="submit" class="btn btn-sm btn-success">Resolve</button>
                    </form>
                    {% else %}
                    <span>Resolved</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'reports.html': '''{% extends "base.html" %}
{% block title %}Reports{% endblock %}
{% block content %}
<h1>Compliance Reports</h1>
<div class="stats-grid">
    <div class="stat-card"><h3>Total Equipment</h3><div class="stat-value">{{ equipment_stats.total }}</div></div>
    <div class="stat-card success"><h3>Active Equipment</h3><div class="stat-value">{{ equipment_stats.active }}</div></div>
    <div class="stat-card"><h3>Total Inspections</h3><div class="stat-value">{{ total_inspections }}</div></div>
    <div class="stat-card {% if non_compliant > 0 %}danger{% else %}success{% endif %}"><h3>Non-Compliant</h3><div class="stat-value">{{ non_compliant }}</div></div>
</div>
<div class="card">
    <h2>Refrigerant Usage</h2>
    <table>
        <thead><tr><th>Refrigerant</th><th>Total Used (lbs)</th></tr></thead>
        <tbody>
            {% for usage in refrigerant_usage %}
            <tr><td>{{ usage[0] }}</td><td>{{ usage[1]|round(2) }} lbs</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'equipment_form.html': '''{% extends "base.html" %}
{% block title %}{% if equipment %}Edit{% else %}Add{% endif %} Equipment{% endblock %}
{% block content %}
<h1>{% if equipment %}Edit{% else %}Add New{% endif %} Equipment</h1>
<div class="card">
    <form method="POST">
        <div class="form-row">
            <div class="form-group">
                <label>Equipment ID *</label>
                <input type="text" name="equipment_id" value="{{ equipment.equipment_id if equipment else '' }}" required>
            </div>
            <div class="form-group">
                <label>Name *</label>
                <input type="text" name="name" value="{{ equipment.name if equipment else '' }}" required>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Type *</label>
                <select name="equipment_type" required>
                    <option value="">Select type...</option>
                    <option value="Chiller" {% if equipment and equipment.equipment_type == 'Chiller' %}selected{% endif %}>Chiller</option>
                    <option value="Air Conditioner" {% if equipment and equipment.equipment_type == 'Air Conditioner' %}selected{% endif %}>Air Conditioner</option>
                    <option value="Freezer" {% if equipment and equipment.equipment_type == 'Freezer' %}selected{% endif %}>Freezer</option>
                    <option value="Refrigerator" {% if equipment and equipment.equipment_type == 'Refrigerator' %}selected{% endif %}>Refrigerator</option>
                </select>
            </div>
            <div class="form-group">
                <label>Location</label>
                <input type="text" name="location" value="{{ equipment.location if equipment else '' }}">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Refrigerant Type *</label>
                <select name="refrigerant_type" required>
                    <option value="CFC" {% if equipment and equipment.refrigerant_type == 'CFC' %}selected{% endif %}>CFC</option>
                    <option value="HCFC" {% if equipment and equipment.refrigerant_type == 'HCFC' %}selected{% endif %}>HCFC</option>
                    <option value="HFC" {% if equipment and equipment.refrigerant_type == 'HFC' %}selected{% endif %}>HFC</option>
                </select>
            </div>
            <div class="form-group">
                <label>Refrigerant Name *</label>
                <select name="refrigerant_name" required>
                    <option value="R-12" {% if equipment and equipment.refrigerant_name == 'R-12' %}selected{% endif %}>R-12</option>
                    <option value="R-22" {% if equipment and equipment.refrigerant_name == 'R-22' %}selected{% endif %}>R-22</option>
                    <option value="R-134a" {% if equipment and equipment.refrigerant_name == 'R-134a' %}selected{% endif %}>R-134a</option>
                    <option value="R-410A" {% if equipment and equipment.refrigerant_name == 'R-410A' %}selected{% endif %}>R-410A</option>
                </select>
            </div>
            <div class="form-group">
                <label>Full Charge (lbs) *</label>
                <input type="number" step="0.1" name="full_charge" value="{{ equipment.full_charge if equipment else '' }}" required>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Install Date</label>
                <input type="date" name="install_date" value="{{ equipment.install_date if equipment else '' }}">
            </div>
            <div class="form-group">
                <label>Leak Rate Threshold (%)</label>
                <input type="number" step="0.1" name="leak_rate_threshold" value="{{ equipment.leak_rate_threshold if equipment else '10.0' }}">
            </div>
            {% if equipment %}
            <div class="form-group">
                <label>Status</label>
                <select name="status">
                    <option value="Active" {% if equipment.status == 'Active' %}selected{% endif %}>Active</option>
                    <option value="Retired" {% if equipment.status == 'Retired' %}selected{% endif %}>Retired</option>
                </select>
            </div>
            {% endif %}
        </div>
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Save Equipment</button>
            <a href="{{ url_for('equipment_list') }}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}''',

    'technician_list.html': '''{% extends "base.html" %}
{% block title %}Technicians{% endblock %}
{% block content %}
<div class="d-flex justify-between align-center mb-3">
    <h1>EPA 608 Certified Technicians</h1>
    <a href="{{ url_for('technician_add') }}" class="btn btn-primary">Add Technician</a>
</div>
<div class="card">
    <table>
        <thead>
            <tr><th>Name</th><th>Cert Number</th><th>Type</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody>
            {% for tech in technicians %}
            <tr>
                <td><strong>{{ tech.name }}</strong></td>
                <td>{{ tech.certification_number }}</td>
                <td><span class="badge badge-info">{{ tech.certification_type }}</span></td>
                <td><span class="badge badge-{{ 'success' if tech.status == 'Active' else 'secondary' }}">{{ tech.status }}</span></td>
                <td><a href="{{ url_for('technician_edit', id=tech.id) }}" class="btn btn-sm btn-secondary">Edit</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'technician_form.html': '''{% extends "base.html" %}
{% block title %}{% if technician %}Edit{% else %}Add{% endif %} Technician{% endblock %}
{% block content %}
<h1>{% if technician %}Edit{% else %}Add New{% endif %} Technician</h1>
<div class="card">
    <form method="POST">
        <div class="form-row">
            <div class="form-group">
                <label>Name *</label>
                <input type="text" name="name" value="{{ technician.name if technician else '' }}" required>
            </div>
            <div class="form-group">
                <label>Certification Number *</label>
                <input type="text" name="certification_number" value="{{ technician.certification_number if technician else '' }}" required>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Certification Type *</label>
                <select name="certification_type" required>
                    <option value="Type I" {% if technician and technician.certification_type == 'Type I' %}selected{% endif %}>Type I</option>
                    <option value="Type II" {% if technician and technician.certification_type == 'Type II' %}selected{% endif %}>Type II</option>
                    <option value="Type III" {% if technician and technician.certification_type == 'Type III' %}selected{% endif %}>Type III</option>
                    <option value="Universal" {% if technician and technician.certification_type == 'Universal' %}selected{% endif %}>Universal</option>
                </select>
            </div>
            <div class="form-group">
                <label>Certification Date *</label>
                <input type="date" name="certification_date" value="{{ technician.certification_date if technician else '' }}" required>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" value="{{ technician.email if technician else '' }}">
            </div>
            <div class="form-group">
                <label>Phone</label>
                <input type="tel" name="phone" value="{{ technician.phone if technician else '' }}">
            </div>
            {% if technician %}
            <div class="form-group">
                <label>Status</label>
                <select name="status">
                    <option value="Active" {% if technician.status == 'Active' %}selected{% endif %}>Active</option>
                    <option value="Inactive" {% if technician.status == 'Inactive' %}selected{% endif %}>Inactive</option>
                </select>
            </div>
            {% endif %}
        </div>
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Save Technician</button>
            <a href="{{ url_for('technician_list') }}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}''',
}

# Create all templates
for filename, content in TEMPLATES.items():
    filepath = os.path.join('templates', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {filepath}')

print(f'\nSuccessfully created {len(TEMPLATES)} template files!')
