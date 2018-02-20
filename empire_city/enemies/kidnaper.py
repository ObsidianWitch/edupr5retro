from empire_city.enemies.enemy import Enemy

class Kidnaper(Enemy):
    def __init__(self, camera, image):
        Enemy.__init__(self, camera, image)

    def kill(self, p):
        kidnaper = self.rect.copy()
        kidnaper.width //= 2
        victim = self.rect.copy()
        victim.width //= 2
        victim.x += victim.width

        victim_killed   = (self.alive and victim.collidepoint(p))
        kidnaper_killed = (self.alive and kidnaper.collidepoint(p))
        if victim_killed or kidnaper_killed: self.alive = False
        return (kidnaper_killed - victim_killed)
