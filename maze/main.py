import types
from shared.window import Window
from maze.states.run import StateRun
from maze.states.end import StateEnd

window = Window(
    title = "Maze",
    size  = (400, 400),
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
        if states.instance.win:
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
