import sys
import retro
from game import Game

window = retro.Window(
    title     = "Pacman",
    size      = (448, 528),
    framerate = 60,
)
events = retro.Events()
game = Game(window)

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    elif events.key_press(retro.K_UP):    game.player.speed[1] = -1
    if   events.key_press(retro.K_DOWN):  game.player.speed[1] =  1
    elif events.key_press(retro.K_LEFT):  game.player.speed[0] = -1
    elif events.key_press(retro.K_RIGHT): game.player.speed[0] =  1

    game.run()

    window.update()
