from typing import List

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class Pack(IDModelMixin, DateTimeModelMixin, RWModel):
    pack_id: str
    pack_name: str
    pack_price: float
    images_per_pack: int