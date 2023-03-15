from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.models.domain.users import SocialAuthType
from app.models.schemas.users import (
    UserInCreate,
    UserInLogin,
    UserInResponse,
    UserWithToken,
)
from app.resources import strings
from app.services import jwt
from app.services.user_identifier_generator import generate_user_identifier
from app.services.authentication import check_email_is_taken, check_username_is_taken

router = APIRouter()


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )
    if user_login.auth_type == SocialAuthType.EMAIL_AUTH and user_login.password == "":
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.PASSWORD_NEEDED,
        )
    
    try:
        user = await users_repo.get_user_by_email(email=user_login.email)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if user_login.auth_type == SocialAuthType.EMAIL_AUTH:
        if not user.check_password(user_login.password):
            raise wrong_login_error


    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return UserInResponse(
        user=UserWithToken(
            identifier=user.identifier,
            username=user.username,
            email=user.email,
            token=token,
            auth_type=user.auth_type
        ),
    )


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name="auth:register",
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    # if await check_username_is_taken(users_repo, user_create.username):
    #     raise HTTPException(
    #         status_code=HTTP_400_BAD_REQUEST,
    #         detail=strings.USERNAME_TAKEN,
    #     )

    if await check_email_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )
    user_idenfier = generate_user_identifier()
    user = await users_repo.create_user(**user_create.dict(), identifier=user_idenfier)

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return UserInResponse(
        user=UserWithToken(
            identifier= user.identifier,
            id_for_apple = user.id_for_apple,
            username=user.username,
            email=user.email,
            token=token,
            auth_type=user.auth_type
        ),
    )