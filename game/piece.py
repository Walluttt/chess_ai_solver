from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, row: int, col:int, color: bool):
        self.color = color
        self.row = row
        self.col = col

    @abstractmethod
    def move(self, new_row: int, new_col: int):
        pass

    def get_pos(self):
        return self.row, self.col
    @abstractmethod
    def get_asset_key(self):
        pass
