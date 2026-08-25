from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Optional
import asyncio
import json

from ...core.database import db
from ..deps import get_current_user_ws
from ...models.user import UserInDB

router = APIRouter()

@router.websocket("/ws/executions/{execution_id}")
async def execution_ws(websocket: WebSocket, execution_id: str):
    user = await get_current_user_ws(websocket)
    if not user:
        return
    await websocket.accept()
    try:
        while True:
            # Poll DB for execution status
            exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id), "user_id": user.id})
            if not exec_doc:
                await websocket.send_json({"type": "error", "message": "Execution not found"})
                await websocket.close()
                return
            # Send current status
            await websocket.send_json({
                "type": "execution_status",
                "status": exec_doc["status"],
                "steps": exec_doc.get("steps", []),
                "current_step": exec_doc.get("current_step", 0),
            })
            if exec_doc["status"] in ["succeeded", "failed", "rolled_back"]:
                await websocket.close()
                return
            await asyncio.sleep(2)  # Poll every 2 seconds
    except WebSocketDisconnect:
        pass
