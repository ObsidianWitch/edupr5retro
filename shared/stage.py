import shared.retro as retro

# A stage is a sprite that can be altered and restored to its `original` state.
# A portition of the sprite's image can be focused by manipulating its `camera`.
class Stage(retro.Sprite):
    def __init__(self, path):
        self.original = retro.Image.from_path(path)
        retro.Sprite.__init__(self, self.original.copy())

    @property
    def camera(self):
        return self.rect
    @camera.setter
    def camera(self, rect):
        self.rect = rect

    def camera2stage(self, p): return (
        p[0] + self.camera.x,
        p[1] + self.camera.y,
    )

    def stage2camera(self, p): return (
        p[0] - self.rect.x,
        p[1] - self.rect.y,
    )

    def clear_all(self):
        self.image.draw_img(self.original, (0, 0))

    def clear_focus(self):
        self.image.draw_img(self.original, self.camera.topleft, self.camera)
