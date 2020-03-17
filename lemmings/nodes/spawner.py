import shared.retro as retro
from lemmings.nodes.lemming import Lemming

class Spawner:
    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        self.group = retro.Group()
        self.position = position
        self.escaped = 0

        self.counter = 0
        self.max = 15
        self.pop_timer = retro.Counter(end = 1, period = 1500)

    @property
    def generated(self): return (self.counter >= self.max)

    def generate(self):
        if (not self.generated) and self.pop_timer.finished:
            l = Lemming(self.window, self.bg, self.position)
            self.group.append(l)
            self.counter += 1
            self.pop_timer.restart()

    def update(self, ui_action):
        self.generate()

        if not self.window.events.mouse_press():
            self.group.update(False)
            return

        click = self.window.events.mouse_pos()
        for l in self.group:
            collision = l.rect.collidepoint(click)
            if collision: l.update(ui_action)
            else: l.update(False)

    def draw_bg(self):
        for l in self.group: l.draw_bg()

    def draw_screen(self):
        for l in self.group: l.draw_screen()
