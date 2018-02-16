import os, inspect

import pygame

from aquarium.fish import Fish
from shared.window import Window
from shared.sprite import Sprite

asset_path = lambda filename: os.path.join("aquarium/data", filename)

bg = Sprite.from_images(
    paths    = [asset_path("fond.png")],
    position = (0, 0)
)

window = Window(
    width  = bg.rect.width,
    height = bg.rect.height,
    title  = "Aquarium"
)

fish1 = Fish(
    window = window,
    speed  = (-2, 0),
    move   = Fish.move1,
    sprite = Sprite.from_images(
        paths    = [asset_path("fish1.bmp")],
        position = (100, 200),
        colorkey = (170, 238, 255),
    )
)
fish1.sprite.scale_ip(0.5)

fish2 = Fish(
    window = window,
    speed  = (2, 1),
    move   = Fish.move2,
    sprite = Sprite.from_images(
        paths    = [asset_path("fish2.bmp")],
        position = (200, 300),
        colorkey = (170, 238, 255)
    )
)

fish3 = Fish(
    window = window,
    speed  = (2, 2),
    move   = Fish.move3,
    sprite = Sprite.from_images(
        paths    = [asset_path("fish3.bmp")],
        position = (200, 200),
        colorkey = (170, 255, 238),
    )
)
fish3.sprite.scale_ip(1.1)

plant1 = Sprite.from_images(
    paths    = [asset_path("plant1.bmp")],
    position = (100, 170),
    colorkey = (255, 7 ,0),
)
plant1.scale_ip(0.5)

plant2 = Sprite.from_images(
    paths    = [asset_path("plant2.bmp")],
    position = (360, 170),
    colorkey = (255, 7 ,0),
)
plant2.scale_ip(0.7)

decor1 = Sprite.from_images(
    paths    = [asset_path("decor1.bmp")],
    position = (500, 175),
    colorkey = (255, 0 ,0),
)
decor1.scale_ip(0.7)

decor2 = Sprite.from_images(
    paths    = [asset_path("decor2.bmp")],
    position = (260, 260),
    colorkey = (255, 7 ,0),
)
decor2.scale_ip(0.3)

layers = [pygame.sprite.Group()] * 5
layers[0].add(bg)
layers[1].add(fish1.sprite, fish2.sprite)
layers[2].add(plant1, plant2)
layers[3].add(fish3.sprite)
layers[4].add(decor1, decor2)

def game():
    # Update
    fish1.update()
    fish2.update()
    fish3.update()

    # Draw
    for layer in layers: layer.draw(window.screen)

window.loop(game)
