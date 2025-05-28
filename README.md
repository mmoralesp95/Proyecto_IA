# Sistema de Gestión de Tareas

## Descripción

Este proyecto es una API RESTful desarrollada con Flask para la gestión de tareas. Permite crear, consultar, actualizar y eliminar tareas, así como consultar la documentación interactiva mediante Swagger.

---

## Requisitos

- Python 3.x
- pip

---

## Instalación

1. **Crea y activa un entorno virtual**  
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Instala las dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

---

## Estructura del Proyecto

```
Proyecto1/
└── Proyecto1/
    ├── app/
    │   ├── modules/
    │   │   ├── __init__.py         # Inicialización de la aplicación Flask
    │   │   ├── task.py             # Clase que define la estructura de una tarea
    │   │   ├── task_manager.py     # Gestor de persistencia de tareas
    │   │   ├── routes.py           # Rutas de la API REST
    │   └── run.py                  # Script para ejecutar la app
    ├── data/
    │   └── tasks.json              # Archivo de almacenamiento de tareas
    ├── tests/                      # Pruebas unitarias
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── test_routes.py
    │   └── test_task_manager.py
    ├── requirements.txt            # Dependencias del proyecto
    └── README.md
```

- **app/modules/**: Código fuente principal de la aplicación Flask.
- **data/**: Carpeta donde se almacena el archivo `tasks.json` con las tareas.
- **tests/**: Pruebas unitarias del proyecto.
- **requirements.txt**: Lista de dependencias necesarias.
- **README.md**: Documentación del proyecto.

---

## Uso

### 1. Ejecutar la aplicación

Desde la carpeta `app`:

```bash
python run.py
```

La API estará disponible en [http://localhost:5000](http://localhost:5000)

---

### 2. Documentación Swagger

Accede a la documentación interactiva (Swagger) en:

```
http://localhost:5000/apidocs
```

---

## Endpoints principales

### Obtener todas las tareas

```
GET /tasks
```

### Obtener una tarea específica

```
GET /tasks/<id>
```

### Crear una nueva tarea

```
POST /tasks
```
**Cuerpo de la petición:**
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

```
PUT /tasks/<id>
```
**Cuerpo de la petición (campos opcionales):**
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

```
DELETE /tasks/<id>
```

---

## Pruebas

Para ejecutar los tests:

```bash
pytest
```

Asegúrate de tener el entorno virtual activado y todas las dependencias instaladas.

---

## Notas

- Si la carpeta `data` no existe, créala manualmente antes de ejecutar la aplicación.
- El archivo `tasks.json` se generará automáticamente al crear la primera tarea.
- Puedes modificar y extender los endpoints según tus necesidades.

---