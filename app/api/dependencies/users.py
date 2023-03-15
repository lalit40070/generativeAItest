from typing import Optional

from fastapi import Depends, HTTPException, Path, Query
from starlette import status

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.tasks import TasksRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.tasks import Task
from app.models.domain.users import User
from app.resources import strings


async def get_user_task_by_id_from_path(
    task_id: int = Path(...),
    task_repo: TasksRepository = Depends(get_repository(TasksRepository))
   
) -> Task:
    try:
        return await task_repo.get_task_by_id(task_id=task_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.TASK_DOESNT_EXIT,
        )

async def get_user_by_identifier(
    user_identifier: str = Path(...),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> User:
    try:
        return await user_repo.get_user_by_identifier(user_identifier=user_identifier)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.USER_DOES_NOT_EXIST_ERROR
        )
