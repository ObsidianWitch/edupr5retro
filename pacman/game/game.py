import types
from retro.src import retro
from pacman.game.maze import Maze
from pacman.game.player import Player
from pacman.game.ghost import Ghost, Ghosts

class Games(list):
    def __init__(self, size):
        list.__init__(self, [Game() for _ in range(size)])

    @property
    def finished(self): return all(g.finished for g in self)

    @property
    def best(self): return sorted(
        self,
        key = lambda g: g.fitness,
        reverse = True
    )[0]

    def reset(self):
        for g in self: g.reset()

class Game:
    def __init__(self):
        self.maze     = Maze()
        self.player   = Player(pos = (208, 264))
        self.ghosts   = Ghosts(num = 4, pos = (208, 168))
        self.finished = False

    @property
    def fitness(self): return self.player.score

    def target(self, iterable):
        target = sorted(
            iterable,
            key = lambda elem: retro.Math.distance(
                self.player.rect.center,
                elem.rect.center
            )
        )
        if target: return target[0]

    def update(self):
        self.player.update(self.maze)
        self.ghosts.update(self.maze, self.player)

        self.finished = (self.maze.bonuses.count <= 0) \
                     or (self.player.collide_ghost(self.ghosts) == -1)

    def draw(self, target):
        target.fill(retro.BLACK)
        self.maze.draw(target)
        self.ghosts.draw(target)
        self.player.draw(target)
        self.player.draw_score(target)

    def reset(self):
        self.__init__()
