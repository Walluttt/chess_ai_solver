"""Minimax algorithm with Alpha-Beta pruning for chess AI"""
from typing import Tuple, Optional
import random
from ..chess_engine.board import ChessBoard
from ..chess_engine.pieces import Color, PieceType
from ..chess_engine.moves import MoveGenerator
from ..chess_engine.rules import GameRules
from .evaluation import Evaluator


class MinimaxAI:
    """Chess AI using Minimax with Alpha-Beta pruning"""
    
    # Difficulty levels (search depth)
    EASY = 2
    MEDIUM = 3
    HARD = 4
    
    def __init__(self, difficulty: int = MEDIUM):
        """
        Initialize AI with difficulty level
        difficulty: search depth (higher = stronger but slower)
        """
        self.difficulty = difficulty
        self.evaluator = Evaluator()
        self.nodes_searched = 0
    
    def get_best_move(self, board: ChessBoard, color: Color) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get the best move for the given color
        Returns: (from_pos, to_pos) tuple or None if no legal moves
        """
        self.nodes_searched = 0
        
        move_gen = MoveGenerator(board)
        all_moves = move_gen.get_all_legal_moves(color)
        
        if not all_moves:
            return None
        
        # Collect all possible moves
        possible_moves = []
        for piece, moves in all_moves:
            for move in moves:
                possible_moves.append((piece.position, move))
        
        if not possible_moves:
            return None
        
        # Use minimax to find best move
        best_move = None
        best_score = float('-inf') if color == Color.WHITE else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Randomize move order to add variety
        random.shuffle(possible_moves)
        
        for from_pos, to_pos in possible_moves:
            # Make move on copy
            board_copy = board.copy()
            board_copy.move_piece(from_pos, to_pos)
            
            # Evaluate position
            if color == Color.WHITE:
                score = self._minimax(board_copy, self.difficulty - 1, alpha, beta, False)
                if score > best_score:
                    best_score = score
                    best_move = (from_pos, to_pos)
                alpha = max(alpha, score)
            else:
                score = self._minimax(board_copy, self.difficulty - 1, alpha, beta, True)
                if score < best_score:
                    best_score = score
                    best_move = (from_pos, to_pos)
                beta = min(beta, score)
        
        return best_move
    
    def _minimax(self, board: ChessBoard, depth: int, alpha: float, beta: float, 
                 is_maximizing: bool) -> float:
        """
        Minimax algorithm with alpha-beta pruning
        
        Args:
            board: Current board state
            depth: Remaining search depth
            alpha: Best score for maximizer
            beta: Best score for minimizer
            is_maximizing: True if maximizing player's turn
        
        Returns:
            Evaluation score for this position
        """
        self.nodes_searched += 1
        
        # Terminal condition: depth 0 or game over
        if depth == 0:
            return self.evaluator.evaluate(board)
        
        game_rules = GameRules(board)
        if game_rules.is_game_over():
            # Game over - return large score
            if game_rules.get_winner() == Color.WHITE:
                return 100000
            elif game_rules.get_winner() == Color.BLACK:
                return -100000
            else:
                return 0  # Draw
        
        move_gen = MoveGenerator(board)
        color = Color.WHITE if is_maximizing else Color.BLACK
        all_moves = move_gen.get_all_legal_moves(color)
        
        # Collect all possible moves
        possible_moves = []
        for piece, moves in all_moves:
            for move in moves:
                possible_moves.append((piece.position, move))
        
        if not possible_moves:
            # No legal moves - stalemate or checkmate
            if game_rules.is_in_check(color):
                # Checkmate
                return 100000 if not is_maximizing else -100000
            else:
                # Stalemate
                return 0
        
        if is_maximizing:
            max_eval = float('-inf')
            for from_pos, to_pos in possible_moves:
                board_copy = board.copy()
                board_copy.move_piece(from_pos, to_pos)
                
                eval_score = self._minimax(board_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            for from_pos, to_pos in possible_moves:
                board_copy = board.copy()
                board_copy.move_piece(from_pos, to_pos)
                
                eval_score = self._minimax(board_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def get_evaluation(self, board: ChessBoard) -> float:
        """Get static evaluation of current position"""
        return self.evaluator.evaluate(board)
