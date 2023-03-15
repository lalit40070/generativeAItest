from fastapi import APIRouter

from app.api.routes import (authentication, users, packs, notifications, styles,
                            purchases, images, tasks) 

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"], prefix="/users")
router.include_router(users.router, tags=["users"], prefix="/user")
router.include_router(packs.router, tags=["packs"], prefix="/packs")
router.include_router(notifications.router, tags=["notifications"], prefix="/notifications")
router.include_router(styles.router, tags=["styles"], prefix="/styles")
router.include_router(purchases.router, tags=["purchases"], prefix="/purchases")
router.include_router(images.router, tags=["images"], prefix="/images")
router.include_router(tasks.router, tags=["tasks"], prefix="/tasks")