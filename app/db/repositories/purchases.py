from typing import List, Optional, Sequence, Union

from asyncpg import Connection, Record
from pypika import Query

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
from app.models.domain.purchase import Purchase, PurchaseStatus
from app.models.domain.users import User
from app.models.domain.packs import Pack


class PurchasesRepository(BaseRepository):  # noqa: WPS214
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._users_repo = UsersRepository(conn)
        self._packs_repo = PacksRepository(conn)

    async def create_purchase(  # noqa: WPS211
        self,
        *,
        purchase_id: int,
        user: str,
        pack: str,
        style_list: List[int],
        purchase_status: str,
        
    ) -> Purchase:
        async with self.connection.transaction():
            purchase_row = await queries.create_new_purchase(
                self.connection,
                purchase_id=purchase_id,
                user_id=user,
                pack_id=pack,
                styles_list= ','.join(str(e) for e in style_list),
                purchase_status=purchase_status                        
            )

        return await self._get_purchase_from_db_record(
            purchase_row=purchase_row,
        )

    async def update_purchase(  # noqa: WPS211
        self,
        *,
        purchase: Purchase,
        purchase_status: Optional[PurchaseStatus],
    ) -> Purchase:
        updated_purchase = purchase.copy(deep=True)
        updated_purchase.purchase_status = purchase_status or purchase.purchase_status

        async with self.connection.transaction():
            updated_purchase.updated_at = await queries.update_purchase(
                self.connection,
                purchase_id=purchase.purchase_id,
                purchase_status=purchase_status or updated_purchase.purchase_status
                
            )

        return updated_purchase

    async def delete_purchase(self, *, purchase: Purchase) -> None:
        async with self.connection.transaction():
            await queries.delete_purchase(
                self.connection,
                purchase_id=purchase.purchase_id,
            )



    async def get_all_purchases(  # noqa: WPS211
        self,
    ) -> List[Purchase]:
    
        purchase_rows = await self.connection.fetch("select * from purchases")
        purchases = [await self._get_purchase_from_db_record(
            purchase_row=purchase_row) for purchase_row in purchase_rows ]
        
        return purchases
        


    async def get_purchase_by_id(  # noqa: WPS211
        self,
        *,
        purchase_id: int
    ) -> Purchase:
        async with self.connection.transaction():
            purchase_row = await queries.get_purchase(
                self.connection,
                purchase_id=purchase_id,
                
            )
        return await self._get_purchase_from_db_record(purchase_row=purchase_row)
           

    async def _get_purchase_from_db_record(
        self,
        *,
        purchase_row: Record,
        
    ) -> Purchase:
        if purchase_row is not None:
        
            return Purchase(
                purchase_id=purchase_row["purchase_id"],
                user =await self._users_repo.get_user_by_identifier(
                    user_identifier=purchase_row["user_identifier"])
                ,
                pack=await self._packs_repo.get_pack_by_id(
                    pack_id=purchase_row["pack_id"]
                ),
                style_list=purchase_row["styles_list"].split(','),
                purchase_status=PurchaseStatus(purchase_row["purchase_status"]),
                created_at=purchase_row["created_at"],
                updated_at=purchase_row["updated_at"],
            )
        else:
            return Purchase(
                purchase_id=0,
                user=await self._users_repo.get_user_by_identifier(
                    user_identifier="")
                ,
                pack=await self._packs_repo.get_pack_by_id(
                    pack_id=1
                ),
                style_list=[],
                purchase_status=PurchaseStatus("failure"),
                created_at=purchase_row["created_at"],
                updated_at=purchase_row["updated_at"],
                
            )
