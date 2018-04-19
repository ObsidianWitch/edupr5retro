import sys
import retro
from game.game import Games
from game.maze import Maze
from nn import NNGAPool

ANALYSIS = sys.argv[1] if len(sys.argv) > 1 else False

window = retro.Window(
    title     = "Pacman",
    size      = (448, 528),
    framerate = 0,
)
events = retro.Events()

games = Games(window, size = 200)
pool = NNGAPool(size = len(games), arch = (7, 10, 4))

def vsub(s1, s2): return (
    s1.rect.centerx - s2.rect.centerx,
    s1.rect.centery - s2.rect.centery,
)

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if not games.finished:
        for i, g in enumerate(games):
            if g.finished: continue
            player = g.player
            ghost  = g.target(g.ghosts)
            bonus  = g.maze.bonuses.nearest(player)

            p = pool[i].predict(
                *vsub(ghost, player) if ghost else (-1.0, -1.0),
                *vsub(bonus, player) if bonus else (-1.0, -1.0),
                ghost.state.current if ghost else 0.0,
                1.0 if player.curcol else 0.0,
                1.0 if player.nxtcol else 0.0,
            )

            dirs = ([-1, 0], [ 0, -1], [ 1,  0], [ 0,  1])
            idir = sorted(
                range(len(p)),
                key = lambda i: p[i],
                reverse = True,
            )[0]
            player.nxtdir = dirs[idir]

            g.update()
        games.best.draw()

    else:
        best_fitness = pool.evolve(games)

        if ANALYSIS:
            print(pool.generation - 1, best_fitness)
            if pool.generation - 1 >= 50: sys.exit()

        games.reset()

    window.update()
