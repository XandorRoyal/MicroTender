
from contextlib import contextmanager
from sqlite3 import connect, Row

from app.settings import Settings


class BaseRepository():
    def __init__(self, settings: Settings):
        self.settings = settings
        self.db_name = settings.DB_NAME
    
    @contextmanager
    def get_connection(self):
        conn = connect(self.db_name)
        conn.row_factory = Row  # Enable column name access
        try:
            yield conn
        finally:
            conn.close()
    