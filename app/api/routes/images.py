from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette import status
from fastapi.responses import JSONResponse
from botocore.client import BaseClient
from fastapi import File, UploadFile
from typing import List
from starlette.status import HTTP_400_BAD_REQUEST



from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.repositories.images import ImageRepository
from app.models.domain.styles import Style
from app.api.dependencies.purchases import get_purchase_by_id_from_path, get_purchase_filters
from app.models.domain.purchase import Purchase
from app.models.schemas.images import (
    ImageInCreate,
    ImageInResponse,
    ListOfImagesInResponse,
    ImagesFilters,
    DeleteImageInCreate
)

from app.resources import strings
from app.services.s3_connector import s3_connector

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ImageInResponse,
    name="images:upload-images",
)
async def upload_new_images(
    images_create: ImageInCreate = Depends(),
    files: List[UploadFile] = File(...),
    images_repo: ImageRepository = Depends(get_repository(ImageRepository)),
    s3: BaseClient = Depends(s3_connector)
) -> ImageRepository:
    image = await images_repo.create_images(

        type = images_create.type,
        files = files,
        user = images_create.user,
        purchase= images_create.purchase,
        style = images_create.style,
        s3 = s3
    )
    return ImageInResponse(type=image.type, url= image.url, style=image.style, created_at= image.created_at,
                            updated_at= image.updated_at)



@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    name="images:delete-images",
    response_class=Response,
)
async def delete_user_selfies(
    images: DeleteImageInCreate = Depends(),
    images_repo: ImageRepository = Depends(get_repository(ImageRepository)),
    s3: BaseClient = Depends(s3_connector)
) -> None:
    
    if images.type.toString() != "selfie":
        raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=strings.SELFIES_DOESNT_EXIST,
            )
    
    await images_repo.delete_user_selfies(
        type = images.type,
        user = images.user,
        purchase = images.purchase,
        s3 = s3
    )