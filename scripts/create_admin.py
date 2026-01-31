from main import app
from controller.database import db
from controller.models import User

from werkzeug.security import generate_password_hash

ADMIN_EMAIL="admin@super.com"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin123"

with app.app_context():
    existing_admin=User.query.filter_by(role="Admin").first()

    if existing_admin:
        print("Admin already exists")
    else:
        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=generate_password_hash(ADMIN_PASSWORD),
            role="Admin"
        )    
        db.session.add(admin)
        db.session.commit()
        print("Admin Created Successfully!")
        print(admin)