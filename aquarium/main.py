import os, inspect

import pygame

from aquarium.fish import Fish
from shared.window import Window
from shared.sprite import Sprite

asset_path = lambda filename: os.path.join("aquarium/data", filename)

bg = Sprite.from_path(asset_path("fond.png"))

window = Window(
    size  = bg.rect.size,
    title = "Aquarium",
)

fish1 = Fish(
    window = window,
    speed  = (-2, 0),
    move   = Fish.move1,
    sprite = Sprite.from_path(
        path     = asset_path("fish1.bmp"),
        position = (100, 200),
    )
)
fish1.colorkey((170, 238, 255))
fish1.scale(0.5)

fish2 = Fish(
    window = window,
    speed  = (2, 1),
    move   = Fish.move2,
    sprite = Sprite.from_path(
        path     = asset_path("fish2.bmp"),
        position = (200, 300),
    )
)
fish2.colorkey((170, 238, 255))

fish3 = Fish(
    window = window,
    speed  = (2, 2),
    move   = Fish.move3,
    sprite = Sprite.from_path(
        path     = asset_path("fish3.bmp"),
        position = (200, 200),
    )
)
fish3.colorkey((170, 255, 238))
fish3.scale(1.1)

plant1 = Sprite.from_path(
    path     = asset_path("plant1.bmp"),
    position = (100, 170),
)
plant1.colorkey((255, 7, 0))
plant1.scale(0.5)

plant2 = Sprite.from_path(
    path     = asset_path("plant2.bmp"),
    position = (360, 170),
)
plant2.colorkey((255, 7, 0))
plant2.scale(0.7)

decor1 = Sprite.from_path(
    path     = asset_path("decor1.bmp"),
    position = (500, 175),
)
decor1.colorkey((255, 0, 0))
decor1.scale(0.7)

decor2 = Sprite.from_path(
    path     = asset_path("decor2.bmp"),
    position = (260, 260),
)
decor2.colorkey((255, 7, 0))
decor2.scale(0.3)

layers = [pygame.sprite.Group()] * 5
layers[0].add(bg)
layers[1].add(fish1, fish2)
layers[2].add(plant1, plant2)
layers[3].add(fish3)
layers[4].add(decor1, decor2)

def game():
    # Update
    fish1.update()
    fish2.update()
    fish3.update()

    # Draw
    for layer in layers: layer.draw(window.screen)

window.loop(game)
