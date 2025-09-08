# player.py
class Player:
    def __init__(self, color, rules_engine):
        self.color = color
        self.pieces = []
        self.rules_engine = rules_engine

    def has_moves(self, board):
        return any(self.rules_engine.get_valid_moves(board, piece) for piece in self.pieces)

    def get_pieces_with_captures(self, board):
        return [p for p in self.pieces if self.rules_engine.get_all_captures(board, p)]