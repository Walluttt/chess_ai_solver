"""Opening book for chess AI"""
from typing import Optional, Tuple, Dict, List
import random


class OpeningBook:
    """Simple opening book with common chess openings"""
    
    def __init__(self):
        """Initialize opening book with common opening moves"""
        # Opening moves stored as sequences
        # Format: position_key -> list of good moves
        self.openings = {
            # Starting position
            "start": [
                ((6, 4), (4, 4)),  # e4
                ((6, 3), (4, 3)),  # d4
                ((7, 6), (5, 5)),  # Nf3
                ((6, 2), (4, 2)),  # c4
            ],
            
            # After 1.e4
            "e4": [
                ((1, 4), (3, 4)),  # e5
                ((1, 2), (3, 2)),  # c5 (Sicilian)
                ((1, 4), (2, 4)),  # e6 (French)
                ((1, 2), (2, 2)),  # c6 (Caro-Kann)
            ],
            
            # After 1.d4
            "d4": [
                ((1, 3), (3, 3)),  # d5
                ((0, 6), (2, 5)),  # Nf6
                ((1, 6), (3, 6)),  # g6 (King's Indian setup)
            ],
            
            # After 1.e4 e5
            "e4e5": [
                ((7, 6), (5, 5)),  # Nf3
                ((7, 5), (4, 2)),  # Bc4 (Italian Game)
            ],
            
            # After 1.d4 d5
            "d4d5": [
                ((6, 2), (4, 2)),  # c4 (Queen's Gambit)
                ((7, 6), (5, 5)),  # Nf3
                ((7, 1), (5, 2)),  # Nc3
            ],
        }
    
    def get_book_move(self, board, move_history: List) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get a move from the opening book based on current position
        
        Args:
            board: Current board state
            move_history: List of moves played so far
        
        Returns:
            (from_pos, to_pos) tuple or None if no book move found
        """
        # Only use opening book for first few moves
        if len(move_history) > 8:
            return None
        
        # Determine opening key based on move history
        key = self._get_opening_key(move_history)
        
        if key in self.openings:
            moves = self.openings[key]
            # Return random move from book to add variety
            return random.choice(moves)
        
        return None
    
    def _get_opening_key(self, move_history: List) -> str:
        """Determine opening key from move history"""
        if not move_history:
            return "start"
        
        # Simple pattern matching for common openings
        if len(move_history) == 1:
            first_move = move_history[0]
            if first_move.get('to') == (4, 4):  # e4
                return "e4"
            elif first_move.get('to') == (4, 3):  # d4
                return "d4"
        
        if len(move_history) == 2:
            first = move_history[0]
            second = move_history[1]
            
            if first.get('to') == (4, 4) and second.get('to') == (3, 4):
                return "e4e5"
            elif first.get('to') == (4, 3) and second.get('to') == (3, 3):
                return "d4d5"
        
        return "unknown"
    
    def add_opening_line(self, key: str, moves: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
        """Add a new opening line to the book"""
        if key not in self.openings:
            self.openings[key] = []
        self.openings[key].extend(moves)
