
def get_account_repository():
    from app.repositories import AccountRepository
    from app.settings import get_settings
    settings = get_settings()
    return AccountRepository(settings)