import retro
import sys

window = retro.Window(
    title = "Pacman",
    size  = (400, 400),
)
events = retro.Events()

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    window.update()
