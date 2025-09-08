# piece_factory.py
from pieces import Man, King # the factory is the one place that knows the concretions

class PieceFactory:
    def create_piece(self, color, piece_type, position):
        if piece_type == 'man':
            return Man(color, position)
        elif piece_type == 'king':
            return King(color, position)
        else:
            raise ValueError(f"Unknown piece type: {piece_type}")
        # This is open for extension. Add a new 'elif' for new piece types.