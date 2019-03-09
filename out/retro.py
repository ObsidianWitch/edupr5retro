import pygame
import numpy
from numbers import Number
from pygame.locals import *

M_LEFT   = 1
M_MIDDLE = 2
M_RIGHT  = 3

BLACK   = (  0,   0,   0)
GREY    = (125, 125, 125)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
CYAN    = (  0, 255, 255)
MAGENTA = (255,   0, 255)
YELLOW  = (255, 255,   0)

class Rect(pygame.Rect):

    def __init__(self, *args):
        pygame.Rect.__init__(self, args)

    def copy(self): return pygame.Rect.copy(self)

    def move(self, *v): pygame.Rect.move_ip(self, v) ; return self

    def clamp(self, rect): pygame.Rect.clamp_ip(self, rect) ; return self

    def union(self, rect): return pygame.Rect.union(self, rect)

    def intersection(self, rect): return pygame.Rect.clip(self, rect)

    def contains(self, rect): return pygame.Rect.contains(self, rect)

    def collidepoint(self, *p): return pygame.Rect.collidepoint(self, p)

    def colliderect(self, rect): return pygame.Rect.colliderect(self, rect)

    __lt__ = property()
    __le__ = property()
    __gt__ = property()
    __ge__ = property()
    move_ip = property()
    inflate = property()
    inflate_ip = property()
    clamp_ip = property()
    clip = property()
    union_ip = property()
    unionall = property()
    unionall_ip = property()
    fit = property()
    normalize = property()
    collidelist = property()
    collidelistall = property()
    collidedict = property()
    collidedictall = property()

class Image:

    def __init__(self, arg):
        if isinstance(arg, Image):
            self.pygsurface = arg.pygsurface.copy()
        elif isinstance(arg, pygame.Surface):
            self.pygsurface = arg
        else:
            self.__init__(pygame.Surface(arg))

    @classmethod
    def from_path(cls, path):
        return cls(pygame.image.load(path))

    @classmethod
    def from_array(cls, array):
        return cls(pygame.surfarray.make_surface(array))

    @classmethod
    def from_ascii(cls, txt, dictionary):
        height = len(txt)
        width  = len(txt[0])

        rgb_sprite = numpy.zeros((width, height, 3))
        for y, x in numpy.ndindex(height, width):
            c = txt[y][x]
            rgb_sprite[x,y] = dictionary[c]

        return cls.from_array(rgb_sprite)

    @classmethod
    def from_spritesheet(cls, path, sprite_size, discard_color):
        spritesheet = cls.from_path(path)

        images = []
        for y in range(spritesheet.rect().h // sprite_size[1]):
            line = []
            for x in range(spritesheet.rect().w // sprite_size[0]):
                img = spritesheet.subimage(Rect(
                    x * sprite_size[0], # x
                    y * sprite_size[1], # y
                    sprite_size[0],     # width
                    sprite_size[1],     # height
                ))
                if img[0, 0] == discard_color: break
                line.append(img)
            images.append(line)

        return images

    def copy(self):
        return self.__class__(self)

    def subimage(self, area):
        return self.__class__(self.pygsurface.subsurface(area))

    def rect(self): return Rect(self.pygsurface.get_rect())

    def __getitem__(self, pos):
        return self.pygsurface.get_at(pos)

    def __setitem__(self, pos, color):
        self.pygsurface.set_at(pos, color)

    def colorkey(self, color):
        self.pygsurface.set_colorkey(color)
        return self

    def fill(self, color):
        self.pygsurface.fill(color)
        return self

    def draw_img(self, img, pos, area = None):
        self.pygsurface.blit(img.pygsurface, pos, area)
        return self

    def draw_rect(self, color, rect, width = 0):
        pygame.draw.rect(self.pygsurface, color, rect, width)
        return self

    def draw_circle(self, color, center, radius, width = 0):
        pygame.draw.circle(self.pygsurface, color, center, radius, width)
        return self

    def draw_line(self, color, start_pos, end_pos, width = 1):
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)
        return self

    def flip(self, x, y):
        self.pygsurface = pygame.transform.flip(self.pygsurface, x, y)
        return self

    def resize(self, size):
        self.pygsurface = pygame.transform.scale(self.pygsurface, size)
        return self

    def scale(self, ratio):
        self.resize(size = (
                int(self.rect().w * ratio),
                int(self.rect().h * ratio),
        ))
        return self

    def rotate(self, angle):
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)
        return self

class Font:

    def __init__(self, size):
        self.pygfont = pygame.font.SysFont(None, size)

    def render(self, text, antialias = False, color = BLACK, bgcolor = None):
        return Image(
            self.pygfont.render(text, antialias, color, bgcolor)
        )

class Window(Image):

    def __init__(self, title, size, framerate = 30):
        pygame.init()
        pygame.mixer.quit()

        pygame.display.set_caption(title)
        surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

    @classmethod
    def time(cls): return pygame.time.get_ticks()

    def cursor(self, enable):
        pygame.mouse.set_visible(enable)

    def update(self):
        self.clock.tick(self.framerate)
        pygame.display.flip()

class Events:

    def __init__(self):
        pass

    def update(self):
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    def event(self, type):
        for e in self.events:
            if e.type == type: return e

    def key_press(self, key):
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return True
        return False

    def key_hold(self, key):
        return self.keyheld[key]

    def key_release(self, key):
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return True
        return False

    def mouse_press(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return True
                elif e.button == button: return True
        return False

    def mouse_hold(self, button = None):
        if any(self.mouseheld):
            if button is None: return True
            else: return self.mouseheld[button - 1]
        return False

    def mouse_release(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return True
                elif e.button == button: return True
        return False

    def mouse_pos(self):
        return pygame.mouse.get_pos()

