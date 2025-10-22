"""
Simple SQLite Database Viewer for EcoFreonTrack
View all tables and records in the database
"""
import sqlite3
from datetime import datetime

DB_PATH = 'instance/epa608_tracker.db'

def view_database():
    """View all tables and their contents"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("=" * 80)
        print("ECOFREONTRACK DATABASE VIEWER")
        print("=" * 80)
        print(f"Database: {DB_PATH}")
        print(f"Accessed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()

        print(f"\nFound {len(tables)} tables:")
        for i, (table_name,) in enumerate(tables, 1):
            print(f"  {i}. {table_name}")

        # Show record counts
        print("\n" + "=" * 80)
        print("RECORD COUNTS")
        print("=" * 80)

        for (table_name,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  {table_name:<30} {count:>10} records")

        # Show equipment details
        print("\n" + "=" * 80)
        print("EQUIPMENT")
        print("=" * 80)
        cursor.execute("SELECT equipment_id, name, refrigerant_name, full_charge, status FROM equipment")
        equipment = cursor.fetchall()

        if equipment:
            print(f"\n{'ID':<15} {'Name':<25} {'Refrigerant':<12} {'Charge':<10} {'Status':<10}")
            print("-" * 80)
            for eq in equipment:
                print(f"{eq[0]:<15} {eq[1]:<25} {eq[2]:<12} {eq[3]:<10} {eq[4]:<10}")
        else:
            print("  No equipment records found")

        # Show technicians
        print("\n" + "=" * 80)
        print("TECHNICIANS")
        print("=" * 80)
        cursor.execute("SELECT name, certification_number, certification_type, status FROM technician")
        technicians = cursor.fetchall()

        if technicians:
            print(f"\n{'Name':<30} {'Cert #':<20} {'Type':<15} {'Status':<10}")
            print("-" * 80)
            for tech in technicians:
                print(f"{tech[0]:<30} {tech[1]:<20} {tech[2]:<15} {tech[3]:<10}")
        else:
            print("  No technician records found")

        # Show refrigerant inventory
        print("\n" + "=" * 80)
        print("REFRIGERANT INVENTORY")
        print("=" * 80)
        cursor.execute("SELECT refrigerant_name, refrigerant_type, quantity_on_hand, reorder_level FROM refrigerant_inventory")
        inventory = cursor.fetchall()

        if inventory:
            print(f"\n{'Refrigerant':<15} {'Type':<10} {'On Hand':<12} {'Reorder Level':<15}")
            print("-" * 80)
            for item in inventory:
                status = "LOW" if item[2] < item[3] else "OK"
                print(f"{item[0]:<15} {item[1]:<10} {item[2]:<12.2f} {item[3]:<15.2f}  [{status}]")
        else:
            print("  No inventory records found")

        # Show recent service logs
        print("\n" + "=" * 80)
        print("RECENT SERVICE LOGS (Last 10)")
        print("=" * 80)
        cursor.execute("""
            SELECT s.service_date, e.equipment_id, s.service_type,
                   s.refrigerant_added, s.refrigerant_recovered
            FROM service_log s
            JOIN equipment e ON s.equipment_id = e.id
            ORDER BY s.service_date DESC
            LIMIT 10
        """)
        services = cursor.fetchall()

        if services:
            print(f"\n{'Date':<12} {'Equipment':<15} {'Type':<15} {'Added':<10} {'Recovered':<10}")
            print("-" * 80)
            for svc in services:
                print(f"{svc[0]:<12} {svc[1]:<15} {svc[2]:<15} {svc[3]:<10.2f} {svc[4]:<10.2f}")
        else:
            print("  No service logs found")

        # Show compliance alerts
        print("\n" + "=" * 80)
        print("ACTIVE COMPLIANCE ALERTS")
        print("=" * 80)
        cursor.execute("""
            SELECT alert_type, severity, title, alert_date, status
            FROM compliance_alert
            WHERE status = 'Active'
            ORDER BY alert_date DESC
            LIMIT 10
        """)
        alerts = cursor.fetchall()

        if alerts:
            print(f"\n{'Type':<25} {'Severity':<12} {'Date':<12} {'Status':<10}")
            print("-" * 80)
            for alert in alerts:
                print(f"{alert[0]:<25} {alert[1]:<12} {alert[3]:<12} {alert[4]:<10}")
                print(f"  Title: {alert[2]}")
        else:
            print("  No active alerts")

        print("\n" + "=" * 80)
        print("END OF DATABASE VIEW")
        print("=" * 80)

        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def export_to_csv():
    """Export all tables to CSV files"""
    import csv

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()

        print("\nExporting tables to CSV...")

        for (table_name,) in tables:
            # Get data
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()

            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]

            # Write to CSV
            filename = f"{table_name}_export.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)  # Header
                writer.writerows(data)    # Data

            print(f"  Exported {table_name} ({len(data)} records) -> {filename}")

        print("\nExport complete!")

        conn.close()

    except Exception as e:
        print(f"Export error: {e}")


def run_custom_query():
    """Run a custom SQL query"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("\n" + "=" * 80)
        print("CUSTOM SQL QUERY")
        print("=" * 80)
        print("Enter your SQL query (or 'quit' to exit):")
        print("Examples:")
        print("  SELECT * FROM equipment WHERE status='Active';")
        print("  SELECT COUNT(*) FROM service_log;")
        print("  SELECT * FROM refrigerant_inventory WHERE quantity_on_hand < reorder_level;")
        print()

        query = input("SQL> ").strip()

        if query.lower() == 'quit':
            return

        cursor.execute(query)

        # If SELECT query, show results
        if query.upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            print(f"\nFound {len(results)} results:")
            print("-" * 80)
            print(" | ".join(columns))
            print("-" * 80)

            for row in results:
                print(" | ".join(str(val) for val in row))
        else:
            conn.commit()
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}")

        conn.close()

    except Exception as e:
        print(f"Query error: {e}")


if __name__ == '__main__':
    print("\nECOFREONTRACK DATABASE TOOLS")
    print("=" * 80)
    print("1. View Database")
    print("2. Export to CSV")
    print("3. Run Custom Query")
    print("4. Exit")
    print()

    choice = input("Select option (1-4): ").strip()

    if choice == '1':
        view_database()
    elif choice == '2':
        export_to_csv()
    elif choice == '3':
        run_custom_query()
    elif choice == '4':
        print("Goodbye!")
    else:
        print("Invalid choice")
