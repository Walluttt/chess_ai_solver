"""Chess board representation and state management"""
from typing import List, Optional, Tuple, Dict
from copy import deepcopy
import json

from .pieces import (
    Piece, Pawn, Rook, Knight, Bishop, Queen, King,
    Color, PieceType
)


class ChessBoard:
    """Chess board representation with 8x8 grid"""
    
    def __init__(self):
        """Initialize chess board with starting position"""
        self.board: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = Color.WHITE
        self.move_history = []
        self.captured_pieces = []
        self.halfmove_clock = 0  # For 50-move rule
        self.fullmove_number = 1
        self.position_history = []  # For repetition detection
        
        # Castling rights
        self.white_kingside_castle = True
        self.white_queenside_castle = True
        self.black_kingside_castle = True
        self.black_queenside_castle = True
        
        self._setup_initial_position()
    
    def _setup_initial_position(self):
        """Set up the standard chess starting position"""
        # White pieces (row 7, 6 from bottom)
        self.board[7][0] = Rook(Color.WHITE, (7, 0))
        self.board[7][1] = Knight(Color.WHITE, (7, 1))
        self.board[7][2] = Bishop(Color.WHITE, (7, 2))
        self.board[7][3] = Queen(Color.WHITE, (7, 3))
        self.board[7][4] = King(Color.WHITE, (7, 4))
        self.board[7][5] = Bishop(Color.WHITE, (7, 5))
        self.board[7][6] = Knight(Color.WHITE, (7, 6))
        self.board[7][7] = Rook(Color.WHITE, (7, 7))
        
        # White pawns
        for col in range(8):
            self.board[6][col] = Pawn(Color.WHITE, (6, col))
        
        # Black pieces (row 0, 1 from top)
        self.board[0][0] = Rook(Color.BLACK, (0, 0))
        self.board[0][1] = Knight(Color.BLACK, (0, 1))
        self.board[0][2] = Bishop(Color.BLACK, (0, 2))
        self.board[0][3] = Queen(Color.BLACK, (0, 3))
        self.board[0][4] = King(Color.BLACK, (0, 4))
        self.board[0][5] = Bishop(Color.BLACK, (0, 5))
        self.board[0][6] = Knight(Color.BLACK, (0, 6))
        self.board[0][7] = Rook(Color.BLACK, (0, 7))
        
        # Black pawns
        for col in range(8):
            self.board[1][col] = Pawn(Color.BLACK, (1, col))
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def set_piece(self, row: int, col: int, piece: Optional[Piece]):
        """Set piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
            if piece:
                piece.position = (row, col)
    
    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                   promotion_piece: Optional[PieceType] = None) -> bool:
        """
        Move a piece from one position to another
        Returns True if move was successful
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.get_piece(from_row, from_col)
        if not piece or piece.color != self.current_turn:
            return False
        
        # Get legal moves for this piece
        from .moves import MoveGenerator
        move_gen = MoveGenerator(self)
        legal_moves = move_gen.get_legal_moves(piece)
        
        if to_pos not in legal_moves:
            return False
        
        # Store move for history
        captured = self.get_piece(to_row, to_col)
        move_record = {
            'from': from_pos,
            'to': to_pos,
            'piece': piece.piece_type,
            'captured': captured.piece_type if captured else None,
            'castling': False,
            'en_passant': False,
            'promotion': None
        }
        
        # Handle special moves
        
        # Castling
        if isinstance(piece, King) and abs(to_col - from_col) == 2:
            move_record['castling'] = True
            if to_col > from_col:  # Kingside
                rook = self.get_piece(from_row, 7)
                self.set_piece(from_row, 7, None)
                self.set_piece(from_row, 5, rook)
                rook.has_moved = True
            else:  # Queenside
                rook = self.get_piece(from_row, 0)
                self.set_piece(from_row, 0, None)
                self.set_piece(from_row, 3, rook)
                rook.has_moved = True
        
        # En passant
        if isinstance(piece, Pawn):
            if abs(to_col - from_col) == 1 and captured is None:
                # En passant capture
                captured_pawn = self.get_piece(from_row, to_col)
                if captured_pawn and isinstance(captured_pawn, Pawn):
                    self.set_piece(from_row, to_col, None)
                    self.captured_pieces.append(captured_pawn)
                    move_record['en_passant'] = True
                    move_record['captured'] = PieceType.PAWN
            
            # Set en passant vulnerability
            if abs(to_row - from_row) == 2:
                piece.en_passant_vulnerable = True
        
        # Reset en passant for other pawns
        for row in range(8):
            for col in range(8):
                p = self.get_piece(row, col)
                if p and isinstance(p, Pawn) and p != piece:
                    p.en_passant_vulnerable = False
        
        # Execute move
        if captured:
            self.captured_pieces.append(captured)
        
        self.set_piece(to_row, to_col, piece)
        self.set_piece(from_row, from_col, None)
        piece.has_moved = True
        
        # Handle pawn promotion
        if isinstance(piece, Pawn):
            if (piece.color == Color.WHITE and to_row == 0) or \
               (piece.color == Color.BLACK and to_row == 7):
                promotion_type = promotion_piece or PieceType.QUEEN
                move_record['promotion'] = promotion_type
                
                # Create promoted piece
                if promotion_type == PieceType.QUEEN:
                    promoted = Queen(piece.color, to_pos)
                elif promotion_type == PieceType.ROOK:
                    promoted = Rook(piece.color, to_pos)
                elif promotion_type == PieceType.BISHOP:
                    promoted = Bishop(piece.color, to_pos)
                elif promotion_type == PieceType.KNIGHT:
                    promoted = Knight(piece.color, to_pos)
                else:
                    promoted = Queen(piece.color, to_pos)
                
                self.set_piece(to_row, to_col, promoted)
        
        # Update castling rights
        if isinstance(piece, King):
            if piece.color == Color.WHITE:
                self.white_kingside_castle = False
                self.white_queenside_castle = False
            else:
                self.black_kingside_castle = False
                self.black_queenside_castle = False
        
        if isinstance(piece, Rook):
            if piece.color == Color.WHITE:
                if from_col == 0:
                    self.white_queenside_castle = False
                elif from_col == 7:
                    self.white_kingside_castle = False
            else:
                if from_col == 0:
                    self.black_queenside_castle = False
                elif from_col == 7:
                    self.black_kingside_castle = False
        
        # Update halfmove clock (for 50-move rule)
        if isinstance(piece, Pawn) or captured:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        
        # Update move counters
        if self.current_turn == Color.BLACK:
            self.fullmove_number += 1
        
        # Store move
        self.move_history.append(move_record)
        
        # Store position for repetition detection
        self.position_history.append(self.get_fen())
        
        # Switch turn
        self.current_turn = self.current_turn.opposite()
        
        return True
    
    def get_all_pieces(self, color: Optional[Color] = None) -> List[Piece]:
        """Get all pieces on the board, optionally filtered by color"""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and (color is None or piece.color == color):
                    pieces.append(piece)
        return pieces
    
    def find_king(self, color: Color) -> Optional[Tuple[int, int]]:
        """Find the king of given color"""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None
    
    def copy(self):
        """Create a deep copy of the board"""
        new_board = ChessBoard.__new__(ChessBoard)
        new_board.board = [[None for _ in range(8)] for _ in range(8)]
        
        # Copy all pieces
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    # Create new piece of same type
                    if isinstance(piece, Pawn):
                        new_piece = Pawn(piece.color, piece.position)
                        new_piece.en_passant_vulnerable = piece.en_passant_vulnerable
                    elif isinstance(piece, Rook):
                        new_piece = Rook(piece.color, piece.position)
                    elif isinstance(piece, Knight):
                        new_piece = Knight(piece.color, piece.position)
                    elif isinstance(piece, Bishop):
                        new_piece = Bishop(piece.color, piece.position)
                    elif isinstance(piece, Queen):
                        new_piece = Queen(piece.color, piece.position)
                    elif isinstance(piece, King):
                        new_piece = King(piece.color, piece.position)
                    else:
                        continue
                    
                    new_piece.has_moved = piece.has_moved
                    new_board.board[row][col] = new_piece
        
        # Copy state
        new_board.current_turn = self.current_turn
        new_board.move_history = self.move_history.copy()
        new_board.captured_pieces = self.captured_pieces.copy()
        new_board.halfmove_clock = self.halfmove_clock
        new_board.fullmove_number = self.fullmove_number
        new_board.position_history = self.position_history.copy()
        
        new_board.white_kingside_castle = self.white_kingside_castle
        new_board.white_queenside_castle = self.white_queenside_castle
        new_board.black_kingside_castle = self.black_kingside_castle
        new_board.black_queenside_castle = self.black_queenside_castle
        
        return new_board
    
    def get_fen(self) -> str:
        """Get FEN (Forsyth-Edwards Notation) representation of current position"""
        fen_parts = []
        
        # Piece placement
        for row in range(8):
            empty = 0
            row_str = ""
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    if empty > 0:
                        row_str += str(empty)
                        empty = 0
                    row_str += str(piece)
                else:
                    empty += 1
            if empty > 0:
                row_str += str(empty)
            fen_parts.append(row_str)
        
        fen = "/".join(fen_parts)
        
        # Active color
        fen += " " + ("w" if self.current_turn == Color.WHITE else "b")
        
        # Castling rights
        castling = ""
        if self.white_kingside_castle:
            castling += "K"
        if self.white_queenside_castle:
            castling += "Q"
        if self.black_kingside_castle:
            castling += "k"
        if self.black_queenside_castle:
            castling += "q"
        fen += " " + (castling if castling else "-")
        
        # En passant target (simplified)
        fen += " -"
        
        # Halfmove clock and fullmove number
        fen += f" {self.halfmove_clock} {self.fullmove_number}"
        
        return fen
    
    def to_dict(self) -> dict:
        """Convert board state to dictionary for JSON serialization"""
        board_state = []
        for row in range(8):
            row_state = []
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    row_state.append({
                        'type': piece.piece_type.value,
                        'color': piece.color.value
                    })
                else:
                    row_state.append(None)
            board_state.append(row_state)
        
        return {
            'board': board_state,
            'current_turn': self.current_turn.value,
            'move_history': self.move_history,
            'halfmove_clock': self.halfmove_clock,
            'fullmove_number': self.fullmove_number,
            'castling_rights': {
                'white_kingside': self.white_kingside_castle,
                'white_queenside': self.white_queenside_castle,
                'black_kingside': self.black_kingside_castle,
                'black_queenside': self.black_queenside_castle
            }
        }
    
    def __str__(self):
        """String representation of board for debugging"""
        result = "  a b c d e f g h\n"
        for row in range(8):
            result += f"{8-row} "
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    result += str(piece) + " "
                else:
                    result += ". "
            result += f"{8-row}\n"
        result += "  a b c d e f g h\n"
        result += f"\nTurn: {self.current_turn.value}\n"
        return result
