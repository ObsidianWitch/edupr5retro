import math
from pathlib import Path
from retro.src import retro
from aquarium.fish import Fish

def asset(filename):
    return str(Path('aquarium/assets') / filename)

class Background(retro.Sprite):
    def __init__(self, path):
        image = retro.Image.from_path(path)
        retro.Sprite.__init__(self, image)

    def tilex(self, target):
        image = retro.Image((target.rect().width, self.rect.height))
        repeat = math.ceil(target.rect().width / self.rect.width)

        for i in range(repeat):
            image.draw_img(self.image, (i * self.rect.width, 0))

        self.image = image
        self.rect.size = image.rect().size

class Game:
    def __init__(self, window):
        self.window = window

        self.bg0 = Background(asset('underwater-fantasy/far.png'))
        self.bg0.rect.bottom = self.window.rect().bottom - 40
        self.bg0.tilex(window)

        self.bg1 = Background(asset('underwater-fantasy/mid.png'))
        self.bg1.rect.bottom = self.window.rect().bottom - 30
        self.bg1.tilex(window)
        self.bg1.image.colorkey(retro.BLACK)

        self.bg2 = Background(asset('underwater-fantasy/near.png'))
        self.bg2.rect.bottom = self.window.rect().bottom
        self.bg2.tilex(window)
        self.bg2.image.colorkey(retro.BLACK)

        self.fish1 = Fish(
            speed = (2, 0),
            path  = asset('underwater-diving/fish1.png'),
        )
        self.fish1.rect.move_ip(100, 80)

        self.fish2 = Fish(
            speed  = (2, 1),
            path   = asset('underwater-diving/fish2.png'),
        )
        self.fish2.rect.move_ip(200, 100)

        self.fish3 = Fish(
            speed  = (2, 2),
            path   = asset('underwater-diving/fish3.png'),
        )
        self.fish3.image.scale(1.25)
        self.fish3.rect.move_ip(200, 100)

        self.bubbles = retro.Sprite.from_spritesheet(
            path = asset('underwater-diving/bubbles.png'),
            animations = retro.Animations(
                frame_size = (23, 40),
                period = 200,
                MAIN = ((0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4), 0),
            )
        )

    def run(self):
        # Update
        self.fish1.move1(self.window)
        self.fish2.move2(self.window)
        self.fish3.move3(self.window)

        # Draw
        self.window.fill((62, 121, 221))
        self.bg0.draw(self.window)
        self.fish1.draw(self.window)
        self.bg1.draw(self.window)
        self.fish2.draw(self.window)
        self.bg2.draw(self.window)
        self.fish3.draw(self.window)
        self.bubbles.draw(self.window, (40, 200))
        self.bubbles.draw(self.window, (550, 200))

window = retro.Window(
    title = 'Underwater',
    size  = (600, 250),
)
window.cursor(False)
game = Game(window)
window.loop(game.run)
