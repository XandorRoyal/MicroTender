"""
This is the main API package for the MicroTender backend. It contains all the API endpoints and related logic.
"""

from .appeal import appeal_router as appeal
from .auth import auth_router as auth
from .account import account_router as account

__all__ = ["appeal", "auth", "account"]