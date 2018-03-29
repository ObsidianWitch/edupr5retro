import retro
from game.maze import Maze
from game.player import Player
from game.ghost import Ghosts
from game.collisions import Collisions

class Game:
    def __init__(self, window):
        self.window = window
        self.maze = Maze()
        self.player = Player()
        self.ghosts = Ghosts()
        self.finished = False

    @property
    def fitness(self): return self.player.score

    def target(self, lst):
        if not lst: return None
        return sorted(
            lst,
            key = lambda t: Collisions.distance(
                self.player.rect.topleft,
                t.rect.topleft
            )
        )[0]

    def update(self):
        self.player.update(self.maze)
        self.ghosts.update(self.maze, self.player)

        self.finished = (not self.maze.bonuses) \
                     or (self.player.collide_ghost(self.ghosts) == -1)

    def draw(self):
        self.window.fill(retro.BLACK)
        self.maze.draw(self.window)
        self.ghosts.draw(self.window)
        self.player.draw(self.window)
        self.player.draw_score(self.window)

    def reset(self): self.__init__(self.window)
