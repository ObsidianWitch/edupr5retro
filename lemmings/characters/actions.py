class Fall:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.animations.start("FALL")
        self.fallcount = 0

    def run(self):
        self.lemming.rect.move_ip(0, 3)
        self.fallcount += 3
        return (self.fallcount >= 100)

class Walk:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.dx = -1

    def run(self, collision_vec):
        if self.dx == collision_vec[0]:
            self.dx *= -1
            self.lemming.rect.move_ip(-self.dx * 20, 0)

        if self.dx < 0:   self.lemming.animations.set("WALK_L")
        elif self.dx > 0: self.lemming.animations.set("WALK_R")

        self.lemming.rect.move_ip(self.dx, 0)

class Dead:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.animations.start("DEAD")

    def run(self):
        if self.lemming.animations.finished: self.lemming.kill()

class Stop:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.animations.start("STOP")

    def run(self): pass

class Actions:
    def __init__(self, lemming):
        self.walk = Walk(lemming)
        self.fall = Fall(lemming)
        self.stop = Stop(lemming)
        self.dead = Dead(lemming)
