import sys
from retro.src import retro
from pacman.game.parameters import Parameters
from pacman.game.game import Game

small_maze = any(arg == "--small" for arg in sys.argv)
parameters = Parameters.small() if small_maze else Parameters.classic()
window = retro.Window(
    title = "Pacman",
    size  = parameters.window_size,
    fps   = 60,
)
game = Game(window, parameters)

def main():
    if not game.finished:
        maze = game.maze
        player = game.player
        ghosts = game.ghosts

        key = window.events.key_press
        if   key(retro.K_UP):    player.nxtdir = [ 0, -1]
        elif key(retro.K_DOWN):  player.nxtdir = [ 0,  1]
        elif key(retro.K_LEFT):  player.nxtdir = [-1,  0]
        elif key(retro.K_RIGHT): player.nxtdir = [ 1,  0]
        elif key(retro.K_SPACE):
            maze.print(player, ghosts)
            print(maze.walls.floor_cells(
                *maze.tile_pos(player.rect.center)
            ))

        game.update()
        game.draw()
    else:
        game.reset()

window.loop(main)
