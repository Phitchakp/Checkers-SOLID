# console_ui.py
class ConsoleUI:
    def get_move(self, board, player):
        # ... (Move the extensive input handling logic from Match.make_move here)
        pass

    def display(self, board, player=None):
        # ... (Logic to display the board, perhaps highlight pieces with captures)
        # This could call a method on board, or use a separate Renderer.
        board.display() # For now, we keep it simple.