

from fastapi import HTTPException


class DuplicateEntry(HTTPException):
    """Exception raised when trying to create a duplicate entry in the database."""

    def __init__(self, detail: str = "Duplicate entry found."):
        super().__init__(status_code=409, detail=detail)

class InsufficientFunds(HTTPException):
    """Exception raised when a user tries to lend or repay more than their available balance."""

    def __init__(self, detail: str = "Insufficient funds."):
        super().__init__(status_code=400, detail=detail)
        
class AppealNotFound(HTTPException):
    """Exception raised when an appeal is not found in the database."""

    def __init__(self, detail: str = "Appeal not found."):
        super().__init__(status_code=404, detail=detail)