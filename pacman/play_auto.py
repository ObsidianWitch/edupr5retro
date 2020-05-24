import sys
import random
import numpy
from retro.src import retro
from pacman.game.game import Game
from pacman.game.maze import Maze

class RandImpulse:
    def __init__(self):
        self.i = 0

    @property
    def enabled(self): return self.i > 0

    def start(self, player):
        self.i = 50
        dirs = [[-1, 0], [ 0, -1], [ 1,  0], [ 0,  1]]
        if player.curdir in dirs:
            dirs.remove(player.curdir)
        return random.choice(dirs)

    def run(self, player):
        if not self.enabled:
            if random.uniform(0, 1) < 0.01:
                return self.start(player)
            else:
                return False
        else:
            self.i -= 1
            return player.nxtdir

class PlayAuto:
    def __init__(self):
        self.window = retro.Window(
            title = "Pacman",
            size  = (448, 528),
            fps   = 0,
        )
        self.game = Game(self.window)
        self.rand_impulse = RandImpulse()

    @classmethod
    def direction(cls, s1, s2, invert = False):
        dv = numpy.subtract(s1.rect.center, s2.rect.center).tolist()
        if invert:
            dv = numpy.negative(dv).tolist()
        if   dv[0] < 0: return [-1,  0]
        elif dv[0] > 0: return [ 1,  0]
        elif dv[1] < 0: return [ 0, -1]
        elif dv[1] > 0: return [ 0,  1]
        else: return False

    @classmethod
    def follow_wall(cls, player):
        if not player.curcol: return False
        elif (not player.nxtcol) or (player.curdir == player.nxtdir):
            return [-player.curdir[1], player.curdir[0]]
        else:
            return [-player.nxtdir[0], -player.nxtdir[1]]

    @classmethod
    def avoid(cls, player, sprite):
        distance = retro.Math.distance(player.rect.center, sprite.rect.center)
        if distance > 50 : return False
        else: return cls.direction(sprite, player, invert = True)

    @classmethod
    def avoid_ghosts(cls, player, ghost):
        if (not ghost) or (ghost.state == ghost.state.FEAR): return False
        return cls.avoid(player, ghost)

    @classmethod
    def seek_sprite(cls, player, sprite):
        if not sprite: return False
        else: return cls.direction(sprite, player)

    def main(self):
        if not self.game.finished:
            player = self.game.player
            bonus  = self.game.maze.bonuses.nearest(player)
            ghost  = self.game.target(self.game.ghosts)

            nxtdir_wall  = self.follow_wall(player)
            nxtdir_ghost = self.avoid_ghosts(player, ghost)
            nxtdir_bonus = self.seek_sprite(player, bonus)
            nxtdir_rand  = self.rand_impulse.run(player)

            if player.curdir == [0, 0]:
                player.nxtdir = [1, 0]
            elif nxtdir_wall:
                player.nxtdir = nxtdir_wall
            elif nxtdir_ghost:
                player.nxtdir = nxtdir_ghost
            elif nxtdir_rand:
                player.nxtdir = nxtdir_rand
            elif nxtdir_bonus:
                player.nxtdir = nxtdir_bonus

            self.game.update()
            self.game.draw()
        else:
            print(self.game.fitness)
            self.game.reset()

    def loop(self):
        self.window.loop(self.main)

PlayAuto().loop()
