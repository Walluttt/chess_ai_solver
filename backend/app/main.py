"""Main FastAPI application"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import init_db
from .api.routes import auth_router, game_router, user_router, ranking_router
from .api.websocket.game_ws import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Initializing database...")
    init_db()
    print("Database initialized!")
    yield
    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(game_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(ranking_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.websocket("/ws/game/{game_id}")
async def websocket_game_endpoint(websocket: WebSocket, game_id: int):
    """WebSocket endpoint for real-time game updates"""
    await manager.connect(websocket, game_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Handle different message types
            message_type = data.get("type")
            
            if message_type == "move":
                # Broadcast move to all players in the game
                await manager.send_move(game_id, data.get("data"))
            
            elif message_type == "chat":
                # Broadcast chat message
                await manager.broadcast_to_game(data, game_id)
            
            elif message_type == "ping":
                # Respond to ping
                await manager.send_personal_message({"type": "pong"}, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)
        await manager.broadcast_to_game(
            {"type": "player_disconnected", "game_id": game_id},
            game_id
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
