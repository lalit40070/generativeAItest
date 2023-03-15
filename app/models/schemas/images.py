from typing import List, Optional
from fastapi import File, UploadFile

from pydantic import BaseModel, Field

from app.models.domain.images import Image, ImageType
from app.models.domain.users import User
from app.models.domain.packs import Pack
from app.models.schemas.rwschema import RWSchema
from datetime import datetime


class ImageInResponse(RWSchema):
    type: str
    url: str
    style: str
    created_at: datetime
    updated_at: datetime


class ImageInCreate(RWSchema):
    type: ImageType
    style: int
    user: str
    purchase: int

class DeleteImageInCreate(RWSchema):
    type: ImageType
    user: str
    purchase: int

class ImagineInUpdate(RWSchema):
    purchase: int


class ListOfImagesInResponse(RWSchema):
    images: List[ImageInResponse]
    images_count: int


class ImagesFilters(BaseModel):
    user: Optional[str] = None
    purchase: Optional [int] = None
    style: Optional[int] = None
    type: Optional[ImageType] = None