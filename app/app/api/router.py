from fastapi import APIRouter
from .routes import auth, commands, executions, repositories, logs, webhooks, settings

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(commands.router, prefix="/commands", tags=["commands"])
api_router.include_router(executions.router, prefix="/executions", tags=["executions"])
api_router.include_router(repositories.router, prefix="/repos", tags=["repositories"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
