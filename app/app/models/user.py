from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

class DeploymentTarget(BaseModel):
    name: str
    url: str
    enabled: bool = True

class UserSettings(BaseModel):
    require_approval: bool = False
    telegram_chat_id: Optional[str] = None
    deployment_targets: List[DeploymentTarget] = []

class UserInDB(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    github_id: int
    username: str
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    access_token: str  # encrypted later
    settings: UserSettings = UserSettings()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
