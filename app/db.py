# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Usar variables de entorno para seguridad
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://dev_user:Root1234@mysql-openai-proyecto.mysql.database.azure.com:3306/entregable3")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()