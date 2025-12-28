import React from 'react'
import Square from './Square'

interface BoardProps {
  board: any[][]
  onSquareClick: (row: number, col: number) => void
  selectedSquare: { row: number; col: number } | null
  legalMoves: { row: number; col: number }[]
  flipped?: boolean
}

const Board: React.FC<BoardProps> = ({
  board,
  onSquareClick,
  selectedSquare,
  legalMoves,
  flipped = false,
}) => {
  const renderBoard = () => {
    const squares = []
    const rows = flipped ? [0, 1, 2, 3, 4, 5, 6, 7] : [7, 6, 5, 4, 3, 2, 1, 0]
    const cols = flipped ? [7, 6, 5, 4, 3, 2, 1, 0] : [0, 1, 2, 3, 4, 5, 6, 7]

    for (const row of rows) {
      for (const col of cols) {
        const piece = board[row][col]
        const isLight = (row + col) % 2 === 0
        const isSelected =
          selectedSquare?.row === row && selectedSquare?.col === col
        const isLegalMove = legalMoves.some(
          (move) => move.row === row && move.col === col
        )

        squares.push(
          <Square
            key={`${row}-${col}`}
            row={row}
            col={col}
            piece={piece}
            isLight={isLight}
            isSelected={isSelected}
            isLegalMove={isLegalMove}
            onClick={() => onSquareClick(row, col)}
          />
        )
      }
    }

    return squares
  }

  return (
    <div className="inline-block shadow-2xl rounded-lg overflow-hidden">
      <div className="grid grid-cols-8 w-[640px] h-[640px]">
        {renderBoard()}
      </div>
    </div>
  )
}

export default Board
