"""
Create Database Tables in Supabase
Runs the SQLAlchemy migrations to create all tables in your Supabase PostgreSQL database
"""
import os
from dotenv import load_dotenv
from flask import Flask
from models import db
from config import get_config

# Load environment variables
load_dotenv()

print("=" * 60)
print("EcoFreonTrack - Create Database Tables")
print("=" * 60)

# Check database type
database_type = os.environ.get('DATABASE_TYPE', 'sqlite')
print(f"\nDatabase Type: {database_type}")

if database_type.lower() != 'supabase':
    print("\n⚠️  WARNING: DATABASE_TYPE is not set to 'supabase'")
    print("   This will create tables in your local SQLite database.")
    response = input("\nContinue anyway? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        exit(0)

# Create Flask app
app = Flask(__name__)
app.config.from_object(get_config('development'))

# Initialize database with app
db.init_app(app)

print("\nCreating database tables...")
db_uri = app.config['SQLALCHEMY_DATABASE_URI']
if 'postgresql' in db_uri:
    print(f"Target: Supabase PostgreSQL")
    print(f"Database: {db_uri[:30]}...{db_uri[-20:]}")
else:
    print(f"Target: SQLite")
    print(f"Database: {db_uri}")

print("\nTables to create:")
tables = [
    "equipment",
    "technician",
    "service_log",
    "leak_inspection",
    "refrigerant_transaction",
    "compliance_alert",
    "refrigerant_inventory",
    "document",
    "technician_certification"
]
for table in tables:
    print(f"  - {table}")

print("\n" + "-" * 60)

try:
    with app.app_context():
        # Create all tables
        print("Running db.create_all()...")
        db.create_all()

        print("\n" + "=" * 60)
        print("✅ SUCCESS! All tables created")
        print("=" * 60)

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        created_tables = inspector.get_table_names()

        print(f"\nVerified {len(created_tables)} tables in database:")
        for table in sorted(created_tables):
            print(f"  ✓ {table}")

        if database_type.lower() == 'supabase':
            print("\n" + "=" * 60)
            print("Next Steps:")
            print("=" * 60)
            print("\n1. Verify tables in Supabase Dashboard:")
            print("   - Go to https://supabase.com/dashboard")
            print("   - Select your project")
            print("   - Click 'Table Editor' to see all tables")
            print("\n2. Start the application:")
            print("   python app.py")
            print("\n3. Access the application at:")
            print("   http://localhost:5000")

except Exception as e:
    print("\n" + "=" * 60)
    print("❌ TABLE CREATION FAILED!")
    print("=" * 60)
    print(f"\nError Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")

    print("\n" + "=" * 60)
    print("Troubleshooting:")
    print("=" * 60)

    error_str = str(e).lower()

    if 'connection' in error_str:
        print("\n❌ Connection Error:")
        print("   - Run test_supabase_connection.py first")
        print("   - Verify your SUPABASE_DB_URL is correct")

    elif 'permission' in error_str or 'access' in error_str:
        print("\n❌ Permission Error:")
        print("   - Check that your database user has CREATE TABLE permissions")
        print("   - Verify your Supabase project is active")

    elif 'already exists' in error_str:
        print("\n✓ Tables might already exist!")
        print("   - Check your Supabase dashboard Table Editor")
        print("   - If tables exist, you can skip this step")

    else:
        print("\n❓ Unknown Error:")
        print("   - Check the error message above")
        print("   - Verify database connection with test_supabase_connection.py")
        print("   - See SUPABASE_SETUP_GUIDE.md for more help")

    exit(1)
