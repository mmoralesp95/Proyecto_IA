# Proyecto IA: Gestión de Historias de Usuario y Tareas con Azure OpenAI

Este proyecto es una aplicación web desarrollada en Flask que permite gestionar historias de usuario y tareas de manera inteligente, utilizando la API de Azure OpenAI para la generación automática de historias y tareas a partir de prompts en lenguaje natural. Incluye integración con bases de datos SQL, despliegue con Docker y un pipeline CI/CD en GitHub Actions.
---
## Características

- **Generación automática de historias de usuario** a partir de prompts usando Azure OpenAI.
- **Generación automática de tareas técnicas** para cada historia de usuario.
- **Gestión CRUD** de historias de usuario y tareas.
- **Interfaz web moderna** con Bootstrap.
- **Persistencia en base de datos SQL** (MySQL por defecto).
- **Despliegue fácil con Docker y docker-compose**.
- **Pipeline CI/CD** con GitHub Actions.
- **Testing automatizado** con pytest.

## Tecnologías utilizadas

- Python 3.11
- Flask
- SQLAlchemy
- Pydantic
- Jinja2
- Azure OpenAI (API)
- MySQL
- Docker & docker-compose
- GitHub Actions (CI/CD)
- Bootstrap 5
---

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
├── test/
├── run.py
├── create_tables.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml
```
---

## Instalación local

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/mmoralesp95/Proyecto_IA.git
   ```
2. **Crea un entorno virtual e instala dependencias:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # o
   source venv/bin/activate  # En Mac/Linux

   pip install -r requirements.txt
   ```
3. **Configura las variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido (ajusta los valores según tu entorno):

   ```
   AZURE_OPENAI_API_KEY=tu_clave
   AZURE_OPENAI_ENDPOINT=tu_endpoint
   OPENAI_API_VERSION=2023-05-15
   AZURE_OPENAI_DEPLOYMENT=nombre_del_modelo
   DATABASE_URL=mysql+pymysql://usuario:contraseña@host:puerto/nombre_basedatos
   APP_SECRET_KEY=secretkey
   ```

4. **Crea las tablas de la base de datos:**
   ```bash
   python create_tables.py
   ```

5. **Ejecuta la aplicación:**
   ```bash
   python run.py
   ```
   Accede a [http://localhost:5000/user-stories](http://localhost:5000/user-stories)

---

## Uso

- Ingresa un prompt en la interfaz para generar una historia de usuario.
- Visualiza, elimina o genera tareas técnicas para cada historia.
- Visualiza las tareas asociadas a cada historia de usuario.
---

## Testing

Para ejecutar los tests automatizados en el terminal:
```sh
pytest
```
---
## CI/CD

El proyecto incluye un pipeline de CI/CD en [`.github/workflows/ci.yml`](.github/workflows/ci.yml) que:

- Instala dependencias.
- Espera a que la base de datos esté lista.
- Ejecuta los tests.
- Construye y sube la imagen Docker a Docker Hub.

### ¿Cómo funciona el pipeline?

- Cada vez que haces un `push` a la rama `main`, GitHub Actions ejecuta automáticamente el workflow.
- Si algún test falla, el pipeline se detiene y no sube la imagen.
- Si todo pasa, la imagen se sube a tu repositorio de Docker Hub.

---

## Variables de entorno

Las variables de entorno utilizadas en la aplicación se gestionan mediante los *secrets* y *variables* de GitHub Actions para el repositorio.

---

## Uso de la imagen desde Docker Hub

Una vez subida, cualquier usuario puede desplegar la aplicación con:
```bash
docker pull mmoralesp23/flask-app:latest
docker run -p 5000:5000 mmoralesp23/flask-app:latest
```
Enlace a la imagen: [https://hub.docker.com/repository/docker/mmoralesp23/flask-app](https://hub.docker.com/repository/docker/mmoralesp23/flask-app)

- Accede a [http://localhost:5000](http://localhost:5000) para ver el saludo inicial.
- Accede a [http://localhost:5000/user-stories](http://localhost:5000/user-stories) para usar la aplicación completa.


**Autor:** Miguel Morales Pareja


