"""User model"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class User(Base):
    """User model for authentication and profile"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Profile information
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # OAuth
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True)
    
    # Relationships
    games_as_white = relationship("Game", back_populates="white_player", foreign_keys="Game.white_player_id")
    games_as_black = relationship("Game", back_populates="black_player", foreign_keys="Game.black_player_id")
    rankings = relationship("Ranking", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"
