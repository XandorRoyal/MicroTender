from pydantic import BaseModel
from typing import List, Dict, Any
from .AppealDTO import AppealDTO

class PaginationDTO(BaseModel):
    page: int = 1
    page_size: int = 10
    total: int = 0
    total_pages: int = 0

class PaginatedAppealsDTO(PaginationDTO):
    data: List[AppealDTO] = []