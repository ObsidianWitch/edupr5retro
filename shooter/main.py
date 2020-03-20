from retro.src import retro
from shooter import states

class Game:
    def __init__(self, window):
        self.window = window
        self.state = None

    def run(self):
        if self.state is None:
            self.state = states.Run(window)

        elif type(self.state) == states.Run:
            if self.state.finished:
                self.state = states.End(window)
            else:
                self.state.run()

        elif type(self.state) == states.End:
            if self.state.restart:
                self.state = states.Run(window)
            else:
                self.state.run()

window = retro.Window(
    title = "Empire City",
    size  = (400, 300),
)
window.cursor(False)
game = Game(window)
window.loop(game.run)
