from pydantic import BaseModel
from typing import Optional

class RepositoryResponse(BaseModel):
    id: str
    owner: str
    name: str
    full_name: str
    url: str
    default_branch: str
