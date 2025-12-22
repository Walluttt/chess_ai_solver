from game.piece import Piece

class Pawn(Piece):

    def __init__(self, row: int, col: int, color: bool):
        super().__init__(row, col, color)
    
    def get_asset_key(self):
        color = "w"
        if(not self.color):
            color = "b"
        return f"{color}{"p"}"
    
    def move(self, new_row: int, new_col: int):
        if(self.color):
            if ((new_row == self.row - 1 or (self.row == 6 and new_row == self.row - 2)) and new_row < 8 and new_row >= 0 and new_col == self.col):
                self.row = new_row
                self.col = new_col
        if(not self.color):
            if ((new_row == self.row + 1 or (self.row == 1 and new_row == self.row + 2)) and new_row < 8 and new_row >= 0 and new_col == self.col):
                self.row = new_row
                self.col = new_col
        return self.row, self.col