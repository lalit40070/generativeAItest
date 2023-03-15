from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.users import User
from app.models.domain.rwmodel import RWModel


class Notification(IDModelMixin, DateTimeModelMixin, RWModel):
    is_allowed: bool
    user_id: str
