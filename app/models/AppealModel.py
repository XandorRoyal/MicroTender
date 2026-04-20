from sqlalchemy import Column, Integer, String, Float
from .base import Base

class AppealModel(Base):
    __tablename__ = "appeals"
    
    id = Column(Integer, primary_key=True)
    appealer_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    monthly_interest = Column(Float, nullable=False)
    pledged = Column(Float, nullable=False, server_default='0')
    remaining_amount = Column(Float, nullable=False, server_default='0')
    status = Column(String, nullable=False, server_default='pending')
