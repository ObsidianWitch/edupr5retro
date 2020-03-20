from __future__ import annotations
import sys
import typing as typ
from numbers import Real
import itertools
import pygame
import numpy
from pygame.locals import *
from pygame import Rect

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

class Math:
    @classmethod
    def distance(cls, p1, p2): return \
        abs(p2[0] - p1[0]) \
      + abs(p2[1] - p1[1])

class Image:
    def __init__(self, arg: typ.Any) -> None:
        if isinstance(arg, Image):
            self.pygsurface: pygame.Surface = arg.pygsurface.copy()
        elif isinstance(arg, pygame.Surface):
            self.pygsurface = arg
        elif isinstance(arg, typ.Sequence):
            Image.__init__(self, pygame.Surface(arg))
        else:
            raise NotImplementedError

    @classmethod
    def from_path(cls, path: str) -> Image:
        return cls(pygame.image.load(path))

    @classmethod
    def from_array(cls, array: numpy.ndarray) -> Image:
        return cls(pygame.surfarray.make_surface(array))

    # Load a spritesheet image from its `path` and cut it in subimages of size
    # `sprite_size`. Subimages containing the `discard_color` color at their
    # topleft corner are discarded. Return a list containg a list of subimages
    # for each line of the spritesheet.
    @classmethod
    def from_spritesheet(cls,
        path: str, sprite_size: typ.Tuple[int, int], discard_color: pygame.Color
    ) -> typ.List[Image]:
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

        return list(itertools.chain(*images))

    def copy(self) -> Image:
        return self.__class__(self)

    # Create a new Image that references its parent. Modifications to either
    # images will effect each other. `area` is the zone to extract from `self`.
    def subimage(self, area: Rect) -> Image:
        return self.__class__(self.pygsurface.subsurface(area))

    # Return a new rectangle at (0, 0) covering the entire image.
    def rect(self) -> Rect:
        return Rect(*self.pygsurface.get_rect())

    def __getitem__(self, pos: typ.Tuple[int, int]) -> pygame.Color:
        return self.pygsurface.get_at(pos)

    def __setitem__(self,
        pos: typ.Tuple[int, int], color: pygame.Color
    ) -> None:
        self.pygsurface.set_at(pos, color)

    # Set the current transparent color key for this image.
    def colorkey(self, color: pygame.Color) -> Image:
        self.pygsurface.set_colorkey(color)
        return self

    def fill(self, color: pygame.Color) -> Image:
        self.pygsurface.fill(color)
        return self

    # Draw `img` onto `self` at `pos`. An optional `area` can be specified can
    # be passed to select a smaller portion of `img` to draw.
    def draw_img(self,
        img: Image, pos: typ.Tuple[int, int], area: typ.Optional[Rect] = None
    ) -> Image:
        self.pygsurface.blit(img.pygsurface, pos, area)
        return self

    def draw_rect(self,
        color: pygame.Color, rect: Rect, width: int = 0
    ) -> Image:
        pygame.draw.rect(self.pygsurface, color, rect, width)
        return self

    def draw_circle(self,
        color: pygame.Color, center: typ.Tuple[int, int], radius: int,
        width: int = 0
    ) -> Image:
        pygame.draw.circle(self.pygsurface, color, center, radius, width)
        return self

    def draw_line(self,
        color: pygame.Color, start_pos: typ.Tuple[int, int],
        end_pos: typ.Tuple[int, int], width: int = 1
    ) -> Image:
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)
        return self

    def flip(self, x: bool, y: bool) -> Image:
        self.pygsurface = pygame.transform.flip(self.pygsurface, x, y)
        return self

    def resize(self, size: typ.Tuple[int, int]) -> Image:
        self.pygsurface = pygame.transform.scale(self.pygsurface, size)
        return self

    def scale(self, ratio: float) -> Image:
        self.resize(size = (
                int(self.rect().w * ratio),
                int(self.rect().h * ratio),
        ))
        return self

    def rotate(self, angle: int) -> Image:
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)
        return self

    def __eq__(self, other):
        return numpy.array_equal(
            pygame.surfarray.pixels3d(self.pygsurface),
            pygame.surfarray.pixels3d(other.pygsurface)
        )

    def save(self, out):
        pygame.image.save(self.pygsurface, out)

class Font:
    def __init__(self, size: int) -> None:
        self.pygfont = pygame.font.SysFont(None, size)

    def render(self,
        text: str,
        antialias: bool = True,
        color: pygame.Color = BLACK,
        bgcolor: pygame.Color = None
    ) -> Image:
        return Image(
            self.pygfont.render(text, antialias, color, bgcolor)
        )

class Window(Image):
    def __init__(self,
        title: str, size: typ.Tuple[int, int], framerate: int = 30,
        headless: bool = False
    ) -> None:
        pygame.init()

        self.headless = headless
        if self.headless:
            surface = pygame.Surface(size)
        else:
            pygame.display.set_caption(title)
            surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

        self.events = Events()

        self.fonts = list(
            Font(size) for size in range(18, 43, 6)
        )

    # Return the number of milliseconds since the window has been initialized.
    @classmethod
    def time(cls) -> int:
        return pygame.time.get_ticks()

    def cursor(self, enable: bool) -> None:
        pygame.mouse.set_visible(enable)

    # Update the content of the window and limit the runtime speed of the game
    # to `self.framerate`.
    def update(self) -> None:
        self.dt = self.clock.tick(self.framerate)
        pygame.display.flip()

    # 1. retrieve new events
    # 2. execute `instructions`
    # 3. update the content of the window
    def loop(self, instructions: typ.Callable) -> None:
        while 1:
            self.events.update()
            if self.events.event(pygame.QUIT): sys.exit()

            instructions()

            self.update()

class Events:
    def __init__(self) -> None:
        pass

    # Retrieve new events. This method should be called each frame.
    def update(self) -> None:
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    # Returns the first event found of the specified `type`.
    def event(self, type: int) -> typ.Optional[pygame.event.Event]:
        for e in self.events:
            if e.type == type: return e
        return None

    def key_press(self, key: int) -> bool:
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return True
        return False

    def key_hold(self, key: int) -> bool:
        return self.keyheld[key]

    def key_release(self, key: int) -> bool:
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return True
        return False

    def mouse_press(self, button: int = None) -> bool:
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return True
                elif e.button == button: return True
        return False

    def mouse_hold(self, button: int = None) -> bool:
        if any(self.mouseheld):
            if button is None: return True
            else: return self.mouseheld[button - 1]
        return False

    def mouse_release(self, button: int = None) -> bool:
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return True
                elif e.button == button: return True
        return False

    def mouse_pos(self) -> typ.Tuple[int, int]:
        return pygame.mouse.get_pos()

class Group(list):
    def __init__(self, *args: Sprite) -> None:
        list.__init__(self, args)
        for e in args: e.groups.append(self)

    def append(self, e: Sprite) -> None:
        list.append(self, e)
        e.groups.append(self)

    def update(self, *args: typ.Any, **kwargs: typ.Any) -> None:
        for e in self: e.update(*args, **kwargs)

    def draw(self, surface: Image) -> None:
        for e in self: e.draw(surface)

class Counter:
    # A counter counts from 0 to `end`. Its value is incremented periodically
    # (`period`). By default the counter does not end (`end = 0`) and is
    # incremented every 1000 ms (`period = 1000`).
    def __init__(self, end: int = 0, period: int = 1000) -> None:
        self.end = end
        self.period = period
        self.restart()

    @property
    def elapsed(self) -> int:
        return (pygame.time.get_ticks() - self.t0) // self.period

    @property
    def remaining(self) -> int:
        return (self.end - self.elapsed)

    @property
    def finished(self) -> bool:
        return (self.elapsed >= self.end)

    def restart(self) -> None:
        self.t0 = pygame.time.get_ticks()

class Animations(typ.Dict[str, typ.Sequence[int]]):
    # Animations are stored as entries in this dictionary. Each entry map a name
    # to frames. Frames are represented by a list of indexes. Each index
    # references an image stored somewhere else. `period` specifies the time
    # necessary in milliseconds to switch to the next frame. By default, the
    # first animation defined in `self` is started.
    #
    # # Example
    # animations = retro.Animations(
    #     period = 100,
    #     WALK_L = range(0, 8),
    #     WALK_R = range(0 + 133, 8 + 133),
    #     FALL_L = range(8, 12),
    #     FALL_R = range(8 + 133, 12 + 133),
    #     ...
    # )
    def __init__(self, period: int, **kwargs: typ.Sequence[int]) -> None:
        dict.__init__(self, **kwargs)
        self.period = period
        if len(self) > 0:
            self.start(name = next(iter(self)))

    # Return the currently played frame's index.
    @property
    def frame(self) -> int:
        i = self.counter.elapsed % len(self.current)
        return self.current[i]

    # Return whether the animation has finished at least once.
    @property
    def finished(self) -> bool:
        return self.counter.finished

    # Sets the animation to play by specifying its `name`.
    def set(self, name: str) -> None:
        self.current = self[name]

    # Specify the animation to play by its `name` and starts it.
    def start(self, name: str) -> None:
        self.set(name)
        self.counter = Counter(
            end    = len(self.current),
            period = self.period,
        )

class Sprite:
    def __init__(self,
        images: typ.List[Image], animations: Animations = None
    ) -> None:
        self.image = images[0]
        self.rect = self.image.rect()
        self.groups: typ.List[Group] = []

        self.images = images
        self.animations = animations

    @classmethod
    def from_path(cls, paths, animations = None):
        images = [ Image.from_path(p) for p in paths ]
        return cls(images, animations)

    @classmethod
    def from_spritesheet(cls,
        path, sprite_size, discard_color, animations = None
    ):
        images = Image.from_spritesheet(path, sprite_size, discard_color)
        return cls(images, animations)

    def kill(self) -> None:
        for g in self.groups: g.remove(self)
        self.groups = []

    # Sets the current `self.image` as the current frame of the animation.
    # Note: this method is called by `Group.update()`.
    def update(self) -> None:
        if self.animations:
            self.image = self.images[self.animations.frame]

    # Draw the sprite's current frame on the specified `image` at
    # `self.rect.topleft`.
    def draw(self, image: Image) -> None:
        image.draw_img(self.image, self.rect.topleft)

class Stage(Sprite):
    # A Stage is a Sprite which can be modified and then restored to its
    # original state (`self.original`). A specific portion of the sprite image
    # can be focused by manipulated `self.camera`.
    def __init__(self, path: str):
        self.original = Image.from_path(path)
        Sprite.__init__(self, [self.original.copy()])

    @property
    def camera(self) -> Rect:
        return self.rect
    @camera.setter
    def camera(self, rect: Rect) -> None:
        self.rect = rect

    ## Transform point `p` from camera space to stage space.
    def camera2stage(self, p: typ.Tuple[int, int]) -> typ.Tuple[int, int]:
        return (p[0] + self.camera.x, p[1] + self.camera.y)

    ## Transform point `p` from stage space to camera space.
    def stage2camera(self, p: typ.Tuple[int, int]) -> typ.Tuple[int, int]:
        return (p[0] - self.rect.x, p[1] - self.rect.y)

    ## Restore stage to its `self.original` state.
    def clear_all(self) -> None:
        self.image.draw_img(self.original, (0, 0))

    ## Restore a portion (`self.camera`) of the stage to its `self.original`
    ## state.
    def clear_focus(self) -> None:
        self.image.draw_img(self.original, self.camera.topleft, self.camera)
class Directions:
    def __init__(self, up, down, left, right):
        self.up    = up
        self.down  = down
        self.left  = left
        self.right = right

    @property
    def vec(self): return [
        self.right - self.left,
        self.down  - self.up,
    ]

    def invert(self):
        helper = lambda v: not v if (v is not None) else None
        self.up    = helper(self.up)
        self.down  = helper(self.down)
        self.left  = helper(self.left)
        self.right = helper(self.right)
        return self

    def replace(self, old_v, new_v):
        helper = lambda v: new_v if (v == old_v) else v
        self.up    = helper(self.up)
        self.down  = helper(self.down)
        self.left  = helper(self.left)
        self.right = helper(self.right)
        return self

    def __contains__(self, v): return v in (
        self.up, self.down, self.left, self.right
    )

    def __repr__(self): return (
            "<Directions(\n"
            f"\tup: {self.up}\n"
            f"\tdown: {self.down}\n"
            f"\tleft: {self.left}\n"
            f"\tright: {self.right}\n"
            ")"
        )

class Collisions:
    @classmethod
    def pixel_checker(cls, surface, color):
        def check(p, offset):
            p = (p[0] + offset[0], p[1] + offset[1])
            if not surface.rect().collidepoint(p):
                return None
            return (surface[p] == color)

        return check

    # Check collisions between `rect` midpoints and adjacent pixels of the
    # specified `color` in `surface`. For each direction, returns True on
    # collision, False on non-collisions, and None in case of undefined
    # behaviour (e.g. outside of the `surface` rect).
    @classmethod
    def pixel_mid(cls, surface, rect, color):
        check = cls.pixel_checker(surface, color)

        return Directions(
            up    = check(rect.midtop,    ( 0, -1)),
            down  = check(rect.midbottom, ( 0,  0)),
            left  = check(rect.midleft,   (-1,  0)),
            right = check(rect.midright,  ( 0,  0)),
        )

    # Check collision between `rect`'s topleft, topright, bottomleft,
    # bottomright points and adjacent pixels of the specified `color` in
    # `surface`. For each direction, returns True on collision, False on
    # non-collisions, and None in case of undefined behaviour (e.g. outside of
    # the `surface` rect).
    @classmethod
    def pixel_vertices(cls, surface, rect, color):
        check = cls.pixel_checker(surface, color)

        return Directions(
            up    = check(rect.topleft,     ( 0, -1))
                 or check(rect.topright,    (-1, -1)),
            down  = check(rect.bottomleft,  ( 0,  0))
                 or check(rect.bottomright, (-1,  0)),
            left  = check(rect.topleft,     (-1,  0))
                 or check(rect.bottomleft,  (-1, -1)),
            right = check(rect.topright,    ( 0,  0))
                 or check(rect.bottomright, ( 0, -1)),
        )

    # Returns a list containing all Sprites in `lst` that intersect with
    # `sprite`. If `kill` is set to True, all Sprites that collide will be
    # removed from `lst`.
    @classmethod
    def sprites(cls, sprite, lst, kill):
        collisions = []
        for s in lst:
            if sprite.rect.colliderect(s):
                collisions.append(s)
                if kill: s.kill()
        return collisions
