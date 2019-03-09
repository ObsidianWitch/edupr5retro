import os
import shared.retro as retro
from aquarium.fish import Fish
from shared.sprite import Sprite

asset_path = lambda filename: os.path.join("aquarium", "data", filename)

bg = Sprite.from_path(asset_path("fond.png"))

window = retro.Window(
    title = "Aquarium",
    size  = bg.rect.size,
)
window.cursor(False)

fish1 = Fish(
    window = window,
    speed  = (-2, 0),
    move   = Fish.move1,
    path   = asset_path("fish1.bmp"),
)
fish1.colorkey((170, 238, 255))
fish1.scale(0.5)
fish1.rect.move(100, 200)

fish2 = Fish(
    window = window,
    speed  = (2, 1),
    move   = Fish.move2,
    path   = asset_path("fish2.bmp"),
)
fish2.colorkey((170, 238, 255))
fish2.rect.move(200, 300)

fish3 = Fish(
    window = window,
    speed  = (2, 2),
    move   = Fish.move3,
    path   = asset_path("fish3.bmp"),
)
fish3.colorkey((170, 255, 238))
fish3.scale(1.1)
fish3.rect.move(200, 200)

plant1 = Sprite.from_path(asset_path("plant1.bmp"))
plant1.colorkey((255, 7, 0))
plant1.scale(0.5)
plant1.rect.move(100, 170)

plant2 = Sprite.from_path(asset_path("plant2.bmp"))
plant2.colorkey((255, 7, 0))
plant2.scale(0.7)
plant2.rect.move(360, 170)

decor1 = Sprite.from_path(asset_path("decor1.bmp"))
decor1.colorkey((255, 0, 0))
decor1.scale(0.7)
decor1.rect.move(500, 175)

decor2 = Sprite.from_path(asset_path("decor2.bmp"))
decor2.colorkey((255, 7, 0))
decor2.scale(0.3)
decor2.rect.move(260, 260)

layers = (
    retro.Group(bg),
    retro.Group(fish1, fish2),
    retro.Group(plant1, plant2),
    retro.Group(fish3),
    retro.Group(decor1, decor2),
)

def game():
    # Update
    fish1.update()
    fish2.update()
    fish3.update()

    # Draw
    for layer in layers: layer.draw(window)

window.loop(game)
