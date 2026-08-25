from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
import httpx
from datetime import datetime
from bson import ObjectId

from ...core.config import settings
from ...core.security import create_access_token
from ...core.database import db
from ...models.user import UserInDB
from ...schemas.auth import TokenResponse, UserResponse
from ..deps import get_current_user

router = APIRouter()

@router.get("/github")
async def github_login():
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.GITHUB_REDIRECT_URI}"
        f"&scope=repo,workflow,read:org"
        f"&state=nexisai_state"  # In production, generate and store state
    )
    return RedirectResponse(github_auth_url)

@router.get("/callback")
async def github_callback(request: Request, code: str = None):
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get GitHub token")
        # Get user info
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_response.json()
        github_id = user_data["id"]
        username = user_data["login"]
        # Upsert user
        existing_user = await db.db.users.find_one({"github_id": github_id})
        now = datetime.utcnow()
        if existing_user:
            user_id = existing_user["_id"]
            await db.db.users.update_one(
                {"_id": user_id},
                {"$set": {"access_token": access_token, "updated_at": now, "avatar_url": user_data.get("avatar_url"), "email": user_data.get("email")}},
            )
        else:
            user_doc = {
                "github_id": github_id,
                "username": username,
                "avatar_url": user_data.get("avatar_url"),
                "email": user_data.get("email"),
                "access_token": access_token,
                "settings": {
                    "require_approval": False,
                    "telegram_chat_id": None,
                    "deployment_targets": [],
                },
                "created_at": now,
                "updated_at": now,
            }
            result = await db.db.users.insert_one(user_doc)
            user_id = result.inserted_id
        # Generate JWT
        token = create_access_token({"sub": str(user_id), "github_id": github_id})
        # Redirect to frontend with token
        redirect_url = f"{settings.FRONTEND_ORIGIN}/auth/callback?token={token}"
        return RedirectResponse(redirect_url)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserInDB = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user.id),
        github_id=current_user.github_id,
        username=current_user.username,
        avatar_url=current_user.avatar_url,
        email=current_user.email,
        settings=current_user.settings.dict(),
    )
