from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.domain.purchase import Purchase, PurchaseStatus
from app.models.domain.users import User
from app.models.domain.packs import Pack
from app.models.schemas.rwschema import RWSchema
from datetime import datetime


class PurchaseInResponse(RWSchema):
    purchase_id: int
    user_identifier: str
    pack: str
    style_list: list
    created_at: datetime
    updated_at: datetime
    status: PurchaseStatus
    


class PurchaseInCreate(RWSchema):
    purchase_id: int
    user: str
    pack: str
    style_list: List[int]
    purchase_status: PurchaseStatus

class PurchaseInUpdate(RWSchema):
    purchase_status: PurchaseStatus


class ListOfPurchasesInResponse(RWSchema):
    purchases: List[PurchaseInResponse]
    purchases_count: int


class PurchaseFilters(BaseModel):
    purchase_id: Optional[int] = None
    user: Optional[str] = None
    pack: Optional [int] = None
    purchase_status: Optional[PurchaseStatus]