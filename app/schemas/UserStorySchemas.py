from pydantic import BaseModel
from typing import List
from app.schemas.UserStorySchema import UserStorySchema

class UserStorySchemas(BaseModel):
    user_stories: List[UserStorySchema]