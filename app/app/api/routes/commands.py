from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from bson import ObjectId
from typing import Optional, List
from datetime import datetime

from ...core.database import db
from ...models.user import UserInDB
from ...models.command import CommandInDB
from ...schemas.command import CommandCreate, CommandResponse
from ..deps import get_current_user
from ...services.langgraph_workflow import parse_command_intent
from ...tasks.execution_runner import run_execution_workflow

router = APIRouter()

@router.post("", response_model=dict)
async def create_command(
    command_data: CommandCreate,
    background_tasks: BackgroundTasks,
    current_user: UserInDB = Depends(get_current_user),
):
    # Validate repo belongs to user
    repo = await db.db.repositories.find_one({"_id": ObjectId(command_data.repo_id), "user_id": current_user.id})
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    # Parse intent
    intent, parsed_args = parse_command_intent(command_data.text)
    # Create command document
    command_doc = {
        "user_id": current_user.id,
        "repo_id": ObjectId(command_data.repo_id),
        "text": command_data.text,
        "intent": intent,
        "parsed_args": parsed_args,
        "created_at": datetime.utcnow(),
    }
    result = await db.db.commands.insert_one(command_doc)
    command_id = result.inserted_id

    # Create execution document
    execution_doc = {
        "command_id": command_id,
        "repo_id": ObjectId(command_data.repo_id),
        "user_id": current_user.id,
        "status": "pending",
        "steps": [],
        "current_step": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    exec_result = await db.db.executions.insert_one(execution_doc)
    execution_id = exec_result.inserted_id

    # Schedule background task
    background_tasks.add_task(run_execution_workflow, str(execution_id))

    return {"execution_id": str(execution_id)}

@router.get("", response_model=List[CommandResponse])
async def list_commands(
    page: int = 1,
    limit: int = 20,
    repo_id: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_user),
):
    query = {"user_id": current_user.id}
    if repo_id:
        query["repo_id"] = ObjectId(repo_id)
    cursor = db.db.commands.find(query).sort("created_at", -1).skip((page-1)*limit).limit(limit)
    commands = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        commands.append(CommandResponse(
            id=doc["_id"],
            text=doc["text"],
            intent=doc["intent"],
            parsed_args=doc.get("parsed_args", {}),
            created_at=doc["created_at"].isoformat(),
        ))
    return commands
