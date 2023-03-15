from typing import Optional

from fastapi import Depends, HTTPException, Path, Query
from starlette import status

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.packs import PacksRepository
from app.models.domain.packs import Pack
from app.models.domain.users import User
from app.resources import strings


async def get_pack_by_id_from_path(
    pack_id: str = Path(...),
    packs_repo: PacksRepository = Depends(get_repository(PacksRepository)),
) -> Pack:
    try:
        return await packs_repo.get_pack_by_id(pack_id=pack_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.PACK_DOES_NOT_EXIST_ERROR,
        )