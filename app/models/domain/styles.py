from typing import List

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from enum import Enum


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class Style(IDModelMixin, DateTimeModelMixin, RWModel):
    style_id: int
    name: str
    prompt_positive: str
    prompt_negative: str
    seed: int
    type: str
    gender: Gender
    sample_image: str
    diffusion_version: str