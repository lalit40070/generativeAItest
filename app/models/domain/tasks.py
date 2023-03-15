from typing import List

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.models.domain.purchase import Purchase
from app.models.domain.users import User
from app.models.domain.styles import Gender
from app.models.domain.packs import Pack
from enum import Enum

class TaskStatus(str, Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'
    SUBMITTED = 'submitted'

    def toString(self):
        if self == "success":
            return "success"
        elif self == "failure":
            return "failure"
        else: 
            return "submitted"

class Task(IDModelMixin, DateTimeModelMixin, RWModel):
    task_id: int
    purchase_id: Purchase
    user_identifier: User
    style_list: List[int]
    gender: Gender
    pack_id: Pack
    status: TaskStatus
