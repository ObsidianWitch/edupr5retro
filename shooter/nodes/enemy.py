from retro.out import retro

class Enemy(retro.Sprite):
    def __init__(self, image):
        retro.Sprite.__init__(self, [image])

        self.alive = True
        self.shoot_timer = retro.Counter(3)

    def kill(self, p):
        killed = (self.alive and self.rect.collidepoint(p))
        if killed: self.alive = False
        return killed

    def shoot(self, target):
        if not self.shoot_timer.finished: return
        self.shoot_timer.restart()
        if target.hide.hidden: return
        target.ammunitions.count -= 3

    def update(self, target):
        if not self.alive: return
        self.shoot(target)

    def draw_shoot_timer(self, font, dest):
        if not self.alive: return

        shoot_timer = retro.Sprite([font.render(
            text  = f"{self.shoot_timer.remaining}",
            color = retro.WHITE,
        )])
        shoot_timer.rect.midbottom = dest.rect().midbottom
        shoot_timer.draw(dest)

    def draw(self, dest):
        if not self.alive: return
        retro.Sprite.draw(self, dest)
