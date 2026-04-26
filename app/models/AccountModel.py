from sqlalchemy import Column, String, Float
from .base import Base

class AccountModel(Base):
    __tablename__ = "accounts"
    
    discord_id = Column(String, primary_key=True, unique=True)
    minecraft_username = Column(String, nullable=True)
    balance = Column(Float, nullable=False, server_default='0')
    created_at = Column(String, nullable=False)