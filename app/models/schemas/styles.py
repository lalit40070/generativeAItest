from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.domain.styles import Style, Gender
from app.models.schemas.rwschema import RWSchema


class StyleForResponse(RWSchema, Style):
    pass

class StyleInResponse(RWSchema):
    style: Style


class StyleInCreate(RWSchema):
    style_id: int
    name: str
    prompt_positive: Optional[str] = None
    prompt_negative: Optional[str] = None
    seed: Optional[int] = None
    type: Optional[str] = None
    gender: Gender
    sample_image: str
    diffusion_version: Optional[str] = None


class StyleInUpdate(RWSchema):
    name: str
    prompt_positive: Optional[str] = None
    prompt_negative: Optional[str] = None
    seed: Optional[int] = None
    type: Optional[str] = None
    gender: Optional[Gender] = None
    sample_image: Optional[str] = None
    diffusion_version: Optional[str] = None


class ListOfStylesInResponse(RWSchema):
    styles: List[StyleForResponse]
    styles_count: int


class StyleFilters(BaseModel):
    style_id: Optional[int] = None
    diffusion_version: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    gender: Optional[str] = None
