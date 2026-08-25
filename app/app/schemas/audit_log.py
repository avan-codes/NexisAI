from pydantic import BaseModel
from typing import Optional, Dict, Any

class AuditLogResponse(BaseModel):
    id: str
    execution_id: Optional[str]
    actor: str
    action: str
    repo: str
    detail: str
    metadata: Dict[str, Any]
    timestamp: str
    ip: Optional[str]
    user_agent: Optional[str]
