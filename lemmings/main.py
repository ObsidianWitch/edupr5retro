import pygame
from retro.src import retro
from lemmings.states.level import Level, Level1, Level2
from lemmings.states.end import End

class Game:
    def __init__(self, window):
        self.window = window
        self.state = None

    def update(self):
        # reset
        if (self.window.events.key_release(retro.K_BACKSPACE)
            and isinstance(self.state, Level)
        ):
            self.state = type(self.state)(self.window)

        if self.state is None:
            self.state = Level1(self.window)
        elif type(self.state) == Level1:
            if self.state.win:
                self.state = Level2(window)
            elif self.state.lost:
                self.state = type(self.state)(self.window)
            else:
                self.state.update()
        elif type(self.state) == Level2:
            if self.state.win:
                self.state = End(window)
            elif self.state.lost:
                self.state = type(self.state)(self.window)
            else:
                self.state.update()
        elif type(self.state) == End:
            if self.state.restart:
                self.state = Level1(window)
            else:
                self.state.update()

    def render(self):
        self.state.render()

window = retro.Window(title='Lemmings', size=(800, 400), fps=45)
window.cursor(pygame.cursors.diamond)
game = Game(window)

window.loop(game.update, game.render)
