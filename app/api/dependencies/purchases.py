from typing import Optional

from fastapi import Depends, HTTPException, Path, Query
from starlette import status

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.purchases import PurchasesRepository
from app.models.domain.purchase import Purchase, PurchaseStatus
from app.models.domain.users import User
from app.models.domain.packs import Pack
from app.models.schemas.purchases import PurchaseFilters
from app.resources import strings


async def get_purchase_by_id_from_path(
    purchase_id: int = Path(...),
    purchase_repo: PurchasesRepository = Depends(get_repository(PurchasesRepository))
   
) -> Purchase:
    try:
        return await purchase_repo.get_purchase_by_id(purchase_id=purchase_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.PURCHASE_DOESNT_EXIT,
        )


def get_purchase_filters(
    purchase_id: Optional[int] = None,
    user: Optional[str] = None,
    pack:Optional[int] = None,
    purchase_status:Optional[PurchaseStatus] = None,

) -> Purchase:
    return PurchaseFilters(
        purchase_id=purchase_id,
        user=user,
        pack=pack,
        purchase_status=purchase_status
    )

    
    
    
    
