import types

from shared.window import Window
from empire_city.state_run import StateRun
from empire_city.state_end import StateEnd

window = Window(
    width  = 400,
    height = 300,
    title  = "Empire City",
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
        end = states.instance.run()
        if not end: return

        states.instance = StateEnd(window)
        states.current  = states.END

    elif states.current == states.END:
        restart = states.instance.run()
        if not restart: return

        states.instance = StateRun(window)
        states.current  = states.RUN

window.loop(game)
