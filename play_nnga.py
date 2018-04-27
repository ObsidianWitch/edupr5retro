import sys
import retro
from game.game import Games
from game.maze import Maze
from nn import NNGAPool

def vsub(s1, s2): return (
    s1.rect.centerx - s2.rect.centerx,
    s1.rect.centery - s2.rect.centery,
)

def update(i, g):
    if g.finished: return
    player = g.player
    ghost  = g.target(g.ghosts)
    bonus  = g.maze.bonuses.nearest(player)

    p = pool[i].predict(
        *vsub(ghost, player) if ghost else (-1.0, -1.0),
        ghost.state.current if ghost else -1,
        *vsub(bonus, player) if bonus else (-1.0, -1.0),
        g.maze.bonuses.count,
        *g.maze.walls.floor_cells(
            *g.maze.tile_pos(player.rect.center)
        )
    )

    dirs = ([-1, 0], [ 0, -1], [ 1,  0], [ 0,  1])
    idir = sorted(
        range(len(p)),
        key = lambda i: p[i],
        reverse = True,
    )[0]
    player.nxtdir = dirs[idir]

    g.update()

window = retro.Window(
    title     = "Pacman",
    size      = (448, 528),
    framerate = 0,
)
events = retro.Events()

games = Games(window, size = 200)
pool = NNGAPool(size = len(games), arch = (10, 10, 10, 4))

while pool.generation <= 50:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if not games.finished:
        for i, g in enumerate(games): update(i, g)
        games.best.draw()
    else:
        best_fitness = pool.evolve(games)
        print(pool.generation - 1, best_fitness)
        games.reset()

    window.update()
