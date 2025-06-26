# app/models/task.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True) # Identificador único de la tarea
    title = Column(String(255), nullable=False) # Título de la tarea
    description = Column(Text) # Descripción detallada de la tarea 
    priority = Column(Enum('baja', 'media', 'alta', 'bloqueante', name='task_priority_enum')) # Prioridad de la tarea (baja, media, alta, bloqueante)
    effort_hours = Column(Float) # Horas de esfuerzo estimadas para completar la tarea
    status = Column(Enum('pendiente', 'en_progreso', 'en_revision', 'completada', name='status_enum'))  # Estado de la tarea (pendiente, en progreso, en revisión, completada)
    assigned_to = Column(String(100)) # Usuario asignado a la tarea (nombre o ID del usuario)
    category = Column(String(100)) # Categoría de la tarea (ej. "Desarrollo", "Pruebas", "Documentación")
    risk_analysis = Column(Text) # Análisis de riesgos asociado a la tarea
    risk_mitigation = Column(Text) # Plan de mitigación de riesgos asociado a la tarea
    user_story_id = Column(Integer, ForeignKey("user_stories.id")) # ID de la historia de usuario a la que pertenece la tarea
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Fecha y hora de creación de la tarea

    user_story = relationship("UserStory", back_populates="tasks") # Relación con la historia de usuario a la que pertenece la tarea
