from main import app
from controller.database import db
from controller import models

with app.app_context():
    db.create_all()
    print("Database created successfully")