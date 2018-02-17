import pygame

from shared.math    import Directions
from shared.window  import Window
from shared.sprite  import Sprite
from empire_city.common import asset_path
from empire_city.player import Player

window = Window(
    width  = 400,
    height = 300,
    title  = "Empire City",
)

camera = window.rect.move(350, 170)

bg = Sprite.from_paths(
    paths    = [asset_path("map.png")],
    position = (0, 0),
)

player = Player(window)

def game():
    # Update
    keys = pygame.key.get_pressed()

    player.move(
        directions = Directions(
            up    = keys[pygame.K_UP],
            down  = keys[pygame.K_DOWN],
            left  = keys[pygame.K_LEFT],
            right = keys[pygame.K_RIGHT],
        )
    )

    # Draw
    window.screen.blit(
        source = bg.image,
        dest   = (0, 0),
        area   = camera
    )

    player.draw()

window.loop(game)
