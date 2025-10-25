"""
Test Supabase Database Connection
Verifies that the connection string in .env is correct and can connect to Supabase
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get the database URL from environment
db_url = os.environ.get('SUPABASE_DB_URL')
database_type = os.environ.get('DATABASE_TYPE', 'sqlite')

print("=" * 60)
print("EcoFreonTrack - Supabase Connection Test")
print("=" * 60)

# Check database type setting
print(f"\nDatabase Type: {database_type}")

if database_type.lower() != 'supabase':
    print("\n⚠️  WARNING: DATABASE_TYPE is not set to 'supabase'")
    print("   Update your .env file to use Supabase:")
    print("   DATABASE_TYPE=supabase")
    print("\nSkipping connection test...")
    exit(0)

# Check if connection string exists
if not db_url:
    print("\n❌ ERROR: SUPABASE_DB_URL not found in environment variables")
    print("\nMake sure your .env file contains:")
    print("SUPABASE_DB_URL=postgresql://postgres:[PASSWORD]@db.project.supabase.co:5432/postgres")
    exit(1)

# Check if it's still the placeholder
if 'your-project' in db_url or '[YOUR-PASSWORD]' in db_url:
    print("\n❌ ERROR: SUPABASE_DB_URL still contains placeholder values")
    print("\nUpdate your .env file with actual Supabase credentials:")
    print("1. Go to https://supabase.com/dashboard")
    print("2. Select your project")
    print("3. Go to Settings > Database")
    print("4. Copy the connection string and update .env")
    exit(1)

# Show sanitized connection info
print(f"\nConnecting to Supabase...")
print(f"Database URL: {db_url[:30]}...{db_url[-20:]}")

try:
    # Create SQLAlchemy engine
    print("\nCreating database engine...")
    engine = create_engine(db_url, echo=False)

    # Test connection
    print("Testing connection...")
    with engine.connect() as connection:
        # Get PostgreSQL version
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]

        # Get current database name
        result = connection.execute(text("SELECT current_database();"))
        db_name = result.fetchone()[0]

        # Get number of tables
        result = connection.execute(text("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """))
        table_count = result.fetchone()[0]

        print("\n" + "=" * 60)
        print("✅ SUCCESS! Connected to Supabase PostgreSQL")
        print("=" * 60)
        print(f"\nDatabase Name: {db_name}")
        print(f"PostgreSQL Version: {version.split(',')[0]}")
        print(f"Tables in database: {table_count}")

        if table_count == 0:
            print("\n⚠️  No tables found. Run create_tables.py to create the schema.")
        elif table_count < 9:
            print("\n⚠️  Expected 9 tables but found {table_count}.")
            print("   Run create_tables.py to ensure all tables are created.")
        else:
            print("\n✅ All tables appear to be created!")

        print("\n" + "=" * 60)
        print("You can now start the application with: python app.py")
        print("=" * 60)

except Exception as e:
    print("\n" + "=" * 60)
    print("❌ CONNECTION FAILED!")
    print("=" * 60)
    print(f"\nError Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")

    # Provide helpful troubleshooting tips
    print("\n" + "=" * 60)
    print("Troubleshooting Tips:")
    print("=" * 60)

    error_str = str(e).lower()

    if 'password' in error_str or 'authentication' in error_str:
        print("\n❌ Authentication Error:")
        print("   - Check that your database password is correct")
        print("   - Update SUPABASE_DB_URL in .env with the correct password")

    elif 'could not connect' in error_str or 'connection refused' in error_str:
        print("\n❌ Connection Error:")
        print("   - Check your internet connection")
        print("   - Verify the host address in SUPABASE_DB_URL")
        print("   - Check if firewall is blocking port 5432")

    elif 'ssl' in error_str:
        print("\n❌ SSL Error:")
        print("   - Try adding ?sslmode=require to the end of SUPABASE_DB_URL")

    elif 'does not exist' in error_str:
        print("\n❌ Database Error:")
        print("   - Check that your Supabase project is active")
        print("   - Verify the database name in the connection string")

    else:
        print("\n❓ Unknown Error:")
        print("   - Double-check all credentials in .env")
        print("   - Verify your Supabase project is running")
        print("   - Check Supabase dashboard for any issues")

    print("\nFor more help, see SUPABASE_SETUP_GUIDE.md")
    exit(1)
