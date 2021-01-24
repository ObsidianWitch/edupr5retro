from retro.src import retro
from maze import states

class Game:
    def __init__(self, window):
        self.window = window
        self.state = None

    def update(self):
        if self.state is None:
            self.state = states.Run(window)

        elif type(self.state) == states.Run:
            if self.state.win:
                self.state = states.End(window)
            else:
                self.state.update()

        elif type(self.state) == states.End:
            if self.state.restart:
                self.state = states.Run(window)
            else:
                self.state.update()

    def render(self):
        self.state.render()

window = retro.Window(title='Maze', size=(400, 400), fps=60)
window.cursor(False)
game = Game(window)

window.loop(game.update, game.render)
