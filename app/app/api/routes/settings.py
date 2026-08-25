from fastapi import APIRouter, Depends, HTTPException
from ...core.database import db
from ...models.user import UserInDB
from ...schemas.settings import SettingsUpdate, SettingsResponse, DeploymentTargetUpdate
from ..deps import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("", response_model=SettingsResponse)
async def get_settings(current_user: UserInDB = Depends(get_current_user)):
    return SettingsResponse(
        require_approval=current_user.settings.require_approval,
        telegram_chat_id=current_user.settings.telegram_chat_id,
        deployment_targets=[DeploymentTargetUpdate(**t.dict()) for t in current_user.settings.deployment_targets],
    )

@router.put("", response_model=SettingsResponse)
async def update_settings(settings_update: SettingsUpdate, current_user: UserInDB = Depends(get_current_user)):
    update_data = {}
    if settings_update.require_approval is not None:
        update_data["settings.require_approval"] = settings_update.require_approval
    if settings_update.telegram_chat_id is not None:
        update_data["settings.telegram_chat_id"] = settings_update.telegram_chat_id
    if settings_update.deployment_targets is not None:
        update_data["settings.deployment_targets"] = [t.dict() for t in settings_update.deployment_targets]
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.db.users.update_one({"_id": current_user.id}, {"$set": update_data})
    # Fetch updated user
    updated_user = await db.db.users.find_one({"_id": current_user.id})
    updated_user_model = UserInDB(**updated_user)
    return SettingsResponse(
        require_approval=updated_user_model.settings.require_approval,
        telegram_chat_id=updated_user_model.settings.telegram_chat_id,
        deployment_targets=[DeploymentTargetUpdate(**t.dict()) for t in updated_user_model.settings.deployment_targets],
    )
