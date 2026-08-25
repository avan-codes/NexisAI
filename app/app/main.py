from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .core.database import connect_to_mongo, close_mongo_connection
from .core.logging import logger
from .api.router import api_router
from .api.routes import ws

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    logger.info("Connected to MongoDB")
    yield
    # Shutdown
    await close_mongo_connection()
    logger.info("Disconnected from MongoDB")

app = FastAPI(
    title="NexisAI API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

# WebSocket route is not under /api/v1
app.websocket("/ws/executions/{execution_id}")(ws.execution_ws)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
