from pydantic import BaseModel
from typing import Optional

class TaskModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = ""
    effort_hours: Optional[int] = None
    status: Optional[str] = ""
    assigned_to: Optional[str] = ""
    category: Optional[str] = ""
    risk_analysis: Optional[str] = ""
    risk_mitigation: Optional[str] = ""