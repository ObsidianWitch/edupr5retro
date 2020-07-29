import pygame
from retro.src import retro
from lemmings.states.level1 import Level1
from lemmings.states.level2 import Level2
from lemmings.states.end import End

class Game:
    def __init__(self, window):
        self.window = window
        self.state = None

    def run(self):
        if self.state is None:
            self.state = Level1(self.window)

        elif type(self.state) == Level1:
            if self.state.win:
                self.state = Level2(window)
            elif self.state.lost:
                self.state = End(window, win = False)
            else:
                self.state.run()

        elif type(self.state) == Level2:
            if self.state.win:
                self.state = End(window, win = True)
            elif self.state.lost:
                self.state = End(window, win = False)
            else:
                self.state.run()

        elif type(self.state) == End:
            if self.state.restart:
                self.state = Level1(window)
            else:
                self.state.run()

window = retro.Window(
    title  = "Lemmings",
    size   = (800, 400),
    fps    = 30,
)
window.cursor(pygame.cursors.diamond)
game = Game(window)

window.loop(game.run)
