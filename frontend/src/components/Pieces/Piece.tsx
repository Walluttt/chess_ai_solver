import React from 'react'

interface PieceProps {
  type: string
  color: string
}

const Piece: React.FC<PieceProps> = ({ type, color }) => {
  const pieceSymbols: { [key: string]: { [key: string]: string } } = {
    white: {
      K: '♔',
      Q: '♕',
      R: '♖',
      B: '♗',
      N: '♘',
      P: '♙',
    },
    black: {
      K: '♚',
      Q: '♛',
      R: '♜',
      B: '♝',
      N: '♞',
      P: '♟',
    },
  }

  const symbol = pieceSymbols[color]?.[type] || ''

  return (
    <div
      className="text-6xl select-none chess-piece"
      style={{
        filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.5))',
      }}
    >
      {symbol}
    </div>
  )
}

export default Piece
