
from fastapi import Depends

from app.dependencies.get_account_repository import get_account_repository
from app.repositories import AccountRepository


class AccountService:

    _instance = None
    @classmethod
    def depends_init(cls, repository: AccountRepository = Depends(get_account_repository)):
        if cls._instance is None:
            cls._instance = cls(repository)
        return cls._instance

    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def create_account(self, discord_id: str):
        self.repository.create_account(discord_id)

    def link_minecraft_account(self, discord_id: str, mc_username: str):
        self.repository.link_minecraft_account(discord_id, mc_username)

    def get_linked_minecraft_username(self, discord_id: str):
        return self.repository.get_linked_minecraft_username(discord_id)

    def unlink_minecraft_account(self, discord_id: str):
        self.repository.link_minecraft_account(discord_id, None)

    def get_id_from_discord(self, discord_id: str):
        return self.repository.get_id_from_discord(discord_id)

    def get_balance(self, discord_id: str):
        return self.repository.get_balance(discord_id)
    
    def update_balance(self, discord_id: str, amount: float):
        self.repository.update_balance(discord_id, amount)