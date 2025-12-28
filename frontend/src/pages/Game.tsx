import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { games } from '../services/api'
import { Board } from '../components/Board'

interface GameState {
  board: any[][]
  current_turn: string
  status: string
  result: string | null
}

const Game: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>()
  const navigate = useNavigate()
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [selectedSquare, setSelectedSquare] = useState<{ row: number; col: number } | null>(null)
  const [legalMoves, setLegalMoves] = useState<{ row: number; col: number }[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadGame()
  }, [gameId])

  const loadGame = async () => {
    try {
      const response = await games.get(Number(gameId))
      setGameState({
        board: response.data.board_state.board,
        current_turn: response.data.current_turn,
        status: response.data.status,
        result: response.data.result,
      })
      setLoading(false)
    } catch (error) {
      console.error('Error loading game:', error)
      setLoading(false)
    }
  }

  const handleSquareClick = async (row: number, col: number) => {
    if (!gameState || gameState.status !== 'playing') return

    // If no square is selected, select this square if it has a piece
    if (!selectedSquare) {
      const piece = gameState.board[row][col]
      if (piece && piece.color === gameState.current_turn) {
        setSelectedSquare({ row, col })
        // In a real implementation, calculate legal moves here
        setLegalMoves([])
      }
      return
    }

    // If clicking the same square, deselect
    if (selectedSquare.row === row && selectedSquare.col === col) {
      setSelectedSquare(null)
      setLegalMoves([])
      return
    }

    // Try to make a move
    try {
      const response = await games.move(Number(gameId), {
        from_row: selectedSquare.row,
        from_col: selectedSquare.col,
        to_row: row,
        to_col: col,
      })

      setGameState({
        board: response.data.board_state.board,
        current_turn: response.data.current_turn,
        status: response.data.status,
        result: response.data.result,
      })
      setSelectedSquare(null)
      setLegalMoves([])
    } catch (error: any) {
      console.error('Invalid move:', error)
      // Try selecting new piece if there is one
      const piece = gameState.board[row][col]
      if (piece && piece.color === gameState.current_turn) {
        setSelectedSquare({ row, col })
        setLegalMoves([])
      } else {
        setSelectedSquare(null)
        setLegalMoves([])
      }
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-2xl">Loading game...</div>
      </div>
    )
  }

  if (!gameState) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-2xl">Game not found</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="flex flex-col items-center gap-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
          <div className="flex justify-between items-center mb-4">
            <button
              onClick={() => navigate('/')}
              className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg transition-colors"
            >
              ← Back
            </button>
            <div className="text-white text-xl font-bold">
              {gameState.status === 'playing' ? (
                <span>Turn: {gameState.current_turn === 'white' ? '⚪ White' : '⚫ Black'}</span>
              ) : (
                <span>Game Over: {gameState.result}</span>
              )}
            </div>
          </div>

          <Board
            board={gameState.board}
            onSquareClick={handleSquareClick}
            selectedSquare={selectedSquare}
            legalMoves={legalMoves}
            flipped={false}
          />
        </div>

        {gameState.status !== 'playing' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              {gameState.result === 'white' && '⚪ White Wins!'}
              {gameState.result === 'black' && '⚫ Black Wins!'}
              {gameState.result === 'draw' && '🤝 Draw!'}
            </h2>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-xl transition-colors"
            >
              New Game
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Game
