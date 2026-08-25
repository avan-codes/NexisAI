from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class UserResponse(BaseModel):
    id: str
    github_id: int
    username: str
    avatar_url: Optional[str]
    email: Optional[str]
    settings: Dict[str, Any]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
