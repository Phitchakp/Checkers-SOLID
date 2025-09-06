class Player:                                               # Encapsulation
    def __init__(self, color):
        self.color = color                                  # Public Attribute
        self.pieces = []

    def has_moves(self, board):                             # Method_moves , Polymorrphism from board
        return any(board.get_valid_moves(piece) for piece in self.pieces)

    def get_pieces_with_captures(self, board):              # Method_captures , Polymorrphism from board
        return [p for p in self.pieces if board.get_all_captures(p)]
