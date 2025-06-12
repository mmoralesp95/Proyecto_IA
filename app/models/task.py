class Task:
    # Constructor de la clase Task. Inicializa los atributos de la tarea.
    def __init__(self, id=None, title=None, description=None, priority=None,
                  effort_hours=None, status=None, assigned_to=None, category=None,
                    risk_analysis=None, risk_mitigation=None):
        # Validaciones de tipo y formato
        if not isinstance(id, int) or id < 1:
            raise ValueError("id must be a positive integer")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(description, str):
            raise ValueError("description must be a string")
        if not isinstance(priority, str):
            raise ValueError("priority must be a string")
        if not isinstance(effort_hours, int) or effort_hours < 0:
            raise ValueError("effort_hours must be a non-negative integer")
        if not isinstance(status, str):
            raise ValueError("status must be a string")
        if not isinstance(assigned_to, str):
            raise ValueError("assigned_to must be a string")
        if not isinstance(category, str):
            raise ValueError("category must be a string")
        if not isinstance(risk_analysis, str):
            raise ValueError("risk_analysis must be a string")
        if not isinstance(risk_mitigation, str):
            raise ValueError("risk_mitigation must be a string")

        self.id = id  # Identificador único de la tarea
        self.title = title  # Título de la tarea
        self.description = description  # Descripción detallada de la tarea
        self.priority = priority  # Prioridad de la tarea (por ejemplo: alta, media, baja)
        self.effort_hours = effort_hours  # Estimación de horas de esfuerzo requeridas
        self.status = status  # Estado actual de la tarea (por ejemplo: pendiente, en progreso, completada)
        self.assigned_to = assigned_to  # Persona asignada a la tarea
        self.category = category # Categoría de la tarea (por ejemplo: desarrollo, pruebas, documentación)
        self.risk_analysis = risk_analysis # Análisis de riesgos asociado a la tarea
        self.risk_mitigation = risk_mitigation # Estrategia de mitigación de riesgos asociada a la tarea

    # Convierte el objeto Task en un diccionario para facilitar su manipulación o serialización.
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "effort_hours": self.effort_hours,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "category": self.category,
            "risk_analysis": self.risk_analysis,
            "risk_mitigation": self.risk_mitigation
        }

    @staticmethod
    # Crea una instancia de Task a partir de un diccionario.
    def from_dict(data):
        return Task(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            priority=data.get("priority"),
            effort_hours=data.get("effort_hours"),
            status=data.get("status"),
            assigned_to=data.get("assigned_to"),
            category=data.get("category"),
            risk_analysis=data.get("risk_analysis"),
            risk_mitigation=data.get("risk_mitigation")
        )
