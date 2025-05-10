class Task:
    # Constructor de la clase Task. Inicializa los atributos de la tarea.
    def __init__(self, id, title, description, priority, effort_hours, status, assigned_to):
        self.id = id  # Identificador único de la tarea
        self.title = title  # Título de la tarea
        self.description = description  # Descripción detallada de la tarea
        self.priority = priority  # Prioridad de la tarea (por ejemplo: alta, media, baja)
        self.effort_hours = effort_hours  # Estimación de horas de esfuerzo requeridas
        self.status = status  # Estado actual de la tarea (por ejemplo: pendiente, en progreso, completada)
        self.assigned_to = assigned_to  # Persona asignada a la tarea

    # Convierte el objeto Task en un diccionario para facilitar su manipulación o serialización.
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "effort_hours": self.effort_hours,
            "status": self.status,
            "assigned_to": self.assigned_to
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
            assigned_to=data.get("assigned_to")
        )
