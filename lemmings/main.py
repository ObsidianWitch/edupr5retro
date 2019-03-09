import pygame
import types
import shared.retro as retro
from lemmings.states.level1 import Level1
from lemmings.states.level2 import Level2
from lemmings.states.end import End

window = retro.Window(
    title  = "Lemmings",
    size   = (800, 400),
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

    elif states.current == states.LEVEL1:
        if states.instance.win:
            states.instance = Level2(window)
            states.current  = states.LEVEL2
        elif states.instance.lost:
            states.instance = End(window, win = False)
            states.current  = states.END
        else:
            states.instance.run()

    elif states.current == states.LEVEL2:
        if states.instance.win:
            states.instance = End(window, win = True)
            states.current  = states.END
        elif states.instance.lost:
            states.instance = End(window, win = False)
            states.current  = states.END
        else:
            states.instance.run()

    elif states.current == states.END:
        if states.instance.restart:
            states.instance = Level1(window)
            states.current  = states.LEVEL1
        else:
            states.instance.run()

window.loop(game)
