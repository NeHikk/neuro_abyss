from rich.traceback import install
install()  

from game.engine import Game

if __name__ == "__main__":
    game = Game()
    game.run()