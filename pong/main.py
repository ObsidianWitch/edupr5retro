from retro.out import retro
from pong import states

class Game:
    def __init__(self, window):
        self.window = window
        self.state = None

    def run(self):
        if self.state is None:
            self.state = states.Run(self.window)

        elif type(self.state) == states.Run:
            if self.state.winner:
                self.state = states.End(self.window, self.state.winner)
            else:
                self.state.run()

        elif type(self.state) == states.End:
            if self.state.restart:
                self.state = states.Run(self.window)
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
