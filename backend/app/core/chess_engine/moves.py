"""Move generation and validation"""
from typing import List, Tuple, Optional
from .pieces import Piece, King, Rook, Pawn, Color


class Move:
    """Represents a chess move"""
    
    def __init__(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                 piece: Piece, captured: Optional[Piece] = None,
                 is_castling: bool = False, is_en_passant: bool = False,
                 promotion: Optional[str] = None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured = captured
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.promotion = promotion
    
    def to_algebraic(self) -> str:
        """Convert move to algebraic notation"""
        files = 'abcdefgh'
        ranks = '87654321'
        
        from_square = files[self.from_pos[1]] + ranks[self.from_pos[0]]
        to_square = files[self.to_pos[1]] + ranks[self.to_pos[0]]
        
        return from_square + to_square
    
    def __repr__(self):
        return f"Move({self.from_pos} -> {self.to_pos})"


class MoveGenerator:
    """Generates legal moves for pieces"""
    
    def __init__(self, board):
        self.board = board
    
    def get_legal_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Get all legal moves for a piece (considering checks)"""
        pseudo_legal = piece.get_possible_moves(self.board)
        legal_moves = []
        
        for move in pseudo_legal:
            if self._is_legal_move(piece, move):
                legal_moves.append(move)
        
        # Add castling moves for king
        if isinstance(piece, King):
            castling_moves = self._get_castling_moves(piece)
            legal_moves.extend(castling_moves)
        
        return legal_moves
    
    def _is_legal_move(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """Check if a move is legal (doesn't leave king in check)"""
        # Make a copy of the board and try the move
        test_board = self.board.copy()
        from_row, from_col = piece.position
        to_row, to_col = to_pos
        
        # Simulate the move
        test_piece = test_board.get_piece(from_row, from_col)
        test_board.set_piece(to_row, to_col, test_piece)
        test_board.set_piece(from_row, from_col, None)
        
        # Check if king is in check after this move
        king_pos = test_board.find_king(piece.color)
        if not king_pos:
            return False
        
        return not self._is_square_attacked(test_board, king_pos, piece.color.opposite())
    
    def _is_square_attacked(self, board, square: Tuple[int, int], by_color: Color) -> bool:
        """Check if a square is attacked by any piece of given color"""
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == by_color:
                    moves = piece.get_possible_moves(board)
                    if square in moves:
                        return True
        return False
    
    def _get_castling_moves(self, king: King) -> List[Tuple[int, int]]:
        """Get castling moves for the king"""
        moves = []
        
        if king.has_moved:
            return moves
        
        row = king.position[0]
        king_col = king.position[1]
        
        # Check castling rights
        if king.color == Color.WHITE:
            can_castle_kingside = self.board.white_kingside_castle
            can_castle_queenside = self.board.white_queenside_castle
        else:
            can_castle_kingside = self.board.black_kingside_castle
            can_castle_queenside = self.board.black_queenside_castle
        
        # Kingside castling
        if can_castle_kingside:
            rook = self.board.get_piece(row, 7)
            if (isinstance(rook, Rook) and not rook.has_moved and
                self.board.get_piece(row, 5) is None and
                self.board.get_piece(row, 6) is None):
                
                # Check if king passes through or ends in check
                if (not self._is_square_attacked(self.board, (row, 4), king.color.opposite()) and
                    not self._is_square_attacked(self.board, (row, 5), king.color.opposite()) and
                    not self._is_square_attacked(self.board, (row, 6), king.color.opposite())):
                    moves.append((row, 6))
        
        # Queenside castling
        if can_castle_queenside:
            rook = self.board.get_piece(row, 0)
            if (isinstance(rook, Rook) and not rook.has_moved and
                self.board.get_piece(row, 1) is None and
                self.board.get_piece(row, 2) is None and
                self.board.get_piece(row, 3) is None):
                
                # Check if king passes through or ends in check
                if (not self._is_square_attacked(self.board, (row, 4), king.color.opposite()) and
                    not self._is_square_attacked(self.board, (row, 3), king.color.opposite()) and
                    not self._is_square_attacked(self.board, (row, 2), king.color.opposite())):
                    moves.append((row, 2))
        
        return moves
    
    def get_all_legal_moves(self, color: Color) -> List[Tuple[Piece, List[Tuple[int, int]]]]:
        """Get all legal moves for all pieces of given color"""
        all_moves = []
        pieces = self.board.get_all_pieces(color)
        
        for piece in pieces:
            legal_moves = self.get_legal_moves(piece)
            if legal_moves:
                all_moves.append((piece, legal_moves))
        
        return all_moves
    
    def has_legal_moves(self, color: Color) -> bool:
        """Check if color has any legal moves"""
        pieces = self.board.get_all_pieces(color)
        for piece in pieces:
            if self.get_legal_moves(piece):
                return True
        return False
