from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Optional, Dict, Any

class CommandInDB(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    user_id: ObjectId
    repo_id: ObjectId
    text: str
    intent: str  # e.g., "update_frontend", "fix_bug", "add_feature"
    parsed_args: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
