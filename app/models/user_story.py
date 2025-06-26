# app/models/user_story.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class UserStory(Base):
    __tablename__ = "user_stories"
    id = Column(Integer, primary_key=True, index=True) # Identificador único de la historia de usuario
    project = Column(String(100), nullable=False) # Proyecto al que pertenece la historia de usuario
    role = Column(String(100), nullable=False) # Rol del usuario que solicita la historia (ej. "Como usuario", "Como administrador")
    goal = Column(String(255), nullable=False) # Objetivo de la historia de usuario (ej. "Quiero poder iniciar sesión")
    reason = Column(String(255), nullable=False) # Razón del objetivo (ej. "Para acceder a mi cuenta")
    description = Column(Text) # Descripción detallada de la historia de usuario
    priority = Column(Enum('baja', 'media', 'alta', 'bloqueante', name='priority_enum')) # Prioridad de la historia de usuario (baja, media, alta, bloqueante)
    story_points = Column(Integer) # Puntos de historia asignados a la historia de usuario (estimación del esfuerzo)
    effort_hours = Column(Float) # Horas de esfuerzo estimadas para completar la historia de usuario
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Fecha y hora de creación de la historia de usuario    

    tasks = relationship("Task", back_populates="user_story", cascade="all, delete-orphan")
