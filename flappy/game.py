import os
import random
import retro

def assets(filename): return os.path.join("assets", filename)

class Ground(retro.Sprite):
    IMG = retro.Image.from_path(assets("ground.png"))
    SPEED = 4

    def __init__(self, window):
        retro.Sprite.__init__(self, [self.IMG])
        self.window = window
        self.shift = (self.rect.width - self.window.rect().width)
        self.rect.bottom = self.window.rect().bottom

    def update(self):
        self.rect.x = (self.rect.x - self.SPEED) % -self.shift

    def draw(self):
        retro.Sprite.draw(self, self.window)

class Pipe:
    def __init__(self, ptop, pbot): self.ptop = ptop ; self.pbot = pbot
    @property
    def left(self): return self.ptop.rect.left
    @property
    def right(self): return self.ptop.rect.right
    @property
    def centerx(self): return self.ptop.rect.centerx
    @property
    def centery(self): return (self.ptop.rect.bottom + self.pbot.rect.top) // 2

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
            self[-1].left + (self.window.rect().right // 2)
        y = random.randrange(
            self.OFFSET_HEIGHT,
            self.window.rect().height
            - self.GAP_HEIGHT
            - Ground.IMG.rect().height
            - self.OFFSET_HEIGHT
        )

        ptop = retro.Sprite([self.IMG_TOP])
        ptop.rect.bottom = ptop.rect.top + y
        ptop.rect.left = x

        pbot = retro.Sprite([self.IMG_BOTTOM])
        pbot.rect.top = y + self.GAP_HEIGHT
        pbot.rect.left = x

        self.append(Pipe(ptop = ptop, pbot = pbot))

    def update(self):
        for pipe in self:
            pipe.ptop.rect.x -= Ground.SPEED
            pipe.pbot.rect.x -= Ground.SPEED

        # generate new pipe when the leftmost pipe starts to disappear
        if (len(self) == 2) and (self[0].left < 0): self.generate()
        # delete leftmost pipe when it goes out of screen
        if self[0].right <= 0: del self[0]

    def draw(self):
        for pipe in self:
            pipe.ptop.draw(self.window)
            pipe.pbot.draw(self.window)

class Bird(retro.Sprite):
    IMG = retro.Image.from_path(assets("bird.png"))
    ACCEL = 1
    DEFAULT_SPEED = -9
    MAX_SPEED = 9

    def __init__(self, window):
        retro.Sprite.__init__(self, [self.IMG])
        self.window = window
        self.fitness = 0
        self.alive = True
        self.rect.center = (75, self.window.rect().centery)
        self.flap()

    def flap(self):
        if self.alive: self.speed_y = self.DEFAULT_SPEED

    def collide(self, *elements): return any(
        self.rect.colliderect(e.rect) for e in elements
    )

    def update(self):
        if self.alive:
            self.speed_y += self.ACCEL
            self.speed_y = min(self.speed_y, self.MAX_SPEED)
            self.rect.y += self.speed_y
            self.fitness += 1

    def draw(self):
        if self.alive: retro.Sprite.draw(self, self.window)

class Game:
    def __init__(self, window, nbirds):
        self.window = window
        self.nbirds = nbirds

        self.bg = retro.Image.from_path(assets("bg.png"))
        self.ground = Ground(window)
        self.pipes = Pipes(window)
        self.target = self.pipes[0]
        self.birds = [Bird(window) for i in range(nbirds)]

        self.finished = False

    def draw_scores(self):
        for i, bird in enumerate(self.birds):
            score = retro.Sprite([self.window.fonts[0].render(
                text  = str(bird.fitness),
                color = retro.WHITE,
            )])
            score.rect.move_ip(10, 10 + (i * score.rect.h))
            score.draw(self.window)

    def run(self):
        # Update
        self.pipes.update()
        self.ground.update()
        for b in self.birds: b.update()

        ## nearest pipe
        b = self.birds[0]
        if b.rect.left > self.target.centerx: self.target = self.pipes[1]

        ## collision between birds, ground, sky and nearest pipe
        for b in self.birds: b.alive = (
            b.alive
            and not b.collide(self.target.ptop, self.target.pbot, self.ground)
            and (not b.rect.y < 0)
        )
        self.finished = all(not b.alive for b in self.birds)

        # Draw
        self.window.draw_img(self.bg, (0, 0))
        self.pipes.draw()
        self.ground.draw()
        for b in self.birds: b.draw()
        self.draw_scores()

    def reset(self):
        self.__init__(self.window, self.nbirds)
