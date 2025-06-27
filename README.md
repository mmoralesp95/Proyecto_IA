# Proyecto Generador de Historias de Usuario y Tareas con IA

Este proyecto es una aplicación web desarrollada con **Flask** que permite generar historias de usuario y tareas técnicas de manera automática utilizando **Azure OpenAI**

## Estructura del Proyecto

```
Proyecto1/
│
├── app/
│   ├── db/                  # Configuración y modelos de la base de datos
│   ├── models/              # Modelos ORM (UserStory, Task, etc.)
│   ├── routes/              # Blueprints y rutas Flask
│   ├── schemas/             # Esquemas de validación y serialización
│   ├── services/            # Lógica de negocio (gestores de historias y tareas)
│   ├── templates/           # Plantillas HTML (Jinja2)
│   └── static/              # Archivos estáticos (CSS, JS, imágenes)
│
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Este archivo
└── run.py                   # Script principal para lanzar la aplicación
```

## Requisitos Previos

- **Python 3.8+**
- Cuenta de **Azure OpenAI** con un modelo desplegado
- Variables de entorno configuradas para Azure OpenAI:
  - `AZURE_OPENAI_KEY`
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_API_VERSION`
  - `AZURE_OPENAI_DEPLOYMENT`
- Variable para base de datos MySQL:
   - `DATABASE_URL`

## Instalación

1. **Descomprimir el proyecto**

2. **Crea un entorno virtual y actívalo:**
   ```bash
   python -m venv venv
   venv\Scripts\activate 
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**  
   Puedes crear un archivo `.env` en la raíz del proyecto o exportarlas en tu terminal:

   ```
   AZURE_OPENAI_KEY=tu_clave
   AZURE_OPENAI_ENDPOINT=tu_endpoint
   AZURE_OPENAI_API_VERSION=2023-05-15
   AZURE_OPENAI_DEPLOYMENT=nombre_del_modelo
   DATABASE_URL=mysql+pymysql://usuario:contraseña@host:puerto/nombre_basedatos
   ```

## Ejecución

1. **Inicializa la base de datos** (si es necesario, según tu configuración). 
   Para crear las tablas necesarias en la base de datos, ejecuta el siguiente comando:
   ```bash
   python create_tables.py
   ```
   Esto generará automáticamente la estructura de la base de datos según la configuración definida.

2. **Lanza la aplicación:**
   ```bash
   python run.py
   ```
3. **Accede a la aplicación**  
   Abre tu navegador en [http://localhost:5000/user-stories](http://localhost:5000/user-stories)

## ¿Qué hace la aplicación?

- Permite generar historias de usuario a partir de un prompt usando IA.
- Permite generar tareas técnicas detalladas para cada historia de usuario haciendo uso de la IA
- Visualiza, elimina y gestiona historias y tareas desde una interfaz web amigable.

## Estructura principal de carpetas

- **app/models/**: Modelos de SQLAlchemy para historias y tareas.
- **app/routes/**: Rutas Flask para la gestión de historias y tareas.
- **app/schemas/**: Modelos de validación y serialización para asegurar la estructura de los datos intercambiados entre la API y la base de datos.
- **app/services/**: Lógica para interactuar con la base de datos.
- **app/templates/**: Plantillas HTML con Bootstrap para la UI.

## Notas

- Asegúrate de tener configurado correctamente tu acceso a Azure OpenAI.
- Puedes personalizar los prompts y la lógica de generación en los servicios.

---

**Autor:**  
Miguel Morales Pareja
