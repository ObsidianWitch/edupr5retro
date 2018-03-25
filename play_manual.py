import sys
import retro
from game import Game

window = retro.Window(
    title     = "Pacman",
    size      = (448, 528),
    framerate = 120,
)
events = retro.Events()
game = Game(window)

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if   events.key_press(retro.K_UP):    game.player.nxtdir = [ 0, -1]
    elif events.key_press(retro.K_DOWN):  game.player.nxtdir = [ 0,  1]
    elif events.key_press(retro.K_LEFT):  game.player.nxtdir = [-1,  0]
    elif events.key_press(retro.K_RIGHT): game.player.nxtdir = [ 1,  0]

    game.run()

    window.update()
