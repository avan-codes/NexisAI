from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import List, Optional, Dict, Any

class StepLog(BaseModel):
    level: str  # info, warning, error
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DiffEntry(BaseModel):
    file: str
    additions: int
    deletions: int
    patch: str

class ExecutionStep(BaseModel):
    name: str  # analyze_repo, create_branch, modify_files, run_tests, create_pr, deploy_preview, monitor
    status: str = "pending"  # pending, running, awaiting_approval, succeeded, failed
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    logs: List[StepLog] = []
    output: Dict[str, Any] = {}
    diff: List[DiffEntry] = []
    pr_url: Optional[str] = None
    deploy_url: Optional[str] = None

class ExecutionInDB(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    command_id: ObjectId
    repo_id: ObjectId
    user_id: ObjectId
    status: str = "pending"  # pending, running, awaiting_approval, succeeded, failed, rolled_back
    branch_name: Optional[str] = None
    commit_sha: Optional[str] = None
    steps: List[ExecutionStep] = []
    current_step: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
