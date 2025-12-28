"""Game management routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import json

from ...database import get_db
from ...services.game_service import GameService
from ...core.chess_engine import ChessBoard, Color, PieceType
from ...core.chess_engine.rules import GameRules
from ...models.user import User
from .auth import get_current_user

router = APIRouter(prefix="/games", tags=["games"])


class GameCreate(BaseModel):
    mode: str  # "local", "ai", "online"
    ai_difficulty: Optional[int] = None
    time_control: Optional[str] = "rapid"
    is_ranked: bool = False


class MoveRequest(BaseModel):
    from_row: int
    from_col: int
    to_row: int
    to_col: int
    promotion: Optional[str] = None


class GameStateResponse(BaseModel):
    game_id: int
    board_state: dict
    current_turn: str
    status: str
    result: Optional[str]
    legal_moves: Optional[dict] = None


@router.post("/create", response_model=dict)
async def create_game(
    game_data: GameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new game"""
    white_player_id = current_user.id if game_data.mode in ["ai", "online"] else None
    
    game = GameService.create_game(
        db,
        mode=game_data.mode,
        white_player_id=white_player_id,
        ai_difficulty=game_data.ai_difficulty,
        time_control=game_data.time_control,
        is_ranked=game_data.is_ranked
    )
    
    board = ChessBoard()
    
    return {
        "game_id": game.id,
        "board_state": board.to_dict(),
        "message": "Game created successfully"
    }


@router.get("/{game_id}", response_model=GameStateResponse)
async def get_game_state(
    game_id: int,
    db: Session = Depends(get_db)
):
    """Get current game state"""
    game = GameService.get_game(db, game_id)
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Reconstruct board from move history
    board = ChessBoard()
    if game.move_history:
        moves = json.loads(game.move_history)
        for move in moves:
            board.move_piece(
                tuple(move['from']),
                tuple(move['to']),
                PieceType[move['promotion']] if move.get('promotion') else None
            )
    
    return GameStateResponse(
        game_id=game.id,
        board_state=board.to_dict(),
        current_turn=board.current_turn.value,
        status=game.status,
        result=game.result
    )


@router.post("/{game_id}/move", response_model=GameStateResponse)
async def make_move(
    game_id: int,
    move_data: MoveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Make a move in the game"""
    game = GameService.get_game(db, game_id)
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.status != "playing":
        raise HTTPException(status_code=400, detail="Game is not in progress")
    
    # Reconstruct board
    board = ChessBoard()
    if game.move_history:
        moves = json.loads(game.move_history)
        for move in moves:
            board.move_piece(
                tuple(move['from']),
                tuple(move['to']),
                PieceType[move['promotion']] if move.get('promotion') else None
            )
    
    # Make the move
    from_pos = (move_data.from_row, move_data.from_col)
    to_pos = (move_data.to_row, move_data.to_col)
    promotion = PieceType[move_data.promotion] if move_data.promotion else None
    
    success = board.move_piece(from_pos, to_pos, promotion)
    
    if not success:
        raise HTTPException(status_code=400, detail="Illegal move")
    
    # Check game state
    rules = GameRules(board)
    game_state = rules.get_game_state()
    
    status = "playing"
    result = None
    
    if game_state == "checkmate":
        status = "checkmate"
        winner = rules.get_winner()
        result = "white" if winner == Color.WHITE else "black"
    elif game_state in ["stalemate", "draw_repetition", "draw_50_move", "draw_insufficient"]:
        status = game_state
        result = "draw"
    
    # Update game in database
    GameService.update_game_state(db, game, board, status, result)
    
    # If AI game, make AI move
    if game.mode == "ai" and status == "playing" and board.current_turn == Color.BLACK:
        ai_move = GameService.get_ai_move(board, game.ai_difficulty or 3)
        
        if ai_move:
            board.move_piece(ai_move[0], ai_move[1])
            
            # Check game state again
            rules = GameRules(board)
            game_state = rules.get_game_state()
            
            if game_state == "checkmate":
                status = "checkmate"
                winner = rules.get_winner()
                result = "white" if winner == Color.WHITE else "black"
            elif game_state in ["stalemate", "draw_repetition", "draw_50_move", "draw_insufficient"]:
                status = game_state
                result = "draw"
            
            GameService.update_game_state(db, game, board, status, result)
    
    return GameStateResponse(
        game_id=game.id,
        board_state=board.to_dict(),
        current_turn=board.current_turn.value,
        status=status,
        result=result
    )


@router.get("/user/history", response_model=List[dict])
async def get_user_games(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20
):
    """Get user's game history"""
    games = GameService.get_user_games(db, current_user.id, limit)
    
    result = []
    for game in games:
        result.append({
            "id": game.id,
            "mode": game.mode,
            "status": game.status,
            "result": game.result,
            "created_at": game.created_at.isoformat(),
            "finished_at": game.finished_at.isoformat() if game.finished_at else None
        })
    
    return result
