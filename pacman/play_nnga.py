import multiprocessing
import itertools
import types
import time
import sys
import numpy
import retro
from game.parameters import Parameters
from game.game import Game, Games
from game.maze import Maze
from nn import NNGAPool

def update_one(game, nn):
    if game.finished: return False

    maze   = game.maze
    player = game.player
    ghost  = game.target(game.ghosts)
    bonus  = maze.bonuses.nearest(player)

    p = nn.predict(
        *numpy.subtract(
            ghost.rect.center, player.rect.center
        ) if ghost else (-1.0, -1.0),
        ghost.state.current if ghost else -1,
        *numpy.subtract(
            bonus.rect.center, player.rect.center
        ) if bonus else (-1.0, -1.0),
        maze.bonuses.count,
        *maze.walls.floor_cells(
            *maze.tile_pos(player.rect.center)
        )
    )

    dirs = ([-1, 0], [ 0, -1], [ 1,  0], [ 0,  1])
    i = sorted(
        range(len(p)),
        key = lambda i: p[i],
        reverse = True,
    )[0]
    player.nxtdir = dirs[i]

    game.update()
    return True

def update_parallel(icore):
    window = retro.Window(
        title     = "Pacman",
        size      = parameters.window_size,
        framerate = 0,
    )
    games = Games(window, parameters, size = len(nn_pool) // cores)
    while not games.finished:
        for igame, game in enumerate(games):
            ipool = (len(games) * icore) + igame
            update_one(game, nn_pool[ipool])
        games.best.draw()
        window.update()

    return tuple(g.fitness for g in games)

def main_parallel():
    if nn_pool.generation > 50: return

    # Update
    start = time.time()
    with multiprocessing.Pool(cores) as mp_pool:
        scores = mp_pool.map(update_parallel, range(cores))
    end = time.time()

    # Adapt
    units = tuple(
        types.SimpleNamespace(fitness = score)
        for score in itertools.chain.from_iterable(scores)
    )

    # Evolve
    best = nn_pool.evolve(units)
    print(nn_pool.generation - 1, best.fitness, end - start)
    main_parallel()

def update_sequential(window, games):
    while not games.finished:
        for i, game in enumerate(games):
            update_one(game, nn_pool[i])
        games.best.draw()
        window.update()

def main_sequential(window = None, games = None):
    if nn_pool.generation > 50: return

    window = window or retro.Window(
        title     = "Pacman",
        size      = parameters.window_size,
        framerate = 0,
    )
    games = games or Games(window, parameters, size = len(nn_pool))

    # Update
    start = time.time()
    update_sequential(window, games)
    end = time.time()

    # Evolve
    best = nn_pool.evolve(games)
    print(nn_pool.generation - 1, best.fitness, end - start)
    games.reset()
    main_sequential(window, games)

nn_pool = NNGAPool(size = 200, arch = (10, 10, 10, 4))
cores = multiprocessing.cpu_count()
parallel = any(arg == "--parallel" for arg in sys.argv)
small_maze = any(arg == "--small" for arg in sys.argv)
parameters = Parameters.small() if small_maze else Parameters.classic()
Game(None, parameters) # set up constants in shared memory

if __name__ == '__main__':
    if parallel: main_parallel()
    else: main_sequential()
