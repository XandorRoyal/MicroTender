from app.dtos.BaseDTO import BaseDTO

class AppealDTO(BaseDTO):
    id: int = None
    appealer_id: str
    title: str
    description: str
    target: float
    monthly_interest: float = 0 
    principal: float = 0
    interest: float = 0
    status: str = "pending"
    created_at: str = None