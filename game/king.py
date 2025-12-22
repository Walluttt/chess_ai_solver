from game.piece import Piece
class King(Piece):

    def __init__(self, row: int, col: int, color: bool):
        super().__init__(row, col, color)

        
    def move(self, new_row: int, new_col: int):
        if(new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8 and new_row <= self.row + 1 and new_row >= self.row -1 and new_col <= self.col + 1 and new_col >= self.col -1):
            self.row = new_row
            self.col = new_col
        return self.row, self.col
    

    def get_asset_key(self):
        color = "w"
        if(not self.color):
            color = "b"
        return f"{color}{"k"}"