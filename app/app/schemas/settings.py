from pydantic import BaseModel
from typing import Optional, List

class DeploymentTargetUpdate(BaseModel):
    name: str
    url: str
    enabled: bool = True

class SettingsUpdate(BaseModel):
    require_approval: Optional[bool] = None
    telegram_chat_id: Optional[str] = None
    deployment_targets: Optional[List[DeploymentTargetUpdate]] = None

class SettingsResponse(BaseModel):
    require_approval: bool
    telegram_chat_id: Optional[str]
    deployment_targets: List[DeploymentTargetUpdate]
