from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserStorySchema(BaseModel):
    id: Optional[int]
    project: str
    role: str
    goal: str
    reason: str
    description: Optional[str]
    priority: Optional[str]
    story_points: Optional[int]
    effort_hours: Optional[float]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True