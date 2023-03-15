from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.domain.packs import Pack
from app.models.schemas.rwschema import RWSchema


class PackForResponse(RWSchema, Pack):
    pass

class PackInResponse(RWSchema):
    Pack: PackForResponse


class PackInCreate(RWSchema):
    pack_id: str
    pack_name: str
    pack_price: float
    images_per_pack: int


class PackInUpdate(RWSchema):
    pack_name: Optional[str] = None
    pack_price: Optional[float] = None
    images_per_pack: Optional[int] = None


class ListOfPacksInResponse(RWSchema):
    packs: List[PackForResponse]
    packs_count: int


class PackFilters(BaseModel):
    pack_id: Optional[str] = None
    pack_name: Optional[str] = None
    pack_price: Optional[str] = None
    images_per_pack: Optional[int] = None