"""
Create Database Tables in Supabase - Simple Version
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Load environment variables
load_dotenv()

print("=" * 60)
print("EcoFreonTrack - Create Supabase Tables")
print("=" * 60)

# Get database URL directly
db_url = os.environ.get('SUPABASE_DB_URL')

if not db_url:
    print("\nERROR: SUPABASE_DB_URL not found")
    exit(1)

print(f"\nDatabase: {db_url[:30]}...{db_url[-20:]}")
print("\nCreating database engine...")

try:
    # Create engine
    engine = create_engine(db_url)

    # Import models after engine is created
    from models import db
    from flask import Flask

    # Create Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)

    print("Creating all tables...")
    with app.app_context():
        db.create_all()

        # Verify tables
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        print("\n" + "=" * 60)
        print("SUCCESS! Created {} tables in Supabase:".format(len(tables)))
        print("=" * 60)
        for table in sorted(tables):
            print(f"  * {table}")

        print("\n" + "=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print("\n1. Verify in Supabase Dashboard:")
        print("   https://supabase.com/dashboard")
        print("\n2. Start the application:")
        print("   python app.py")

except Exception as e:
    print("\n" + "=" * 60)
    print("ERROR: Table creation failed")
    print("=" * 60)
    print(f"\nError: {str(e)}")
    exit(1)
