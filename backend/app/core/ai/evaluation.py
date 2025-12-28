"""Position evaluation for chess AI"""
from typing import Dict
from ..chess_engine.pieces import (
    Piece, Pawn, Rook, Knight, Bishop, Queen, King, Color, PieceType
)
from ..chess_engine.board import ChessBoard


class Evaluator:
    """Evaluates chess positions"""
    
    # Piece values in centipawns
    PIECE_VALUES = {
        PieceType.PAWN: 100,
        PieceType.KNIGHT: 320,
        PieceType.BISHOP: 330,
        PieceType.ROOK: 500,
        PieceType.QUEEN: 900,
        PieceType.KING: 20000
    }
    
    # Piece-square tables for positional evaluation
    # Pawn position bonuses
    PAWN_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]
    
    # Knight position bonuses
    KNIGHT_TABLE = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]
    
    # Bishop position bonuses
    BISHOP_TABLE = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]
    
    # Rook position bonuses
    ROOK_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ]
    
    # Queen position bonuses
    QUEEN_TABLE = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ]
    
    # King position bonuses (middlegame)
    KING_TABLE_MIDDLE = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]
    
    # King position bonuses (endgame)
    KING_TABLE_END = [
        [-50,-40,-30,-20,-20,-30,-40,-50],
        [-30,-20,-10,  0,  0,-10,-20,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-30,  0,  0,  0,  0,-30,-30],
        [-50,-30,-30,-30,-30,-30,-30,-50]
    ]
    
    def __init__(self):
        pass
    
    def evaluate(self, board: ChessBoard) -> float:
        """
        Evaluate position from white's perspective
        Positive = white advantage, Negative = black advantage
        """
        score = 0.0
        
        # Material evaluation
        score += self._evaluate_material(board)
        
        # Positional evaluation
        score += self._evaluate_position(board)
        
        # Pawn structure
        score += self._evaluate_pawn_structure(board)
        
        # King safety
        score += self._evaluate_king_safety(board)
        
        # Mobility
        score += self._evaluate_mobility(board)
        
        return score
    
    def _evaluate_material(self, board: ChessBoard) -> float:
        """Evaluate material balance"""
        score = 0.0
        
        for piece in board.get_all_pieces():
            value = self.PIECE_VALUES[piece.piece_type]
            if piece.color == Color.WHITE:
                score += value
            else:
                score -= value
        
        return score
    
    def _evaluate_position(self, board: ChessBoard) -> float:
        """Evaluate piece positions using piece-square tables"""
        score = 0.0
        
        is_endgame = self._is_endgame(board)
        
        for piece in board.get_all_pieces():
            row, col = piece.position
            
            # Get position bonus from piece-square table
            if isinstance(piece, Pawn):
                table = self.PAWN_TABLE
            elif isinstance(piece, Knight):
                table = self.KNIGHT_TABLE
            elif isinstance(piece, Bishop):
                table = self.BISHOP_TABLE
            elif isinstance(piece, Rook):
                table = self.ROOK_TABLE
            elif isinstance(piece, Queen):
                table = self.QUEEN_TABLE
            elif isinstance(piece, King):
                table = self.KING_TABLE_END if is_endgame else self.KING_TABLE_MIDDLE
            else:
                continue
            
            # Flip table for black pieces
            if piece.color == Color.WHITE:
                bonus = table[row][col]
                score += bonus
            else:
                bonus = table[7 - row][col]
                score -= bonus
        
        return score
    
    def _evaluate_pawn_structure(self, board: ChessBoard) -> float:
        """Evaluate pawn structure (doubled, isolated, passed pawns)"""
        score = 0.0
        
        white_pawns = [p for p in board.get_all_pieces(Color.WHITE) if isinstance(p, Pawn)]
        black_pawns = [p for p in board.get_all_pieces(Color.BLACK) if isinstance(p, Pawn)]
        
        # Doubled pawns penalty
        for color, pawns in [(Color.WHITE, white_pawns), (Color.BLACK, black_pawns)]:
            pawn_files = {}
            for pawn in pawns:
                col = pawn.position[1]
                pawn_files[col] = pawn_files.get(col, 0) + 1
            
            for file_count in pawn_files.values():
                if file_count > 1:
                    penalty = (file_count - 1) * 10
                    if color == Color.WHITE:
                        score -= penalty
                    else:
                        score += penalty
        
        # Isolated pawns penalty
        for color, pawns in [(Color.WHITE, white_pawns), (Color.BLACK, black_pawns)]:
            for pawn in pawns:
                col = pawn.position[1]
                has_neighbor = False
                
                for adj_col in [col - 1, col + 1]:
                    if 0 <= adj_col < 8:
                        for other_pawn in pawns:
                            if other_pawn.position[1] == adj_col:
                                has_neighbor = True
                                break
                
                if not has_neighbor:
                    penalty = 15
                    if color == Color.WHITE:
                        score -= penalty
                    else:
                        score += penalty
        
        # Passed pawns bonus
        for pawn in white_pawns:
            if self._is_passed_pawn(board, pawn, Color.WHITE):
                row = pawn.position[0]
                bonus = (7 - row) * 10  # Closer to promotion = higher bonus
                score += bonus
        
        for pawn in black_pawns:
            if self._is_passed_pawn(board, pawn, Color.BLACK):
                row = pawn.position[0]
                bonus = row * 10
                score -= bonus
        
        return score
    
    def _is_passed_pawn(self, board: ChessBoard, pawn: Pawn, color: Color) -> bool:
        """Check if pawn is a passed pawn"""
        row, col = pawn.position
        
        # Check columns (same and adjacent)
        check_cols = [col - 1, col, col + 1]
        
        if color == Color.WHITE:
            # Check if there are no enemy pawns in front
            for check_row in range(row - 1, -1, -1):
                for check_col in check_cols:
                    if 0 <= check_col < 8:
                        piece = board.get_piece(check_row, check_col)
                        if piece and isinstance(piece, Pawn) and piece.color == Color.BLACK:
                            return False
        else:
            # Check if there are no enemy pawns in front
            for check_row in range(row + 1, 8):
                for check_col in check_cols:
                    if 0 <= check_col < 8:
                        piece = board.get_piece(check_row, check_col)
                        if piece and isinstance(piece, Pawn) and piece.color == Color.WHITE:
                            return False
        
        return True
    
    def _evaluate_king_safety(self, board: ChessBoard) -> float:
        """Evaluate king safety"""
        score = 0.0
        
        # In endgame, king safety is less important
        if self._is_endgame(board):
            return score
        
        # Check pawn shield for both kings
        for color in [Color.WHITE, Color.BLACK]:
            king_pos = board.find_king(color)
            if not king_pos:
                continue
            
            row, col = king_pos
            pawn_shield = 0
            
            if color == Color.WHITE:
                # Check pawns in front of king
                for dc in [-1, 0, 1]:
                    check_col = col + dc
                    if 0 <= check_col < 8:
                        for dr in [1, 2]:
                            if row - dr >= 0:
                                piece = board.get_piece(row - dr, check_col)
                                if piece and isinstance(piece, Pawn) and piece.color == Color.WHITE:
                                    pawn_shield += 5
            else:
                # Check pawns in front of king
                for dc in [-1, 0, 1]:
                    check_col = col + dc
                    if 0 <= check_col < 8:
                        for dr in [1, 2]:
                            if row + dr < 8:
                                piece = board.get_piece(row + dr, check_col)
                                if piece and isinstance(piece, Pawn) and piece.color == Color.BLACK:
                                    pawn_shield += 5
            
            if color == Color.WHITE:
                score += pawn_shield
            else:
                score -= pawn_shield
        
        return score
    
    def _evaluate_mobility(self, board: ChessBoard) -> float:
        """Evaluate piece mobility"""
        from ..chess_engine.moves import MoveGenerator
        
        move_gen = MoveGenerator(board)
        
        white_mobility = 0
        for piece in board.get_all_pieces(Color.WHITE):
            white_mobility += len(piece.get_possible_moves(board))
        
        black_mobility = 0
        for piece in board.get_all_pieces(Color.BLACK):
            black_mobility += len(piece.get_possible_moves(board))
        
        # Mobility bonus (small weight)
        return (white_mobility - black_mobility) * 0.1
    
    def _is_endgame(self, board: ChessBoard) -> bool:
        """Determine if position is in endgame"""
        queens = sum(1 for p in board.get_all_pieces() if isinstance(p, Queen))
        
        # No queens = likely endgame
        if queens == 0:
            return True
        
        # Count non-pawn, non-king pieces
        minor_pieces = sum(1 for p in board.get_all_pieces() 
                          if isinstance(p, (Knight, Bishop, Rook, Queen)))
        
        # Few pieces left = endgame
        return minor_pieces <= 6
