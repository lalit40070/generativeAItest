from datetime import datetime
from typing import Optional

from pypika import Parameter as CommonParameter, Query, Table
from app.models.domain.styles import Gender


class Parameter(CommonParameter):
    def __init__(self, count: int) -> None:
        super().__init__("${0}".format(count))


class TypedTable(Table):
    __table__ = ""

    def __init__(
        self,
        name: Optional[str] = None,
        schema: Optional[str] = None,
        alias: Optional[str] = None,
        query_cls: Optional[Query] = None,
    ) -> None:
        if name is None:
            if self.__table__:
                name = self.__table__
            else:
                name = self.__class__.__name__

        super().__init__(name, schema, alias, query_cls)


class Users(TypedTable):
    __table__ = "users"

    id: int
    username: str
    identifier: str
    id_for_apple:str
    is_active: bool


class Packs(TypedTable):
    __table__ = "pack"

    id: int
    pack_id: str
    pack_name: str
    pack_price: float
    images_per_pack: int
    created_at: datetime
    updated_at: datetime


class Notifications(TypedTable):
    __table__ = "notifications"

    is_allowed:bool
    user_id: str


class Styles(TypedTable):
    __table__ = "style"

    style_id: int
    name: str
    prompt_positive: str
    prompt_negative: str
    seed: int
    type: str
    gender: str
    sample_image: str
    diffusion_version: str


class Purchases(TypedTable):
    __table__ = "purchases"

    purchase_id:int
    user_identifier: str
    pack_id: int
    styles_list: str
    purchase_status: str


class Images(TypedTable):
    __table__ ="images"
    type: str
    url: str
    style: int
    user_id: int
    purchase_id: int


class Tasks(TypedTable):
    __table__ = "tasks"
    task_id: int
    user_identifier: str
    style_list: list
    gender: str
    pack_id: int
    task_status: str


users = Users()
packs = Packs()
notifications = Notifications()
style = Styles()
Purchase = Purchases()
Image = Images()
