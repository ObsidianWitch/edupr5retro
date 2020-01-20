import types
import shared.retro as retro
from maze.states.run import StateRun
from maze.states.end import StateEnd

class Game:
    def __init__(self, window):
        self.window = window
        self.state = None

    def run(self):
        if self.state is None:
            self.state = StateRun(window)

        elif type(self.state) == StateRun:
            if self.state.win:
                self.state = StateEnd(window)
            else:
                self.state.run()

        elif type(self.state) == StateEnd:
            if self.state.restart:
                self.state = StateRun(window)
            else:
                self.state.run()

window = retro.Window(
    title = "Maze",
    size  = (400, 400),
)
window.cursor(False)
game = Game(window)
window.loop(game.run)
