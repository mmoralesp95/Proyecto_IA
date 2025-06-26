# create_tables.py
from app.db import engine, Base
from app.models.user_story import UserStory
from app.models.task import Task

Base.metadata.create_all(bind=engine)
print("Tablas creadas exitosamente.")