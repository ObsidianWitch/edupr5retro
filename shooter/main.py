import types
import include.retro as retro
from shooter.states.run import StateRun
from shooter.states.end import StateEnd

window = retro.Window(
    title = "Empire City",
    size  = (400, 300),
)
window.cursor(False)

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

    elif states.current == states.RUN:
        if states.instance.end:
            states.instance = StateEnd(window)
            states.current  = states.END
        else:
            states.instance.run()

    elif states.current == states.END:
        if states.instance.restart:
            states.instance = StateRun(window)
            states.current  = states.RUN
        else:
            states.instance.run()

window.loop(game)
