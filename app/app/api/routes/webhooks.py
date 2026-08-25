from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import json

from ...core.config import settings
from ...core.database import db
from ...services.github import handle_github_event
from ...services.telegram import handle_telegram_update

router = APIRouter()

@router.post("/github")
async def github_webhook(request: Request):
    # Verify signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    body = await request.body()
    secret = settings.GITHUB_CLIENT_SECRET.encode()  # In production, use webhook secret
    expected = "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=401, detail="Invalid signature")
    event = request.headers.get("X-GitHub-Event")
    payload = json.loads(body)
    await handle_github_event(event, payload)
    return {"status": "ok"}

@router.post("/telegram")
async def telegram_webhook(request: Request):
    body = await request.json()
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret != settings.TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret")
    await handle_telegram_update(body)
    return {"status": "ok"}
