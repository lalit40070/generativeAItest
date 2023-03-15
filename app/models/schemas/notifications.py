from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.domain.notifications import Notification
from app.models.schemas.rwschema import RWSchema


class NotificationForResponse(RWSchema, Notification):
    notification: Notification

class NotificationInResponse(RWSchema):
    notification: Notification


class NotificationInUpdate(RWSchema):
    is_allowed: Optional[bool]


class NotificationInCreate(RWSchema):
    is_allowed: Optional[bool]
    user_id: str

class NotificationInUpdate(RWSchema):
    is_allowed: Optional[bool] = False
