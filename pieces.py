from abc import ABC, abstractmethod

class Piece(ABC):                                       # Inheritance, Polymorphism
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.is_king = False

    @abstractmethod
    def get_valid_moves(self, board):
        pass

    def make_king(self):
        self.is_king = True

    def get_directions(self):
        if self.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return [(-1, -1), (-1, 1)] if self.color == 'light' else [(1, -1), (1, 1)]


class Man(Piece):
    def get_valid_moves(self, board):
        return board.get_valid_moves(self)


class King(Piece):
    def get_valid_moves(self, board):
        return board.get_valid_moves(self)
