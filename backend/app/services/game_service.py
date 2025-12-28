"""Game service for managing chess games"""
import json
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.game import Game
from ..models.user import User
from ..models.ranking import Ranking
from ..core.chess_engine import ChessBoard
from ..core.ai import MinimaxAI
from .elo_service import ELOService
from ..config import settings


class GameService:
    """Service for managing chess games"""
    
    @staticmethod
    def create_game(db: Session, mode: str, white_player_id: Optional[int] = None,
                   black_player_id: Optional[int] = None, ai_difficulty: Optional[int] = None,
                   time_control: Optional[str] = None, is_ranked: bool = False) -> Game:
        """Create a new chess game"""
        game = Game(
            mode=mode,
            white_player_id=white_player_id,
            black_player_id=black_player_id,
            ai_difficulty=ai_difficulty,
            time_control=time_control,
            is_ranked=is_ranked,
            status="playing",
            started_at=datetime.utcnow()
        )
        
        db.add(game)
        db.commit()
        db.refresh(game)
        
        return game
    
    @staticmethod
    def get_game(db: Session, game_id: int) -> Optional[Game]:
        """Get game by ID"""
        return db.query(Game).filter(Game.id == game_id).first()
    
    @staticmethod
    def update_game_state(db: Session, game: Game, board: ChessBoard, 
                         status: str, result: Optional[str] = None):
        """Update game state after a move"""
        game.move_history = json.dumps(board.move_history)
        game.final_position = board.get_fen()
        game.status = status
        
        if result:
            game.result = result
            game.finished_at = datetime.utcnow()
            
            # Update ELO if ranked game
            if game.is_ranked and game.white_player_id and game.black_player_id:
                GameService._update_rankings(db, game, result)
        
        db.commit()
    
    @staticmethod
    def _update_rankings(db: Session, game: Game, result: str):
        """Update player rankings after game"""
        # Get rankings
        white_ranking = db.query(Ranking).filter(
            Ranking.user_id == game.white_player_id
        ).first()
        black_ranking = db.query(Ranking).filter(
            Ranking.user_id == game.black_player_id
        ).first()
        
        if not white_ranking or not black_ranking:
            return
        
        # Get current ratings based on time control
        time_control = game.time_control or "rapid"
        
        if time_control == "blitz":
            white_rating = white_ranking.blitz_rating
            black_rating = black_ranking.blitz_rating
        elif time_control == "classical":
            white_rating = white_ranking.classical_rating
            black_rating = black_ranking.classical_rating
        else:  # rapid
            white_rating = white_ranking.rapid_rating
            black_rating = black_ranking.rapid_rating
        
        # Calculate rating changes
        change_white, change_black = ELOService.calculate_rating_change(
            white_rating, black_rating, result, settings.K_FACTOR
        )
        
        # Update ratings
        if time_control == "blitz":
            white_ranking.blitz_rating += change_white
            black_ranking.blitz_rating += change_black
            white_ranking.blitz_peak = max(white_ranking.blitz_peak, white_ranking.blitz_rating)
            black_ranking.blitz_peak = max(black_ranking.blitz_peak, black_ranking.blitz_rating)
            white_ranking.blitz_games += 1
            black_ranking.blitz_games += 1
        elif time_control == "classical":
            white_ranking.classical_rating += change_white
            black_ranking.classical_rating += change_black
            white_ranking.classical_peak = max(white_ranking.classical_peak, white_ranking.classical_rating)
            black_ranking.classical_peak = max(black_ranking.classical_peak, black_ranking.classical_rating)
            white_ranking.classical_games += 1
            black_ranking.classical_games += 1
        else:
            white_ranking.rapid_rating += change_white
            black_ranking.rapid_rating += change_black
            white_ranking.rapid_peak = max(white_ranking.rapid_peak, white_ranking.rapid_rating)
            black_ranking.rapid_peak = max(black_ranking.rapid_peak, black_ranking.rapid_rating)
            white_ranking.rapid_games += 1
            black_ranking.rapid_games += 1
        
        # Update statistics
        white_ranking.total_games += 1
        black_ranking.total_games += 1
        
        if result == "white":
            white_ranking.wins += 1
            black_ranking.losses += 1
            if time_control == "blitz":
                white_ranking.blitz_wins += 1
                black_ranking.blitz_losses += 1
            elif time_control == "classical":
                white_ranking.classical_wins += 1
                black_ranking.classical_losses += 1
            else:
                white_ranking.rapid_wins += 1
                black_ranking.rapid_losses += 1
        elif result == "black":
            black_ranking.wins += 1
            white_ranking.losses += 1
            if time_control == "blitz":
                black_ranking.blitz_wins += 1
                white_ranking.blitz_losses += 1
            elif time_control == "classical":
                black_ranking.classical_wins += 1
                white_ranking.classical_losses += 1
            else:
                black_ranking.rapid_wins += 1
                white_ranking.rapid_losses += 1
        else:  # draw
            white_ranking.draws += 1
            black_ranking.draws += 1
            if time_control == "blitz":
                white_ranking.blitz_draws += 1
                black_ranking.blitz_draws += 1
            elif time_control == "classical":
                white_ranking.classical_draws += 1
                black_ranking.classical_draws += 1
            else:
                white_ranking.rapid_draws += 1
                black_ranking.rapid_draws += 1
        
        # Store ELO changes in game
        game.elo_change_white = change_white
        game.elo_change_black = change_black
        
        db.commit()
    
    @staticmethod
    def get_user_games(db: Session, user_id: int, limit: int = 20) -> List[Game]:
        """Get recent games for a user"""
        return db.query(Game).filter(
            (Game.white_player_id == user_id) | (Game.black_player_id == user_id)
        ).order_by(Game.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_ai_move(board: ChessBoard, difficulty: int):
        """Get AI move for current board position"""
        ai = MinimaxAI(difficulty)
        move = ai.get_best_move(board, board.current_turn)
        return move
