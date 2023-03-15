from typing import List, Optional, Sequence, Union

from asyncpg import Connection, Record
from pypika import Query
import aiohttp
import asyncio



from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.queries.tables import (
    Parameter,
    packs,
    users,
    style,
)
from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository
from app.db.repositories.packs import PacksRepository
from app.db.repositories.purchases import PurchasesRepository
from app.models.domain.purchase import Purchase, PurchaseStatus
from app.models.domain.users import User
from app.models.domain.tasks import Task, TaskStatus
from app.models.domain.styles import Gender
from app.services.post_requests import post_request, fire_and_forget
from app.models.domain.images import ImageType
from app.core.config import get_app_settings
from app.config.tasks import post_to_generate_avatars_api

SETTINGS = get_app_settings()

class TasksRepository(BaseRepository):  # noqa: WPS214
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._users_repo = UsersRepository(conn)
        self._packs_repo = PacksRepository(conn)
        self._purchase_repo = PurchasesRepository(conn)


    async def create_task(  # noqa: WPS211
        self,
        *,
        purchase_id: int,
        user_identifier: str,
        style_list: list[int],
        gender: str,
        pack_id: str,
        images_per_style: int
    ) -> Task:
        status = "submitted"

        
        async with self.connection.transaction():
            task_row = await queries.create_new_task(
                self.connection,
                purchase_id= purchase_id,
                user_identifier=user_identifier,
                style_list= ','.join(str(e) for e in style_list),
                gender=gender,
                pack_id=pack_id, 
                task_status=status,
            )
        task_row_parsed = await self._get_task_from_db_record(
                            task_row=task_row,
                    )
        image_row = await queries.get_images_row(self.connection,
                                                user_identifier=user_identifier, 
                                                purchase_id=purchase_id, 
                                                type=ImageType.SELFIE.toString())
        
        request_body = dict({"user_id": user_identifier,
                        "styles_list": style_list,
                        "purchase_id": purchase_id,
                         "gender": gender,
                         "task_id": task_row["id"],
                         "images":image_row["url"],
                         "image_count":images_per_style})
        in_queue_tasks = await self.connection.fetch("select * from tasks where task_status='{}'".
                                                    format(TaskStatus.SUBMITTED.toString()))

        #celery_task = post_to_generate_avatars_api.apply_async(args=[request_body, len(in_queue_tasks)])

        """ Without Celery """
        fire_and_forget(SETTINGS.ds_api_url, body=request_body, request_type="POST")
               
        return task_row_parsed

    async def update_task(  # noqa: WPS211
        self,
        *,
        task: Task,
        task_status: Optional[TaskStatus],
    ) -> Task:
        updated_task = task.copy(deep=True)
        updated_task.status = task_status or task.status

        async with self.connection.transaction():
            updated_task.updated_at = await queries.update_task(
                self.connection,
                task_id=task.task_id,
                task_status=task_status or updated_task.status
                
            )

        return updated_task

    # async def delete_purchase(self, *, purchase: Purchase) -> None:
    #     async with self.connection.transaction():
    #         await queries.delete_purchase(
    #             self.connection,
    #             purchase_id=purchase.purchase_id,
    #         )



    async def get_all_tasks(  # noqa: WPS211
        self,
    ) -> List[Task]:
    
        task_rows = await self.connection.fetch("select * from tasks")
        tasks = [await self._get_task_from_db_record(
            task_row=task_row) for task_row in task_rows ]
        
        return tasks
        



    async def get_task_by_id(  # noqa: WPS211
        self,
        *,
        task_id: int
    ) -> Task:
        async with self.connection.transaction():
            task_row = await queries.get_task_by_id(
                self.connection,
                task_id=task_id,
                
            )
        return await self._get_task_from_db_record(task_row=task_row)
           

    async def _get_task_from_db_record(
        self,
        *,
        task_row: Record,
        
    ) -> Task:
        if task_row is not None:
            return Task(
                task_id=task_row["id"],
                purchase_id =await self._purchase_repo.get_purchase_by_id(
                    purchase_id=task_row["purchase_id"])
                ,
                user_identifier =await self._users_repo.get_user_by_identifier(
                    user_identifier=task_row["user_identifier"])
                ,
                pack_id =await self._packs_repo.get_pack_by_id(
                    pack_id=task_row["pack_id"])
                ,
                style_list=task_row["style_list"].split(','),
                status=TaskStatus(task_row["task_status"]),
                gender = Gender(task_row["gender"]),
                created_at=task_row["created_at"],
                updated_at=task_row["updated_at"],
            )


        else:
            return Task(
                task_id=0,
                purchase_id =await self._purchase_repo.get_purchase_by_id(
                    purchase_id=0)
                ,
                user_identifier =await self._users_repo.get_user_by_identifier(
                    user_identifier="")
                ,
                pack_id =await self._packs_repo.get_pack_by_id(
                    pack_id=0)
                ,
                style_list="",
                status="failure",
                gender = "other",
                created_at=task_row["created_at"],
                updated_at=task_row["updated_at"],
            )
