from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from typing import Optional, List
from datetime import datetime

from ...core.database import db
from ...models.user import UserInDB
from ...schemas.execution import (
    ExecutionDetail, ExecutionSummary, ExecutionListResponse, ApprovalRequest
)
from ..deps import get_current_user
from ...tasks.execution_runner import resume_execution_after_approval

router = APIRouter()

def _serialize_execution_summary(exec_doc, repo_doc=None, command_doc=None) -> ExecutionSummary:
    duration = None
    if exec_doc.get("updated_at") and exec_doc.get("created_at"):
        duration = (exec_doc["updated_at"] - exec_doc["created_at"]).total_seconds()
    return ExecutionSummary(
        id=str(exec_doc["_id"]),
        status=exec_doc["status"],
        repo_full_name=repo_doc["full_name"] if repo_doc else "unknown",
        command_text=command_doc["text"] if command_doc else "",
        created_at=exec_doc["created_at"].isoformat(),
        duration=duration,
    )

@router.get("", response_model=ExecutionListResponse)
async def list_executions(
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    repo_id: Optional[str] = None,
    search: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_user),
):
    query = {"user_id": current_user.id}
    if status:
        query["status"] = status
    if repo_id:
        query["repo_id"] = ObjectId(repo_id)
    if search:
        # search in command text by joining commands collection
        command_ids = []
        async for cmd in db.db.commands.find({"user_id": current_user.id, "text": {"$regex": search, "$options": "i"}}):
            command_ids.append(cmd["_id"])
        if command_ids:
            query["command_id"] = {"$in": command_ids}
        else:
            query["_id"] = None  # no results
    total = await db.db.executions.count_documents(query)
    total_pages = (total + limit - 1) // limit
    cursor = db.db.executions.find(query).sort("created_at", -1).skip((page-1)*limit).limit(limit)
    items = []
    async for exec_doc in cursor:
        repo_doc = await db.db.repositories.find_one({"_id": exec_doc["repo_id"]})
        command_doc = await db.db.commands.find_one({"_id": exec_doc["command_id"]})
        items.append(_serialize_execution_summary(exec_doc, repo_doc, command_doc))
    return ExecutionListResponse(items=items, total=total, page=page, limit=limit, total_pages=total_pages)

@router.get("/{execution_id}", response_model=ExecutionDetail)
async def get_execution(execution_id: str, current_user: UserInDB = Depends(get_current_user)):
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id), "user_id": current_user.id})
    if not exec_doc:
        raise HTTPException(status_code=404, detail="Execution not found")
    # Convert steps
    steps = []
    for step in exec_doc.get("steps", []):
        steps.append({
            "name": step["name"],
            "status": step["status"],
            "started_at": step.get("started_at").isoformat() if step.get("started_at") else None,
            "finished_at": step.get("finished_at").isoformat() if step.get("finished_at") else None,
            "logs": step.get("logs", []),
            "output": step.get("output", {}),
            "diff": step.get("diff", []),
            "pr_url": step.get("pr_url"),
            "deploy_url": step.get("deploy_url"),
        })
    return ExecutionDetail(
        id=str(exec_doc["_id"]),
        command_id=str(exec_doc["command_id"]),
        repo_id=str(exec_doc["repo_id"]),
        user_id=str(exec_doc["user_id"]),
        status=exec_doc["status"],
        branch_name=exec_doc.get("branch_name"),
        commit_sha=exec_doc.get("commit_sha"),
        steps=steps,
        current_step=exec_doc.get("current_step", 0),
        created_at=exec_doc["created_at"].isoformat(),
        updated_at=exec_doc["updated_at"].isoformat(),
    )

@router.post("/{execution_id}/approve")
async def approve_execution(execution_id: str, current_user: UserInDB = Depends(get_current_user)):
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id), "user_id": current_user.id})
    if not exec_doc:
        raise HTTPException(status_code=404, detail="Execution not found")
    if exec_doc["status"] != "awaiting_approval":
        raise HTTPException(status_code=400, detail="Execution is not awaiting approval")
    # Set current step to approved and resume
    current_step = exec_doc.get("current_step", 0)
    if current_step >= len(exec_doc["steps"]):
        raise HTTPException(status_code=400, detail="Invalid step")
    await db.db.executions.update_one(
        {"_id": ObjectId(execution_id)},
        {"$set": {f"steps.{current_step}.status": "succeeded", "status": "running", "updated_at": datetime.utcnow()}}
    )
    # Resume workflow in background
    import asyncio
    asyncio.create_task(resume_execution_after_approval(execution_id))
    return {"message": "Approved, resuming"}

@router.post("/{execution_id}/reject")
async def reject_execution(execution_id: str, approval: ApprovalRequest, current_user: UserInDB = Depends(get_current_user)):
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id), "user_id": current_user.id})
    if not exec_doc:
        raise HTTPException(status_code=404, detail="Execution not found")
    if exec_doc["status"] != "awaiting_approval":
        raise HTTPException(status_code=400, detail="Execution is not awaiting approval")
    await db.db.executions.update_one(
        {"_id": ObjectId(execution_id)},
        {"$set": {"status": "failed", "updated_at": datetime.utcnow()}}
    )
    # Optionally rollback: delete branch, close PR (implemented later)
    return {"message": "Rejected"}

@router.post("/{execution_id}/retry")
async def retry_execution(execution_id: str, current_user: UserInDB = Depends(get_current_user)):
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id), "user_id": current_user.id})
    if not exec_doc:
        raise HTTPException(status_code=404, detail="Execution not found")
    # Create new execution based on same command
    command_doc = await db.db.commands.find_one({"_id": exec_doc["command_id"]})
    if not command_doc:
        raise HTTPException(status_code=400, detail="Original command not found")
    new_exec = {
        "command_id": command_doc["_id"],
        "repo_id": exec_doc["repo_id"],
        "user_id": current_user.id,
        "status": "pending",
        "steps": [],
        "current_step": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = await db.db.executions.insert_one(new_exec)
    new_id = result.inserted_id
    import asyncio
    asyncio.create_task(run_execution_workflow(str(new_id)))
    return {"new_execution_id": str(new_id)}
