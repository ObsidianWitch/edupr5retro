from shared.sprite import Sprite
from empire_city.common import asset_path

class Hints:
    def __init__(self, camera):
        self.camera = camera
        self.window = camera.window
        self.bg     = camera.bg

        self.sprites = (
            Sprite.from_path(asset_path("fleche_gauche.png")),
            Sprite.from_path(asset_path("fleche_droite.png")),
        )
        self.sprites[0].rect.midleft  = self.window.rect.midleft
        self.sprites[1].rect.midright = self.window.rect.midright

    def draw_screen(self, player, enemy):
        if not enemy.alive: return

        enemy_visible = self.camera.display_zone.colliderect(enemy.rect)
        if enemy_visible: return

        arrow_i = (self.camera.bg_space(
            player.crosshair.rect.center
        )[0] < enemy.rect.x)
        self.sprites[arrow_i].draw(self.window.screen)
