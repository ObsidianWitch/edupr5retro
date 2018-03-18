import sys
import retro

window = retro.Window(
    title = "Flappy Bird",
    size  = (288, 512),
)
events = retro.Events()

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    # TODO

    window.update()
