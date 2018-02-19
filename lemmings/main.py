import types

from shared.window import Window
from lemmings.state_run import StateRun

window = Window(
    width  = 800,
    height = 400,
    title  = "Lemmings",
)

states = types.SimpleNamespace(
    START    = 0,
    RUN      = 1,
    current  = 0,
    instance = None,
)

def game():
    if states.current == states.START:
        states.instance = StateRun(window)
        states.current  = states.RUN

    if states.current == states.RUN:
        states.instance.run()

window.loop(game)
