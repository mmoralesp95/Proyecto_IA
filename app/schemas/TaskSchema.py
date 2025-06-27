from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskSchema(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    priority: Optional[str]
    effort_hours: Optional[float]
    status: Optional[str]
    category: Optional[str]
    risk_analysis: Optional[str]
    risk_mitigation: Optional[str]
    assigned_to: Optional[str]
    user_story_id: Optional[int]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

