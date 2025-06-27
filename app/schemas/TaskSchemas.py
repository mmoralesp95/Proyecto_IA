from pydantic import BaseModel
from typing import List
from app.schemas.TaskSchema import TaskSchema

class TaskSchemas(BaseModel):
    tasks: List[TaskSchema]