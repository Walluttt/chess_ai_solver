"""Chess piece definitions and movement logic"""
from typing import List, Tuple, Optional
from enum import Enum


class PieceType(Enum):
    """Chess piece types"""
    PAWN = "P"
    KNIGHT = "N"
    BISHOP = "B"
    ROOK = "R"
    QUEEN = "Q"
    KING = "K"


class Color(Enum):
    """Player colors"""
    WHITE = "white"
    BLACK = "black"
    
    def opposite(self):
        """Return opposite color"""
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class Piece:
    """Base class for chess pieces"""
    
    def __init__(self, color: Color, piece_type: PieceType, position: Tuple[int, int]):
        self.color = color
        self.piece_type = piece_type
        self.position = position
        self.has_moved = False
    
    def __str__(self):
        """String representation of piece"""
        symbol = self.piece_type.value
        return symbol if self.color == Color.WHITE else symbol.lower()
    
    def __repr__(self):
        return f"{self.color.value} {self.piece_type.value} at {self.position}"
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for this piece (to be overridden by subclasses)"""
        raise NotImplementedError
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8


class Pawn(Piece):
    """Pawn piece implementation"""
    
    def __init__(self, color: Color, position: Tuple[int, int]):
        super().__init__(color, PieceType.PAWN, position)
        self.en_passant_vulnerable = False
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible pawn moves"""
        moves = []
        row, col = self.position
        direction = -1 if self.color == Color.WHITE else 1
        
        # Forward move
        new_row = row + direction
        if self.is_valid_position(new_row, col) and board.get_piece(new_row, col) is None:
            moves.append((new_row, col))
            
            # Double move from starting position
            if not self.has_moved:
                new_row2 = row + 2 * direction
                if board.get_piece(new_row2, col) is None:
                    moves.append((new_row2, col))
        
        # Captures (diagonal)
        for dc in [-1, 1]:
            new_col = col + dc
            if self.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target and target.color != self.color:
                    moves.append((new_row, new_col))
                
                # En passant
                adjacent = board.get_piece(row, new_col)
                if (isinstance(adjacent, Pawn) and 
                    adjacent.color != self.color and 
                    adjacent.en_passant_vulnerable):
                    moves.append((new_row, new_col))
        
        return moves


class Rook(Piece):
    """Rook piece implementation"""
    
    def __init__(self, color: Color, position: Tuple[int, int]):
        super().__init__(color, PieceType.ROOK, position)
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible rook moves"""
        moves = []
        row, col = self.position
        
        # Horizontal and vertical directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class Knight(Piece):
    """Knight piece implementation"""
    
    def __init__(self, color: Color, position: Tuple[int, int]):
        super().__init__(color, PieceType.KNIGHT, position)
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible knight moves"""
        moves = []
        row, col = self.position
        
        # All 8 possible knight moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves


class Bishop(Piece):
    """Bishop piece implementation"""
    
    def __init__(self, color: Color, position: Tuple[int, int]):
        super().__init__(color, PieceType.BISHOP, position)
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible bishop moves"""
        moves = []
        row, col = self.position
        
        # Diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class Queen(Piece):
    """Queen piece implementation"""
    
    def __init__(self, color: Color, position: Tuple[int, int]):
        super().__init__(color, PieceType.QUEEN, position)
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible queen moves (combination of rook and bishop)"""
        moves = []
        row, col = self.position
        
        # All 8 directions (horizontal, vertical, and diagonal)
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class King(Piece):
    """King piece implementation"""
    
    def __init__(self, color: Color, position: Tuple[int, int]):
        super().__init__(color, PieceType.KING, position)
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible king moves"""
        moves = []
        row, col = self.position
        
        # All 8 adjacent squares
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_row, new_col = row + dr, col + dc
                if self.is_valid_position(new_row, new_col):
                    target = board.get_piece(new_row, new_col)
                    if target is None or target.color != self.color:
                        moves.append((new_row, new_col))
        
        return moves
