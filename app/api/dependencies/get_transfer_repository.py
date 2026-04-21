from fastapi import Depends
from app.repositories import TransferRepository, DatabaseManager
from app.settings import Settings, get_settings

def get_transfer_repository(settings: Settings = Depends(get_settings), database_manager: DatabaseManager = Depends(DatabaseManager.depends_init)):
    return TransferRepository(settings, database_manager)