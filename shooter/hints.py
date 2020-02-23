from shared.sprite import Sprite
from shooter.path import asset

class Hints:
    def __init__(self, camera):
        self.camera = camera
        self.window = camera.window

        self.sprites = (
            Sprite.from_path(asset("arrow_left.png")),
            Sprite.from_path(asset("arrow_right.png")),
        )
        self.sprites[0].rect.midleft  = self.window.rect().midleft
        self.sprites[1].rect.midright = self.window.rect().midright

    def draw(self, player, enemy, dest):
        if not enemy.alive: return

        enemy_visible = self.camera.rect.colliderect(enemy.rect)
        if enemy_visible: return

        arrow_i = (self.camera.bg_space(
            player.crosshair.rect.center
        )[0] < enemy.rect.x)
        self.sprites[arrow_i].draw(dest)
