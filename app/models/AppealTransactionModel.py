from sqlalchemy import Column, Integer, String, Float
from .base import Base

class AppealTransactionModel(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True)
    appeal_id = Column(Integer, nullable=False)
    account_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(String, nullable=False) 
    type = Column(String, nullable=False, server_default='dispersement')
 