import sys
import retro
from game.game import Game

window = retro.Window(
    title     = "Pacman",
    size      = (320, 240),
    framerate = 60,
)
events = retro.Events()
game = Game(window)

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if not game.finished:
        maze = game.maze
        player = game.player
        ghosts = game.ghosts

        if   events.key_press(retro.K_UP):    player.nxtdir = [ 0, -1]
        elif events.key_press(retro.K_DOWN):  player.nxtdir = [ 0,  1]
        elif events.key_press(retro.K_LEFT):  player.nxtdir = [-1,  0]
        elif events.key_press(retro.K_RIGHT): player.nxtdir = [ 1,  0]
        elif events.key_press(retro.K_SPACE):
            maze.print(player, ghosts)
            print(maze.walls.floor_cells(
                *maze.tile_pos(player.rect.center)
            ))

        game.update()
        game.draw()
    else:
        game.reset()

    window.update()
