# rules_engine.py
from abc import ABC, abstractmethod

class RulesEngine(ABC):
    """Abstract class defining the interface for any game rules."""
    @abstractmethod
    def get_valid_moves(self, board, piece):
        pass

    @abstractmethod
    def get_all_captures(self, board, piece, position=None, visited=None):
        pass

    @abstractmethod
    def is_promotion_move(self, board, piece, dest):
        pass

class CheckersRulesEngine(RulesEngine):
    """Concrete implementation of the rules for Checkers."""

    def get_valid_moves(self, board, piece):
        captures = self.get_all_captures(board, piece)
        if captures:
            return captures
        return self._get_simple_moves(board, piece)

    def _get_simple_moves(self, board, piece):
        moves = []
        directions = piece.get_directions()
        row, col = piece.position
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if board.in_bounds((r, c)) and board.get_piece_at((r, c)) is None:
                moves.append((r, c))
        return moves

    def get_all_captures(self, board, piece, position=None, visited=None):
        # ... (Copy the logic from the old Board.get_all_captures method,
        #  but change 'self.grid' to 'board.get_piece_at()')
        # Example of one changed line:
        # OLD: enemy = self.grid[mid_r][mid_c]
        # NEW: enemy = board.get_piece_at((mid_r, mid_c))
        pass

    def is_promotion_move(self, board, piece, dest):
        end_row, _ = dest
        return (piece.color == 'light' and end_row == 0) or (piece.color == 'dark' and end_row == 7)