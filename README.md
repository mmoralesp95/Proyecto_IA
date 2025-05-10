# Sistema de Gestión de Tareas

## Descripción
Sistema de gestión de tareas que permite crear, leer, actualizar y eliminar tareas a través de una API REST. Cada tarea incluye título, descripción, prioridad, horas de esfuerzo, estado y persona asignada.

## Requisitos
- Python 3.x
- Flask
- pip (gestor de paquetes de Python)

## Instalación
1. Clonar el repositorio
2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto
- `app/`: Directorio principal de la aplicación
  - `__init__.py`: Inicialización de la aplicación Flask
  - `task.py`: Clase que define la estructura de una tarea
  - `task_manager.py`: Gestor de persistencia de tareas
  - `routes.py`: Rutas de la API REST
- `tasks.json`: Archivo de almacenamiento de tareas

## Uso de la API
### Obtener todas las tareas
```bash
GET /tasks
```

### Obtener una tarea específica
```bash
GET /tasks/<id>
```

### Crear una nueva tarea
```bash
POST /tasks
```
Cuerpo de la petición:
```json
{
    "title": "Título de la tarea",
    "description": "Descripción detallada",
    "priority": "alta",
    "effort_hours": 5,
    "status": "pendiente",
    "assigned_to": "Nombre del responsable"
}
```

### Actualizar una tarea
```bash
PUT /tasks/<id>
```
Cuerpo de la petición (campos opcionales):
```json
{
    "title": "Nuevo título",
    "description": "Nueva descripción",
    "priority": "media",
    "effort_hours": 3,
    "status": "en progreso",
    "assigned_to": "Nuevo responsable"
}
```

### Eliminar una tarea
```bash
DELETE /tasks/<id>
```

## Ejecución
Para iniciar el servidor:
```bash
python app.py
```

La API estará disponible en `http://localhost:5000` 