from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette import status
from fastapi.responses import JSONResponse


from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.api.dependencies.packs import get_pack_by_id_from_path
from app.db.repositories.packs import PacksRepository
from app.models.domain.packs import Pack
from app.models.domain.users import User
from app.models.schemas.packs import (
    ListOfPacksInResponse,
    PackForResponse,
    PackInCreate,
    PackFilters,
    PackInUpdate,
    PackInResponse
)
from app.resources import strings
from app.services.packs import check_pack_exists


router = APIRouter()


@router.get("", response_model=ListOfPacksInResponse, name="packs:list-packs")
async def list_packs(
    packs_repo: PacksRepository = Depends(get_repository(PacksRepository)),
) -> ListOfPacksInResponse:
    packs = await packs_repo.get_all_packs(
    )
    packs_for_response = [PackForResponse.from_orm(pack) for pack in packs]
    return ListOfPacksInResponse(
        packs=packs_for_response,
        packs_count=len(packs_for_response),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PackInResponse,
    name="packs:create-pack",
)
async def create_new_pack(
    pack_create: PackInCreate = Body(..., embed=True, alias="pack"),
    packs_repo: PacksRepository = Depends(get_repository(PacksRepository)),
) -> PackInResponse:

    pack = await packs_repo.create_pack(
        pack_id=pack_create.pack_id,
        pack_name=pack_create.pack_name,
        pack_price=pack_create.pack_price,
        images_per_pack=pack_create.images_per_pack
    )

    return PackInResponse(Pack=PackForResponse.from_orm(pack))


@router.put(
    "/{pack_id}",
    response_model=PackInResponse,
    name="packs:update-pack",
)
async def update_pack_by_id(
    pack_update: PackInUpdate = Body(..., embed=True, alias="pack"),
    current_pack: Pack = Depends(get_pack_by_id_from_path),
    pack_repo: PacksRepository = Depends(get_repository(PacksRepository)),
) -> PackInResponse:

    pack = await pack_repo.update_pack(
        pack=current_pack,
        pack_name= pack_update.pack_name,
        pack_price= pack_update.pack_price,
        images_per_pack= pack_update.images_per_pack,
        
    )
    return PackInResponse(Pack=PackInCreate.from_orm(pack))


@router.delete(
    "/{pack_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="packs:delete-pack",
    response_class=Response,
)
async def delete_pack_by_id(
    pack:Pack = Depends(get_pack_by_id_from_path),
    pack_repo: PacksRepository = Depends(get_repository(PacksRepository)),
) -> None:
    await pack_repo.delete_pack(pack=pack)



@router.get(
    "/{pack_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="packs:get-pack",
    response_class=Response,
)
async def get_pack_by_id(
    pack:Pack = Depends(get_pack_by_id_from_path),
    pack_repo: PacksRepository = Depends(get_repository(PacksRepository)),
) -> None:
    pack = await pack_repo.get_pack_by_id(pack_id=pack.pack_id)
    #return JSONResponse(content=PackInResponse(Pack=pack))
    return JSONResponse(content = {"pack_name": pack.pack_name, "pack_id": pack.pack_id,
                         "images_per_pack": pack.images_per_pack, "pack_price": pack.pack_price,
                         })