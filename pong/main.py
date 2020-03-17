import shared.retro as retro
from pong.states.run import StateRun
from pong.states.end import StateEnd

class Game:
    def __init__(self, window):
        self.window = window
        self.state = None

    def run(self):
        if self.state is None:
            self.state = StateRun(self.window)

        elif type(self.state) == StateRun:
            if self.state.winner:
                self.state = StateEnd(self.window, self.state.winner)
            else:
                self.state.run()

        elif type(self.state) == StateEnd:
            if self.state.restart:
                self.state = StateRun(self.window)
            else:
                self.state.run()

window = retro.Window(
    size      = (600, 400),
    title     = "Pong",
    framerate = 60,
)
window.cursor(False)
game = Game(window)
window.loop(game.run)
