"""User profile routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from ...database import get_db
from ...services.auth_service import AuthService
from ...models.user import User
from ...models.ranking import Ranking
from .auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


class UserProfileResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    email: str
    created_at: str
    ranking: Optional[dict] = None


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    ranking = db.query(Ranking).filter(Ranking.user_id == current_user.id).first()
    
    ranking_data = None
    if ranking:
        ranking_data = {
            "blitz_rating": ranking.blitz_rating,
            "rapid_rating": ranking.rapid_rating,
            "classical_rating": ranking.classical_rating,
            "total_games": ranking.total_games,
            "wins": ranking.wins,
            "losses": ranking.losses,
            "draws": ranking.draws
        }
    
    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        full_name=current_user.full_name,
        email=current_user.email,
        created_at=current_user.created_at.isoformat(),
        ranking=ranking_data
    )


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user profile by ID"""
    user = AuthService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    ranking = db.query(Ranking).filter(Ranking.user_id == user.id).first()
    
    ranking_data = None
    if ranking:
        ranking_data = {
            "blitz_rating": ranking.blitz_rating,
            "rapid_rating": ranking.rapid_rating,
            "classical_rating": ranking.classical_rating,
            "total_games": ranking.total_games,
            "wins": ranking.wins,
            "losses": ranking.losses,
            "draws": ranking.draws
        }
    
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        created_at=user.created_at.isoformat(),
        ranking=ranking_data
    )


@router.put("/me", response_model=UserProfileResponse)
async def update_profile(
    update_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name
    
    if update_data.avatar_url is not None:
        current_user.avatar_url = update_data.avatar_url
    
    db.commit()
    
    ranking = db.query(Ranking).filter(Ranking.user_id == current_user.id).first()
    
    ranking_data = None
    if ranking:
        ranking_data = {
            "blitz_rating": ranking.blitz_rating,
            "rapid_rating": ranking.rapid_rating,
            "classical_rating": ranking.classical_rating,
            "total_games": ranking.total_games,
            "wins": ranking.wins,
            "losses": ranking.losses,
            "draws": ranking.draws
        }
    
    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        full_name=current_user.full_name,
        email=current_user.email,
        created_at=current_user.created_at.isoformat(),
        ranking=ranking_data
    )
