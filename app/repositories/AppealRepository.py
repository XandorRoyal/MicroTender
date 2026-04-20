from app.dtos.AppealDTO import AppealDTO
from app.settings import Settings

from .BaseRepository import BaseRepository

class AppealRepository(BaseRepository):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.table_name = "appeals"

    def _row_to_appeal(self, row):
        """Convert a database row to appeal dictionary"""
        if row:
            return {
                "id": row["id"],
                "appealer_id": row["appealer_id"],
                "title": row["title"],
                "description": row["description"],
                "amount": row["amount"],
                "monthly_interest": row["monthly_interest"],
                "remaining_amount": row["remaining_amount"],
                "pledged": row["pledged"],
                "status": row["status"]
            }
        return None
    
    def create_appeal(self, appeal: AppealDTO):
        data = {
            "appealer_id": appeal.appealer_id,
            "title": appeal.title,
            "description": appeal.description,
            "amount": appeal.amount,
            "monthly_interest": appeal.monthly_interest,
            "remaining_amount": appeal.remaining_amount,
            "pledged": appeal.pledged,
            "status": appeal.status
        }
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {self.table_name} (appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status)
                VALUES (:appealer_id, :title, :description, :amount, :monthly_interest, :remaining_amount, :pledged, :status)
            """, data)
            conn.commit()
            
            # Get the created appeal with the auto-generated ID using the same connection
            appeal_id = cursor.lastrowid
            cursor.execute(f"SELECT id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status FROM {self.table_name} WHERE id = ?", (appeal_id,))
            row = cursor.fetchone()
            return self._row_to_appeal(row)
        

    def get_appeal(self, appeal_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status FROM appeals WHERE id = ?", (appeal_id,))
            row = cursor.fetchone()
            return self._row_to_appeal(row)

    def get_appeals(self, page: int = 1, page_size: int = 10):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            total = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Get paginated data
            cursor.execute("""
                SELECT id, appealer_id, title, description, amount, monthly_interest, remaining_amount, pledged, status 
                FROM appeals 
                ORDER BY id DESC
                LIMIT ? OFFSET ?
            """, (page_size, offset))
            
            rows = cursor.fetchall()
            data = [self._row_to_appeal(row) for row in rows]
            
            total_pages = (total + page_size - 1) // page_size  # Ceiling division
            
            return {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": total_pages,
                "data": data
            }
        
    def update_appeal_status(self, appeal_id, new_status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appeals SET status = ? WHERE id = ?", (new_status, appeal_id))
            conn.commit()
            return self.get_appeal(appeal_id)  # Return the updated appeal

    def update_appeal_pledged(self, appeal_id, new_pledged):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appeals SET pledged = ? WHERE id = ?", (new_pledged, appeal_id))
            conn.commit()

    def update_amount_remaining(self, appeal_id, new_remaining_amount):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appeals SET remaining_amount = ? WHERE id = ?", (new_remaining_amount, appeal_id))
            conn.commit()