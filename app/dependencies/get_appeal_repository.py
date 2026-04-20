from fastapi.params import Depends
from app.repositories.AppealRepository import AppealRepository
from app.settings import Settings, get_settings

def get_appeal_repository(settings: Settings = Depends(get_settings)):
    return AppealRepository(settings)