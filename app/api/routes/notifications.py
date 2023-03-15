from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette import status
from fastapi.responses import JSONResponse


from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.repositories.notifications import NotificationRepository
from app.models.domain.notifications import Notification
from app.api.dependencies.notifications import get_user_by_id_from_path
from app.models.domain.users import User
from app.models.schemas.notifications import (
    NotificationForResponse,
    NotificationInCreate,
    NotificationInResponse,
    NotificationInUpdate
)
from app.resources import strings
from app.services.packs import check_pack_exists


router = APIRouter()


@router.put(
    "/{user_id}",
    response_model=NotificationInResponse,
    name="notification:update-notifications",
)
async def update_notification_allowed_by_user(
    notifcation_update: NotificationInUpdate = Body(..., embed=True, alias="notification"),
    current_notification: Notification = Depends(get_user_by_id_from_path),
    notification_repo: NotificationRepository = Depends(get_repository(NotificationRepository)),
) -> NotificationInResponse:

    notification = await notification_repo.update_notification(
        notification = current_notification,
        is_allowed = notifcation_update.is_allowed
        
    )

    
    return NotificationInResponse(notification = NotificationInCreate.from_orm(notification))

