from empire_city.nodes.enemies.enemy import Enemy

class Runner(Enemy):
    def __init__(self, camera, image):
        Enemy.__init__(self, camera, image)
        self.dx = -2

    def move(self):
        self.rect.x += self.dx

        if self.bg.rect.contains(self.rect): return

        self.dx *= -1
        self.flip_ip(xflip = True)
        self.rect.clamp_ip(self.bg.rect)

    def update(self, target):
        Enemy.update(self, target)
        self.move()
