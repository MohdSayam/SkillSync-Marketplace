"""
Setup script - creates database and admin user in one command.
Run: python scripts/setup.py
"""
from main import app
from controller.database import db
from controller.models import User
from werkzeug.security import generate_password_hash

ADMIN_EMAIL = "admin@skillsync.com"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

with app.app_context():
    db.create_all()
    print("Database tables created.")

    existing_admin = User.query.filter_by(role="Admin").first()
    if existing_admin:
        print("Admin user already exists.")
    else:
        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=generate_password_hash(ADMIN_PASSWORD),
            role="Admin"
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created - Email: {ADMIN_EMAIL}, Password: {ADMIN_PASSWORD}")

print("Setup complete. Run 'python main.py' to start the server.")
