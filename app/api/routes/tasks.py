from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette import status
from fastapi.responses import JSONResponse


from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.repositories.tasks import TasksRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.tasks import Task
from app.api.dependencies.tasks import get_task_by_id_from_path, get_tasks_filter
from app.models.domain.purchase import Purchase
from app.models.schemas.tasks import (
    ListOfTasksInResponse,
    TaskFilters,
    TaskInCreate,
    TaskInResponse,
    TaskInUpdate
)

from app.resources import strings
from app.services.firebase import post_to_firebase


router = APIRouter()

@router.get("", response_model=ListOfTasksInResponse, name="purchases:list-tasks")
async def list_tasks(
    tasks_filter: TaskFilters = Depends(get_tasks_filter),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository)),
) -> ListOfTasksInResponse:
    tasks = await tasks_repo.get_all_tasks(
    )
    # styles = await styles_repo.filter_styles(
    #     style_id=styles_filter.style_id,
    #     gender=styles_filter.gender,
    #     name=styles_filter.name,
    #     type=styles_filter.type,
    #     diffusion_version=styles_filter.diffusion_version,
    # )
    tasks_for_response = [TaskInResponse(task_id=task.task_id, user_identifier= task.user_identifier.identifier,
                             purchase_id= task.purchase_id.purchase_id, style_list=task.style_list,
                             created_at=task.created_at, updated_at=task.updated_at,
                             status=task.status) for task in tasks]
    return ListOfTasksInResponse(
        tasks=tasks_for_response,
        tasks_count=len(tasks_for_response),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskInResponse,
    name="tasks:create-task",
)
async def create_new_task(
    task_create: TaskInCreate = Body(..., embed=True, alias="task"),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository)),
) -> TasksRepository:

    task = await tasks_repo.create_task(
        purchase_id = task_create.purchase_id,
        user_identifier = task_create.user_identifier,
        style_list = task_create.style_list,
        gender= task_create.gender,
        pack_id = task_create.pack_id,
        images_per_style = task_create.images_per_style
    )

    return TaskInResponse(task_id=task.task_id, user_identifier= task.user_identifier.identifier,
                             purchase_id= task.purchase_id.purchase_id, style_list=task.style_list,
                             created_at=task.created_at, updated_at=task.updated_at,
                             status=task.status)

@router.put(
    "/{task_id}",
    response_model=TaskInResponse,
    name="tasks:update-task",
)
async def update_task_by_id(
    task_update: TaskInUpdate = Body(..., embed=True, alias="purchase"),
    current_task: Task = Depends(get_task_by_id_from_path),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository)),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> TaskInResponse:

    task = await tasks_repo.update_task(
        task=current_task,
        task_status=task_update.status,
    )

    # ! No exception is being handled
    user = await user_repo.get_user_by_identifier(user_identifier=task.user_identifier.identifier)

    status = await post_to_firebase(
        fcm_token=user.fcm_token,
        body=strings.FIREBASE_NOTIFICATION_BODY,
        title=strings.FIREBASE_NOTIFICATION_TITLE
    )

    return TaskInResponse(task_id=task.task_id, user_identifier=task.user_identifier.identifier,
                             purchase_id=task.purchase_id.purchase_id, style_list=task.style_list,
                             created_at=task.created_at, updated_at=task.updated_at,
                             status=task.status)
