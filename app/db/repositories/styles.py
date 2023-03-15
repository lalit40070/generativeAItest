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
from app.models.domain.styles import Style,Gender
from app.models.domain.users import User
from app.services.s3_generate_presigned_urls import gen_pre_signed_url, gen_cloud_front_url
from app.services.s3_connector import s3_connector


class StylesRepository(BaseRepository):  # noqa: WPS214
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)

    async def create_style(  # noqa: WPS211
        self,
        *,
        style_id: int,
        name: str,
        prompt_positive: str,
        prompt_negative: str,
        seed: int,
        type: str,
        gender: str,
        sample_image: str,
        diffusion_version: str,
        
    ) -> Style:
        async with self.connection.transaction():
            style_row = await queries.create_new_style(
                self.connection,
                style_id=style_id,
                name=name,
                prompt_positive=prompt_positive,
                prompt_negative=prompt_negative,
                seed=seed,
                type=type,
                gender=gender,
                sample_image=sample_image,
                diffusion_version=diffusion_version
                
            )

        return await self._get_style_from_db_record(
            style_row=style_row,
        )

    async def update_style(  # noqa: WPS211
        self,
        *,
        style: Style,
        name: Optional[str] = None,
        prompt_positive: Optional[str] = None,
        prompt_negative: Optional[str] = None,
        seed: Optional[int] = None,
        type: Optional[str] = None,
        gender: Optional[Gender] = None,
        sample_image: Optional[str] = None,
        diffusion_version: Optional[str],
    ) -> Style:
        updated_style = style.copy(deep=True)
        updated_style.name = name or style.name
        updated_style.prompt_positive = prompt_positive or updated_style.prompt_positive
        updated_style.prompt_negative = prompt_negative or updated_style.prompt_negative
        updated_style.seed = seed or updated_style.seed
        updated_style.type = type or updated_style.type
        updated_style.gender = gender or updated_style.gender
        updated_style.sample_image = sample_image or style.sample_image
        updated_style.diffusion_version = diffusion_version or style.diffusion_version

        async with self.connection.transaction():
            updated_style.updated_at = await queries.update_style(
                self.connection,
                style_id=style.style_id,
                name=updated_style.name,
                prompt_positive=updated_style.prompt_positive,
                prompt_negative=updated_style.prompt_negative,
                seed=updated_style.seed,
                type=updated_style.type,
                gender=updated_style.gender,
                sample_image=updated_style.sample_image,
                diffusion_version=updated_style.diffusion_version
                
            )

        return updated_style

    async def delete_style(self, *, style: Style) -> None:
        async with self.connection.transaction():
            await queries.delete_style(
                self.connection,
                style_id=style.style_id,
            )



    async def get_all_styles(  # noqa: WPS211
        self,
    ) -> List[Style]:
    
        style_rows = await self.connection.fetch("select * from style")
        styles = [await self._get_style_from_db_record(
            style_row=style_row) for style_row in style_rows ]
        s3_connector_obj = s3_connector()
        style_urls = [gen_cloud_front_url(style['url']) for style in styles]
        
        return styles
        
    async def filter_styles(
        self, 
        style_id: Optional[int]= None,
        name: Optional[str] = None,
        type: Optional[str] = None,
        gender: Optional[Gender] = None,
        diffusion_version: Optional[str]= None
    ) -> List[Style]:
        query = Query.from_(
            style,
        ).select(
            style.style_id,
            style.name,
            style.prompt_positive,
            style.prompt_negative,
            style.seed,
            style.type,
            style.gender,
            style.sample_image,
            style.diffusion_version,
            style.created_at,
            style.updated_at         
        ).where((style.style_id == style_id) | (style.name == name) | (style.type == type) 
                | (style.gender == gender) | (style.diffusion_version == diffusion_version))

        style_rows = await self.connection.fetch(query.get_sql())

        styles = [await self._get_style_from_db_record(
            style_row=style_row) for style_row in style_rows]

        return styles


    async def get_style_by_id(  # noqa: WPS211
        self,
        *,
        style_id: int
    ) -> Style:
    
        async with self.connection.transaction():
            style_row = await queries.get_style(
                self.connection,
                style_id=style_id,
                
            )
        return await self._get_style_from_db_record(style_row=style_row)
           

    async def _get_style_from_db_record(
        self,
        *,
        style_row: Record,
        
    ) -> Style:
        s3_connector_obj = s3_connector()
        if style_row is not None:
            return Style(
                style_id=style_row["style_id"],
                name=style_row["name"],
                prompt_positive=style_row["prompt_positive"],
                prompt_negative=style_row["prompt_negative"],
                seed=style_row["seed"],
                type=style_row["type"],
                gender=Gender(style_row["gender"]),
                sample_image=gen_cloud_front_url(style_row["sample_image"]),
                diffusion_version=style_row["diffusion_version"],
                created_at=style_row["created_at"],
                updated_at=style_row["updated_at"],
            )
        else:
            return Style(
                style_id=0,
                name="",
                prompt_positive="",
                prompt_negative="",
                seed=0,
                type="",
                gender=Gender("other"),
                sample_image="",
                diffusion_version="",
                
            )
