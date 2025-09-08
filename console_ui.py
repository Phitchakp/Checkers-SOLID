# console_ui.py
import re

class ConsoleUI:
    def get_move(self, board, player):
        capturing_pieces = player.get_pieces_with_captures(board)
        
        while True:
            try:
                move_str = input(f"Player {player.color}, enter your piece then your move (e.g., a3 b4) or 'gg' to quit: ").lower().strip()
                
                if move_str == 'gg':
                    return None
                
                # Input format validation
                if not re.match(r"^[a-h][1-8]\s[a-h][1-8]$", move_str):
                    print("Invalid format. Please use 'col_start row_start col_end row_end' format (e.g., a3 b4).")
                    continue
                
                start_str, dest_str = move_str.split()
                
                # Convert string coordinates to tuple coordinates
                start_col = ord(start_str[0]) - ord('a')
                start_row = 8 - int(start_str[1])
                start_pos = (start_row, start_col)
                
                dest_col = ord(dest_str[0]) - ord('a')
                dest_row = 8 - int(dest_str[1])
                dest_pos = (dest_row, dest_col)
                
                piece = board.get_piece_at(start_pos)
                
                # Validate that a piece exists and belongs to the current player
                if not piece or piece.color != player.color:
                    print("There is no piece of your color at the starting position.")
                    continue
                
                # Enforce mandatory capture
                if capturing_pieces and piece not in capturing_pieces:
                    print("You must make a capture if available.")
                    continue
                
                # Correct move validation
                is_simple_move = not capturing_pieces
                if is_simple_move:
                    valid_moves = board.rules_engine.get_valid_moves(board, piece)
                    if dest_pos not in valid_moves:
                        print("Invalid simple move.")
                        continue
                    return piece, [dest_pos]
                else:
                    # Logic for capture moves
                    capture_paths = board.rules_engine.get_all_captures(board, piece)
                    
                    found_valid_capture = False
                    for path in capture_paths:
                        if path[0] == dest_pos:
                            found_valid_capture = True
                            return piece, path
                            
                    if not found_valid_capture:
                        print("Invalid capture move. Please select a valid jump destination.")
                        continue
                
            except Exception as e:
                print(f"Error in input. Try again. ({e})")

    def display(self, board, player=None):
        print("  a b c d e f g h")
        print(" +----------------")
        for i, row in enumerate(board.grid):
            print(f"{8-i}|", end="")
            for piece in row:
                if piece is None:
                    print(".", end=" ")
                else:
                    symbol = "●" if piece.color == "dark" else "○"
                    if piece.is_king:
                        symbol = "♚" if piece.color == "dark" else "♔"
                    print(symbol, end=" ")
            print(f"|{8-i}")
        print(" +----------------")
        print("  a b c d e f g h")