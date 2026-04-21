from fastapi import HTTPException
    
class DuplicateEntry(HTTPException):
    """Exception raised when trying to create a duplicate entry in the database."""

    def __init__(self, detail: str = "Duplicate entry found."):
        super().__init__(status_code=409, detail=detail)