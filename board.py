# board.py
# Remove: from pieces import Man

class Board:
    def __init__(self, rules_engine, piece_factory): # Dependencies are injected!
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.highlight_positions = []
        self.rules_engine = rules_engine
        self.piece_factory = piece_factory
        self.setup_board()

    def setup_board(self):
        # Use the factory to create pieces, don't hardcode 'Man'
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    # The factory decides what type of piece to create
                    piece = self.piece_factory.create_piece('dark', 'man', (row, col))
                    self.grid[row][col] = piece
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = self.piece_factory.create_piece('light', 'man', (row, col))
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

        # Delegate the promotion check to the rules engine
        if self.rules_engine.is_promotion_move(self, piece, dest):
            piece.make_king()

        # Check for capture
        if abs(end_row - start_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            self.grid[mid_row][mid_col] = None
            return True
        return False

    # DELETE the methods get_valid_moves, get_simple_moves, get_all_captures.
    # The board doesn't need to know the rules anymore.

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < 8 and 0 <= c < 8

    # The display method could be kept here for simplicity, but for a pure SRP fix,
    # it should also be moved to a Renderer class.