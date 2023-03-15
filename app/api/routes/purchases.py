from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette import status
from fastapi.responses import JSONResponse


from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.repositories.purchases import PurchasesRepository
from app.models.domain.styles import Style
from app.api.dependencies.purchases import get_purchase_by_id_from_path, get_purchase_filters
from app.models.domain.purchase import Purchase
from app.models.schemas.purchases import (
    ListOfPurchasesInResponse,
    PurchaseInResponse,
    PurchaseFilters,
    PurchaseInUpdate,
    PurchaseStatus,
    PurchaseInCreate
)

from app.resources import strings


router = APIRouter()

@router.get("", response_model=ListOfPurchasesInResponse, name="purchases:list-purchases")
async def list_purchases(
    purchases_filter: PurchaseFilters = Depends(get_purchase_filters),
    purchases_repo: PurchasesRepository = Depends(get_repository(PurchasesRepository)),
) -> ListOfPurchasesInResponse:
    purchases = await purchases_repo.get_all_purchases(
    )
    # styles = await styles_repo.filter_styles(
    #     style_id=styles_filter.style_id,
    #     gender=styles_filter.gender,
    #     name=styles_filter.name,
    #     type=styles_filter.type,
    #     diffusion_version=styles_filter.diffusion_version,
    # )
    purchases_for_response = [PurchaseInResponse(purchase_id=purchase.purchase_id, user_identifier= purchase.user.identifier,
                             pack= purchase.pack.pack_id, style_list=purchase.style_list,
                             created_at=purchase.created_at, updated_at=purchase.updated_at,
                             status=purchase.purchase_status) for purchase in purchases]
    return ListOfPurchasesInResponse(
        purchases=purchases_for_response,
        purchases_count=len(purchases_for_response),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PurchaseInResponse,
    name="purchases:create-purchase",
)
async def create_new_purchase(
    purchase_create: PurchaseInCreate = Body(..., embed=True, alias="purchase"),
    purchase_repo: PurchasesRepository = Depends(get_repository(PurchasesRepository)),
) -> PurchasesRepository:

    purchase = await purchase_repo.create_purchase(
    
        purchase_id = purchase_create.purchase_id,
        user = purchase_create.user,
        pack = purchase_create.pack,
        style_list= purchase_create.style_list,
        purchase_status = purchase_create.purchase_status,
    )
    return PurchaseInResponse(purchase_id=purchase.purchase_id, user_identifier= purchase.user.identifier,
                             pack= purchase.pack.pack_id, style_list=purchase.style_list,
                             created_at=purchase.created_at, updated_at=purchase.updated_at,
                             status=purchase.purchase_status)


@router.put(
    "/{purchase_id}",
    response_model=PurchaseInResponse,
    name="purchases:update-purchase",
)
async def update_purchase_by_id(
    purchase_update: PurchaseInUpdate = Body(..., embed=True, alias="purchase"),
    current_purchase: Purchase = Depends(get_purchase_by_id_from_path),
    purchase_repo: PurchasesRepository = Depends(get_repository(PurchasesRepository)),
) -> PurchaseInResponse:

    purchase = await purchase_repo.update_purchase(
        purchase=current_purchase,
        purchase_status= purchase_update.purchase_status,
       
        
    )
    return PurchaseInResponse(purchase_id=purchase.purchase_id, user_identfier= purchase.user,
                             pack= purchase.pack, style_list=purchase.style_list,
                             created_at=purchase.created_at, updated_at=purchase.updated_at)

@router.delete(
    "/{purchase_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="packs:delete-purchase",
    response_class=Response,
)
async def delete_purchase_by_id(
    purchase:Purchase = Depends(get_purchase_by_id_from_path),
    purchase_repo: PurchasesRepository = Depends(get_repository(PurchasesRepository)),
) -> None:
    await purchase_repo.delete_purchase(purchase=purchase)