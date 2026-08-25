from pydantic import BaseModel
from typing import Optional, Dict, Any

class CommandCreate(BaseModel):
    repo_id: str
    text: str

class CommandResponse(BaseModel):
    id: str
    text: str
    intent: str
    parsed_args: Dict[str, Any]
    created_at: str
