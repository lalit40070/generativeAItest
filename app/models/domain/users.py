from typing import Optional

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.services import security
from enum import Enum

class SocialAuthType(str, Enum):
    APPLE_AUTH = 'apple_auth'
    GOOGLE_AUTH = 'google_auth'
    EMAIL_AUTH = 'email_auth'

    def toString(self):
        if self == "apple_auth":
            return "apple_auth"
        elif self == "google_auth":
            return "google_auth"
        else:
            return "email_auth"

class User(RWModel):
    username: Optional[str] = None
    identifier: str
    email: str
    device_id: Optional[str] = None
    fcm_token: Optional[str] = None
    is_subscribed: Optional[bool] = False
    auth_type: SocialAuthType
    id_for_apple: Optional[str] = None
    is_active: Optional[bool] = True


class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)