from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.api.dependencies.users import get_user_task_by_id_from_path, get_user_by_identifier
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.users import (UserInResponse, UserInUpdate, UserWithToken,
                                     UserInGetEmail, UserForGetEmail, UserPacksInResponse,
                                     UserPackInResponse, UserPacksBriefInResponse)
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.models.domain.tasks import Task

router = APIRouter()


@router.get("", response_model=UserInResponse, name="users:get-current-user")
async def retrieve_current_user(
    user: User = Depends(get_current_user_authorizer()),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            token=token,
        ),
    )


@router.get("/pack", response_model=list[UserPacksBriefInResponse], name="users:get-user-packs")
async def retrieve_user_packs(
    user: User = Depends(get_current_user_authorizer()),
    settings: AppSettings = Depends(get_app_settings),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> list[UserPacksBriefInResponse]:
    
    packs = await users_repo.get_user_packs(user_identifier=user.identifier)
    return packs


@router.get("/pack/{task_id}", response_model=UserPackInResponse, name="users:get-user-packs-by-id")
async def retrieve_user_packs(
    user: User = Depends(get_current_user_authorizer()),
    task: Task = Depends(get_user_task_by_id_from_path),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserPackInResponse:
    
    packs = await users_repo.get_user_packs_by_task_id(user_identifier=user.identifier, task=task)
    return packs

@router.post("/email", response_model=UserForGetEmail, name="users:get-user-email-fromid")
async def retrieve_user_email(
    user_update: UserInGetEmail = Body(..., embed=True, alias="user"),
    settings: AppSettings = Depends(get_app_settings),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserForGetEmail:

    user = await users_repo.get_user_by_apple_id(id_for_apple = user_update.id_for_apple)
    
    return UserForGetEmail(
       user = user,
       email = user.email
    )

@router.delete(
    "",
    status_code=HTTP_204_NO_CONTENT,
    name="users:delete-user",
    response_class=Response,
)
async def delete_user_by_identifier(
    user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> None:
    await users_repo.delete_user(user_identifier=user.identifier)

@router.put("", response_model=UserInResponse, name="users:update-current-user")
async def update_current_user(
    user_update: UserInUpdate = Body(..., embed=True, alias="user"),
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    if user_update.username and user_update.username != current_user.username:
        if await check_username_is_taken(users_repo, user_update.username):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=strings.USERNAME_TAKEN,
            )

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(users_repo, user_update.email):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=strings.EMAIL_TAKEN,
            )

    user = await users_repo.update_user(user=current_user, **user_update.dict())

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return UserInResponse(
        user=UserWithToken(
            id_for_apple = user.id_for_apple,
            username=user.username,
            email=user.email,
            token=token,
        ),
    )

