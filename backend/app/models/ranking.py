"""Ranking model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Ranking(Base):
    """Ranking model for ELO ratings"""
    
    __tablename__ = "rankings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Rating by time control
    blitz_rating = Column(Integer, default=1200)
    rapid_rating = Column(Integer, default=1200)
    classical_rating = Column(Integer, default=1200)
    
    # Statistics
    total_games = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    
    # Stats by time control
    blitz_games = Column(Integer, default=0)
    blitz_wins = Column(Integer, default=0)
    blitz_losses = Column(Integer, default=0)
    blitz_draws = Column(Integer, default=0)
    
    rapid_games = Column(Integer, default=0)
    rapid_wins = Column(Integer, default=0)
    rapid_losses = Column(Integer, default=0)
    rapid_draws = Column(Integer, default=0)
    
    classical_games = Column(Integer, default=0)
    classical_wins = Column(Integer, default=0)
    classical_losses = Column(Integer, default=0)
    classical_draws = Column(Integer, default=0)
    
    # Peak ratings
    blitz_peak = Column(Integer, default=1200)
    rapid_peak = Column(Integer, default=1200)
    classical_peak = Column(Integer, default=1200)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="rankings")
    
    def __repr__(self):
        return f"<Ranking user_id={self.user_id}>"
