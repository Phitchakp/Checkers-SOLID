# match.py

class Match:
    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.current_player_index = 1
        self.assign_pieces() # Call this to assign pieces to players at the start.

    def assign_pieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece_at((r, c))
                if piece:
                    for player in self.players:
                        if player.color == piece.color:
                            player.pieces.append(piece)

    def start_game(self, ui_adapter):
        print("Starting Checkers game!")
        while True:
            current_player = self.players[self.current_player_index]
            ui_adapter.display(self.board, current_player)

            if not current_player.has_moves(self.board):
                print(f"{current_player.color} cannot move. Game over.")
                break

            move_result = ui_adapter.get_move(self.board, current_player)
            if move_result is None: # User typed "gg" to quit
                print("Game ended by user.")
                break

            piece, move_path = move_result
            
            # Handle single moves and multi-jumps
            for dest_pos in move_path:
                self.board.move_piece(piece, dest_pos)
            
            self.switch_turn()

    def switch_turn(self):
        self.current_player_index = 1 - self.current_player_index