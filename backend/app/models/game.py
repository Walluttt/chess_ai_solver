"""Game model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Game(Base):
    """Game model for storing chess games"""
    
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Players
    white_player_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    black_player_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Game mode
    mode = Column(String, nullable=False)  # "local", "ai", "online"
    ai_difficulty = Column(Integer, nullable=True)  # For AI games
    
    # Game state
    status = Column(String, nullable=False, default="playing")  # playing, checkmate, stalemate, draw, abandoned
    result = Column(String, nullable=True)  # "white", "black", "draw"
    
    # Game data
    pgn = Column(Text, nullable=True)  # PGN notation of the game
    move_history = Column(Text, nullable=True)  # JSON string of moves
    final_position = Column(Text, nullable=True)  # FEN of final position
    
    # Time control
    time_control = Column(String, nullable=True)  # "blitz", "rapid", "classical"
    initial_time = Column(Integer, nullable=True)  # Initial time in seconds
    increment = Column(Integer, nullable=True)  # Increment in seconds
    
    # Ranked game
    is_ranked = Column(Boolean, default=False)
    elo_change_white = Column(Integer, nullable=True)
    elo_change_black = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    
    # Relationships
    white_player = relationship("User", back_populates="games_as_white", foreign_keys=[white_player_id])
    black_player = relationship("User", back_populates="games_as_black", foreign_keys=[black_player_id])
    
    def __repr__(self):
        return f"<Game {self.id} - {self.status}>"
