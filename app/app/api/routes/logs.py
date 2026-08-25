from fastapi import APIRouter, Depends, Query, Response
from typing import Optional
from bson import ObjectId
from datetime import datetime
import csv
import io

from ...core.database import db
from ...models.user import UserInDB
from ...schemas.audit_log import AuditLogResponse
from ..deps import get_current_user

router = APIRouter()

@router.get("", response_model=List[AuditLogResponse])
async def get_logs(
    page: int = 1,
    limit: int = 50,
    execution_id: Optional[str] = None,
    actor: Optional[str] = None,
    action: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_user),
):
    query = {}
    if execution_id:
        query["execution_id"] = ObjectId(execution_id)
    if actor:
        query["actor"] = actor
    if action:
        query["action"] = action
    if from_date or to_date:
        date_query = {}
        if from_date:
            date_query["$gte"] = datetime.fromisoformat(from_date)
        if to_date:
            date_query["$lte"] = datetime.fromisoformat(to_date)
        if date_query:
            query["timestamp"] = date_query
    cursor = db.db.audit_logs.find(query).sort("timestamp", -1).skip((page-1)*limit).limit(limit)
    logs = []
    async for log in cursor:
        logs.append(AuditLogResponse(
            id=str(log["_id"]),
            execution_id=str(log.get("execution_id")) if log.get("execution_id") else None,
            actor=log["actor"],
            action=log["action"],
            repo=log.get("repo", ""),
            detail=log.get("detail", ""),
            metadata=log.get("metadata", {}),
            timestamp=log["timestamp"].isoformat(),
            ip=log.get("ip"),
            user_agent=log.get("user_agent"),
        ))
    return logs

@router.get("/export")
async def export_logs_csv(
    execution_id: Optional[str] = None,
    actor: Optional[str] = None,
    action: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_user),
):
    # Similar query as above, but return CSV
    query = {}
    if execution_id:
        query["execution_id"] = ObjectId(execution_id)
    if actor:
        query["actor"] = actor
    if action:
        query["action"] = action
    if from_date or to_date:
        date_query = {}
        if from_date:
            date_query["$gte"] = datetime.fromisoformat(from_date)
        if to_date:
            date_query["$lte"] = datetime.fromisoformat(to_date)
        if date_query:
            query["timestamp"] = date_query
    cursor = db.db.audit_logs.find(query).sort("timestamp", -1)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp", "actor", "action", "repo", "detail"])
    async for log in cursor:
        writer.writerow([log["timestamp"].isoformat(), log["actor"], log["action"], log.get("repo", ""), log.get("detail", "")])
    output.seek(0)
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=audit_logs.csv"})
