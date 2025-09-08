# rules_engine.py
from abc import ABC, abstractmethod

class RulesEngine(ABC):
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
        """
        Recursively finds all possible capture moves for a piece.
        This handles single jumps and multi-jumps.
        """
        if position is None:
            position = piece.position
        
        if visited is None:
            visited = set()
        
        captures = []
        row, col = position
        directions = piece.get_directions()

        for dr, dc in directions:
            mid_r, mid_c = row + dr, col + dc
            end_r, end_c = row + 2 * dr, col + 2 * dc
            
            if not board.in_bounds((end_r, end_c)) or not board.in_bounds((mid_r, mid_c)):
                continue
                
            jumped_piece = board.get_piece_at((mid_r, mid_c))
            landing_spot = board.get_piece_at((end_r, end_c))

            if jumped_piece and jumped_piece.color != piece.color and landing_spot is None:
                if (mid_r, mid_c) in visited:
                    continue
                
                # Recursively find subsequent jumps from the new position
                next_visited = visited.copy()
                next_visited.add((mid_r, mid_c))
                sub_captures = self.get_all_captures(board, piece, (end_r, end_c), next_visited)
                
                if sub_captures:
                    for path in sub_captures:
                        captures.append([(end_r, end_c)] + path)
                else:
                    captures.append([(end_r, end_c)])
    
        return captures if captures else []

    def is_promotion_move(self, board, piece, dest):
        end_row, _ = dest
        return (piece.color == 'light' and end_row == 0) or (piece.color == 'dark' and end_row == 7)

    def is_jump_move(self, start_pos, dest_pos):
        return abs(start_pos[0] - dest_pos[0]) == 2