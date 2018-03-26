from game.maze import Maze
from game.player import Player
from game.ghost import Ghosts

class Game:
    def __init__(self, window):
        self.window = window
        self.maze = Maze()
        self.player = Player()
        self.ghosts = Ghosts()

    @property
    def finished(self): return self.player.bonuses == Maze.N_BONUS

    def run(self):
        # Update
        self.player.update(self.maze)
        self.ghosts.update(self.player, self.maze)

        if self.ghosts.collide(self.player): self.reset()

        # Draw
        self.maze.draw(self.window)
        self.ghosts.draw(self.window)
        self.player.draw(self.window)

    def reset(self): self.__init__(self.window)
