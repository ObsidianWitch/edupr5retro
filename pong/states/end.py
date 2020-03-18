import shared.retro as retro

class StateEnd:
    def __init__(self, window, winner):
        self.window = window
        self.restart = False

        self.txt = retro.Sprite(self.window.fonts[4].render(
            text    = f"JOUEUR {winner} GAGNANT",
            color   = retro.YELLOW,
            bgcolor = retro.RED,
        ))
        self.txt.rect.center = self.window.rect().center

    def run(self):
        # Update
        key = self.window.events.key_press
        self.restart = key(retro.K_SPACE)

        # Draw
        self.txt.draw(self.window)
