import random

import pygame

from shared.math   import Directions
from shared.window import Window
from shared.sprite import Sprite
from empire_city.common  import asset_path
from empire_city.camera  import Camera
from empire_city.player  import Player
from empire_city.enemies import Enemies

window = Window(
    width  = 400,
    height = 300,
    title  = "Empire City",
)

bg0 = Sprite.from_paths([asset_path("map.png")])
bg  = Sprite.from_paths([asset_path("map.png")])

player = Player(window)

enemies = Enemies(bg)

camera = Camera(
    window   = window,
    bg       = bg,
    position = (350, 170),
)

def bg_space(p): return (
        p[0] + camera.display_zone.x,
        p[1] + camera.display_zone.y,
    )

def move():
    scroll_vec = camera.scroll_zone_collide(
        player.crosshair.rect.center
    ).vec

    player.move(
        move_vec = Directions(
            up    = window.keys[pygame.K_UP],
            down  = window.keys[pygame.K_DOWN],
            left  = window.keys[pygame.K_LEFT],
            right = window.keys[pygame.K_RIGHT],
        ).vec,
        collisions_vec = scroll_vec,
    )

    camera.update(scroll_vec)

def shoot():
    shoot = False
    for event in window.events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            shoot = True
            break

    if not shoot: return

    player.crosshair.rect.move_ip(
        random.randint(-2, 2),
        random.randint(-2, 2)
    )
    enemies.killcollide(
        bg_space(player.crosshair.rect.center)
    )

def game():
    # Update
    move()
    shoot()
    enemies.update()

    # Draw
    ## bg drawing
    bg.image.blit(bg0.image, (0, 0))
    enemies.draw()

    ## screen drawing
    window.screen.blit(
        source = bg.image,
        dest   = (0, 0),
        area   = camera.display_zone
    )
    player.draw()

window.loop(game)
