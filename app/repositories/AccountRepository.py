from app.models import AccountModel
from app.repositories.DatasbaseManager import DatabaseManager
from app.settings import Settings

class AccountRepository():
    def __init__(self, settings: Settings, database_manager: DatabaseManager):
        self.table_name = "accounts"
        self.database_manager = database_manager

    async def create_account(self, discord_id: str) -> AccountModel:
        query = """
        INSERT INTO accounts (discord_id, created_at) VALUES ($1, NOW()) RETURNING *
        """
        model = await self.database_manager.fetchone(query, [discord_id], AccountModel)
        return model

    async def link_minecraft_account(self, discord_id: str, mc_username: str):
        query = f"""
        INSERT INTO {self.table_name} (discord_id, minecraft_username, created_at)
        VALUES ($1, $2, NOW())
        ON CONFLICT(discord_id)
        DO UPDATE SET minecraft_username = EXCLUDED.minecraft_username
        RETURNING *
        """
        model = await self.database_manager.fetchone(query, [discord_id, mc_username], AccountModel)
        return model

    async def get_linked_minecraft_username(self, discord_id: str):
        query = f"SELECT minecraft_username FROM {self.table_name} WHERE discord_id = $1"
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(query, discord_id)
            return row["minecraft_username"] if row else None

    async def get_balance(self, discord_id: str):
        query = f"SELECT balance FROM {self.table_name} WHERE discord_id = $1"
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(query, discord_id)
            return row["balance"] if row else None
        
    async def update_balance(self, discord_id: str, amount: float):
        query = f"""
        UPDATE {self.table_name}
        SET balance = balance + $1
        WHERE discord_id = $2
        RETURNING balance
        """
        async with self.database_manager.get_connection() as conn:
            return await conn.fetchval(query, amount, discord_id)