from abc import ABC, abstractmethod

class Piece(ABC):
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


class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []

    def has_moves(self, board):
        return any(board.get_valid_moves(piece) for piece in self.pieces)

    def get_pieces_with_captures(self, board):
        return [p for p in self.pieces if board.get_all_captures(p)]


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
            return True  # Captured
        return False

    def get_valid_moves(self, piece):
        return self.get_all_captures(piece) or self.get_simple_moves(piece)

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
        self.highlight_positions = []  # Clear after display


class Match:
    def __init__(self):
        self.board = Board()
        self.players = [Player('dark'), Player('light')]
        self.current_player_index = 0
        self.assign_pieces()

    def assign_pieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece_at((r, c))
                if piece:
                    for player in self.players:
                        if player.color == piece.color:
                            player.pieces.append(piece)

    def start_game(self):
        print("Starting Checkers game!")
        self.display_with_highlights()
        while True:
            self.display_with_highlights()
            player = self.players[self.current_player_index]
            print(f"{player.color}'s turn")
            if not player.has_moves(self.board):
                print(f"{player.color} cannot move. Game over.")
                break

            moved = self.make_move(player)
            if moved:
                self.switch_turn()

    def display_with_highlights(self):
        current_player = self.players[self.current_player_index]
        capturing_pieces = current_player.get_pieces_with_captures(self.board)
        self.board.highlight_positions = [p.position for p in capturing_pieces]
        self.board.display()

    def make_move(self, player):
        capturing_pieces = player.get_pieces_with_captures(self.board)
        while True:
            try:
                raw_input = input("Enter piece position to move (row col or type 'GG' to quit): ")
                if raw_input.strip().lower() == 'gg':
                    print("Game ended by user.")
                    exit()
                from_pos = tuple(map(int, raw_input.split()))
                piece = self.board.get_piece_at(from_pos)
                if not piece or piece.color != player.color:
                    print("Invalid piece selected.")
                    continue

                if capturing_pieces and piece not in capturing_pieces:
                    print("You must play a piece that can capture.")
                    continue

                captures = self.board.get_all_captures(piece)
                if captures:
                    print("Multiple captures available:")
                    for i, path in enumerate(captures):
                        print(f"{i + 1}: {path}")
                    choice = int(input("Select capture path number: ")) - 1
                    for next_pos in captures[choice]:
                        mid_row = (piece.position[0] + next_pos[0]) // 2
                        mid_col = (piece.position[1] + next_pos[1]) // 2
                        self.board.grid[mid_row][mid_col] = None
                        self.board.move_piece(piece, next_pos)

                        # After full path, check for additional captures (e.g., after becoming king)
                    while True:
                        new_captures = self.board.get_all_captures(piece)
                        if new_captures:
                            print("Continuing multiple captures with new king...")
                            next_path = new_captures[0]  # default: follow first path
                            for next_pos in next_path:
                                mid_row = (piece.position[0] + next_pos[0]) // 2
                                mid_col = (piece.position[1] + next_pos[1]) // 2
                                self.board.grid[mid_row][mid_col] = None
                                self.board.move_piece(piece, next_pos)
                        else:
                            break
                        # After each move, check for further captures (especially if kinged)
                        new_captures = self.board.get_all_captures(piece)
                        if new_captures:
                            print("Continuing multiple captures with new king...")
                            captures = new_captures
                            choice = 0  # default to first path
                        else:
                            break
                    return True
                else:
                    raw_dest = input("Enter destination position (row col or type 'GG' to quit): ")
                    if raw_dest.strip().lower() == 'gg':
                        print("Game ended by user.")
                        exit()
                    to_pos = tuple(map(int, raw_dest.split()))
                    if to_pos in self.board.get_simple_moves(piece):
                        self.board.move_piece(piece, to_pos)
                        return True
                    else:
                        print("Invalid move. Try again.")
            except Exception as e:
                print("Error in input. Try again.", e)

    def switch_turn(self):
        self.current_player_index = 1 - self.current_player_index


class Checkers:
    def __init__(self):
        self.match = Match()

    def run(self):
        self.match.start_game()


if __name__ == "__main__":
    game = Checkers()
    game.run()
