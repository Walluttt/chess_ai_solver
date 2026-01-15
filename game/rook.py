from game.piece import Piece

class Rook(Piece):

    def __init__(self, row: int, col: int, color: bool):
        super().__init__(row, col, color)
        self.moved = False

    def move(self, new_row: int, new_col: int):
        if (new_row >= 0 and new_row < 8 and new_col == self.col):
            self.row = new_row
            self.col = new_col
            self.moved = True
        elif (new_col >= 0 and new_col < 8 and new_row == self.row):
            self.col = new_col
            self.row = new_row
            self.moved = True
        return self.row, self.col
    
    def get_asset_key(self):
        color = "w"
        if(not self.color):
            color = "b"
        return f"{color}{"r"}"