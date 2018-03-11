from lemmings.nodes.lemming import Lemming
from shared.sprite import Group
from shared.timer import Timer

# Lemming generator.
class Lemmings:
    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        self.group = Group()
        self.position = position
        self.escaped = 0

        self.counter = 0
        self.max = 15
        self.pop_timer = Timer(end = 15, period = 100)

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
