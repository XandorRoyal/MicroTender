from pydantic import BaseModel

class AppealDTO(BaseModel):
    id: int = None
    appealer_id: str
    title: str
    description: str
    amount: float
    monthly_interest: float = 0 
    remaining_amount: float = 0
    pledged: float = 0
    status: str = "pending"