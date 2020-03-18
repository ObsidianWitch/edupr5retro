import shared.retro as retro

class StateEnd:
    def __init__(self, window):
        self.window = window
        self.restart = False

        self.txt = retro.Sprite(self.window.fonts[4].render(
            text    = f"WIN",
            color   = retro.WHITE,
            bgcolor = retro.BLACK,
        ))
        self.txt.rect.center = self.window.rect().center

    def run(self):
        # Update
        key = self.window.events.key_press
        self.restart = key(retro.K_SPACE)

        # Draw
        self.txt.draw(self.window)
