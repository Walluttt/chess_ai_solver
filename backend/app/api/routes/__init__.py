"""API routes package"""
from .auth import router as auth_router
from .game import router as game_router
from .user import router as user_router
from .ranking import router as ranking_router

__all__ = ["auth_router", "game_router", "user_router", "ranking_router"]
