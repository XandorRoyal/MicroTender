
from datetime import datetime

from app.models import AppealTransactionModel
from app.repositories.DatasbaseManager import DatabaseManager
from app.settings import Settings
from app.repositories.BaseRepository import BaseRepository


class TransferRepository(BaseRepository):
    def __init__(self, settings: Settings, database_manager: DatabaseManager):
        super().__init__(settings)
        self.database_manager = database_manager

    def _row_to_transfer(self, row):
        """Convert a database row to transfer dictionary"""
        if row:
            return AppealTransactionModel(
                id=row["id"],
                appeal_id=row["appeal_id"],
                account_id=row["account_id"],
                amount=row["amount"],
                type=row["type"],
                created_at=row["created_at"]
            )
    
    async def create_transfer(self, appeal_id, account_id, amount, transaction_type, created_at=None):
        if created_at is None:
            created_at = datetime.now()
        query = """
            INSERT INTO transfers (appeal_id, account_id, amount, type, created_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, appeal_id, account_id, amount, type, created_at
        """
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(query, appeal_id, account_id, amount, transaction_type, created_at)
            return self._row_to_transfer(row)
    
    async def get_transfer(self, transfer_id):
        query = "SELECT id, appeal_id, account_id, amount, type, created_at FROM transfers WHERE id = $1"
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(query, transfer_id)
            if row:
                return self._row_to_transfer(row)
            return None
        
    async def get_transfers_for_appeal(self, appeal_id):
        query = "SELECT id, appeal_id, account_id, amount, type, created_at FROM transfers WHERE appeal_id = $1"
        async with self.database_manager.get_connection() as conn:
            rows = await conn.fetch(query, appeal_id)
            return [
                self._row_to_transfer(row) for row in rows
            ]
        
    async def get_transfers_for_appeal_lending(self, appeal_id):
        query = """
            SELECT id, appeal_id, account_id, amount, type, created_at
            FROM transfers
            WHERE appeal_id = $1 AND type = 'lending'
        """
        async with self.database_manager.get_connection() as conn:
            rows = await conn.fetch(query, appeal_id)
            return [
                self._row_to_transfer(row) for row in rows
            ]
    