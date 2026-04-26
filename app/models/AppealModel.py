from sqlalchemy import Column, Integer, String, Float
from .base import Base

class AppealModel(Base):
    __tablename__ = "appeals"
    
    id = Column(Integer, primary_key=True)
    appealer_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    target = Column(Float, nullable=False) 
    monthly_interest = Column(Float, nullable=False) 
    principal = Column(Float, nullable=False, server_default='0') 
    interest = Column(Float, nullable=False, server_default='0') 
    status = Column(String, nullable=False, server_default='pending')
    created_at = Column(String, nullable=False)
