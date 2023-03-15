from typing import Optional

from fastapi import Depends, HTTPException, Path, Query
from starlette import status

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.tasks import TasksRepository
from app.models.domain.users import User
from app.models.domain.tasks import Task, TaskStatus
from app.models.schemas.tasks import TaskFilters
from app.resources import strings


async def get_task_by_id_from_path(
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


def get_tasks_filter(
    task_id: Optional[int] = None,
    user: Optional[str] = None,
    pack:Optional[int] = None,
    purchase: Optional[int] = None,
    task_status:Optional[TaskStatus] = None,

) -> Task:
    return TaskFilters(
        task_id=task_id,
        user=user,
        pack=pack,
        purchase=purchase,
        task_status=task_status
    )
