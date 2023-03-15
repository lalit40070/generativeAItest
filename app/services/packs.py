from app.db.errors import EntityDoesNotExist
from app.db.repositories.packs import PacksRepository
from app.models.domain.packs import Pack
from app.models.domain.users import User


async def check_pack_exists(packs_repo: PacksRepository, pack_id: int) -> bool:
    try:
        await packs_repo.get_pack_by_id(pack_id=pack_id)
    except EntityDoesNotExist:
        return False

    return True
