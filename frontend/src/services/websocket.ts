import { io, Socket } from 'socket.io-client'

const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

class WebSocketService {
  private socket: Socket | null = null

  connect(gameId: number) {
    this.socket = io(`${WS_BASE_URL}/ws/game/${gameId}`, {
      transports: ['websocket'],
    })

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
    })

    return this.socket
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  sendMove(moveData: any) {
    if (this.socket) {
      this.socket.emit('message', {
        type: 'move',
        data: moveData,
      })
    }
  }

  onMove(callback: (data: any) => void) {
    if (this.socket) {
      this.socket.on('move', callback)
    }
  }

  onGameState(callback: (data: any) => void) {
    if (this.socket) {
      this.socket.on('game_state', callback)
    }
  }

  onError(callback: (error: string) => void) {
    if (this.socket) {
      this.socket.on('error', callback)
    }
  }
}

export default new WebSocketService()
