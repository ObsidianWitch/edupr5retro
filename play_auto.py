import sys
import random
import retro
from game.collisions import Collisions
from game.game import Game

class RandWalk:
    def __init__(self):
        self.i = 0

    @property
    def enabled(self): return self.i > 0

    def start(self, player):
        self.i = 50
        dirs = [[-1, 0], [ 0, -1], [ 1,  0], [ 0,  1]]
        if player.curdir in dirs: dirs.remove(player.curdir)
        return random.choice(dirs)

    def run(self, player):
        if not self.enabled:
            if random.uniform(0, 1) < 0.01: return self.start(player)
            else: return False
        else:
            self.i -= 1
            return True

def direction(s1, s2, invert = False):
    dx = s1.rect.centerx - s2.rect.centerx
    dy = s1.rect.centery - s2.rect.centery
    dx = -dx if invert else dx
    dy = -dy if invert else dy
    if   dx < 0: return [-1,  0]
    elif dx > 0: return [ 1,  0]
    elif dy < 0: return [ 0, -1]
    elif dy > 0: return [ 0,  1]
    else: return False

def walls(player):
    if not player.curcol: return False
    elif (not player.nxtcol) or (player.curdir == player.nxtdir):
        return [-player.curdir[1], player.curdir[0]]
    else:
        return [-player.nxtdir[0], -player.nxtdir[1]]

def bonuses(player, bonus):
    if not bonus: return False
    else: return direction(bonus, player)

def ghosts(player, ghost):
    if (not ghost) or (ghost.state == ghost.STATES.FEAR): return False

    distance = Collisions.distance(player.rect.center, ghost.rect.center)
    if distance > 2500 : return False
    else: return direction(ghost, player, invert = True)

window = retro.Window(
    title     = "Pacman",
    size      = (448, 528),
    framerate = 0,
)
events = retro.Events()
game = Game(window)
randwalk = RandWalk()

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if not game.finished:
        player = game.player
        bonus  = game.maze.bonuses.nearest(player.rect.topleft)
        ghost  = game.target(game.ghosts)

        nxtdir_w = walls(player)
        nxtdir_g = ghosts(player, ghost)
        nxtdir_b = bonuses(player, bonus)
        nxtdir_r = randwalk.run(player)

        if game.player.curdir == [0, 0]: game.player.nxtdir = [-1, 0]
        elif nxtdir_w: player.nxtdir = nxtdir_w
        elif nxtdir_g: player.nxtdir = nxtdir_g
        elif nxtdir_r:
            if isinstance(nxtdir_r, tuple): player.nxtdir = nxtdir_r
        elif nxtdir_b: player.nxtdir = nxtdir_b

        game.update()
        game.draw()
    else:
        game.reset()

    window.update()
