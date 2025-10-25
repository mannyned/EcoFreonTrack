"""
Setup RBAC System
Creates the user table in Supabase and creates an initial admin user
"""
import os
from dotenv import load_dotenv
from app import app
from models import db, User

# Load environment variables
load_dotenv()

def create_user_table():
    """Create the user table in the database"""
    print("=" * 60)
    print("Creating User Table")
    print("=" * 60)

    try:
        with app.app_context():
            # Create user table
            db.create_all()
            print("\n SUCCESS: User table created (or already exists)")
            print("\nYou can verify in Supabase Dashboard:")
            print("- Go to Table Editor")
            print("- Look for 'user' table")

    except Exception as e:
        print(f"\n ERROR: Failed to create user table")
        print(f"Error: {str(e)}")
        return False

    return True


def create_admin_user():
    """Create the initial admin user"""
    print("\n" + "=" * 60)
    print("Creating Initial Admin User")
    print("=" * 60)

    try:
        with app.app_context():
            # Check if admin user already exists
            existing_admin = User.query.filter_by(username='admin').first()

            if existing_admin:
                print("\n WARNING: Admin user already exists!")
                print(f"Username: {existing_admin.username}")
                print(f"Email: {existing_admin.email}")
                print(f"Status: {'Active' if existing_admin.is_active else 'Inactive'}")

                response = input("\nDo you want to reset the admin password? (y/n): ")
                if response.lower() == 'y':
                    password = input("Enter new password (minimum 6 characters): ")
                    if len(password) < 6:
                        print(" ERROR: Password must be at least 6 characters")
                        return False

                    existing_admin.set_password(password)
                    existing_admin.is_active = True
                    db.session.commit()

                    print("\n SUCCESS: Admin password reset!")
                    print(f"Username: admin")
                    print(f"Password: {password}")
                else:
                    print("\nNo changes made.")
                return True

            # Create new admin user
            print("\nCreating default admin account...")
            print("You can change these credentials later.")

            admin = User(
                username='admin',
                email='admin@ecofreontrack.com',
                full_name='System Administrator',
                role='admin',
                is_active=True,
                is_verified=True
            )

            # Set default password
            default_password = 'Admin123!'
            admin.set_password(default_password)

            db.session.add(admin)
            db.session.commit()

            print("\n" + "=" * 60)
            print(" SUCCESS: Admin user created!")
            print("=" * 60)
            print("\nDefault Login Credentials:")
            print(f"  Username: admin")
            print(f"  Password: {default_password}")
            print("\nIMPORTANT:")
            print("1. Save these credentials securely")
            print("2. Log in and change the password immediately")
            print("3. Create additional users as needed")
            print("=" * 60)

    except Exception as e:
        print(f"\n ERROR: Failed to create admin user")
        print(f"Error: {str(e)}")
        db.session.rollback()
        return False

    return True


def main():
    """Main setup function"""
    print("\n" + "=" * 60)
    print("EcoFreonTrack - RBAC System Setup")
    print("=" * 60)

    # Step 1: Create user table
    if not create_user_table():
        print("\n FAILED: Could not create user table")
        return

    # Step 2: Create admin user
    if not create_admin_user():
        print("\n FAILED: Could not create admin user")
        return

    print("\n" + "=" * 60)
    print(" RBAC Setup Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Start the application: python app.py")
    print("2. Go to http://localhost:5000/login")
    print("3. Log in with the admin credentials")
    print("4. Navigate to User Management to create more users")
    print("=" * 60)


if __name__ == '__main__':
    main()
