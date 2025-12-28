"""WebSocket handler for real-time chess games"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json


class ConnectionManager:
    """Manages WebSocket connections for chess games"""
    
    def __init__(self):
        # game_id -> list of websocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, game_id: int):
        """Connect a client to a game"""
        await websocket.accept()
        
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        
        self.active_connections[game_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, game_id: int):
        """Disconnect a client from a game"""
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
            
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific client"""
        await websocket.send_json(message)
    
    async def broadcast_to_game(self, message: dict, game_id: int):
        """Broadcast a message to all clients in a game"""
        if game_id in self.active_connections:
            for connection in self.active_connections[game_id]:
                await connection.send_json(message)
    
    async def send_move(self, game_id: int, move_data: dict):
        """Send a move to all players in a game"""
        message = {
            "type": "move",
            "data": move_data
        }
        await self.broadcast_to_game(message, game_id)
    
    async def send_game_state(self, game_id: int, state_data: dict):
        """Send game state update to all players"""
        message = {
            "type": "game_state",
            "data": state_data
        }
        await self.broadcast_to_game(message, game_id)
    
    async def send_error(self, websocket: WebSocket, error_message: str):
        """Send an error message to a client"""
        message = {
            "type": "error",
            "message": error_message
        }
        await self.send_personal_message(message, websocket)


manager = ConnectionManager()
