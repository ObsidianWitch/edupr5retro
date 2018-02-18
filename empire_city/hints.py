from shared.sprite import Sprite
from empire_city.common  import asset_path

class Hints:
    def __init__(self, camera, player, enemy):
        self.camera = camera
        self.window = camera.window
        self.bg     = camera.bg

        self.player = player
        self.enemy  = enemy

        self.sprites = (
            Sprite.from_paths([asset_path("fleche_gauche.png")]),
            Sprite.from_paths([asset_path("fleche_droite.png")]),
        )
        self.sprites[0].rect.midleft = self.window.rect.midleft
        self.sprites[1].rect.midright = self.window.rect.midright

    def draw_screen(self):
        if not self.enemy.alive: return

        enemy_visible = self.camera.display_zone.colliderect(
            self.enemy.mob.rect
        )
        if enemy_visible: return

        arrow_i = (
            self.camera.bg_space(
                self.player.crosshair.rect.center
            )[0] < self.enemy.mob.rect.x
        )
        self.window.screen.blit(
            self.sprites[arrow_i].image,
            self.sprites[arrow_i].rect
        )
