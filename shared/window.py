import sys
import include.retro as retro

class Window(retro.Window):
    def __init__(self, title, size):
        retro.Window.__init__(self, title, size)

        # Ascending size fonts
        self.fonts = list(
            retro.Font(size)
            for size in range(18, 43, 6)
        )

        self.events = retro.Events()

    def loop(self, instructions):
        while 1:
            self.events.update()
            if self.events.event(retro.QUIT): sys.exit()

            instructions()

            self.update()
