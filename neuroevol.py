import retro
import sys
from game import Game

window = retro.Window(
    title = "Flappy Bird",
    size  = (288, 512),
)
events = retro.Events()

game = Game(window, nbirds = 10)

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if not game.finished:
        for i, b in enumerate(game.birds):
            if b.alive and events.key_press(retro.K_SPACE): b.flap()
        game.run()
    else:
        game.reset()

    window.update()
