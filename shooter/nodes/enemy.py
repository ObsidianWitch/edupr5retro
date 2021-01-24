from retro.src import retro

class Enemy(retro.Sprite):
    def __init__(self, image):
        retro.Sprite.__init__(self, image)

        self.alive = True
        self.shoot_ticker = retro.Ticker(end=180)

    def kill(self, p):
        killed = (self.alive and self.rect.collidepoint(p))
        if killed: self.alive = False
        return killed

    def shoot(self, target):
        if not self.shoot_ticker.finished: return
        self.shoot_ticker.restart()
        if target.hide.hidden: return
        target.ammunitions.count -= 3

    def update(self, target):
        if not self.alive: return
        self.shoot(target)

    def draw_shoot_ticker(self, font, dest):
        if not self.alive: return

        shoot_ticker = retro.Sprite(font.render(
            text  = f"{self.shoot_ticker.remaining}",
            color = retro.WHITE,
        ))
        shoot_ticker.rect.midbottom = dest.rect().midbottom
        shoot_ticker.draw(dest)

    def draw(self, dest):
        if not self.alive: return
        retro.Sprite.draw(self, dest)
