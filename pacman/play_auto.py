import sys
import random
import numpy
from retro.src import retro
from pacman.game.parameters import Parameters
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

def direction(s1, s2, invert = False):
    dv = numpy.subtract(s1.rect.center, s2.rect.center).tolist()
    if invert:
        dv = numpy.negative(dv).tolist()
    if   dv[0] < 0: return [-1,  0]
    elif dv[0] > 0: return [ 1,  0]
    elif dv[1] < 0: return [ 0, -1]
    elif dv[1] > 0: return [ 0,  1]
    else: return False

def follow_wall(player):
    if not player.curcol: return False
    elif (not player.nxtcol) or (player.curdir == player.nxtdir):
        return [-player.curdir[1], player.curdir[0]]
    else:
        return [-player.nxtdir[0], -player.nxtdir[1]]

def avoid(player, sprite):
    distance = retro.Math.distance(player.rect.center, sprite.rect.center)
    if distance > 50 : return False
    else: return direction(sprite, player, invert = True)

def avoid_ghosts(player, ghost):
    if (not ghost) or (ghost.state == ghost.state.FEAR): return False
    return avoid(player, ghost)

def seek_sprite(player, sprite):
    if not sprite: return False
    else: return direction(sprite, player)

small_maze = any(arg == "--small" for arg in sys.argv)
parameters = Parameters.small() if small_maze else Parameters.classic()
window = retro.Window(
    title = "Pacman",
    size  = parameters.window_size,
    fps   = 0,
)
game = Game(window, parameters)
rand_impulse = RandImpulse()

def main():
    if not game.finished:
        player = game.player
        bonus  = game.maze.bonuses.nearest(player)
        ghost  = game.target(game.ghosts)

        nxtdir_wall  = follow_wall(player)
        nxtdir_ghost = avoid_ghosts(player, ghost)
        nxtdir_bonus = seek_sprite(player, bonus)
        nxtdir_rand  = rand_impulse.run(player)

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

        game.update()
        game.draw()
    else:
        print(game.fitness)
        game.reset()

window.loop(main)
