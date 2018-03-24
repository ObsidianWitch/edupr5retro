import sys
import retro
from game import Game

window = retro.Window(
    title = "Pacman",
    size  = (448, 528),
)
events = retro.Events()
game = Game(window)

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    game.run()

    window.update()
