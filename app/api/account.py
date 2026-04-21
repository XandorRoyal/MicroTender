from fastapi import APIRouter, Depends
import discordoauth2 as do2

from app.services import AccountService
from app.settings import get_settings

settings = get_settings()

client = do2.AsyncClient(settings.APP_ID, secret=settings.APP_SECRET, redirect=f"{settings.PROTOCOL}://{settings.BASE_URL}:{settings.PORT}{settings.AUTHENTICATION_ENDPOINT}")

account_router = APIRouter(prefix="/account", tags=["account"])

@account_router.post("/create/{discord_id}")
async def create_account(discord_id: str, account_service: AccountService = Depends(AccountService.depends_init)):
    return await account_service.create_account(discord_id)

@account_router.get("/get_linked_mc_username/{discord_id}")
async def get_linked_mc_username(discord_id: str, account_service: AccountService = Depends(AccountService.depends_init)):
    return await account_service.get_linked_minecraft_username(discord_id)

@account_router.put("/unlink_minecraft/{discord_id}")
async def unlink_minecraft(discord_id: str, account_service: AccountService = Depends(AccountService.depends_init)):
    return await account_service.unlink_minecraft_account(discord_id)

@account_router.get("/balance/{discord_id}")
async def get_balance(discord_id: str, account_service: AccountService = Depends(AccountService.depends_init)):
    return await account_service.get_balance(discord_id)

@account_router.post("/add_balance/{discord_id}")
async def add_balance(discord_id: str, amount: float, account_service: AccountService = Depends(AccountService.depends_init)):
    return await account_service.update_balance(discord_id, amount)