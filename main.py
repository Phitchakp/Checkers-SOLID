# main.py

from match import Match
from board import Board
from player import Player
from console_ui import ConsoleUI
from piece_factory import PieceFactory
from rules_engine import CheckersRulesEngine

class Checkers:
    def __init__(self):
        rules_engine = CheckersRulesEngine()
        piece_factory = PieceFactory()
        
        board = Board(rules_engine, piece_factory)
        
        black_player = Player("dark", rules_engine)
        red_player = Player("light", rules_engine)
        players = [black_player, red_player]
        
        # Populate players with pieces from the board
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at((row, col))
                if piece:
                    if piece.color == "dark":
                        black_player.pieces.append(piece)
                    else:
                        red_player.pieces.append(piece)

        ui_adapter = ConsoleUI()

        self.match = Match(board, players)
        self.ui_adapter = ui_adapter

    def run(self):
        self.match.start_game(self.ui_adapter)

if __name__ == "__main__":
    game = Checkers()
    game.run()