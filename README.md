# Sistema de Gestión de Tareas con IA

## Descripción

Este proyecto es una API RESTful desarrollada con Flask para la gestión de tareas. Permite crear, consultar, actualizar y eliminar tareas, así como realizar análisis y descripciones automáticas mediante IA (Azure OpenAI). Incluye documentación interactiva mediante Swagger.

---

## Requisitos

- Python 3.8 o superior
- pip
- Cuenta y credenciales de Azure OpenAI (para endpoints de IA)
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

3. **Configura las variables de entorno**  
   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido (ajusta tus valores):

   ```
   AZURE_OPENAI_API_KEY=TU_API_KEY
   OPENAI_API_VERSION=2025-01-01-preview
   AZURE_OPENAI_ENDPOINT=https://<tu-endpoint>.cognitiveservices.azure.com/
   AZURE_OPENAI_DEPLOYMENT=nombre-de-tu-deployment
   ```

---

## Estructura del Proyecto

```
Proyecto1/
├── app/
│   ├── models/
│   │   └── taskModel.py         # Modelo Pydantic de la tarea
│   ├── routes/
│   │   └── routes.py            # Rutas de la API REST y endpoints IA
│   ├── services/
│   │   ├── __init__.py          # Inicialización y configuración de servicios (incluye cliente IA)
│   │   └── task_manager.py      # Gestor de persistencia de tareas usando TaskModel
│   └── __init__.py              # Inicialización del paquete app
├── data/
│   └── tasks.json               # Archivo de almacenamiento de tareas
├── tests/                       # Pruebas unitarias y de integración
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_routes.py
│   └── test_task_manager.py
├── run.py                       # Script principal para ejecutar la app
├── requirements.txt             # Dependencias del proyecto
├── .env                         # Variables de entorno (no subir a git)
└── README.md
```

- **app/models/**: Modelos de datos (Pydantic).
- **app/routes/**: Rutas y lógica de la API REST y endpoints de IA.
- **app/services/**: Lógica de negocio, persistencia y cliente IA.
- **data/**: Carpeta donde se almacena el archivo `tasks.json` con las tareas.
- **tests/**: Pruebas unitarias y de integración.
- **run.py**: Script principal para ejecutar la aplicación.
- **requirements.txt**: Lista de dependencias necesarias.
- **.env**: Variables de entorno para la configuración de Azure OpenAI.
- **README.md**: Documentación del proyecto.

---

## Uso

### 1. Ejecutar la aplicación

Desde la **raíz del proyecto**:

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
    "assigned_to": "Nombre del responsable",
    "category": "desarrollo",
    "risk_analysis": "",
    "risk_mitigation": ""
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
    "assigned_to": "Nuevo responsable",
    "category": "infraestructura",
    "risk_analysis": "Nuevo análisis",
    "risk_mitigation": "Nuevo plan"
}
```

### Eliminar una tarea

```
DELETE /tasks/<id>
```

---

## Endpoints IA (Azure OpenAI)

### Generar descripción automática de tarea

```
POST /ai/tasks/describe
```
**Cuerpo de la petición:**
```json
{
    "title": "Título de la tarea",
    "priority": "alta",
    "status": "pendiente",
    "assigned_to": "Nombre del responsable"
}
```
**Respuesta:**
```json
{
    "id": null,
    "title": "Título de la tarea",
    "description": "Descripción generada por IA...",
    "priority": "alta",
    "effort_hours": 0,
    "status": "pendiente",
    "assigned_to": "Nombre del responsable",
    "category": "",
    "risk_analysis": "",
    "risk_mitigation": ""
}
```

### Auditar tarea (análisis y mitigación de riesgos)

```
POST /ai/tasks/audit
```
**Cuerpo de la petición:**  
Todos los campos menos `risk_analysis` y `risk_mitigation`.
```json
{
    "id": 1,
    "title": "Título de la tarea",
    "description": "Descripción detallada",
    "priority": "alta",
    "effort_hours": 5,
    "status": "pendiente",
    "assigned_to": "Nombre del responsable",
    "category": "desarrollo"
}
```
**Respuesta:**
```json
{
    "id": 1,
    "title": "Título de la tarea",
    "description": "Descripción detallada",
    "priority": "alta",
    "effort_hours": 5,
    "status": "pendiente",
    "assigned_to": "Nombre del responsable",
    "category": "desarrollo",
    "risk_analysis": "Análisis generado por IA...",
    "risk_mitigation": "Plan de mitigación generado por IA..."
}
```

---


### Categorizar tarea automáticamente

```
POST /ai/tasks/categorize
```
**Cuerpo de la petición:**
```json
{
    "title": "Título de la tarea",
    "description": "Descripción detallada"
}
```
**Respuesta:**
```json
{
    "category": "Categoría sugerida por IA"
}
```
> Este endpoint utiliza IA para sugerir una categoría adecuada para la tarea según su título y descripción.

---
### Estimar esfuerzo de tarea automáticamente

```
POST /ai/tasks/estimate
```
**Cuerpo de la petición:**
```json
{
    "title": "Título de la tarea",
    "description": "Descripción detallada"
}
```
**Respuesta:**
```json
{
    "effort_hours": 8
}
```
> Este endpoint utiliza IA para sugerir una estimación de horas de esfuerzo para la tarea según su título y descripción.

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
- Los endpoints de IA requieren credenciales y configuración de Azure OpenAI válidas en el archivo `.env`.
- Los campos `risk_analysis` y `risk_mitigation` pueden ser completados manualmente o por los endpoints de IA.

---