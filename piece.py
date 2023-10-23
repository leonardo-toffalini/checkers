from enum import Enum

class Color(Enum):
    BLACK = -1
    RED = 1

class Piece:
    def __init__(self, pos: tuple[int, int], color: Color, board):
        self.pos = pos
        self.color = color
        self.board = board