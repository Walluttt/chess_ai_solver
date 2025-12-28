"""Ranking and leaderboard routes"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List

from ...database import get_db
from ...models.ranking import Ranking
from ...models.user import User

router = APIRouter(prefix="/rankings", tags=["rankings"])


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    rating: int
    games: int
    wins: int
    losses: int
    draws: int
    
    class Config:
        from_attributes = True


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    time_control: str = Query("rapid", regex="^(blitz|rapid|classical)$"),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """Get leaderboard for specified time control"""
    
    # Query rankings based on time control
    if time_control == "blitz":
        rankings = db.query(Ranking, User).join(User).filter(
            Ranking.blitz_games >= 10  # Minimum games requirement
        ).order_by(desc(Ranking.blitz_rating)).limit(limit).all()
    elif time_control == "classical":
        rankings = db.query(Ranking, User).join(User).filter(
            Ranking.classical_games >= 10
        ).order_by(desc(Ranking.classical_rating)).limit(limit).all()
    else:  # rapid
        rankings = db.query(Ranking, User).join(User).filter(
            Ranking.rapid_games >= 10
        ).order_by(desc(Ranking.rapid_rating)).limit(limit).all()
    
    leaderboard = []
    for rank, (ranking, user) in enumerate(rankings, start=1):
        if time_control == "blitz":
            rating = ranking.blitz_rating
            games = ranking.blitz_games
            wins = ranking.blitz_wins
            losses = ranking.blitz_losses
            draws = ranking.blitz_draws
        elif time_control == "classical":
            rating = ranking.classical_rating
            games = ranking.classical_games
            wins = ranking.classical_wins
            losses = ranking.classical_losses
            draws = ranking.classical_draws
        else:
            rating = ranking.rapid_rating
            games = ranking.rapid_games
            wins = ranking.rapid_wins
            losses = ranking.rapid_losses
            draws = ranking.rapid_draws
        
        leaderboard.append(LeaderboardEntry(
            rank=rank,
            user_id=user.id,
            username=user.username,
            rating=rating,
            games=games,
            wins=wins,
            losses=losses,
            draws=draws
        ))
    
    return leaderboard


@router.get("/user/{user_id}", response_model=dict)
async def get_user_ranking(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed ranking information for a user"""
    ranking = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    
    if not ranking:
        return {
            "message": "User has no ranking yet",
            "user_id": user_id
        }
    
    return {
        "user_id": user_id,
        "blitz": {
            "rating": ranking.blitz_rating,
            "peak": ranking.blitz_peak,
            "games": ranking.blitz_games,
            "wins": ranking.blitz_wins,
            "losses": ranking.blitz_losses,
            "draws": ranking.blitz_draws
        },
        "rapid": {
            "rating": ranking.rapid_rating,
            "peak": ranking.rapid_peak,
            "games": ranking.rapid_games,
            "wins": ranking.rapid_wins,
            "losses": ranking.rapid_losses,
            "draws": ranking.rapid_draws
        },
        "classical": {
            "rating": ranking.classical_rating,
            "peak": ranking.classical_peak,
            "games": ranking.classical_games,
            "wins": ranking.classical_wins,
            "losses": ranking.classical_losses,
            "draws": ranking.classical_draws
        },
        "overall": {
            "total_games": ranking.total_games,
            "wins": ranking.wins,
            "losses": ranking.losses,
            "draws": ranking.draws
        }
    }
