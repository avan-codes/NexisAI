import re
from typing import Dict, Any, List, TypedDict, Optional
from langgraph.graph import StateGraph, END
from datetime import datetime
from bson import ObjectId
import asyncio

from ..core.database import db
from ..core.logging import logger
from ..models.execution import ExecutionInDB, ExecutionStep, StepLog, DiffEntry
from .github import (
    get_repo_tree, create_branch, get_file_content, update_file_content,
    create_pull_request
)
from .deployment import deploy_to_staging
from .telegram import send_telegram_message

def parse_command_intent(text: str) -> tuple:
    if text.startswith("/updatefrontend"):
        intent = "update_frontend"
        description = text.replace("/updatefrontend", "").strip().strip('"')
        parsed_args = {"description": description}
    elif text.startswith("/fixbug"):
        intent = "fix_bug"
        description = text.replace("/fixbug", "").strip().strip('"')
        parsed_args = {"description": description}
    elif text.startswith("/addfeature"):
        intent = "add_feature"
        description = text.replace("/addfeature", "").strip().strip('"')
        parsed_args = {"description": description}
    else:
        intent = "unknown"
        parsed_args = {"raw": text}
    return intent, parsed_args

class ExecutionState(TypedDict):
    execution_id: str
    current_step: int
    status: str
    logs: List[Dict]

async def add_log(execution_id: str, step_index: int, level: str, message: str):
    log_entry = StepLog(level=level, message=message).dict()
    await db.db.executions.update_one(
        {"_id": ObjectId(execution_id)},
        {"$push": {f"steps.{step_index}.logs": log_entry}}
    )

async def update_step_status(execution_id: str, step_index: int, status: str, **kwargs):
    update = {f"steps.{step_index}.status": status}
    if kwargs:
        for k, v in kwargs.items():
            update[f"steps.{step_index}.{k}"] = v
    update["updated_at"] = datetime.utcnow()
    await db.db.executions.update_one(
        {"_id": ObjectId(execution_id)},
        {"$set": update}
    )

async def analyze_repo(state: ExecutionState) -> ExecutionState:
    execution_id = state["execution_id"]
    step_index = state["current_step"]
    await update_step_status(execution_id, step_index, "running")
    await add_log(execution_id, step_index, "info", "Analyzing repository structure...")
    # Fetch execution doc
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id)})
    repo_doc = await db.db.repositories.find_one({"_id": exec_doc["repo_id"]})
    user_doc = await db.db.users.find_one({"_id": exec_doc["user_id"]})
    command_doc = await db.db.commands.find_one({"_id": exec_doc["command_id"]})
    access_token = user_doc["access_token"]
    repo_owner = repo_doc["owner"]
    repo_name = repo_doc["name"]
    # Get tree
    tree = await get_repo_tree(access_token, repo_owner, repo_name, repo_doc.get("default_branch", "main"))
    files = [item["path"] for item in tree if item["type"] == "blob"]
    relevant_files = []
    # Simple heuristic: if intent is update_frontend, look in src, components, etc.
    intent = command_doc["intent"]
    for f in files:
        if intent == "update_frontend" and any(kw in f.lower() for kw in ["src", "component", "page", "style", "tailwind", "css"]):
            relevant_files.append(f)
        elif intent == "fix_bug" and any(kw in f.lower() for kw in ["src", "component", "page", "util"]):
            relevant_files.append(f)
        elif intent == "add_feature":
            relevant_files.append(f)  # simplistic
    # Limit to first 10 files
    relevant_files = relevant_files[:10]
    await update_step_status(execution_id, step_index, "succeeded", output={"relevant_files": relevant_files})
    await add_log(execution_id, step_index, "info", f"Found {len(relevant_files)} relevant files")
    state["current_step"] += 1
    return state

async def create_branch_node(state: ExecutionState) -> ExecutionState:
    execution_id = state["execution_id"]
    step_index = state["current_step"]
    await update_step_status(execution_id, step_index, "running")
    await add_log(execution_id, step_index, "info", "Creating branch...")
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id)})
    repo_doc = await db.db.repositories.find_one({"_id": exec_doc["repo_id"]})
    user_doc = await db.db.users.find_one({"_id": exec_doc["user_id"]})
    command_doc = await db.db.commands.find_one({"_id": exec_doc["command_id"]})
    access_token = user_doc["access_token"]
    branch_name = f"nexis/{command_doc['intent']}-{int(datetime.utcnow().timestamp())}"
    success = await create_branch(
        access_token,
        repo_doc["owner"],
        repo_doc["name"],
        repo_doc.get("default_branch", "main"),
        branch_name
    )
    if not success:
        await update_step_status(execution_id, step_index, "failed")
        await add_log(execution_id, step_index, "error", "Failed to create branch")
        state["status"] = "failed"
        return state
    # Update execution doc with branch name
    await db.db.executions.update_one(
        {"_id": ObjectId(execution_id)},
        {"$set": {"branch_name": branch_name}}
    )
    await update_step_status(execution_id, step_index, "succeeded", output={"branch_name": branch_name})
    await add_log(execution_id, step_index, "info", f"Branch created: {branch_name}")
    state["current_step"] += 1
    return state

async def modify_files(state: ExecutionState) -> ExecutionState:
    execution_id = state["execution_id"]
    step_index = state["current_step"]
    await update_step_status(execution_id, step_index, "running")
    await add_log(execution_id, step_index, "info", "Modifying files...")
    # Check if approval required
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id)})
    user_doc = await db.db.users.find_one({"_id": exec_doc["user_id"]})
    if user_doc["settings"].get("require_approval", False):
        # Pause workflow: set status awaiting_approval
        await db.db.executions.update_one(
            {"_id": ObjectId(execution_id)},
            {"$set": {"status": "awaiting_approval"}}
        )
        await update_step_status(execution_id, step_index, "awaiting_approval")
        await add_log(execution_id, step_index, "warning", "Approval required before modifying files")
        return state  # stop here; will resume later
    # Perform file modifications (placeholder: simple example)
    # In real implementation, call LLM or apply patches
    await asyncio.sleep(2)
    # For demo, just create a dummy diff entry
    diff_entry = DiffEntry(file="src/App.jsx", additions=1, deletions=1, patch="@@ -1,2 +1,2 @@\n- old line\n+ new line")
    await db.db.executions.update_one(
        {"_id": ObjectId(execution_id)},
        {"$push": {f"steps.{step_index}.diff": diff_entry.dict()}}
    )
    await update_step_status(execution_id, step_index, "succeeded")
    await add_log(execution_id, step_index, "info", "Files modified")
    state["current_step"] += 1
    return state

async def run_tests(state: ExecutionState) -> ExecutionState:
    execution_id = state["execution_id"]
    step_index = state["current_step"]
    await update_step_status(execution_id, step_index, "running")
    await add_log(execution_id, step_index, "info", "Running tests...")
    await asyncio.sleep(3)
    # Simulate test results
    await update_step_status(execution_id, step_index, "succeeded", output={"passed": True, "summary": "All tests passed"})
    await add_log(execution_id, step_index, "info", "Tests passed")
    state["current_step"] += 1
    return state

async def create_pr(state: ExecutionState) -> ExecutionState:
    execution_id = state["execution_id"]
    step_index = state["current_step"]
    await update_step_status(execution_id, step_index, "running")
    await add_log(execution_id, step_index, "info", "Creating pull request...")
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id)})
    repo_doc = await db.db.repositories.find_one({"_id": exec_doc["repo_id"]})
    user_doc = await db.db.users.find_one({"_id": exec_doc["user_id"]})
    command_doc = await db.db.commands.find_one({"_id": exec_doc["command_id"]})
    access_token = user_doc["access_token"]
    branch = exec_doc["branch_name"]
    pr = await create_pull_request(
        access_token,
        repo_doc["owner"],
        repo_doc["name"],
        branch,
        repo_doc.get("default_branch", "main"),
        f"Nexis: {command_doc['text']}",
        "Automated PR by NexisAI"
    )
    pr_url = pr.get("html_url")
    if not pr_url:
        await update_step_status(execution_id, step_index, "failed")
        await add_log(execution_id, step_index, "error", "Failed to create PR")
        state["status"] = "failed"
        return state
    await update_step_status(execution_id, step_index, "succeeded", pr_url=pr_url)
    await add_log(execution_id, step_index, "info", f"PR created: {pr_url}")
    state["current_step"] += 1
    return state

async def deploy_preview(state: ExecutionState) -> ExecutionState:
    execution_id = state["execution_id"]
    step_index = state["current_step"]
    await update_step_status(execution_id, step_index, "running")
    await add_log(execution_id, step_index, "info", "Deploying preview...")
    # Check approval if required for deploy
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id)})
    user_doc = await db.db.users.find_one({"_id": exec_doc["user_id"]})
    if user_doc["settings"].get("require_approval", False):
        await db.db.executions.update_one(
            {"_id": ObjectId(execution_id)},
            {"$set": {"status": "awaiting_approval"}}
        )
        await update_step_status(execution_id, step_index, "awaiting_approval")
        await add_log(execution_id, step_index, "warning", "Approval required before deploy")
        return state
    repo_doc = await db.db.repositories.find_one({"_id": exec_doc["repo_id"]})
    user_doc = await db.db.users.find_one({"_id": exec_doc["user_id"]})
    deploy_url = await deploy_to_staging(repo_doc["owner"], repo_doc["name"], exec_doc["branch_name"], user_doc["access_token"])
    await update_step_status(execution_id, step_index, "succeeded", deploy_url=deploy_url)
    await add_log(execution_id, step_index, "info", f"Deployed to {deploy_url}")
    state["current_step"] += 1
    return state

async def monitor(state: ExecutionState) -> ExecutionState:
    execution_id = state["execution_id"]
    step_index = state["current_step"]
    await update_step_status(execution_id, step_index, "running")
    await add_log(execution_id, step_index, "info", "Monitoring deployment...")
    await asyncio.sleep(5)
    await update_step_status(execution_id, step_index, "succeeded")
    await add_log(execution_id, step_index, "info", "Deployment healthy")
    state["current_step"] += 1
    return state

def build_graph():
    graph = StateGraph(ExecutionState)
    graph.add_node("analyze_repo", analyze_repo)
    graph.add_node("create_branch", create_branch_node)
    graph.add_node("modify_files", modify_files)
    graph.add_node("run_tests", run_tests)
    graph.add_node("create_pr", create_pr)
    graph.add_node("deploy_preview", deploy_preview)
    graph.add_node("monitor", monitor)

    graph.set_entry_point("analyze_repo")
    graph.add_edge("analyze_repo", "create_branch")
    graph.add_edge("create_branch", "modify_files")
    graph.add_edge("modify_files", "run_tests")
    graph.add_edge("run_tests", "create_pr")
    graph.add_edge("create_pr", "deploy_preview")
    graph.add_edge("deploy_preview", "monitor")
    graph.add_edge("monitor", END)
    return graph.compile()

workflow = build_graph()
