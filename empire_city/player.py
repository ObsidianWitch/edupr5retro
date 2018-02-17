from empire_city.common import asset_path
from shared.sprite import Sprite

class Player:
    def __init__(self, window):
        self.window = window

        self.speed = 5

        self.crosshair = Sprite.from_paths(
            paths    = [asset_path("viseur.png")],
            position = (0, 0),
        )
        self.crosshair.rect.center = window.rect.center

    def draw(self):
        self.window.screen.blit(
            source = self.crosshair.image,
            dest   = self.crosshair.rect
        )

    def move(self, directions):
        move_vec = directions.vec
        self.crosshair.rect.move_ip(
            move_vec[0] * self.speed,
            move_vec[1] * self.speed,
        )
