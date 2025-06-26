# app/services/task_manager.py

from app.models.task import Task
from app.db import SessionLocal

class TaskManager:
    def __init__(self):
        self.db = SessionLocal()

    def get_tasks_by_user_story(self, user_story_id):
        return self.db.query(Task).filter(Task.user_story_id == user_story_id).all()

    def create_task(self, title, description, priority, effort_hours, status, assigned_to, user_story_id, category=None, risk_analysis=None, risk_mitigation=None):
        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            effort_hours=effort_hours,
            status=status,
            assigned_to=assigned_to,
            user_story_id=user_story_id,
            category=category,
            risk_analysis=risk_analysis,
            risk_mitigation=risk_mitigation
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task
    
    def delete_tasks_by_user_story(self, user_story_id):
        tasks = self.db.query(Task).filter(Task.user_story_id == user_story_id).all()
        for task in tasks:
            self.db.delete(task)
        self.db.commit()


