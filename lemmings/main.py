import pygame
import types

from shared.window import Window
from lemmings.state_run import StateRun
from lemmings.state_end import StateEnd

window = Window(
    width  = 800,
    height = 400,
    title  = "Lemmings",
    cursor = True,
)

pygame.mouse.set_cursor(*pygame.cursors.diamond)

states = types.SimpleNamespace(
    START    = 0,
    RUN      = 1,
    END      = 2,
    current  = 0,
    instance = None,
)

def game():
    if states.current == states.START:
        states.instance = StateRun(window)
        states.current  = states.RUN

    if states.current == states.RUN:
        if states.instance.win:
            states.instance = StateEnd(window)
            states.current  = states.END
        else:
            states.instance.run()

    if states.current == states.END:
        if states.instance.restart:
            states.instance = StateRun(window)
            states.current  = states.RUN
        else:
            states.instance.run()

window.loop(game)
