"""
Fix SQLite database issues by backing up and recreating fresh schema
"""
import os
import shutil
from datetime import datetime
from pathlib import Path

# Get paths
instance_dir = Path(__file__).parent / 'instance'
dev_db = instance_dir / 'epa608_tracker_dev.db'
backup_db = instance_dir / f'epa608_tracker_dev.db.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

print(f"Instance directory: {instance_dir}")
print(f"Development database: {dev_db}")
print(f"Backup location: {backup_db}")

# Create instance directory if it doesn't exist
instance_dir.mkdir(exist_ok=True)

# Backup existing database if it exists
if dev_db.exists():
    print(f"\nBacking up existing database...")
    shutil.copy2(dev_db, backup_db)
    print(f"[OK] Backup created: {backup_db}")
else:
    print(f"\nNo existing database found at {dev_db}")

# Now create fresh database with Flask app
print(f"\nCreating fresh database with schema...")
from app import app, db

with app.app_context():
    # Drop all existing tables first
    print("Dropping existing tables...")
    db.drop_all()
    print("[OK] Existing tables dropped")

    # Create all tables
    print("Creating tables...")
    db.create_all()
    print("[OK] Database schema created successfully!")

    # Initialize with default data
    from models import RefrigerantInventory

    if RefrigerantInventory.query.count() == 0:
        print("\nInitializing default refrigerant inventory...")
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
        print(f"[OK] Initialized {len(common_refrigerants)} refrigerant types")

print("\n" + "="*60)
print("[OK] Database fix complete!")
print("="*60)
