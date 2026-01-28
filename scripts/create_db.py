from sqlalchemy import create_engine
from app.db import models
from app.db.base import Base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

print("Database created successfully")