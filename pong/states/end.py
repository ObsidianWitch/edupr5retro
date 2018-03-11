import include.retro as retro
class StateEnd:
    def __init__(self, window, winner):
        self.window = window
        self.restart = False

        self.txt_img = self.window.fonts[4].render(
            text    = f"JOUEUR {winner} GAGNANT",
            color   = retro.YELLOW,
            bgcolor = retro.RED,
        )
        self.txt_rect = self.txt_img.rect
        self.txt_rect.center = self.window.rect.center

    def run(self):
        # Update
        key = self.window.events.key_press
        self.restart = key(retro.K_SPACE)

        # Draw
        self.window.draw_image(self.txt_img, self.txt_rect)
