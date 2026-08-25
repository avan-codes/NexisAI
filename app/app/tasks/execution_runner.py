import asyncio
from bson import ObjectId
from ..core.database import db
from ..core.logging import logger
from ..services.langgraph_workflow import workflow
from datetime import datetime

async def run_execution_workflow(execution_id: str):
    logger.info(f"Starting execution workflow for {execution_id}")
    # Initialize steps in DB
    step_names = ["analyze_repo", "create_branch", "modify_files", "run_tests", "create_pr", "deploy_preview", "monitor"]
    steps = [{"name": name, "status": "pending"} for name in step_names]
    await db.db.executions.update_one(
        {"_id": ObjectId(execution_id)},
        {"$set": {"steps": steps, "status": "running", "updated_at": datetime.utcnow()}}
    )
    initial_state = {
        "execution_id": execution_id,
        "current_step": 0,
        "status": "running",
        "logs": [],
    }
    result = await workflow.ainvoke(initial_state)
    final_status = result.get("status", "succeeded")
    await db.db.executions.update_one(
        {"_id": ObjectId(execution_id)},
        {"$set": {"status": final_status, "updated_at": datetime.utcnow()}}
    )
    logger.info(f"Execution {execution_id} finished with status {final_status}")

async def resume_execution_after_approval(execution_id: str):
    # Find current step (awaiting approval) and set to succeeded, then continue
    exec_doc = await db.db.executions.find_one({"_id": ObjectId(execution_id)})
    if not exec_doc:
        return
    current_step = exec_doc.get("current_step", 0)
    if current_step < len(exec_doc["steps"]):
        await db.db.executions.update_one(
            {"_id": ObjectId(execution_id)},
            {"$set": {
                f"steps.{current_step}.status": "succeeded",
                "status": "running",
                "updated_at": datetime.utcnow(),
            }}
        )
        # Run workflow from current step
        # For simplicity, we restart from current step by setting state.current_step
        state = {
            "execution_id": execution_id,
            "current_step": current_step,
            "status": "running",
            "logs": [],
        }
        result = await workflow.ainvoke(state, config={"recursion_limit": 100})
        final_status = result.get("status", "succeeded")
        await db.db.executions.update_one(
            {"_id": ObjectId(execution_id)},
            {"$set": {"status": final_status, "updated_at": datetime.utcnow()}}
        )
