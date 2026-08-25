from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Optional

class RepositoryInDB(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    owner: str
    name: str
    full_name: str
    url: str
    default_branch: str = "main"
    webhook_id: Optional[int] = None
    connected_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: ObjectId

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
