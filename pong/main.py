from retro.src import retro
from pong import states

class Game:
    def __init__(self, window):
        self.window = window
        self.state = None

    def update(self):
        if self.state is None:
            self.state = states.Run(self.window)

        elif type(self.state) == states.Run:
            if self.state.winner:
                self.state = states.End(self.window, self.state.winner)
            else:
                self.state.update()

        elif type(self.state) == states.End:
            if self.state.restart:
                self.state = states.Run(self.window)
            else:
                self.state.update()

    def render(self):
        self.state.render()

window = retro.Window(title='Pong', size=(600, 400), fps=120)
window.cursor(False)
game = Game(window)

window.loop(game.update, game.render)
