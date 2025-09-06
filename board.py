from pieces import Man

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.highlight_positions = []
        self.setup_board()

    def setup_board(self):
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = Man('dark', (row, col))
                    self.grid[row][col] = piece
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = Man('light', (row, col))
                    self.grid[row][col] = piece

    def get_piece_at(self, pos):
        row, col = pos
        return self.grid[row][col]

    def move_piece(self, piece, dest):
        start_row, start_col = piece.position
        end_row, end_col = dest
        self.grid[start_row][start_col] = None
        piece.position = (end_row, end_col)
        self.grid[end_row][end_col] = piece

        if (piece.color == 'light' and end_row == 0) or (piece.color == 'dark' and end_row == 7):
            piece.make_king()

        if abs(end_row - start_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            self.grid[mid_row][mid_col] = None
            return True
        return False

    def get_valid_moves(self, piece):                       # Polymorrphism from pieces
        return self.get_simple_moves(piece) or self.get_all_captures(piece)

    def get_simple_moves(self, piece):
        moves = []
        directions = piece.get_directions()
        row, col = piece.position
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.in_bounds((r, c)) and self.grid[r][c] is None:
                moves.append((r, c))
        return moves

    def get_all_captures(self, piece, position=None, visited=None):
        if visited is None:
            visited = set()
        if position is None:
            position = piece.position

        captures = []
        row, col = position
        directions = piece.get_directions()

        for dr, dc in directions:
            mid_r, mid_c = row + dr, col + dc
            end_r, end_c = row + 2*dr, col + 2*dc
            if not self.in_bounds((end_r, end_c)) or not self.in_bounds((mid_r, mid_c)):
                continue
            enemy = self.grid[mid_r][mid_c]
            if enemy and enemy.color != piece.color and self.grid[end_r][end_c] is None and (mid_r, mid_c) not in visited:
                next_visited = visited.copy()
                next_visited.add((mid_r, mid_c))
                next_captures = self.get_all_captures(piece, (end_r, end_c), next_visited)
                if next_captures:
                    for path in next_captures:
                        captures.append([(end_r, end_c)] + path)
                else:
                    captures.append([(end_r, end_c)])

        return [path for path in captures] if captures else []

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < 8 and 0 <= c < 8

    def display(self):
        print("   " + " ".join(str(i) for i in range(8)))
        for r in range(8):
            row_str = str(r) + "  "
            for c in range(8):
                piece = self.grid[r][c]
                if (r, c) in self.highlight_positions:
                    row_str += '* '
                elif piece is None:
                    row_str += '. '
                elif piece.color == 'dark':
                    row_str += 'Dk ' if piece.is_king else 'D '
                else:
                    row_str += 'Lk ' if piece.is_king else 'L '
            print(row_str)
        self.highlight_positions = []
