import pygame
import types

from shared.window import Window
from lemmings.states.level1 import Level1
from lemmings.states.level2 import Level2
from lemmings.states.end import End

window = Window(
    width  = 800,
    height = 400,
    title  = "Lemmings",
    cursor = True,
)

pygame.mouse.set_cursor(*pygame.cursors.diamond)

states = types.SimpleNamespace(
    START    = 0,
    LEVEL1   = 1,
    LEVEL2   = 2,
    END      = 3,
    current  = 0,
    instance = None,
)

def game():
    if states.current == states.START:
        states.instance = Level1(window)
        states.current  = states.LEVEL1

    if states.current == states.LEVEL1:
        if states.instance.win:
            states.instance = Level2(window)
            states.current  = states.LEVEL2
        else:
            states.instance.run()

    if states.current == states.LEVEL2:
        if states.instance.win:
            states.instance = End(window)
            states.current  = states.END
        else:
            states.instance.run()

    if states.current == states.END:
        if states.instance.restart:
            states.instance = Level1(window)
            states.current  = states.LEVEL1
        else:
            states.instance.run()

window.loop(game)
