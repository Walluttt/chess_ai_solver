from enum import Enum

class Couleur(Enum):
    WHITE = "w"
    BLACK = "b"

class TypePiece(Enum):
    PAWN ="p" 
    KNIGHT ="n" 
    BISHOP ="b" 
    ROOK ="r" 
    QUEEN="q" 
    King="k" 
