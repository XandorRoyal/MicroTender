from app.dtos.AppealDTO import AppealDTO
from app.models import AppealModel
from app.repositories.DatasbaseManager import DatabaseManager
from app.settings import Settings

from .BaseRepository import BaseRepository

class AppealRepository(BaseRepository):
    def __init__(self, settings: Settings, database_manager: DatabaseManager):
        super().__init__(settings)
        self.table_name = "appeals"
        self.database_manager = database_manager

    def _row_to_appeal(self, row):
        """Convert a database row to an appeal model."""
        if row:
            return AppealModel(
                id=row["id"],
                appealer_id=row["appealer_id"],
                title=row["title"],
                description=row["description"],
                amount=row["amount"],
                monthly_interest=row["monthly_interest"],
                remaining_amount=row["remaining_amount"],
                pledged=row["pledged"],
                status=row["status"],
            )
        return None
    
    async def create_appeal(self, appeal: AppealDTO):
        query = f"""
            INSERT INTO {self.table_name} (appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status
        """
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(
                query,
                appeal.appealer_id,
                appeal.title,
                appeal.description,
                appeal.amount,
                appeal.monthly_interest,
                appeal.remaining_amount,
                appeal.pledged,
                appeal.status,
            )
            return self._row_to_appeal(row)
        

    async def get_appeal(self, appeal_id):
        query = """
            SELECT id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status
            FROM appeals
            WHERE id = $1
        """
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(query, appeal_id)
            return self._row_to_appeal(row)

    async def get_appeals(self, page: int = 1, page_size: int = 10):
        count_query = f"SELECT COUNT(*) FROM {self.table_name}"
        data_query = """
            SELECT id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status
            FROM appeals
            ORDER BY id DESC
            LIMIT $1 OFFSET $2
        """
        offset = (page - 1) * page_size

        async with self.database_manager.get_connection() as conn:
            total = await conn.fetchval(count_query)
            rows = await conn.fetch(data_query, page_size, offset)

        data = [self._row_to_appeal(row) for row in rows]
        total_pages = (total + page_size - 1) // page_size

        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "data": data,
        }
        
    async def update_appeal_status(self, appeal_id, new_status):
        query = """
            UPDATE appeals
            SET status = $1
            WHERE id = $2
            RETURNING id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status
        """
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(query, new_status, appeal_id)
            return self._row_to_appeal(row)

    async def update_appeal_pledged(self, appeal_id, new_pledged):
        query = """
            UPDATE appeals
            SET pledged = $1
            WHERE id = $2
            RETURNING id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status
        """
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(query, new_pledged, appeal_id)
            return self._row_to_appeal(row)

    async def update_amount_remaining(self, appeal_id, new_remaining_amount):
        query = """
            UPDATE appeals
            SET remaining_amount = $1
            WHERE id = $2
            RETURNING id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status
        """
        async with self.database_manager.get_connection() as conn:
            row = await conn.fetchrow(query, new_remaining_amount, appeal_id)
            return self._row_to_appeal(row)