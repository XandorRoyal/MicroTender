
from asyncpg import UniqueViolationError
from fastapi import Depends

from app.api.exceptions import DuplicateEntry
from app.api.dependencies.get_account_repository import get_account_repository
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

    async def create_account(self, discord_id: str):
        try:
            return await self.repository.create_account(discord_id)
        except UniqueViolationError:
            raise DuplicateEntry(f"An account with discord_id {discord_id} already exists.")

    async def link_minecraft_account(self, discord_id: str, mc_username: str):
        await self.repository.link_minecraft_account(discord_id, mc_username)

    async def get_linked_minecraft_username(self, discord_id: str):
        return await self.repository.get_linked_minecraft_username(discord_id)

    async def unlink_minecraft_account(self, discord_id: str):
        return await self.repository.link_minecraft_account(discord_id, None)

    async def get_balance(self, discord_id: str):
        return await self.repository.get_balance(discord_id)
    
    async def update_balance(self, discord_id: str, amount: float):
        return await self.repository.update_balance(discord_id, amount)