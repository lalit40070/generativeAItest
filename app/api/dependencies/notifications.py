from typing import Optional

from fastapi import Depends, HTTPException, Path, Query
from starlette import status

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.notifications import NotificationRepository
from app.models.domain.notifications import Notification
from app.models.domain.users import User
from app.resources import strings


async def get_user_by_id_from_path(
    user_id: str = Path(...),
    notifications_repo: NotificationRepository = Depends(get_repository(NotificationRepository))
   
) -> Notification:
    try:
        return await notifications_repo.get_notification_status_of_user(user_id=user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.PACK_DOES_NOT_EXIST_ERROR,
        )