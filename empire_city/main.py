import pygame

from shared.window import Window
from shared.sprite import Sprite
from empire_city.common  import asset_path
from empire_city.camera  import Camera
from empire_city.player import Player
from empire_city.enemy  import Enemy

window = Window(
    width  = 400,
    height = 300,
    title  = "Empire City",
)

bg0 = Sprite.from_paths([asset_path("map.png")])
bg  = Sprite.from_paths([asset_path("map.png")])

camera = Camera(
    window   = window,
    bg       = bg,
    position = (350, 170),
)

player = Player(window, camera)
enemy = Enemy(bg)

hint_left = Sprite.from_paths([asset_path("fleche_gauche.png")])
hint_left.rect.midleft = window.rect.midleft
hint_right = Sprite.from_paths([asset_path("fleche_droite.png")])
hint_right.rect.midright = window.rect.midright

def draw_hints():
    if not enemy.alive: return

    enemy_visible = camera.display_zone.colliderect(enemy.mob.rect)
    if enemy_visible: return

    enemy_left = (
        camera.bg_space(player.crosshair.rect.center)[0] > enemy.mob.rect.x
    )
    if enemy_left: window.screen.blit(hint_left.image, hint_left.rect)
    else: window.screen.blit(hint_right.image, hint_right.rect)

def game():
    # Update
    scroll_vec = camera.scroll_zone_collide(
        player.crosshair.rect.center
    ).vec
    player.move(scroll_vec)
    camera.move(scroll_vec)
    player.shoot(enemy)
    enemy.update()

    # Draw
    ## bg drawing
    bg.image.blit(bg0.image, (0, 0))
    enemy.draw()

    ## screen drawing
    window.screen.blit(
        source = bg.image,
        dest   = (0, 0),
        area   = camera.display_zone
    )
    player.draw()
    draw_hints()

window.loop(game)
