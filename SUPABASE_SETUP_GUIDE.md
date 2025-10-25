# Supabase Setup Guide for EcoFreonTrack

This guide will walk you through setting up Supabase as your database for EcoFreonTrack.

## Prerequisites

- A Supabase account (sign up at https://supabase.com)
- Python packages already installed:
  - `supabase>=2.22.1`
  - `psycopg2-binary>=2.9.11`

## Step 1: Create a Supabase Project

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Fill in the project details:
   - **Name**: EcoFreonTrack (or your preferred name)
   - **Database Password**: Create a strong password and SAVE IT
   - **Region**: Choose the region closest to you
4. Click "Create new project"
5. Wait 2-3 minutes for the project to be provisioned

## Step 2: Get Your Supabase Credentials

Once your project is ready:

### 2.1 Get API URL and Keys

1. In your Supabase dashboard, go to **Settings** (gear icon) > **API**
2. You'll see:
   - **Project URL** - Copy this (e.g., `https://abcdefghijk.supabase.co`)
   - **anon public key** - Copy this long API key (starts with `eyJ...`)

### 2.2 Get Database Connection String

1. In your Supabase dashboard, go to **Settings** > **Database**
2. Scroll down to **Connection string**
3. Select the **URI** tab
4. Copy the connection string (it looks like this):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijk.supabase.co:5432/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with the database password you created in Step 1

## Step 3: Update Your .env File

Open `C:\Users\Manny\EcoFreonTrack\.env` and update these values:

```ini
# Database Type - set to 'supabase' to use Supabase
DATABASE_TYPE=supabase

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key-here
SUPABASE_DB_URL=postgresql://postgres:[YOUR-PASSWORD]@db.your-project.supabase.co:5432/postgres
```

Replace:
- `https://your-project.supabase.co` with your actual Project URL
- `your-anon-public-key-here` with your actual anon public key
- `[YOUR-PASSWORD]@db.your-project.supabase.co` with your actual password and project subdomain

## Step 4: Test the Database Connection

Create a test script to verify your connection:

```python
# test_supabase_connection.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Get the database URL from environment
db_url = os.environ.get('SUPABASE_DB_URL')

if not db_url:
    print("ERROR: SUPABASE_DB_URL not found in environment variables")
    exit(1)

print(f"Testing connection to Supabase...")
print(f"Database URL: {db_url[:30]}...{db_url[-20:]}")  # Print partial URL for security

try:
    # Create engine
    engine = create_engine(db_url)

    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"\n✅ SUCCESS! Connected to PostgreSQL")
        print(f"Database version: {version}")

except Exception as e:
    print(f"\n❌ CONNECTION FAILED!")
    print(f"Error: {str(e)}")
    exit(1)
```

Run the test:
```bash
cd EcoFreonTrack
python test_supabase_connection.py
```

## Step 5: Create Database Tables

Once the connection test passes, create the database tables:

```python
# create_tables.py
import os
from dotenv import load_dotenv
from flask import Flask
from models import db
from config import get_config

load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config.from_object(get_config('development'))

# Initialize database
db.init_app(app)

print("Creating database tables in Supabase...")
print(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI'][:30]}...")

try:
    with app.app_context():
        # Create all tables
        db.create_all()
        print("\n✅ SUCCESS! All tables created:")
        print("  - equipment")
        print("  - technician")
        print("  - service_log")
        print("  - leak_inspection")
        print("  - refrigerant_transaction")
        print("  - compliance_alert")
        print("  - refrigerant_inventory")
        print("  - document")
        print("  - technician_certification")

except Exception as e:
    print(f"\n❌ TABLE CREATION FAILED!")
    print(f"Error: {str(e)}")
    exit(1)
```

Run the script:
```bash
python create_tables.py
```

## Step 6: Verify Tables in Supabase Dashboard

1. Go to your Supabase dashboard
2. Click on **Table Editor** (table icon on left)
3. You should see all 9 tables:
   - equipment
   - technician
   - service_log
   - leak_inspection
   - refrigerant_transaction
   - compliance_alert
   - refrigerant_inventory
   - document
   - technician_certification

## Step 7: Start the Application

```bash
cd EcoFreonTrack
python app.py
```

The application should now start and connect to Supabase!

## Step 8: File Storage Setup (Optional - Future Enhancement)

Currently, files are stored locally in the `uploads/` folder. To use Supabase Storage:

1. In Supabase dashboard, go to **Storage**
2. Create a new bucket called `ecofreontrack-documents`
3. Set the bucket to **Private** (requires authentication)
4. Update `file_utils.py` to use Supabase Storage API instead of local filesystem

We can implement this in a future update if needed.

## Troubleshooting

### Connection Refused Error
- Check that your database password is correct
- Verify the connection string format
- Ensure no firewall is blocking port 5432

### SSL Error
- Supabase requires SSL connections. The connection string should include `?sslmode=require` at the end if having issues:
  ```
  postgresql://postgres:password@db.project.supabase.co:5432/postgres?sslmode=require
  ```

### Module Not Found Error
- Make sure you installed the packages:
  ```bash
  pip install supabase psycopg2-binary
  ```

### Tables Not Created
- Check that `DATABASE_TYPE=supabase` in your .env file
- Verify the database connection string is correct
- Look at the error message for specific issues

## Switching Back to SQLite

If you need to switch back to SQLite for local development:

1. Edit `.env` and change:
   ```ini
   DATABASE_TYPE=sqlite
   ```

2. Restart the application

The app will automatically use the local SQLite database.

## Support

If you encounter issues:
1. Check the Supabase documentation: https://supabase.com/docs
2. Check the error logs in your terminal
3. Verify all credentials are correct in the .env file
