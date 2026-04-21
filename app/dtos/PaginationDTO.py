from typing import List

from app.dtos.BaseDTO import BaseDTO
from .AppealDTO import AppealDTO

class PaginationDTO(BaseDTO):
    page: int = 1
    page_size: int = 10
    total: int = 0
    total_pages: int = 0

class PaginatedAppealsDTO(PaginationDTO):
    data: List[AppealDTO] = []