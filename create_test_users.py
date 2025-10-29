"""
Create test users with different roles for testing role-based dashboards
"""
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_test_users():
    """Create test users for each role"""
    with app.app_context():
        # Check if users already exist
        existing_users = User.query.all()
        if existing_users:
            print(f"\nFound {len(existing_users)} existing users:")
            for user in existing_users:
                print(f"  - {user.email} ({user.role})")

            response = input("\nDo you want to create additional test users? (y/n): ")
            if response.lower() != 'y':
                print("Exiting...")
                return

        print("\n=== Creating Test Users ===\n")

        # 1. Create Technician User
        tech_user = User.query.filter_by(email='technician@ecofreon.com').first()
        if not tech_user:
            tech_user = User(
                username='technician',
                email='technician@ecofreon.com',
                password_hash=generate_password_hash('tech123'),
                full_name='John Technician',
                role='technician',
                company_name='EcoFreon Services',
                is_active=True
            )
            db.session.add(tech_user)
            print("[OK] Created Technician user:")
            print("  Email: technician@ecofreon.com")
            print("  Password: tech123")
            print("  Role: technician")
        else:
            print("[OK] Technician user already exists")

        # 2. Create Compliance Manager User
        manager_user = User.query.filter_by(email='manager@ecofreon.com').first()
        if not manager_user:
            manager_user = User(
                username='manager',
                email='manager@ecofreon.com',
                password_hash=generate_password_hash('manager123'),
                full_name='Sarah Manager',
                role='compliance_manager',
                company_name='EcoFreon Services',
                is_active=True
            )
            db.session.add(manager_user)
            print("\n[OK] Created Compliance Manager user:")
            print("  Email: manager@ecofreon.com")
            print("  Password: manager123")
            print("  Role: compliance_manager")
        else:
            print("\n[OK] Compliance Manager user already exists")

        # 3. Create Auditor User
        auditor_user = User.query.filter_by(email='auditor@ecofreon.com').first()
        if not auditor_user:
            auditor_user = User(
                username='auditor',
                email='auditor@ecofreon.com',
                password_hash=generate_password_hash('audit123'),
                full_name='Mike Auditor',
                role='auditor',
                company_name='EcoFreon Services',
                is_active=True
            )
            db.session.add(auditor_user)
            print("\n[OK] Created Auditor user:")
            print("  Email: auditor@ecofreon.com")
            print("  Password: audit123")
            print("  Role: auditor")
        else:
            print("\n[OK] Auditor user already exists")

        # 4. Create Admin User
        admin_user = User.query.filter_by(email='admin@ecofreon.com').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@ecofreon.com',
                password_hash=generate_password_hash('admin123'),
                full_name='Admin User',
                role='admin',
                company_name='EcoFreon Services',
                is_active=True
            )
            db.session.add(admin_user)
            print("\n[OK] Created Admin user:")
            print("  Email: admin@ecofreon.com")
            print("  Password: admin123")
            print("  Role: admin")
        else:
            print("\n[OK] Admin user already exists")

        # Commit all changes
        db.session.commit()

        print("\n" + "="*50)
        print("[OK] Test users created successfully!")
        print("="*50)
        print("\nYou can now log in with:")
        print("\n1. TECHNICIAN VIEW:")
        print("   Email: technician@ecofreon.com")
        print("   Password: tech123")
        print("\n2. MANAGER VIEW:")
        print("   Email: manager@ecofreon.com")
        print("   Password: manager123")
        print("\n3. AUDITOR VIEW:")
        print("   Email: auditor@ecofreon.com")
        print("   Password: audit123")
        print("\n4. ADMIN VIEW:")
        print("   Email: admin@ecofreon.com")
        print("   Password: admin123")
        print("\nNavigate to: http://127.0.0.1:3000/login")
        print("="*50 + "\n")

if __name__ == '__main__':
    create_test_users()
