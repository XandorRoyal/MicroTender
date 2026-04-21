from fastapi.params import Depends
from app.repositories import AppealRepository, DatabaseManager
from app.settings import Settings, get_settings

def get_appeal_repository(settings: Settings = Depends(get_settings), database_manager: DatabaseManager = Depends(DatabaseManager.depends_init)):
    return AppealRepository(settings, database_manager)