from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Optional, Dict, Any

class AuditLogInDB(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    execution_id: Optional[ObjectId] = None
    actor: str  # GitHub username or "system"
    action: str  # create_branch, modify_file, run_tests, create_pr, deploy, approve, reject, etc.
    repo: str
    detail: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ip: Optional[str] = None
    user_agent: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
