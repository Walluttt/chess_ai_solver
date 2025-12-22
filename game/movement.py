from gamestate import GameState
from game.piece import Piece
from game.pawn import Pawn
from game.rook import Rook
from game.knight import Knight
from game.bishop import Bishop
from game.queen import Queen
from game.king import King


def get_valid_moves(piece: Piece, board) -> list[tuple[int, int]]:
    """Retourne liste des coups valides (row, col) pour une pièce."""
    if isinstance(piece, Pawn):
        return _get_pawn_moves(piece, board)
    elif isinstance(piece, Rook):
        return _get_rook_moves(piece, board)
    elif isinstance(piece, Knight):
        return _get_knight_moves(piece, board)
    elif isinstance(piece, Bishop):
        return _get_bishop_moves(piece, board)
    elif isinstance(piece, Queen):
        return _get_queen_moves(piece, board)
    elif isinstance(piece, King):
        return _get_king_moves(piece, board)
    return []


def is_valid_move(piece: Piece, to_row: int, to_col: int, board) -> bool:
    """Vérifie si un coup est valide."""
    valid_moves = get_valid_moves(piece, board)
    return (to_row, to_col) in valid_moves


def _get_pawn_moves(pawn: Pawn, board) -> list[tuple[int, int]]:
    moves = []
    direction = -1 if pawn.color else 1  # white monte, black descend
    
    # Avance simple
    nr = pawn.row + direction
    if 0 <= nr < 8 and board[nr][pawn.col] is None:
        moves.append((nr, pawn.col))
        
        # Double depuis départ
        if not pawn.has_moved:
            nr2 = pawn.row + 2 * direction
            mid = pawn.row + direction
            if board[mid][pawn.col] is None and board[nr2][pawn.col] is None:
                moves.append((nr2, pawn.col))
    
    # Captures diagonales
    for dc in [-1, 1]:
        nc = pawn.col + dc
        if 0 <= nc < 8 and 0 <= nr < 8:
            target = board[nr][nc]
            if target and target.color != pawn.color:
                moves.append((nr, nc))
    
    return moves



def _get_rook_moves(rook: Rook, board) -> list[tuple[int, int]]:
    moves = []
    # Directions: ↑ ↓ ← →
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        r, c = rook.row + dr, rook.col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] is None:
                moves.append((r, c))
            elif board[r][c].color != rook.color:
                moves.append((r, c))
                break
            else:
                break
            r += dr
            c += dc
    return moves