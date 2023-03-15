from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette import status
from fastapi.responses import JSONResponse


from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.repositories.styles import StylesRepository
from app.models.domain.styles import Style
from app.api.dependencies.styles import get_style_by_id_from_path, get_style_filters
from app.models.domain.users import User
from app.models.schemas.styles import (
    StyleForResponse,
    StyleFilters,
    StyleInResponse,
    StyleInUpdate,
    StyleInCreate,
    ListOfStylesInResponse
)
from app.resources import strings


router = APIRouter()

@router.get("", response_model=ListOfStylesInResponse, name="styles:list-styles")
async def list_styles(
    styles_filter: StyleFilters = Depends(get_style_filters),
    styles_repo: StylesRepository = Depends(get_repository(StylesRepository)),
) -> ListOfStylesInResponse:
    # styles = await styles_repo.get_all_styles(
    # )
    styles = await styles_repo.filter_styles(
        style_id=styles_filter.style_id,
        gender=styles_filter.gender,
        name=styles_filter.name,
        type=styles_filter.type,
        diffusion_version=styles_filter.diffusion_version,
    )
    styles_for_response = [StyleForResponse.from_orm(style) for style in styles]
    return ListOfStylesInResponse(
        styles=styles_for_response,
        styles_count=len(styles_for_response),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=StyleInResponse,
    name="styles:create-style",
)
async def create_new_style(
    style_create: StyleInCreate = Body(..., embed=True, alias="style"),
    styles_repo: StylesRepository = Depends(get_repository(StylesRepository)),
) -> StyleInResponse:

    style = await styles_repo.create_style(
        style_id=style_create.style_id,
        name=style_create.name,
        prompt_positive=style_create.prompt_positive,
        prompt_negative=style_create.prompt_negative,
        seed=style_create.seed,
        type=style_create.type,
        gender=style_create.gender,
        sample_image=style_create.sample_image,
        diffusion_version=style_create.diffusion_version
    )
    return StyleInResponse(style=style)


@router.put(
    "/{style_id}",
    response_model=StyleInResponse,
    name="styles:update-style",
)
async def update_style_by_style_id(
    style_update: StyleInUpdate = Body(..., embed=True, alias="style"),
    current_style: Style = Depends(get_style_by_id_from_path),
    style_repo: StylesRepository = Depends(get_repository(StylesRepository)),
) -> StyleInResponse:

    style = await style_repo.update_style(
        style=current_style,
        name=style_update.name,
        prompt_positive=style_update.prompt_positive,
        prompt_negative=style_update.prompt_negative,
        seed=style_update.seed,
        type=style_update.type,
        gender=style_update.gender,
        sample_image=style_update.sample_image,
        diffusion_version=style_update.diffusion_version,
        
    )
    return StyleInResponse(style=style)



@router.delete(
    "/{style_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="packs:delete-style",
    response_class=Response,
)
async def delete_style_by_id(
    style:Style = Depends(get_style_by_id_from_path),
    style_repo: StylesRepository = Depends(get_repository(StylesRepository)),
) -> None:
    await style_repo.delete_style(style=style)

