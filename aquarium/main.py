from pathlib import Path
import shared.retro as retro
from aquarium.fish import Fish

def asset(filename):
    return str(Path('aquarium/data') / filename)

class Game:
    def __init__(self, window):
        self.window = window

        bg = retro.Sprite.from_path([asset("fond.png")])

        fish1 = Fish(
            speed  = (-2, 0),
            move   = lambda self: Fish.move1(self, window.rect()),
            path   = asset("fish1.bmp"),
        )
        fish1.image.colorkey((170, 238, 255))
        fish1.image.scale(0.5)
        fish1.rect.move_ip(100, 200)

        fish2 = Fish(
            speed  = (2, 1),
            move   = lambda self: Fish.move2(self, window.rect()),
            path   = asset("fish2.bmp"),
        )
        fish2.image.colorkey((170, 238, 255))
        fish2.rect.move_ip(200, 300)

        fish3 = Fish(
            speed  = (2, 2),
            move   = lambda self: Fish.move3(self, window.rect()),
            path   = asset("fish3.bmp"),
        )
        fish3.image.colorkey((170, 255, 238))
        fish3.image.scale(1.1)
        fish3.rect.move_ip(200, 200)

        plant1 = retro.Sprite.from_path([asset("plant1.bmp")])
        plant1.image.colorkey((255, 7, 0))
        plant1.image.scale(0.5)
        plant1.rect.move_ip(100, 170)

        plant2 = retro.Sprite.from_path([asset("plant2.bmp")])
        plant2.image.colorkey((255, 7, 0))
        plant2.image.scale(0.7)
        plant2.rect.move_ip(360, 170)

        decor1 = retro.Sprite.from_path([asset("decor1.bmp")])
        decor1.image.colorkey((255, 0, 0))
        decor1.image.scale(0.7)
        decor1.rect.move_ip(500, 175)

        decor2 = retro.Sprite.from_path([asset("decor2.bmp")])
        decor2.image.colorkey((255, 7, 0))
        decor2.image.scale(0.3)
        decor2.rect.move_ip(260, 260)

        self.layers = (
            retro.Group(bg),
            retro.Group(fish1, fish2),
            retro.Group(plant1, plant2),
            retro.Group(fish3),
            retro.Group(decor1, decor2),
        )

    def run(self):
        # Update
        for layer in self.layers:
            layer.update()

        # Draw
        for layer in self.layers:
            layer.draw(self.window)

window = retro.Window(
    title = "Aquarium",
    size  = (800, 400),
)
window.cursor(False)
game = Game(window)
window.loop(game.run)
