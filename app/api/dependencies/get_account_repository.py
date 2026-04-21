from fastapi import Depends

from app.settings import Settings, get_settings
from app.repositories import DatabaseManager, AccountRepository

def get_account_repository(settings: Settings = Depends(get_settings), database_manager: DatabaseManager = Depends(DatabaseManager.depends_init)):
    return AccountRepository(settings, database_manager)