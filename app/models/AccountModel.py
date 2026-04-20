from sqlalchemy import Column, Integer, String, Float
from .base import Base

class AccountModel(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, nullable=False, unique=True)
    minecraft_username = Column(String, nullable=True)
    balance = Column(Float, nullable=False, server_default='0')
    