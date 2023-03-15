from typing import List, Optional, Sequence, Union

from asyncpg import Connection, Record
from pypika import Query

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.queries.tables import (
    Parameter,
    notifications,
    users

)
from app.db.repositories.base import BaseRepository
from app.models.domain.notifications import Notification
from app.models.domain.users import User


class NotificationRepository(BaseRepository):  # noqa: WPS214
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)


    async def update_notification(  # noqa: WPS211
        self,
        *,
        notification: Notification,
        is_allowed: Optional[bool] = False,
       
    ) -> Notification:
        updated_notification = notification.copy(deep=True)
        updated_notification.is_allowed = is_allowed
    
        async with self.connection.transaction():
            updated_notification.updated_at = await queries.update_notification(
                self.connection,
                is_allowed = updated_notification.is_allowed,
                user_id = notification.user_id
                
            )

        return updated_notification


    async def get_notification_status_of_user(  # noqa: WPS211
        self,
        *,
        user_id: str
       
    ) -> Notification:
    
        async with self.connection.transaction():
            notification_row = await queries.get_notification(
                self.connection,
                user_id=user_id,
                            
            )
        return await self._get_notification_from_db_record(notification_row=notification_row)

                   
    async def _get_notification_from_db_record(
        self,
        *,
        notification_row: Record,
        
    ) -> Notification:
        
            return Notification(
                is_allowed = notification_row["is_allowed"],
                user_id = notification_row ["user_id"]
            )
