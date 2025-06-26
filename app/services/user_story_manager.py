from app.models.user_story import UserStory
from app.db import SessionLocal
from sqlalchemy.orm import joinedload

class UserStoryManager:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_user_stories(self):
        return (
        self.db.query(UserStory)
        .options(joinedload(UserStory.tasks))
        .order_by(UserStory.created_at.desc())
        .all()
    )
    
    def get_user_story_by_id(self, user_story_id):
        return self.db.query(UserStory).options(joinedload(UserStory.tasks)).filter(UserStory.id == user_story_id).first()

    def create_user_story(self, project, role, goal, reason, description, priority, story_points, effort_hours):
        new_story = UserStory(
            project=project,
            role=role,
            goal=goal,
            reason=reason,
            description=description,
            priority=priority,
            story_points=story_points,
            effort_hours=effort_hours
        )
        self.db.add(new_story)
        self.db.commit()
        self.db.refresh(new_story)
        return new_story

    def close(self):
        self.db.close()
    
    def delete_user_story(self, user_story_id):
        user_story = self.get_user_story_by_id(user_story_id)
        if user_story:
            self.db.delete(user_story)
            self.db.commit()
            return True
        return False

