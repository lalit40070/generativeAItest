from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from app.models.domain.users import User
from app.models.schemas.rwschema import RWSchema
from app.models.domain.users import SocialAuthType
from app.models.domain.tasks import TaskStatus

class UserInLogin(RWSchema):
    email: EmailStr
    password: Optional[str] = None
    auth_type:SocialAuthType
    # device_id: Optional[str] = None
    # fcm_token: Optional[str] = None
    # is_subscribed: Optional[bool] = False
    # auth_type: SocialAuthType


class UserInCreate(UserInLogin):
    device_id: Optional[str] = None
    fcm_token: Optional[str] = None
    is_subscribed: Optional[bool] = False
    auth_type: SocialAuthType
    username: Optional[str] = None
    id_for_apple: Optional[str] =None


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    device_id: Optional[str] = None
    fcm_token: Optional[str] = None
    is_subscribed: Optional[bool] = False
    auth_type: SocialAuthType


class UserWithToken(User):
    token: str


class UserInResponse(RWSchema):
    user: UserWithToken

class UserInGetEmail(RWSchema):
    id_for_apple: str

class UserForGetEmail(RWSchema):
    email: str
    user: User



class UserPackImageResultsRows(RWSchema):
    images_url:list[str]
    style_name:str

class UserPackInResponse(RWSchema):
    # images_url: str
    # style_name: str
    # style_place_holder_image: str
    # status: TaskStatus
    # pack_name: str
    # number_of_images: int
    image_rows: list[UserPackImageResultsRows]
    pack_id: str
    task_status: str
    images_per_pack: int
    time_left:float
    banner_image:str
    task_id:int


class UserPacksBriefInResponse(RWSchema):
    pack_id: str
    task_status: str
    images_per_pack: int
    time_left:float
    banner_image:str
    task_id:int


class UserPackProcessingInReponse(UserPackInResponse):
    time_left: float


class UserPacksInResponse(RWSchema):
    tasks: list[UserPackInResponse]


