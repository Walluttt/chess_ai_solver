"""ELO rating calculation service"""
import math
from typing import Tuple


class ELOService:
    """Service for ELO rating calculations"""
    
    @staticmethod
    def calculate_expected_score(rating_a: int, rating_b: int) -> float:
        """
        Calculate expected score for player A against player B
        
        Args:
            rating_a: ELO rating of player A
            rating_b: ELO rating of player B
        
        Returns:
            Expected score (0 to 1)
        """
        return 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))
    
    @staticmethod
    def calculate_new_rating(current_rating: int, expected_score: float, 
                           actual_score: float, k_factor: int = 32) -> int:
        """
        Calculate new ELO rating after a game
        
        Args:
            current_rating: Current ELO rating
            expected_score: Expected score (from calculate_expected_score)
            actual_score: Actual score (1 for win, 0.5 for draw, 0 for loss)
            k_factor: K-factor (higher = more volatile ratings)
        
        Returns:
            New ELO rating
        """
        new_rating = current_rating + k_factor * (actual_score - expected_score)
        return round(new_rating)
    
    @staticmethod
    def calculate_rating_change(rating_a: int, rating_b: int, 
                               result: str, k_factor: int = 32) -> Tuple[int, int]:
        """
        Calculate rating changes for both players
        
        Args:
            rating_a: Current rating of player A
            rating_b: Current rating of player B
            result: Result from A's perspective ("win", "draw", "loss")
            k_factor: K-factor for calculation
        
        Returns:
            Tuple of (rating_change_a, rating_change_b)
        """
        # Calculate expected scores
        expected_a = ELOService.calculate_expected_score(rating_a, rating_b)
        expected_b = 1 - expected_a
        
        # Determine actual scores
        if result == "win":
            actual_a = 1.0
            actual_b = 0.0
        elif result == "draw":
            actual_a = 0.5
            actual_b = 0.5
        else:  # loss
            actual_a = 0.0
            actual_b = 1.0
        
        # Calculate new ratings
        new_rating_a = ELOService.calculate_new_rating(rating_a, expected_a, actual_a, k_factor)
        new_rating_b = ELOService.calculate_new_rating(rating_b, expected_b, actual_b, k_factor)
        
        # Calculate changes
        change_a = new_rating_a - rating_a
        change_b = new_rating_b - rating_b
        
        return (change_a, change_b)
