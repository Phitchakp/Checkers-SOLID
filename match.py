# match.py
# from board import Board (We will inject the board now)
# from player import Player

class Match:
    def __init__(self, board, players): # Dependencies are injected!
        self.board = board
        self.players = players
        self.current_player_index = 0

    def start_game(self, ui_adapter): # Accept a UI adapter to handle input/output
        print("Starting Checkers game!")
        ui_adapter.display(self.board)
        while True:
            current_player = self.players[self.current_player_index]
            ui_adapter.display(self.board, current_player)

            if not current_player.has_moves(self.board):
                print(f"{current_player.color} cannot move. Game over.")
                break

            # Delegate the entire process of getting a move to the UI adapter.
            move_result = ui_adapter.get_move(self.board, current_player)
            if move_result is None: # e.g., user quit
                break

            piece, destination = move_result
            captured = self.board.move_piece(piece, destination)
            self.switch_turn()

    def switch_turn(self):
        self.current_player_index = 1 - self.current_player_index