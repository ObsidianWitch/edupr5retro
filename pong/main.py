import types
import pygame

from shared.window import Window
from pong.state_run import StateRun
from pong.state_end import StateEnd

window = Window(
    width  = 600,
    height = 400,
    title  = "Pong"
)

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
        if states.instance.winner:
            states.instance = StateEnd(window, states.instance.winner)
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
