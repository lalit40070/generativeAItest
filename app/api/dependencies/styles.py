from typing import Optional

from fastapi import Depends, HTTPException, Path, Query
from starlette import status

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.styles import StylesRepository
from app.models.domain.styles import Style, Gender
from app.models.domain.users import User
from app.models.schemas.styles import StyleFilters
from app.resources import strings


async def get_style_by_id_from_path(
    style_id: int = Path(...),
    style_repo: StylesRepository = Depends(get_repository(StylesRepository))
   
) -> Style:
    try:
        return await style_repo.get_style_by_id(style_id=style_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.STYLE_DOESNT_EXIT,
        )


def get_style_filters(
    style_id: Optional[int] = None,
    gender: Optional[Gender] = None,
    name:Optional[str] = None,
    type:Optional[str] = None,
    diffusion_version: Optional[str] = None

) -> Style:
    return StyleFilters(
        style_id=style_id,
        gender=gender,
        name=name,
        type=type,
        diffusion_version=diffusion_version,
    )

    
    
    
    
