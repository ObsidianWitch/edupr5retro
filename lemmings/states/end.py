import shared.retro as retro

class End:
    def __init__(self, window, win):
        self.window = window
        self.restart = False

        self.txt = retro.Sprite(self.window.fonts[4].render(
            text    = "WIN" if win else "LOST",
            color   = retro.WHITE,
            bgcolor = retro.BLACK,
        ))
        self.txt.rect.center = self.window.rect().center

    def run(self):
        # Update
        self.restart = self.window.events.key_press(retro.K_SPACE)

        # Draw
        self.txt.draw(self.window)
