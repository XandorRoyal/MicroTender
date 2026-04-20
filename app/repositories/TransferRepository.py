
from datetime import datetime

from app.models import AppealTransactionModel
from app.repositories.BaseRepository import BaseRepository


class TransferRepository(BaseRepository):
    def __init__(self, settings):
        super().__init__(settings)

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
    
    def create_transfer(self, appeal_id, account_id, amount, transaction_type, created_at=None):
        if created_at is None:
            created_at = datetime.now()
        data = {
            "appeal_id": appeal_id,
            "account_id": account_id,
            "amount": amount,
            "transaction_type": transaction_type,
            "created_at": created_at
        }
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transfers (appeal_id, account_id, amount, type, created_at)
                VALUES (:appeal_id, :account_id, :amount, :transaction_type, :created_at)
            """, data)
            conn.commit()
    
    def get_transfer(self, transfer_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, appeal_id, account_id, amount, type, created_at FROM transfers WHERE id = ?", (transfer_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_transfer(row)
            return None
        
    def get_transfers_for_appeal(self, appeal_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, appeal_id, account_id, amount, type, created_at FROM transfers WHERE appeal_id = ?", (appeal_id,))
            rows = cursor.fetchall()
            return [
                self._row_to_transfer(row) for row in rows
            ]
        
    def get_transfers_for_appeal_lending(self, appeal_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, appeal_id, account_id, amount, type, created_at FROM transfers WHERE appeal_id = ? AND type = 'lending'", (appeal_id,))
            rows = cursor.fetchall()
            return [
                self._row_to_transfer(row) for row in rows
            ]
    