from fastapi import Depends
from app.repositories.TransferRepository import TransferRepository
from app.settings import Settings, get_settings

def get_transfer_repository(settings: Settings = Depends(get_settings)):
    return TransferRepository(settings)