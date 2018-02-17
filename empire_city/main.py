import os

import pygame

from shared.window  import Window
from shared.sprite import Sprite

asset_path = lambda filename: os.path.join("empire_city/data", filename)

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

def game():
    # Update

    # Draw
    window.screen.blit(
        source = bg.image,
        dest   = (0, 0),
        area   = camera
    )

window.loop(game)
