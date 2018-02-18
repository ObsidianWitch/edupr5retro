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
        winner = states.instance.run()
        if winner == 0: return

        states.instance = StateEnd(window, winner)
        states.current  = states.END

    elif states.current == states.END:
        restart = states.instance.run()
        if not restart: return

        states.instance = StateRun(window)
        states.current  = states.RUN

window.loop(game)
