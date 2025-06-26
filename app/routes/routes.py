from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.user_story_manager import UserStoryManager
from app.services.task_manager import TaskManager
from app.schemas.UserStorySchema import UserStorySchema
from app.schemas.TaskSchema import TaskSchemas
from openai import AzureOpenAI
import os
import json

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
    stories = user_story_manager.get_all_user_stories()
    return render_template('user-stories.html', stories=stories)

# Crear una nueva historia de usuario
@routes.route('/user-stories', methods=['POST'])
def add_user_story():
    prompt = request.form.get('prompt', '').strip()
    if not prompt:
        flash('Por favor, ingresa un prompt para generar tareas.')
        return redirect(url_for('routes.user_stories'))
    # Aquí podrías llamar a IA o a tu lógica de generación.
    
    try:
        flash('Generando historia de usuario...')
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
        user_story = completion.choices[0].message.parsed
    except Exception as e:
        flash(f'Error al generar la historia de usuario: {str(e)}')
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
        flash(f'Error al crear la historia de usuario: {str(e)}')
    return redirect(url_for('routes.user_stories'))

# Mostrar tareas de una historia de usuario
@routes.route('/user-stories/<int:user_story_id>/tasks', methods=['GET'])
def show_tasks(user_story_id):
    story = user_story_manager.get_user_story_by_id(user_story_id)
    if story is None:
        flash('Historia de usuario no encontrada.')
        return redirect(url_for('routes.user_stories'))
    
    tasks = task_manager.get_tasks_by_user_story(user_story_id)
    return render_template('tasks.html', story=story, tasks=tasks, user_story_id=user_story_id, user_story_title=story.project)

# Añadir una tarea a una historia de usuario con IA
@routes.route('/user-stories/<int:user_story_id>/tasks', methods=['POST'])
def add_task(user_story_id):
    user_story = user_story_manager.get_user_story_by_id(user_story_id)
    if user_story is None:
        flash('Historia de usuario no encontrada.')
        return redirect(url_for('routes.user_stories'))
    
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

        tasks = TaskSchemas(**tasks_data.model_dump())

        for task in tasks.tasks:
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
        flash('Tareas generadas y guardadas correctamente.')
    except Exception as e:
        flash(f'Error al generar las tareas: {str(e)}') 
    return redirect(url_for('routes.show_tasks', user_story_id=user_story_id))


# Eliminar una historia de usuario y sus tareas asociadas
@routes.route('/user-stories/<int:user_story_id>/delete', methods=['POST']) 
def delete_user_story(user_story_id):
    user_story = user_story_manager.get_user_story_by_id(user_story_id)
    if user_story is None:
        flash('Historia de usuario no encontrada.')
        return redirect(url_for('routes.user_stories'))
    
    try:
        task_manager.delete_tasks_by_user_story(user_story_id)
        user_story_manager.delete_user_story(user_story_id)
        flash('Historia de usuario y tareas asociadas eliminadas correctamente.')
    except Exception as e:
        flash(f'Error al eliminar la historia de usuario: {str(e)}')
    
    return redirect(url_for('routes.user_stories'))



