# Proyecto de Gestión de Historias de Usuario y Tareas

Este proyecto es una aplicación web desarrollada en Python con Flask que permite gestionar historias de usuario y tareas asociadas, integrando funcionalidades de IA para la generación, categorización, estimación y auditoría de tareas mediante Azure OpenAI.

## Características principales

- **Gestión de historias de usuario:** Crear, listar y eliminar historias de usuario con campos como proyecto, rol, objetivo, razón, prioridad, puntos de historia y esfuerzo estimado.
- **Gestión de tareas:** Generar tareas automáticamente a partir de historias de usuario usando IA, listar tareas por historia, y eliminar tareas asociadas.
- **IA integrada:** Utiliza Azure OpenAI para:
  - Generar historias de usuario y tareas detalladas.
  - Describir, categorizar y estimar tareas.
  - Auditar tareas con análisis y mitigación de riesgos.
- **Persistencia en base de datos:** Utiliza SQLAlchemy para interactuar con la base de datos relacional.
- **API RESTful:** Rutas para operaciones CRUD sobre tareas, con documentación Swagger.
- **Frontend responsivo:** Interfaz web basada en Bootstrap.

## Estructura del proyecto

```
.
├── app/
│   ├── db.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── templates/
├── run.py
├── create_tables.py
├── requirements.txt
└── README.md
```

## Instalación


1. **Crea y activa un entorno virtual:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**
   Crea un archivo `.env` en la raíz con el siguiente contenido (ajusta según tu entorno):

   ```
   DATABASE_URL=mysql+mysqlconnector://usuario:contraseña@localhost/nombre_bd
   AZURE_OPENAI_KEY=tu_clave
   AZURE_OPENAI_API_VERSION=2023-05-15
   AZURE_OPENAI_ENDPOINT=https://<tu-endpoint>.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=nombre_del_modelo
   APP_SECRET_KEY=una_clave_secreta
   ```

5. **Crea las tablas en la base de datos:**
   ```sh
   python create_tables.py
   ```

6. **Ejecuta la aplicación:**
   ```sh
   python run.py
   ```

   Accede a [http://localhost:5000/user-stories](http://localhost:5000/user-stories)


## Uso

- **Historias de usuario:** Desde la interfaz web puedes crear nuevas historias de usuario usando prompts en lenguaje natural.
- **Tareas:** Genera tareas automáticamente para cada historia de usuario, visualízalas y gestiona su estado.
- **API:** Consulta y manipula tareas mediante endpoints REST (ver rutas en `app/routes/routesa.py`).

## Estructura de carpetas relevante

- `app/models/`: Modelos de SQLAlchemy y Pydantic.
- `app/services/`: Lógica de negocio para historias y tareas.
- `app/routes/`: Rutas Flask para frontend y API.
- `app/templates/`: Plantillas HTML (Jinja2).

## Créditos

Desarrollado por [Tu Nombre] como parte del