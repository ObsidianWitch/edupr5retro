from retro.src import retro

class End:
    def __init__(self, window):
        self.window = window
        self.restart = False

        self.txt = retro.Sprite(self.window.fonts[4].render(
            text    = "WIN",
            color   = retro.WHITE,
            bgcolor = retro.BLACK,
        ))
        self.txt.rect.center = self.window.rect().center

    def update(self):
        self.restart = (not self.restart) \
                   and self.window.events.key_press(retro.K_SPACE)

    def render(self):
        self.txt.draw(self.window)
