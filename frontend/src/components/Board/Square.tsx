import React from 'react'
import Piece from '../Pieces/Piece'

interface SquareProps {
  row: number
  col: number
  piece: any
  isLight: boolean
  isSelected: boolean
  isLegalMove: boolean
  onClick: () => void
}

const Square: React.FC<SquareProps> = ({
  row,
  col,
  piece,
  isLight,
  isSelected,
  isLegalMove,
  onClick,
}) => {
  const bgColor = isLight ? 'bg-board-light' : 'bg-board-dark'
  const selectedClass = isSelected ? 'ring-4 ring-yellow-400' : ''
  const legalMoveClass = isLegalMove ? 'legal-move' : ''

  return (
    <div
      className={`
        relative w-full h-full flex items-center justify-center
        ${bgColor} ${selectedClass} ${legalMoveClass}
        hover:opacity-90 transition-opacity cursor-pointer
        chess-square
      `}
      onClick={onClick}
    >
      {piece && <Piece type={piece.type} color={piece.color} />}
    </div>
  )
}

export default Square
