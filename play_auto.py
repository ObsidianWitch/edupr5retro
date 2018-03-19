import retro
import sys
from game import Game

window = retro.Window(
    title = "Flappy Bird",
    size  = (288, 512),
)
events = retro.Events()

game = Game(window, nbirds = 1)

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if not game.finished:
        b = game.birds[0]
        v_distance = b.rect.y - game.target.centery
        if v_distance + b.speed_y > 0: b.flap()
        game.run()
    else:
        game.reset()

    window.update()
