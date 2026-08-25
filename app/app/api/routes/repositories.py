from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime

from ...core.database import db
from ...models.user import UserInDB
from ...schemas.repository import RepositoryResponse
from ..deps import get_current_user

router = APIRouter()

@router.get("", response_model=List[RepositoryResponse])
async def list_repositories(current_user: UserInDB = Depends(get_current_user)):
    cursor = db.db.repositories.find({"user_id": current_user.id})
    repos = []
    async for repo in cursor:
        repos.append(RepositoryResponse(
            id=str(repo["_id"]),
            owner=repo["owner"],
            name=repo["name"],
            full_name=repo["full_name"],
            url=repo["url"],
            default_branch=repo.get("default_branch", "main"),
        ))
    return repos

@router.post("/connect")
async def connect_repository(current_user: UserInDB = Depends(get_current_user)):
    # Implementation would use GitHub App installation flow or OAuth to add repos.
    # For now, we just return a message.
    return {"message": "Repository connection initiated, check GitHub"}
