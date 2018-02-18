import types

from shared.window  import Window
from maze.state_run import StateRun
from maze.state_end import StateEnd

window = Window(
    width  = 400,
    height = 400,
    title  = "Maze"
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
        win = states.instance.run()
        if not win: return

        states.instance = StateEnd(window)
        states.current  = states.END

    elif states.current == states.END:
        restart = states.instance.run()
        if not restart: return

        states.instance = StateRun(window)
        states.current  = states.RUN

window.loop(game)
