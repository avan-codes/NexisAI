from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class StepLogResponse(BaseModel):
    level: str
    message: str
    timestamp: str

class DiffEntryResponse(BaseModel):
    file: str
    additions: int
    deletions: int
    patch: str

class StepResponse(BaseModel):
    name: str
    status: str
    started_at: Optional[str]
    finished_at: Optional[str]
    logs: List[StepLogResponse]
    output: Dict[str, Any]
    diff: List[DiffEntryResponse]
    pr_url: Optional[str]
    deploy_url: Optional[str]

class ExecutionSummary(BaseModel):
    id: str
    status: str
    repo_full_name: str
    command_text: str
    created_at: str
    duration: Optional[float]

class ExecutionDetail(BaseModel):
    id: str
    command_id: str
    repo_id: str
    user_id: str
    status: str
    branch_name: Optional[str]
    commit_sha: Optional[str]
    steps: List[StepResponse]
    current_step: int
    created_at: str
    updated_at: str

class ExecutionListResponse(BaseModel):
    items: List[ExecutionSummary]
    total: int
    page: int
    limit: int
    total_pages: int

class ApprovalRequest(BaseModel):
    reason: Optional[str] = None
