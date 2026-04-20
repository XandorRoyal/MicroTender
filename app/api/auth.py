from fastapi import APIRouter, Depends, Query
import discordoauth2 as do2
from fastapi.responses import RedirectResponse

from app.services import AccountService, AuthService
from app.settings import get_settings

settings = get_settings()

client = do2.AsyncClient(settings.APP_ID, secret=settings.APP_SECRET, redirect=f"{settings.PROTOCOL}://{settings.BASE_URL}:{settings.PORT}{settings.AUTHENTICATION_ENDPOINT}")

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/login")
async def login():
    url = client.generate_uri(scope=["identify"])
    return RedirectResponse(url)

@auth_router.get("/authenticate")
async def authenticate(code: str = Query(...)):
    access = await client.exchange_code(code)
    identity = await access.fetch_identify()
    print(f"User identity: {identity}")

@auth_router.post("/verify_minecraft/{discord_id}")
def verify_minecraft(discord_id: str, mc_username: str, service: AuthService = Depends(AuthService.depends_init), account_service: AccountService = Depends(AccountService.depends_init)):
    verified = service.verify_minecraft_user(mc_username) 
    if verified:
        print("Verified!")
        # Link the Minecraft account to the Discord user
        account_service.link_minecraft_account(discord_id, mc_username)
    return verified

@auth_router.get("/get_linked_mc_username/{discord_id}")
def get_linked_mc_username(discord_id: str, account_service: AccountService = Depends(AccountService.depends_init)):
    return account_service.get_linked_minecraft_username(discord_id)

@auth_router.put("/unlink_minecraft/{discord_id}")
def unlink_minecraft(discord_id: str, account_service: AccountService = Depends(AccountService.depends_init)):
    return account_service.unlink_minecraft_account(discord_id)

@auth_router.get("/get_id_from_discord/{discord_id}")
def get_id_from_discord(discord_id: str, account_service: AccountService = Depends(AccountService.depends_init)):
    return account_service.get_id_from_discord(discord_id)

@auth_router.get("/balance/{discord_id}")
def get_balance(discord_id: str, account_service: AccountService = Depends(AccountService.depends_init)):
    return account_service.get_balance(discord_id)

@auth_router.post("/add_balance/{discord_id}")
def add_balance(discord_id: str, amount: float, account_service: AccountService = Depends(AccountService.depends_init)):
    return account_service.update_balance(discord_id, amount)