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

bg = Sprite.from_paths([asset_path("map.png")])

player = Player(window)

enemies = Enemies(bg)

camera = Camera(
    window   = window,
    bg       = bg,
    position = (350, 170),
)

def game():
    # Update
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

    enemies.update()

    # Draw
    window.screen.blit(
        source = bg.image,
        dest   = (0, 0),
        area   = camera.display_zone
    )

    player.draw()
    enemies.draw()

window.loop(game)
