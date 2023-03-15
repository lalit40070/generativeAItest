from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.domain.tasks import Task, TaskStatus
from app.models.domain.styles import Gender
from app.models.domain.users import User
from app.models.domain.packs import Pack
from app.models.schemas.rwschema import RWSchema
from datetime import datetime


class TaskInResponse(RWSchema):
    task_id: int
    user_identifier: str
    purchase_id: int
    style_list: list
    status: str
    created_at: datetime
    updated_at: datetime
     
    


class TaskInCreate(RWSchema):
    purchase_id: int
    user_identifier: str
    style_list: list[int]
    gender: Gender
    pack_id: str
    images_per_style: int

class TaskInUpdate(RWSchema):
    status: TaskStatus


class ListOfTasksInResponse(RWSchema):
    tasks: List[TaskInResponse]
    tasks_count: int


class TaskFilters(BaseModel):
    task_id: Optional[int] = None
    user: Optional[str] = None
    purchase: Optional[int] = None
    pack: Optional [str] = None
    status: Optional[TaskStatus] = None