from typing import List

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.models.domain.styles import Style
from app.models.domain.users import User
from app.models.domain.packs import Pack
from enum import Enum

class PurchaseStatus(str, Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'

class Purchase(IDModelMixin, DateTimeModelMixin, RWModel):
    purchase_id: int
    user: User
    pack: Pack
    style_list: List[int]
    purchase_status: PurchaseStatus