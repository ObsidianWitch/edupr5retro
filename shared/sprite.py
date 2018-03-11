import numpy
import include.retro as retro

class Group(list):
    def __init__(self, *args):
        args = list(args)
        list.__init__(self, args)
        for e in args:
            if self not in e.groups: e.groups.append(self)


    def append(self, e):
        list.append(self, e)
        e.groups.append(self)

    def update(self):
        for e in self: e.update()

    def draw(self, surface):
        for e in self: e.draw(surface)

class Sprite:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.rect
        self.groups = []

    @classmethod
    def from_path(cls, path):
        return cls(retro.Image.from_path(path))

    @classmethod
    def from_ascii(cls, txt, dictionary):
        height = len(txt)
        width  = len(txt[0])

        rgb_sprite = numpy.zeros((width, height, 3))
        for y, x in numpy.ndindex(height, width):
            c = txt[y][x]
            rgb_sprite[x,y] = dictionary[c]

        return cls(retro.Image.from_array(rgb_sprite))

    def flip(self, xflip = False, yflip = False):
        self.image.flip(xflip, yflip)

    def scale(self, ratio):
        self.image.scale(ratio)
        self.rect = self.image.rect.move(self.rect.topleft)

    def colorkey(self, color):
        self.image.colorkey(color)

    def kill(self):
        for g in self.groups: g.remove(self)
        self.groups = []

    def update(self): pass

    def draw(self, image):
        image.draw_image(self.image, self.rect)
