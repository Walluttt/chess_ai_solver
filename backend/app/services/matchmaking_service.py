"""Matchmaking service for online games"""
import json
from typing import Optional, Tuple
from datetime import datetime, timedelta
from ..database import redis_client


class MatchmakingService:
    """Service for matchmaking online games"""
    
    QUEUE_KEY = "matchmaking:queue:"
    QUEUE_TIMEOUT = 300  # 5 minutes
    
    @staticmethod
    def add_to_queue(user_id: int, rating: int, time_control: str = "rapid"):
        """Add user to matchmaking queue"""
        queue_key = f"{MatchmakingService.QUEUE_KEY}{time_control}"
        
        player_data = {
            "user_id": user_id,
            "rating": rating,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add to sorted set with rating as score
        redis_client.zadd(queue_key, {json.dumps(player_data): rating})
        
        # Set expiration
        redis_client.expire(queue_key, MatchmakingService.QUEUE_TIMEOUT)
    
    @staticmethod
    def remove_from_queue(user_id: int, time_control: str = "rapid"):
        """Remove user from matchmaking queue"""
        queue_key = f"{MatchmakingService.QUEUE_KEY}{time_control}"
        
        # Get all players in queue
        players = redis_client.zrange(queue_key, 0, -1)
        
        # Find and remove player
        for player_json in players:
            player_data = json.loads(player_json)
            if player_data["user_id"] == user_id:
                redis_client.zrem(queue_key, player_json)
                break
    
    @staticmethod
    def find_match(user_id: int, rating: int, time_control: str = "rapid", 
                   rating_range: int = 200) -> Optional[Tuple[int, int]]:
        """
        Find a match for the user
        
        Args:
            user_id: User ID looking for match
            rating: User's rating
            time_control: Time control category
            rating_range: Maximum rating difference
        
        Returns:
            Tuple of (opponent_user_id, opponent_rating) or None
        """
        queue_key = f"{MatchmakingService.QUEUE_KEY}{time_control}"
        
        # Get players within rating range
        min_rating = rating - rating_range
        max_rating = rating + rating_range
        
        players = redis_client.zrangebyscore(queue_key, min_rating, max_rating)
        
        # Find first player that is not the current user
        for player_json in players:
            player_data = json.loads(player_json)
            opponent_id = player_data["user_id"]
            
            if opponent_id != user_id:
                # Remove both players from queue
                redis_client.zrem(queue_key, player_json)
                MatchmakingService.remove_from_queue(user_id, time_control)
                
                return (opponent_id, player_data["rating"])
        
        # No match found, add to queue
        MatchmakingService.add_to_queue(user_id, rating, time_control)
        return None
    
    @staticmethod
    def get_queue_size(time_control: str = "rapid") -> int:
        """Get number of players in queue"""
        queue_key = f"{MatchmakingService.QUEUE_KEY}{time_control}"
        return redis_client.zcard(queue_key)
    
    @staticmethod
    def clear_old_entries(time_control: str = "rapid"):
        """Remove old entries from queue"""
        queue_key = f"{MatchmakingService.QUEUE_KEY}{time_control}"
        
        players = redis_client.zrange(queue_key, 0, -1)
        cutoff_time = datetime.utcnow() - timedelta(seconds=MatchmakingService.QUEUE_TIMEOUT)
        
        for player_json in players:
            player_data = json.loads(player_json)
            timestamp = datetime.fromisoformat(player_data["timestamp"])
            
            if timestamp < cutoff_time:
                redis_client.zrem(queue_key, player_json)
