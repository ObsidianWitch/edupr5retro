import sys
import os
import types
import random
import retro

def assets(filename): return os.path.join("assets", filename)

class Sprite:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.rect()

    def collide(self, *args):
        for elem in args:
            if self.rect.colliderect(elem): return True
        return False

    def update(self): pass
    def draw(self, image): image.draw_img(self.image, self.rect)

class Ground(Sprite):
    IMG = retro.Image.from_path(assets("ground.png"))
    SPEED = 4

    def __init__(self, window):
        Sprite.__init__(self, self.IMG)
        self.window = window
        self.shift = (self.rect.width - self.window.rect().width)
        self.rect.bottom = self.window.rect().bottom

    def update(self):
        self.rect.x = (self.rect.x - self.SPEED) % -self.shift

    def draw(self):
        Sprite.draw(self, self.window)

class Pipes(list):
    IMG_BOTTOM = retro.Image.from_path(assets("pipe.png"))
    IMG_TOP = IMG_BOTTOM.copy().flip(x = True, y = True)
    GAP_HEIGHT = 100
    OFFSET_HEIGHT = 80

    def __init__(self, window):
        self.window = window
        list.__init__(self)
        self.generate()
        self.generate()

    def generate(self):
        x = self.window.rect().right if not self else \
            self[-1].top.rect.x + (self.window.rect().right // 2)
        y = random.randrange(
            self.OFFSET_HEIGHT,
            self.window.rect().height
            - self.GAP_HEIGHT
            - Ground.IMG.rect().height
            - self.OFFSET_HEIGHT
        )

        top = Sprite(self.IMG_TOP)
        top.rect.bottom = top.rect.top + y
        top.rect.left = x

        bot = Sprite(self.IMG_BOTTOM)
        bot.rect.top = y + self.GAP_HEIGHT
        bot.rect.left = x

        self.append(types.SimpleNamespace(top = top, bot = bot))

    def update(self):
        for pipe in self:
            pipe.top.rect.x -= Ground.SPEED
            pipe.bot.rect.x -= Ground.SPEED

        leftmost_rect = self[0].top.rect
        # generate new pipe when the leftmost pipe starts to disappear
        if (len(self) == 2) and (leftmost_rect.left < 0): self.generate()
        # delete leftmost pipe when it goes out of screen
        if leftmost_rect.right <= 0: del self[0]

    def draw(self):
        for pipe in self:
            pipe.top.draw(self.window)
            pipe.bot.draw(self.window)

class Bird(Sprite):
    IMG = retro.Image.from_path(assets("bird.png"))
    DEFAULT_SPEED = -9
    MAX_SPEED = 9

    def __init__(self, Window):
        Sprite.__init__(self, self.IMG)
        self.window = window
        self.rect.center = (75, self.window.rect().centery)
        self.accel_y = 1
        self.flap()
        self.travelled = 0

    def flap(self):
        self.speed_y = self.DEFAULT_SPEED

    def update(self):
        self.speed_y += self.accel_y
        self.speed_y = min(self.speed_y, self.MAX_SPEED)
        self.rect.y += self.speed_y
        self.travelled += 1

    def draw(self):
        Sprite.draw(self, self.window)

class Game:
    def __init__(self, window, events):
        self.window = window
        self.events = events

        self.bg = retro.Image.from_path(assets("bg.png"))
        self.ground = Ground(window)
        self.pipes = Pipes(window)
        self.bird = Bird(window)

        self.finished = False

    def run(self):
        # Update
        self.events.update()
        if self.events.event(retro.QUIT): sys.exit()
        if self.events.key_press(retro.K_SPACE): self.bird.flap()

        self.pipes.update()
        self.ground.update()
        self.bird.update()

        self.finished = self.bird.collide(
            self.pipes[0].top, self.pipes[0].bot, self.ground
        )

        # Draw
        self.window.draw_img(self.bg, (0, 0))
        self.pipes.draw()
        self.ground.draw()
        self.bird.draw()

        self.window.update()

    def end(self):
        # Update
        self.events.update()
        if self.events.event(retro.QUIT): sys.exit()
        if self.events.key_press(retro.K_SPACE):
            self.__init__(self.window, self.events)

        # Draw
        self.window.update()

window = retro.Window(
    title = "Flappy Bird",
    size  = (288, 512),
)
events = retro.Events()

game = Game(window, events)

while 1:
    if not game.finished: game.run()
    else: game.end()
