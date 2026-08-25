from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from bson import ObjectId
from typing import Optional

from ..core.security import decode_token
from ..core.database import db
from ..models.user import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user_id = payload["sub"]
    user = await db.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    user["_id"] = str(user["_id"])
    return UserInDB(**user)

async def get_current_user_ws(websocket: WebSocket) -> Optional[UserInDB]:
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return None
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        await websocket.close(code=1008)
        return None
    user_id = payload["sub"]
    user = await db.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        await websocket.close(code=1008)
        return None
    user["_id"] = str(user["_id"])
    return UserInDB(**user)
