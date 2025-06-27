from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.user_story_manager import UserStoryManager
from app.services.task_manager import TaskManager
from app.schemas.UserStorySchema import UserStorySchema
from app.schemas.TaskSchemas import TaskSchemas
from openai import AzureOpenAI
import os

routes = Blueprint('routes', __name__)

# Managers
user_story_manager = UserStoryManager()
task_manager = TaskManager()


# Configurar Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
# Nombre del modelo de despliegue
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Mostrar todas las historias de usuario
@routes.route('/user-stories', methods=['GET'])
def user_stories():
    """
    Mostrar todas las historias de usuario.
    Esta función recupera todas las historias de usuario almacenadas y las muestra en una plantilla HTML.
    Se utiliza el UserStoryManager para obtener las historias de usuario y renderizar la plantilla correspondiente.
    Se espera que las historias de usuario se muestren en una tabla o lista, permitiendo al usuario ver detalles como el proyecto, rol, objetivo, razón, descripción, prioridad, puntos de historia y horas de esfuerzo.
    Si no hay historias de usuario, se mostrará un mensaje indicando que no hay historias disponibles.
    Se pueden realizar acciones adicionales como crear nuevas historias de usuario o eliminar historias existentes desde esta vista.
    :return: Renderiza la plantilla 'user-stories.html' con las historias de usuario.
    :rtype: flask.Response
    """
    stories = user_story_manager.get_all_user_stories() # Obtener todas las historias de usuario
    if not stories:
        flash('No hay historias de usuario disponibles.', 'info')
        return render_template('user-stories.html', stories=[])
    return render_template('user-stories.html', stories=stories)

# Crear una nueva historia de usuario
@routes.route('/user-stories', methods=['POST'])
def add_user_story():
    """
    Crear una nueva historia de usuario utilizando IA.
    Esta función recibe un prompt del usuario a través de un formulario, lo procesa utilizando el modelo
    de IA de Azure OpenAI y genera una historia de usuario basada en el prompt proporcionado.
    Si el prompt está vacío, se muestra un mensaje de error. Si la generación es exitosa, se guarda la historia de usuario
    en la base de datos utilizando el UserStoryManager. En caso de error durante la generación o el guardado, se muestra un mensaje de error.
    :return: Redirige a la vista de historias de usuario con un mensaje de éxito o error.
    :rtype: flask.Response  
    """
    # Obtener el prompt del formulario
    if not deployment_name: 
        flash('El modelo de IA no está configurado correctamente.', 'error')
        return redirect(url_for('routes.user_stories'))
    if not client:
        flash('El cliente de IA no está configurado correctamente.', 'error')
        return redirect(url_for('routes.user_stories'))
    
    prompt = request.form.get('prompt', '').strip()
    if not prompt:
        flash('Por favor, ingresa un prompt para generar tareas.', 'error')
        return redirect(url_for('routes.user_stories'))
    
    # Generar la historia de usuario utilizando IA
    try:
        # Configurar el modelo de IA y el formato de respuesta
        completion = client.beta.chat.completions.parse(
            model=deployment_name,
            messages=[
                {"role": "system", "content": 
                '''
                Eres un asistente de creación de historias de usuario, cada historia de usuario tendrá la siguiente estructura:
                    project: Nombre del proyecto,
                    role: Rol del usuario que solicita la historia (ej. "Como usuario", "Como administrador"),
                    goal: Objetivo de la historia de usuario (ej. "Quiero poder iniciar sesión"),
                    reason: Razón del objetivo (ej. "Para acceder a mi cuenta"),
                    description: Descripción detallada de la historia de usuario,
                    priority: Prioridad de la historia de usuario (baja, media, alta, bloqueante),
                    story_points: Puntos de historia asignados a la historia de usuario (estimación del esfuerzo),
                    effort_hours: Horas de esfuerzo estimadas para completar la historia de usuario
                '''},
                {"role": "user", "content": prompt}],
                response_format=UserStorySchema
        )
        user_story = completion.choices[0].message.parsed # Obtener la historia de usuario generada
    except Exception as e:
        flash(f'Error al generar la historia de usuario: {str(e)}', 'error')
        return redirect(url_for('routes.user_stories'))
    
    # Guardar la historia de usuario generada   
    try:
        user_story_manager.create_user_story(
            project=user_story.project,
            role=user_story.role,
            goal=user_story.goal,
            reason=user_story.reason,
            description=user_story.description,
            priority=user_story.priority,
            story_points=user_story.story_points,
            effort_hours=user_story.effort_hours
        )
        flash('Historia de usuario creada correctamente.')
    except Exception as e:
        flash(f'Error al crear la historia de usuario: {str(e)}', 'error')
    return redirect(url_for('routes.user_stories'))

# Mostrar tareas de una historia de usuario
@routes.route('/user-stories/<int:user_story_id>/tasks', methods=['GET'])
def show_tasks(user_story_id):
    """
    Mostrar las tareas asociadas a una historia de usuario específica.
    Esta función recupera las tareas asociadas a una historia de usuario específica utilizando el ID proporcionado.
    Si la historia de usuario no se encuentra, se muestra un mensaje de error y se redirige a la lista de historias de usuario.
    Si se encuentran tareas, se renderiza la plantilla 'tasks.html' con la historia de usuario y las tareas asociadas.
    :param user_story_id: ID de la historia de usuario para la cual se desean mostrar las tareas.
    :type user_story_id: int       
    :return: Renderiza la plantilla 'tasks.html' con la historia de usuario y sus tareas.
    :rtype: flask.Response
    """
    # Obtener la historia de usuario por ID
    story = user_story_manager.get_user_story_by_id(user_story_id)
    if story is None:
        flash('Historia de usuario no encontrada.')
        return redirect(url_for('routes.user_stories'))
    # Obtener las tareas asociadas a la historia de usuario
    tasks = task_manager.get_tasks_by_user_story(user_story_id)
    if not tasks:
        flash('No hay tareas asociadas a esta historia de usuario.', 'info')
        return render_template('tasks.html', story=story, tasks=[], user_story_id=user_story_id, user_story_title=story.project)
    return render_template('tasks.html', story=story, tasks=tasks, user_story_id=user_story_id, user_story_title=story.project)

# Añadir una tarea a una historia de usuario con IA
@routes.route('/user-stories/<int:user_story_id>/tasks', methods=['POST'])
def add_task(user_story_id):
    user_story = user_story_manager.get_user_story_by_id(user_story_id)
    if user_story is None:
        flash('Historia de usuario no encontrada.', 'error')
        return redirect(url_for('routes.user_stories'))
    if not deployment_name:
        flash('El modelo de IA no está configurado correctamente.', 'error')
        return redirect(url_for('routes.show_tasks', user_story_id=user_story_id))
    if not client:
        flash('El cliente de IA no está configurado correctamente.', 'error')
        return redirect(url_for('routes.show_tasks', user_story_id=user_story_id))
    # Generar las tareas utilizando IA
    # Preparar el prompt para la IA
    prompt = "Eres un Producto Owner experto en la creación de tareas para historias de usuario. Debes generar tareas tecnicamente precisas y detalladas basadas en la historia de usuario proporcionada:\n\n"
    prompt += f"Historia de Usuario:\n- Proyecto: {user_story.project}\n"
    prompt += f"- Rol: {user_story.role}\n" 
    prompt += f"- Objetivo: {user_story.goal}\n"
    prompt += f"- Razón: {user_story.reason}\n"
    prompt += f"- Descripción: {user_story.description}\n"
    prompt += f"- Prioridad: {user_story.priority}\n"   
    prompt += f"- Puntos de Historia: {user_story.story_points}\n"
    prompt += f"- Horas de Esfuerzo: {user_story.effort_hours}\n\n"
    prompt += "Por favor, genera una lista de tareas detalladas que deben realizarse para completar esta historia de usuario. Cada tarea debe incluir:\n"
    prompt += "- Título de la tarea\n"
    prompt += "- Descripción detallada de la tarea\n"   
    prompt += "- Prioridad (baja, media, alta, bloqueante)\n"
    prompt += "- Horas de esfuerzo estimadas\n"
    prompt += "- Estado (pendiente, en progreso, en revisión, completada)\n"
    prompt += "- Usuario asignado (nombre o ID del usuario)\n"
    prompt += "- Categoría de la tarea (ej. 'Desarrollo', 'Pruebas', 'Documentación')\n"
    prompt += "- Análisis de riesgos asociado a la tarea\n"
    prompt += "- Plan de mitigación de riesgos asociado a la tarea\n"
    prompt += "Formato de respuesta:\n"
    prompt += "```json\n"
    prompt += "{\n"
    prompt += "  \"tasks\": [\n"
    prompt += "    {\n"
    prompt += "      \"title\": \"Título de la tarea\",\n"
    prompt += "      \"description\": \"Descripción detallada de la tarea\",\n"
    prompt += "      \"priority\": \"baja/ media/ alta/ bloqueante\",\n"
    prompt += "      \"effort_hours\": 0.0,\n"
    prompt += "      \"status\": \"pendiente/ en progreso/ en revisión/ completada\",\n"
    prompt += "      \"assigned_to\": \"Nombre o ID del usuario\",\n"
    prompt += "      \"category\": \"Categoría de la tarea\",\n"
    prompt += "      \"risk_analysis\": \"Análisis de riesgos asociado a la tarea\",\n"     
    prompt += "      \"risk_mitigation\": \"Plan de mitigación de riesgos asociado a la tarea\"\n"
    prompt += "    }\n"
    prompt += "  ]\n"
    prompt += "}\n"
    prompt += "```"
    # Llamar al modelo de IA para generar las tareas
    try:
        completion = client.beta.chat.completions.parse(
            model=deployment_name,
            messages=[
                {"role": "system", "content": 
                '''
                Eres un Product Owner experto en la creación de tareas para historias de usuario.
                '''},
                {"role": "user", "content": prompt}],
            response_format=TaskSchemas
        )
        tasks_data = completion.choices[0].message.parsed

        tasks = TaskSchemas(**tasks_data.model_dump()) # Obtener las tareas generadas


        # Guardar las tareas generadas en la base de datos
        for task in tasks.tasks:
            # Verificar que la tarea tenga un título y una descripción
            if not task.title or not task.description:
                flash('Todas las tareas deben tener un título y una descripción.', 'error')
                return redirect(url_for('routes.show_tasks', user_story_id=user_story_id))
            task_manager.create_task(
                title=task.title,
                description=task.description,
                priority=task.priority,
                effort_hours=task.effort_hours,
                status=task.status,
                assigned_to=task.assigned_to,
                category=task.category,
                risk_analysis=task.risk_analysis,
                risk_mitigation=task.risk_mitigation,
                user_story_id=user_story_id
            )
        flash('Tareas generadas y guardadas correctamente.', 'info')
    except Exception as e:
        flash(f'Error al generar las tareas: {str(e)}', 'error') 
    return redirect(url_for('routes.show_tasks', user_story_id=user_story_id))


# Eliminar una historia de usuario y sus tareas asociadas
@routes.route('/user-stories/<int:user_story_id>/delete', methods=['POST']) 
def delete_user_story(user_story_id):
    """
    Eliminar una historia de usuario y todas las tareas asociadas a ella.
    Esta función recibe el ID de una historia de usuario y elimina tanto la historia de usuario como todas las tareas asociadas a ella.
    Si la historia de usuario no se encuentra, se muestra un mensaje de error. Si la eliminación es exitosa, se muestra un mensaje de éxito.
    En caso de error durante la eliminación, se muestra un mensaje de error.    
    :param user_story_id: ID de la historia de usuario a eliminar.
    :type user_story_id: int
    :return: Redirige a la vista de historias de usuario con un mensaje de éxito o error.
    :rtype: flask.Response
    """
    # Obtener la historia de usuario por ID
    user_story = user_story_manager.get_user_story_by_id(user_story_id)
    if user_story is None:
        flash('Historia de usuario no encontrada.', 'error')
        return redirect(url_for('routes.user_stories'))
    
    try:
        task_manager.delete_tasks_by_user_story(user_story_id)
        user_story_manager.delete_user_story(user_story_id)
        flash('Historia de usuario y tareas asociadas eliminadas correctamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar la historia de usuario: {str(e)}', 'error')
    
    return redirect(url_for('routes.user_stories'))



