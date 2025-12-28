from game import piece
from game.rook import Rook
from game.knight import Knight
from game.bishop import Bishop
from game.queen import Queen
from game.king import King
from game.pawn import Pawn

class GameState:
    
    def __init__(self):
        # Le self.board_state est l'attribut central
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.state = self._initialize_board_pieces() 
        self.current_turn = True
        self.castling_rights = {'wks': True, 'bqs': True}
        
    # def _initialize_self.board_pieces(self):
    #     self.board_SIZE = 8
    #     self.board = [[None for _ in range(self.board_SIZE)] for _ in range(self.board_SIZE)]
    #     self.board[0][4] = King(0, 4, 'black')
    #     self.board[4][4] = King(4, 4, 'white')
    #     return self.board
    
    def switch_turn(self):
        self.current_turn = False if self.current_turn == True else True

    def _initialize_board_pieces(self):
        # Rangée 0 noirs
        # Rangée 0 : Pièces lourdes Noires
        # (row, col, color)
        self.board[0][0] = Rook(0, 0, False)
        self.board[0][1] = Knight(0, 1, False)
        self.board[0][2] = Bishop(0, 2, False)
        self.board[0][3] = Queen(0, 3, False) # Dame avant le Roi dans la notation FEN
        self.board[0][4] = King(0, 4, False)  # Roi
        self.board[0][5] = Bishop(0, 5, False)
        self.board[0][6] = Knight(0, 6, False)
        self.board[0][7] = Rook(0, 7, False)

        # Rangée 1 : Pions Noirs
        for col in range(8):
            self.board[1][col] = Pawn(1, col, False)
        
        # Rangée 6 : Pions Blancs
        for col in range(8):
            self.board[6][col] = Pawn(6, col, True)
            
        # Rangée 7 : Pièces lourdes Blanches
        # (row, col, color)
        self.board[7][0] = Rook(7, 0, True)
        self.board[7][1] = Knight(7, 1, True)
        self.board[7][2] = Bishop(7, 2, True)
        self.board[7][3] = Queen(7, 3, True)
        self.board[7][4] = King(7, 4, True)
        self.board[7][5] = Bishop(7, 5, True)
        self.board[7][6] = Knight(7, 6, True)
        self.board[7][7] = Rook(7, 7, True)

        return self.board
    
    def update_board(self, piece: piece.Piece, row: int, col: int):
        self.board[piece.row][piece.col] = piece
        self.board[row][col] = None
        return self.board
    
    def move_piece(self, piece, to_row, to_col):
        # 1. On met à jour le plateau interne
        row, col = piece.get_pos
        self.board[row][col] = None
        self.board[to_row][to_col] = piece
        
        # 2. Mise à jour des coordonnées de la pièce (important !)
        piece.row = to_row
        piece.col = to_col
        
        # 3. On renvoie juste True pour dire "Mouvement OK"
        return True
    def highlight_moves(self, piece):
        """Pour l'UI: cases à surligner."""
        pass