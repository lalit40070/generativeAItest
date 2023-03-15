from typing import List, Optional, Sequence, Union
from fastapi import File, UploadFile

from asyncpg import Connection, Record
from pypika import Query
from botocore.client import BaseClient


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
from app.db.repositories.purchases import PurchasesRepository
from app.models.domain.purchase import Purchase, PurchaseStatus
from app.models.domain.users import User
from app.models.domain.packs import Pack
from app.models.domain.images import Image
from app.services.s3_uploader import upload_file_to_bucket
from app.services.s3_fetch_all_images import delete_user_selfies


class ImageRepository(BaseRepository):  # noqa: WPS214
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._users_repo = UsersRepository(conn)
        self._purchase_repo = PurchasesRepository(conn)

    async def create_images(  # noqa: WPS211
        self,
        *,
        type: str,
        files: List[UploadFile],
        style: int,
        user: str,
        purchase: int,
        s3: BaseClient
    ) -> Image:
        url = upload_file_to_bucket(s3_client=s3, files=files, user_id=user, _type=type, purchase=purchase, style_id=style)
        
        
        async with self.connection.transaction():
            image_row = await queries.create_images(
                self.connection,
                type=type,
                url=url,
                style=style,
                user_id=user, 
                purchase_id=purchase,                        
            ) 
        return await self._get_images_from_db_record(
            image_row=image_row,
        )

    async def delete_user_selfies(
        self,
        type: str,
        user: str,
        purchase: int,
        s3:BaseClient
    ) -> None:
        delete_user_selfies(folder=type, user=user, purchase=purchase)


           

    async def _get_images_from_db_record(
        self,
        *,
        image_row: Record,
        
    ) -> Image:
        
        if image_row is not None:
            return Image(
                type = image_row["type"],
                url = image_row["url"],
                style = image_row["style"],
                user =await self._users_repo.get_user_by_identifier(
                    user_identifier=image_row["user_identifier"])
                ,
                purchase=await self._purchase_repo.get_purchase_by_id(
                    purchase_id=image_row["purchase_id"]
                ),
                created_at=image_row["created_at"],
                updated_at=image_row["updated_at"],
               
            )
        else:
            return Image(
                type = "",
                url = "",
                style = "",
                user =await self._users_repo.get_user_by_identifier(
                    user_id="")
                ,
                purchase=await self._purchase_repo.get_purchase_by_id(
                    purchase=0
                ),
                created_at=image_row["created_at"],
                updated_at=image_row["updated_at"],
               
            )
