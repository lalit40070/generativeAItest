from typing import List

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.models.domain.styles import Style
from app.models.domain.users import User
from app.models.domain.purchase import Purchase
from enum import Enum

class ImageType(str, Enum):
    SELFIE = 'selfie'
    AVATAR = 'avatar'

    def toString(self):
        if self == "avatar":
            return "avatar"
        else:
            return "selfie"
        
class Image(IDModelMixin, DateTimeModelMixin, RWModel):
    type: ImageType
    url: str
    style: int
    user: User
    purchase: Purchase


   