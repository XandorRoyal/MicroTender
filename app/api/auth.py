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
async def verify_minecraft(discord_id: str, mc_username: str, service: AuthService = Depends(AuthService.depends_init), account_service: AccountService = Depends(AccountService.depends_init)):
    verified = service.verify_minecraft_user(mc_username) 
    if verified:
        print("Verified!")
        # Link the Minecraft account to the Discord user
        await account_service.link_minecraft_account(discord_id, mc_username)
    return verified
