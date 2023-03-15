from typing import List, Optional, Sequence, Union

from asyncpg import Connection, Record
from pypika import Query

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.queries.tables import (
    Parameter,
    packs,
    users,
)
from app.db.repositories.base import BaseRepository
from app.models.domain.packs import Pack
from app.models.domain.users import User


class PacksRepository(BaseRepository):  # noqa: WPS214
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)

    async def create_pack(  # noqa: WPS211
        self,
        *,
        pack_id: str,
        pack_name: str,
        pack_price: float,
        images_per_pack: int,
    ) -> Pack:
        async with self.connection.transaction():
            pack_row = await queries.create_new_pack(
                self.connection,
                pack_id=pack_id,
                pack_name=pack_name,
                pack_price=pack_price,
                images_per_pack=images_per_pack,
                
            )

        return await self._get_pack_from_db_record(
            pack_row=pack_row,
        )

    async def update_pack(  # noqa: WPS211
        self,
        *,
        pack: Pack,
        pack_name: Optional[str] = None,
        pack_price: Optional[str] = None,
        images_per_pack: Optional[int] = None,
    ) -> Pack:
        updated_pack = pack.copy(deep=True)
        updated_pack.pack_name = pack_name
        updated_pack.pack_price = pack_price or pack.pack_price
        updated_pack.images_per_pack = images_per_pack or pack.images_per_pack
        

        async with self.connection.transaction():
            updated_pack.updated_at = await queries.update_pack(
                self.connection,
                pack_id=pack.pack_id,
                pack_name=updated_pack.pack_name,
                pack_price=updated_pack.pack_price,
                images_per_pack=updated_pack.images_per_pack,
                
            )

        return updated_pack

    async def delete_pack(self, *, pack: Pack) -> None:
        async with self.connection.transaction():
            await queries.delete_pack(
                self.connection,
                pack_id=pack.pack_id,
            )



    async def get_all_packs(  # noqa: WPS211
        self,
    ) -> List[Pack]:
    
        pack_rows = await self.connection.fetch("select * from packs")
        packs = [await self._get_pack_from_db_record(
            pack_row=pack_row) for pack_row in pack_rows ]
        
        return packs
        


    async def get_pack_by_id(  # noqa: WPS211
        self,
        *,
        pack_id: str
    ) -> Pack:
    
        async with self.connection.transaction():
            pack_row = await queries.get_pack(
                self.connection,
                pack_id=pack_id,
                
            )
        return await self._get_pack_from_db_record(pack_row=pack_row)
           

    async def _get_pack_from_db_record(
        self,
        *,
        pack_row: Record,
        
    ) -> Pack:
        if pack_row is not None:
            return Pack(
                id_= pack_row["id"],
                pack_id=pack_row["pack_id"],
                pack_name=pack_row["pack_name"],
                pack_price=pack_row["pack_price"],
                images_per_pack=pack_row["images_per_pack"],
                created_at=pack_row["created_at"],
                updated_at=pack_row["updated_at"],
            )
        else:
            return Pack(id_= 0,
                pack_id=0,
                pack_name="None",
                pack_price=0,
                images_per_pack=0,
            )
