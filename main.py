from match import Match                     

class Checkers:
    def __init__(self):
        self.match = Match()                # from class Match

    def run(self):                          
        self.match.start_game()             # start game from Match

if __name__ == "__main__":
    game = Checkers()
    game.run()
