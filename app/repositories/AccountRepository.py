from .BaseRepository import BaseRepository

class AccountRepository(BaseRepository):
    def __init__(self, settings):
        super().__init__(settings)
        self.table_name = "accounts"

    def create_account(self, discord_id: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} (discord_id) VALUES (?)",
                (discord_id)
            )
            conn.commit()

    def link_minecraft_account(self, discord_id: str, mc_username: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} (discord_id, minecraft_username) VALUES (:discord_id, :minecraft_username) ON CONFLICT(discord_id) DO UPDATE SET minecraft_username=excluded.minecraft_username",
                {"discord_id": discord_id, "minecraft_username": mc_username}
            )
            conn.commit()

    def get_linked_minecraft_username(self, discord_id: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT minecraft_username FROM {self.table_name} WHERE discord_id = ?", (discord_id,))
            row = cursor.fetchone()
            return row["minecraft_username"] if row else None

    def get_id_from_discord(self, discord_id: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id FROM {self.table_name} WHERE discord_id = ?", (discord_id,))
            row = cursor.fetchone()
            return row["id"] if row else None

    def get_balance(self, discord_id: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT balance FROM {self.table_name} WHERE discord_id = ?", (discord_id,))
            row = cursor.fetchone()
            return row["balance"] if row else None
        
    def update_balance(self, discord_id: str, amount: float):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.table_name} SET balance = balance + ? WHERE discord_id = ?", (amount, discord_id))
            conn.commit()