from lemmings.characters.lemmings import Lemmings
from lemmings.bg import BG
from lemmings.ui import UI

class StateRun:
    def __init__(self, window):
        self.window = window
        self.bg = BG()
        self.lemmings = Lemmings(self.window, self.bg)
        self.ui = UI(self.window)

    def run(self):
        # update
        self.ui.update()
        self.lemmings.update(self.ui.selection.state)

        # Draw
        self.bg.clear()
        self.lemmings.draw_bg()

        self.window.screen.blit(self.bg.current, (0,0))
        self.ui.draw()
        self.lemmings.draw_screen()
