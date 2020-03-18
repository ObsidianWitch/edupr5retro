import shared.retro as retro
from lemmings.nodes.actions import Actions

class UI:
    def __init__(self, window):
        self.window = window

        self.icons = retro.Group()
        self.populate_icons()
        self.selection = self.icons[0]
        self.position_icons()

    def populate_icons(self):
        for action in Actions.USABLE:
            sprite = retro.Sprite(action.ICON)
            sprite.state = action
            self.icons.append(sprite)

    def position_icons(self):
        rect = retro.Rect(
            0, 0,
            len(self.icons) * self.selection.rect.width,
            self.selection.rect.height
        )
        rect.midbottom = self.window.rect().midbottom

        for i, s in enumerate(self.icons):
            s.rect.top  = rect.top
            s.rect.left = rect.left + (i * s.rect.width)

    def update(self):
        if not self.window.events.mouse_press(): return

        pos = self.window.events.mouse_pos()
        for s in self.icons:
            if s.rect.collidepoint(pos):
                self.selection = s

    def draw_selection(self):
        self.window.draw_rect(
            color = retro.WHITE,
            rect  = self.selection.rect,
            width = 2,
        )

    def draw(self):
        self.icons.draw(self.window)
        self.draw_selection()
