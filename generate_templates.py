"""
Generate all HTML templates for EPA 608 Refrigerant Tracker
Run this script once to create all template files
"""
import os

# Template content dictionary
templates = {
    'dashboard.html': '''{% extends "base.html" %}

{% block title %}Dashboard - EPA 608 Tracker{% endblock %}

{% block content %}
<h1>Compliance Dashboard</h1>

<div class="stats-grid">
    <div class="stat-card success">
        <h3>Active Equipment</h3>
        <div class="stat-value">{{ total_equipment }}</div>
    </div>

    <div class="stat-card success">
        <h3>Certified Technicians</h3>
        <div class="stat-value">{{ total_technicians }}</div>
    </div>

    <div class="stat-card {% if active_alerts > 0 %}danger{% else %}success{% endif %}">
        <h3>Active Alerts</h3>
        <div class="stat-value">{{ active_alerts }}</div>
    </div>

    <div class="stat-card {% if low_inventory|length > 0 %}warning{% else %}success{% endif %}">
        <h3>Low Inventory Items</h3>
        <div class="stat-value">{{ low_inventory|length }}</div>
    </div>
</div>

{% if active_alerts > 0 %}
<div class="card">
    <h2>Active Compliance Alerts</h2>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Severity</th>
                <th>Title</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for alert in alerts[:5] %}
            <tr>
                <td>{{ alert.alert_date }}</td>
                <td>{{ alert.alert_type }}</td>
                <td><span class="badge badge-{{ 'danger' if alert.severity == 'Critical' else 'warning' }}">{{ alert.severity }}</span></td>
                <td>{{ alert.title }}</td>
                <td><a href="{{ url_for('alert_list') }}" class="btn btn-sm btn-primary">View</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <div class="mt-2 text-right">
        <a href="{{ url_for('alert_list') }}" class="btn btn-primary">View All Alerts</a>
    </div>
</div>
{% endif %}

{% if upcoming_inspections|length > 0 %}
<div class="card">
    <h2>Upcoming Inspections (Next 7 Days)</h2>
    <table>
        <thead>
            <tr>
                <th>Equipment ID</th>
                <th>Equipment Name</th>
                <th>Next Inspection Date</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for item in upcoming_inspections %}
            <tr>
                <td>{{ item.equipment.equipment_id }}</td>
                <td>{{ item.equipment.name }}</td>
                <td>{{ item.next_date }}</td>
                <td><a href="{{ url_for('equipment_detail', id=item.equipment.id) }}" class="btn btn-sm btn-primary">View</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endif %}

<div class="card">
    <h2>Recent Service Activity</h2>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Equipment</th>
                <th>Type</th>
                <th>Technician</th>
                <th>Refrigerant Added</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for service in recent_services %}
            <tr>
                <td>{{ service.service_date }}</td>
                <td>{{ service.equipment.equipment_id }}</td>
                <td>{{ service.service_type }}</td>
                <td>{{ service.technician.name }}</td>
                <td>{{ service.refrigerant_added }} lbs</td>
                <td><a href="{{ url_for('equipment_detail', id=service.equipment_id) }}" class="btn btn-sm btn-primary">View</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if low_inventory|length > 0 %}
<div class="card">
    <h2>Low Inventory Warnings</h2>
    <table>
        <thead>
            <tr>
                <th>Refrigerant</th>
                <th>Type</th>
                <th>On Hand</th>
                <th>Reorder Level</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for item in low_inventory %}
            <tr>
                <td>{{ item.refrigerant_name }}</td>
                <td>{{ item.refrigerant_type }}</td>
                <td>{{ item.quantity_on_hand }} lbs</td>
                <td>{{ item.reorder_level }} lbs</td>
                <td><span class="badge badge-warning">Below Reorder Level</span></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <div class="mt-2 text-right">
        <a href="{{ url_for('inventory_list') }}" class="btn btn-primary">Manage Inventory</a>
    </div>
</div>
{% endif %}
{% endblock %}
''',

    'equipment_list.html': '''{% extends "base.html" %}

{% block title %}Equipment - EPA 608 Tracker{% endblock %}

{% block content %}
<div class="d-flex justify-between align-center mb-3">
    <h1>Equipment Inventory</h1>
    <a href="{{ url_for('equipment_add') }}" class="btn btn-primary">Add New Equipment</a>
</div>

<div class="card">
    <table>
        <thead>
            <tr>
                <th>Equipment ID</th>
                <th>Name</th>
                <th>Type</th>
                <th>Location</th>
                <th>Refrigerant</th>
                <th>Full Charge</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for equip in equipment %}
            <tr>
                <td><strong>{{ equip.equipment_id }}</strong></td>
                <td>{{ equip.name }}</td>
                <td>{{ equip.equipment_type }}</td>
                <td>{{ equip.location or 'N/A' }}</td>
                <td>{{ equip.refrigerant_name }} ({{ equip.refrigerant_type }})</td>
                <td>{{ equip.full_charge }} lbs</td>
                <td><span class="badge badge-{{ 'success' if equip.status == 'Active' else 'secondary' }}">{{ equip.status }}</span></td>
                <td>
                    <a href="{{ url_for('equipment_detail', id=equip.id) }}" class="btn btn-sm btn-primary">View</a>
                    <a href="{{ url_for('equipment_edit', id=equip.id) }}" class="btn btn-sm btn-secondary">Edit</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
''',

    'equipment_detail.html': '''{% extends "base.html" %}

{% block title %}{{ equipment.equipment_id }} - Equipment Detail{% endblock %}

{% block content %}
<div class="d-flex justify-between align-center mb-3">
    <h1>Equipment: {{ equipment.equipment_id }}</h1>
    <div>
        <a href="{{ url_for('equipment_edit', id=equipment.id) }}" class="btn btn-secondary">Edit Equipment</a>
        <a href="{{ url_for('equipment_list') }}" class="btn btn-primary">Back to List</a>
    </div>
</div>

<div class="compliance-status {% if compliant %}compliant{% else %}non-compliant{% endif %}">
    <div class="status-icon">{% if compliant %}✓{% else %}⚠{% endif %}</div>
    <div class="status-text">
        <h3>{% if compliant %}Compliant{% else %}Non-Compliant{% endif %}</h3>
        <p>Annual Leak Rate: {{ annual_leak_rate|round(2) }}% (Threshold: {{ equipment.leak_rate_threshold }}%)</p>
    </div>
</div>

<div class="card">
    <h2>Equipment Information</h2>
    <div class="form-row">
        <div><strong>Equipment ID:</strong> {{ equipment.equipment_id }}</div>
        <div><strong>Name:</strong> {{ equipment.name }}</div>
        <div><strong>Type:</strong> {{ equipment.equipment_type }}</div>
        <div><strong>Location:</strong> {{ equipment.location or 'N/A' }}</div>
        <div><strong>Manufacturer:</strong> {{ equipment.manufacturer or 'N/A' }}</div>
        <div><strong>Model:</strong> {{ equipment.model_number or 'N/A' }}</div>
        <div><strong>Serial Number:</strong> {{ equipment.serial_number or 'N/A' }}</div>
        <div><strong>Status:</strong> <span class="badge badge-{{ 'success' if equipment.status == 'Active' else 'secondary' }}">{{ equipment.status }}</span></div>
    </div>
</div>

<div class="card">
    <h2>Refrigerant Information</h2>
    <div class="form-row">
        <div><strong>Refrigerant Type:</strong> {{ equipment.refrigerant_type }}</div>
        <div><strong>Refrigerant Name:</strong> {{ equipment.refrigerant_name }}</div>
        <div><strong>Full Charge:</strong> {{ equipment.full_charge }} lbs</div>
        <div><strong>Leak Rate Threshold:</strong> {{ equipment.leak_rate_threshold }}%</div>
        <div><strong>Inspection Frequency:</strong> Every {{ equipment.inspection_frequency }} days</div>
    </div>
</div>

<div class="card">
    <div class="d-flex justify-between align-center mb-2">
        <h2>Leak Inspections</h2>
        <a href="{{ url_for('leak_inspection_add') }}" class="btn btn-success">Add Inspection</a>
    </div>
    {% if inspections %}
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Leak Detected</th>
                <th>Current Charge</th>
                <th>Leak Rate</th>
                <th>Compliant</th>
                <th>Technician</th>
            </tr>
        </thead>
        <tbody>
            {% for inspection in inspections %}
            <tr>
                <td>{{ inspection.inspection_date }}</td>
                <td>{{ inspection.inspection_type }}</td>
                <td><span class="badge badge-{{ 'danger' if inspection.leak_detected else 'success' }}">{{ 'Yes' if inspection.leak_detected else 'No' }}</span></td>
                <td>{{ inspection.current_charge or 'N/A' }} lbs</td>
                <td>{{ inspection.annual_leak_rate|round(2) if inspection.annual_leak_rate else 'N/A' }}%</td>
                <td><span class="badge badge-{{ 'success' if inspection.compliant else 'danger' }}">{{ 'Yes' if inspection.compliant else 'No' }}</span></td>
                <td>{{ inspection.technician.name }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No inspections recorded.</p>
    {% endif %}
</div>

<div class="card">
    <div class="d-flex justify-between align-center mb-2">
        <h2>Service History</h2>
        <a href="{{ url_for('service_log_add') }}" class="btn btn-success">Add Service Log</a>
    </div>
    {% if services %}
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Added</th>
                <th>Recovered</th>
                <th>Leak Found</th>
                <th>Technician</th>
            </tr>
        </thead>
        <tbody>
            {% for service in services %}
            <tr>
                <td>{{ service.service_date }}</td>
                <td>{{ service.service_type }}</td>
                <td>{{ service.refrigerant_added }} lbs</td>
                <td>{{ service.refrigerant_recovered }} lbs</td>
                <td><span class="badge badge-{{ 'warning' if service.leak_found else 'success' }}">{{ 'Yes' if service.leak_found else 'No' }}</span></td>
                <td>{{ service.technician.name }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No service logs recorded.</p>
    {% endif %}
</div>
{% endblock %}
''',

# Continue with remaining templates (truncated for space)
}

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Write each template
for filename, content in templates.items():
    filepath = os.path.join('templates', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {filepath}')

print('\nAll main templates created successfully!')
print('Note: Additional templates (forms, lists, etc.) will be needed.')
print('Run the app with: python app.py')
