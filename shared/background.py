import shared.retro as retro

class Background:
    def __init__(self, path):
        self.original = retro.Image.from_path(path)
        self.current  = self.original.copy()
        self.rect = self.original.rect()

    def clear(self):
        self.current.draw_img(self.original, (0, 0))
