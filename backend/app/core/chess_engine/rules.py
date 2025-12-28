"""Game rules and state checking"""
from typing import Optional
from .pieces import Color, King, Pawn, Knight, Bishop, Rook, Queen
from .moves import MoveGenerator


class GameState:
    """Possible game states"""
    PLAYING = "playing"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW_REPETITION = "draw_repetition"
    DRAW_50_MOVE = "draw_50_move"
    DRAW_INSUFFICIENT = "draw_insufficient"


class GameRules:
    """Implements chess game rules and state checking"""
    
    def __init__(self, board):
        self.board = board
        self.move_gen = MoveGenerator(board)
    
    def is_in_check(self, color: Color) -> bool:
        """Check if the king of given color is in check"""
        king_pos = self.board.find_king(color)
        if not king_pos:
            return False
        
        return self.move_gen._is_square_attacked(self.board, king_pos, color.opposite())
    
    def is_checkmate(self, color: Color) -> bool:
        """Check if color is in checkmate"""
        if not self.is_in_check(color):
            return False
        
        return not self.move_gen.has_legal_moves(color)
    
    def is_stalemate(self, color: Color) -> bool:
        """Check if position is stalemate"""
        if self.is_in_check(color):
            return False
        
        return not self.move_gen.has_legal_moves(color)
    
    def is_draw_by_repetition(self) -> bool:
        """Check if position is drawn by threefold repetition"""
        if len(self.board.position_history) < 9:  # Need at least 9 moves for threefold
            return False
        
        current_position = self.board.get_fen().split()[0]  # Only compare piece positions
        count = 0
        
        for position in self.board.position_history:
            if position.split()[0] == current_position:
                count += 1
                if count >= 3:
                    return True
        
        return False
    
    def is_draw_by_50_move_rule(self) -> bool:
        """Check if position is drawn by 50-move rule"""
        return self.board.halfmove_clock >= 100  # 50 moves = 100 half-moves
    
    def is_insufficient_material(self) -> bool:
        """Check if there's insufficient material for checkmate"""
        pieces = self.board.get_all_pieces()
        
        # Count pieces
        white_pieces = [p for p in pieces if p.color == Color.WHITE]
        black_pieces = [p for p in pieces if p.color == Color.BLACK]
        
        # King vs King
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return True
        
        # King and Bishop/Knight vs King
        if len(white_pieces) == 2 and len(black_pieces) == 1:
            non_king = [p for p in white_pieces if not isinstance(p, King)][0]
            if isinstance(non_king, (Bishop, Knight)):
                return True
        
        if len(black_pieces) == 2 and len(white_pieces) == 1:
            non_king = [p for p in black_pieces if not isinstance(p, King)][0]
            if isinstance(non_king, (Bishop, Knight)):
                return True
        
        # King and Bishop vs King and Bishop (same color squares)
        if len(white_pieces) == 2 and len(black_pieces) == 2:
            white_non_king = [p for p in white_pieces if not isinstance(p, King)]
            black_non_king = [p for p in black_pieces if not isinstance(p, King)]
            
            if (white_non_king and black_non_king and
                isinstance(white_non_king[0], Bishop) and
                isinstance(black_non_king[0], Bishop)):
                
                # Check if bishops are on same color squares
                w_row, w_col = white_non_king[0].position
                b_row, b_col = black_non_king[0].position
                
                if (w_row + w_col) % 2 == (b_row + b_col) % 2:
                    return True
        
        return False
    
    def get_game_state(self) -> str:
        """Get current game state"""
        current_color = self.board.current_turn
        
        # Check for checkmate
        if self.is_checkmate(current_color):
            return GameState.CHECKMATE
        
        # Check for stalemate
        if self.is_stalemate(current_color):
            return GameState.STALEMATE
        
        # Check for draw conditions
        if self.is_draw_by_repetition():
            return GameState.DRAW_REPETITION
        
        if self.is_draw_by_50_move_rule():
            return GameState.DRAW_50_MOVE
        
        if self.is_insufficient_material():
            return GameState.DRAW_INSUFFICIENT
        
        # Check for check
        if self.is_in_check(current_color):
            return GameState.CHECK
        
        return GameState.PLAYING
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        state = self.get_game_state()
        return state in [
            GameState.CHECKMATE,
            GameState.STALEMATE,
            GameState.DRAW_REPETITION,
            GameState.DRAW_50_MOVE,
            GameState.DRAW_INSUFFICIENT
        ]
    
    def get_winner(self) -> Optional[Color]:
        """Get winner if game is over, None for draw"""
        if self.get_game_state() == GameState.CHECKMATE:
            return self.board.current_turn.opposite()
        return None
