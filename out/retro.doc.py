import sys
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

class Math:
    # Méthodes de classe

    ## ~~~{.python .prototype}
    ## clamp(val: Number, minval: Number, maxval: Number) -> Number
    ## ~~~
    ## Restreint `val` dans [`minval`, `maxval`].
    @classmethod
    def clamp(cls, val, minval, maxval):
        return minval if val < minval \
          else maxval if val > maxval \
          else val

class Rect(pygame.Rect):
    # Constructeur

    ## ~~~{.python .prototype}
    ## Rect(int left, int top, int width, int height) -> Rect
    ## Rect(2-tuple topleft, 2-tuple size) -> Rect
    ## Rect(Rect rect) -> Rect
    ## ~~~
    ## Crée un rectangle.
    ##
    ## Les propriétés ci-dessous permettent de bouger et d'aligner le rectangle.
    ##
    ## ~~~
    ## x, y
    ## top, left, bottom, right
    ## topleft, bottomleft, topright, bottomright
    ## midtop, midleft, midbottom, midright
    ## center, centerx, centery
    ## size, width, height, w, h
    ## ~~~
    ##
    ## ~~~python
    ## # Exemple
    ## r = Rect((0, 0), (7, 7)) # -> <rect(0, 0, 7, 7)>
    ## r = Rect(0, 0, 7, 7)     # -> <rect(0, 0, 7, 7)>
    ## r.topleft = (1, 1)       # -> <rect(1, 1, 7, 7)>
    ## r.size                   # -> (7, 7)
    ## r.center                 # -> (4, 4)
    ## r.bottomright            # -> (8, 8)
    ## r.topleft = r.center     # -> <rect(4, 4, 7, 7)>
    ## ~~~
    ##
    ## Il faut noter que les propriétés `bottom` et `right` décrivent des
    ## positions en dehors du rectangle. Ci-dessous un schéma des
    ## propriétés de position.
    ##
    ## ~~~{ .interpunct }
    ## +-------+·   | a: topleft     == (left, top) == (x, y)
    ## |a··b···|c   | b: midtop      == (centerx, top)
    ## |·······|·   | c: topright    == (right, top)
    ## |d··e···|f   | d: midleft     == (left, centery)
    ## |·······|·   | e: center      == (centerx, centery)
    ## |·······|·   | f: midright    == (right, centery)
    ## +-------+·   | g: bottomleft  == (left, bottom)
    ## ·g··h····i   | h: midbottom   == (centerx, bottom)
    ##              | i: bottomright == (right, bottom)
    ## ~~~
    def __init__(self, *args):
        pygame.Rect.__init__(self, args)

    # Méthodes

    ## ~~~{.python .prototype}
    ## copy() -> Rect
    ## ~~~
    ## Retourne un nouveau rectangle possédant la même position et la même
    ## taille que l'original.
    def copy(self): return pygame.Rect.copy(self)

    ## ~~~{.python .prototype}
    ## move(2-tuple v)
    ## move(int x, int y)
    ## ~~~
    ## Déplace le rectangle de `x` et `y`.
    def move(self, *v): pygame.Rect.move_ip(self, v)

    ## ~~~{.python .prototype}
    ## clamp(Rect rect)
    ## ~~~
    ## Déplace le rectangle actuel dans `rect`. Si le rectangle actuel est
    ## trop grand pour rentrer dans `rect`, il sera centré à l'intérieur et sa
    ## taille ne changera pas.
    def clamp(self, rect): pygame.Rect.clamp_ip(self, rect)

    ## ~~~{.python .prototype}
    ## union(Rect rect) -> Rect
    ## ~~~
    ## Retourne un nouveau rectangle étant l'union du rectangle actuel et de
    ## `rect`.
    def union(self, rect): return pygame.Rect.union(self, rect)

    ## ~~~{.python .prototype}
    ## intersection(Rect rect) -> Rect
    ## ~~~
    ## Retourne un nouveau rectangle étant l'intersection du rectangle actuel
    ## et de `rect`.
    def intersection(self, rect): return pygame.Rect.clip(self, rect)

    ## ~~~{.python .prototype}
    ## contains(Rect rect) -> bool
    ## ~~~
    ## Teste si `rect` est complétement à l'intérieur du rectangle actuel.
    def contains(self, rect): return pygame.Rect.contains(self, rect)

    ## ~~~{.python .prototype}
    ## collidepoint(2-tuple p) -> bool
    ## collidepoint(int x, int y) -> bool
    ## ~~~
    ## Teste si `p` est à l'intérieur du rectangle actuel.
    def collidepoint(self, *p): return pygame.Rect.collidepoint(self, p)

    ## ~~~{.python .prototype}
    ## colliderect(Rect rect) -> bool
    ## ~~~
    ## Teste s'il y intersection entre `rect` et le rectangle actuel.
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
    # Constructeur

    ## ~~~{.python .prototype}
    ## Image(2-tuple size) -> Image
    ## Image(Image image) -> Image
    ## ~~~
    ## Crée une image.
    def __init__(self, arg):
        if isinstance(arg, Image):
            self.pygsurface = arg.pygsurface.copy()
        elif isinstance(arg, pygame.Surface):
            self.pygsurface = arg
        else:
            self.__init__(pygame.Surface(arg))

    # Méthodes de classe

    ## ~~~{.python .prototype}
    ## from_path(str path) -> Image
    ## ~~~
    ## Crée une image à partir d'un fichier dont le chemin est `path`.
    @classmethod
    def from_path(cls, path):
        return cls(pygame.image.load(path))

    ## ~~~{.python .prototype}
    ## from_array(2D-array array) -> Image
    ## ~~~
    ## Crée une image à partir du tableau à 2 dimensions `array`.
    @classmethod
    def from_array(cls, array):
        return cls(pygame.surfarray.make_surface(array))

    ## ~~~{.python .prototype}
    ## from_ascii(list txt, dict dictionary) -> Image
    ## ~~~
    ## Crée une image à partir de `txt`, une liste de chaînes de caractères.
    ## A chaque caractère possible dans `txt` est associé une couleur
    ## correspondante dans `dictionnary`.
    ## L'image est crée en remplaçant chaque caractère par sa couleur associée.
    @classmethod
    def from_ascii(cls, txt, dictionary):
        height = len(txt)
        width  = len(txt[0])

        rgb_sprite = numpy.zeros((width, height, 3))
        for y, x in numpy.ndindex(height, width):
            c = txt[y][x]
            rgb_sprite[x,y] = dictionary[c]

        return cls.from_array(rgb_sprite)

    ## ~~~{.python .prototype}
    ## from_spritesheet(
    ##     str path, 2-tuple sprite_size, 3-tuple discard_color
    ## ) -> 2D-list
    ## ~~~
    ## Charge une image (spritesheet) à partie de son chemin `path`, et découpe
    ## celle-ci en sous-images de taille `sprite_size`. Les sous-images
    ## possédant la couleur `discard_color` au pixel (0, 0) sont éliminées.
    ## Retourne une liste contenant une liste d'images pour chaque ligne de la
    ## spritesheet.
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

    # Méthodes

    ## ~~~{.python .prototype}
    ## copy() -> Image
    ## ~~~
    ## Crée une copie complète de l'image actuelle.
    def copy(self):
        return self.__class__(self)

    ## ~~~{.python .prototype}
    ## subimage(Rect area) -> Image
    ## ~~~
    ## Crée une nouvelle image faisant référence à une zone plus petite de
    ## l'image actuelle. `area` correspond à la zone à extraire de l'image
    ## actuelle.
    def subimage(self, area):
        return self.__class__(self.pygsurface.subsurface(area))

    ## ~~~{.python .prototype}
    ## rect() -> Rect
    ## ~~~
    ## Retourne un nouveau rectangle positionné en (0, 0) et de la taille de
    ## l'image actuelle.
    def rect(self): return Rect(self.pygsurface.get_rect())

    ## ~~~{.python .prototype}
    ## [int x, int y] -> pygame.Color
    ## ~~~
    ## Renvoie la couleur du pixel à la position spécifiée.
    ##
    ## ~~~python
    ## # Exemple
    ## i = Image((20, 20))
    ## print(i[0, 0]) # (0, 0, 0, 255)
    ## ~~~
    def __getitem__(self, pos):
        return self.pygsurface.get_at(pos)

    ## ~~~{.python .prototype}
    ## [int x, int y] = 3-tuple color
    ## ~~~
    ## Définit la couleur du pixel à la position spécifiée.
    ##
    ## ~~~python
    ## # Exemple
    ## i = Image((20, 20))
    ## i[0, 0] = (0, 255, 0)
    ## print(i[0, 0]) # (0, 255, 0, 255)
    ## ~~~
    def __setitem__(self, pos, color):
        self.pygsurface.set_at(pos, color)

    ## ~~~{.python .prototype}
    ## colorkey(3-tuple color)
    ## ~~~
    ## Définit la couleur de transparence de l'image.
    def colorkey(self, color):
        self.pygsurface.set_colorkey(color)
        return self

    ## ~~~{.python .prototype}
    ## fill(3-tuple color)
    ## ~~~
    ## Remplit l'image d'une couleur.
    def fill(self, color):
        self.pygsurface.fill(color)
        return self

    ## ~~~{.python .prototype}
    ## draw_img(Image img, 2-tuple pos, Rect area = None)
    ## ~~~
    ## Dessine une image (`img`) à la position spécifiée (`pos`) sur l'image
    ## actuelle. Une zone spécifique de `img` peut être dessinée à l'aide de
    ## `area`.
    def draw_img(self, img, pos, area = None):
        self.pygsurface.blit(img.pygsurface, pos, area)
        return self

    ## ~~~{.python .prototype}
    ## draw_rect(3-tuple color, Rect rect, int width = 0)
    ## ~~~
    ## Dessine un rectangle `rect` de couleur `color` et d'épaisseur de bordure
    ## `width`. Si width est égal à 0, le rectangle sera plein.
    def draw_rect(self, color, rect, width = 0):
        pygame.draw.rect(self.pygsurface, color, rect, width)
        return self

    ## ~~~{.python .prototype}
    ## draw_circle(3-tuple color, 2-tuple center, int radius, int width = 0)
    ## ~~~
    ## Dessine un cercle de couleur `color`, de centre `center`, de rayon
    ## `radius` et d'épaisseur de bordure `width`. Si `width` est égal à 0, le
    ## cercle sera plein.
    def draw_circle(self, color, center, radius, width = 0):
        pygame.draw.circle(self.pygsurface, color, center, radius, width)
        return self

    ## ~~~{.python .prototype}
    ## draw_line(
    ##     3-tuple color, 2-tuple start_pos, 2-tuple end_pos, int width = 1
    ## )
    ## ~~~
    ## Dessine une ligne de couleur `color`, de position de départ `start_pos`,
    ## de position d'arrivée `end_pos` et d'épaisseur `width`.
    def draw_line(self, color, start_pos, end_pos, width = 1):
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)
        return self

    ## ~~~{.python .prototype}
    ## flip(bool x, bool y)
    ## ~~~
    ## Inverse l'image horizontalement (`x`) et/ou verticalement (`y`).
    def flip(self, x, y):
        self.pygsurface = pygame.transform.flip(self.pygsurface, x, y)
        return self

    ## ~~~{.python .prototype}
    ## resize(2-tuple size)
    ## ~~~
    ## Redimensionne l'image. Sa nouvelle taille sera `size`.
    def resize(self, size):
        self.pygsurface = pygame.transform.scale(self.pygsurface, size)
        return self

    ## ~~~{.python .prototype}
    ## scale(float ratio)
    ## ~~~
    ## Mise à l'échelle de l'image.
    def scale(self, ratio):
        self.resize(size = (
                int(self.rect().w * ratio),
                int(self.rect().h * ratio),
        ))
        return self

    ## ~~~{.python .prototype}
    ## rotate(int angle)
    ## ~~~
    ## Fait pivoter l'image d'un `angle` spécifié en degrés.
    def rotate(self, angle):
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)
        return self

class Font:
    # Constructeur

    ## ~~~{.python .prototype}
    ## Font(2-tuple size) -> Font
    ## ~~~
    ## Création d'un objet permettant d'écrire du texte sur une image. La
    ## taille de la police d'écriture est spécifiée par `size`.
    def __init__(self, size):
        self.pygfont = pygame.font.SysFont(None, size)

    # Méthodes

    ## ~~~{.python .prototype}
    ## render(
    ##     str text, bool antialias = False,
    ##     3-tuple color = BLACK, 3-tuple bgcolor = None
    ## )
    ## ~~~
    ## Crée une Image avec le texte (`text`) spécifié dessus. Ce texte peut être
    ## lissé (`antialias`), d'une couleur spécifique (`color`) et avoir une
    ## couleur de fond (`bgcolor`). Si aucune couleur de fond n'est spécifiée,
    ## le fond sera transparent.
    def render(self, text, antialias = False, color = BLACK, bgcolor = None):
        return Image(
            self.pygfont.render(text, antialias, color, bgcolor)
        )

class Window(Image):
    # Héritage

    ## > [Image](#classe-image)

    # constructeur

    ## ~~~{.python .prototype}
    ## Window(str title, 2-tuple size, int framerate = 30)
    ## ~~~
    ## Crée une fenêtre ayant pour titre `title` et de taille `size`. Le
    ## `framerate` est limité à 30 FPS par défaut.
    def __init__(self, title, size, framerate = 30):
        pygame.init()
        pygame.mixer.quit()

        pygame.display.set_caption(title)
        surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

        self.events = Events()

        self.fonts = list(
            Font(size) for size in range(18, 43, 6)
        )

    # Attributs

    ## ~~~{.python .prototype}
    ## fonts -> list<Font>
    ## ~~~
    ## Liste de polices de tailles ascendantes (18, 24, 30, 36 et 42).

    ## ~~~{.python .prototype}
    ## events -> Events
    ## ~~~

    # Méthodes de classe

    ## ~~~{.python .prototype}
    ## time() -> int
    ## ~~~
    ## Retourne le temps en millisecondes qui s'est écoulé depuis
    ## l'initialisation d'une fenêtre.
    @classmethod
    def time(cls): return pygame.time.get_ticks()

    # Méthodes

    ## ~~~{.python .prototype}
    ## cursor(bool enable)
    ## ~~~
    ## Active ou désactive le curseur. Par défaut, le curseur est activé.
    def cursor(self, enable):
        pygame.mouse.set_visible(enable)

    ## ~~~{.python .prototype}
    ## update()
    ## ~~~
    ## Met à jour le contenu de la fenêtre et limite le framerate.
    ## Cette méthode doit être appelée à chaque itération de la boucle
    ## principale du jeu.
    def update(self):
        self.clock.tick(self.framerate)
        pygame.display.flip()

    ## ~~~{.python .prototype}
    ## loop(function instructions)
    ## ~~~
    ## Boucle principale du jeu.
    ##
    ## 1. récupère les nouveaux événements (`events.update()`)
    ## 2. exécute `instructions`
    ## 3. met à jour le contenu de la fenêtre (`update()`)
    def loop(self, instructions):
        while 1:
            self.events.update()
            if self.events.event(pygame.QUIT): sys.exit()

            instructions()

            self.update()

class Events:
    # Constructeur

    ## ~~~{.python .prototype}
    ## Events() -> Events
    ## ~~~
    ## Gestion de la file d'événements, de la souris et du clavier.
    ##
    ## Un événement ([`pygame.event.Event`](https://www.pygame.org/docs/ref/event.html#pygame.event.Event))
    ## est constitué d'un type et d'attributs différents en fonction du type de
    ## l'événement. Si vous souhaitez obtenir plus de détails, veuillez vous
    ## référer à la documentation du module
    ## [pygame.event](https://www.pygame.org/docs/ref/event.html).
    ## La liste des événements est disponible dans la section
    ## [Constantes](#événements).
    def __init__(self):
        pass

    # Méthodes

    ## ~~~{.python .prototype}
    ## update()
    ## ~~~
    ## Récupère les nouveaux événements disponibles. Cette méthode doit être
    ## appelée à chaque *frame* dans le jeu.
    def update(self):
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    ## ~~~{.python .prototype}
    ## event(int type) -> pygame.event.Event
    ## ~~~
    ## Cherche un événement du [`type`](#événements) spécifié.
    ## Retourne le premier événement trouvé ou `None`.
    def event(self, type):
        for e in self.events:
            if e.type == type: return e

    ## ~~~{.python .prototype}
    ## key_press(int key) -> bool
    ## ~~~
    ## Retourne si la [touche du clavier](#clavier) spécifiée vient d'être
    ## enfoncée.
    def key_press(self, key):
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return True
        return False

    ## ~~~{.python .prototype}
    ## key_hold(int key) -> bool
    ## ~~~
    ## Retourne si la [touche du clavier](#clavier) spécifiée est maintenue
    ## enfoncée.
    def key_hold(self, key):
        return self.keyheld[key]

    ## ~~~{.python .prototype}
    ## key_release(int key) -> bool
    ## ~~~
    ## Retourne si la [touche du clavier](#clavier) spécifiée vient d'être
    ## relâchée.
    def key_release(self, key):
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_press(int button = None) -> bool
    ## ~~~
    ## Retourne si un [bouton de la souris](#souris) vient d'être enfoncé.
    def mouse_press(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return True
                elif e.button == button: return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_hold(int button = None) -> bool
    ## ~~~
    ## Retourne si un [bouton de la souris](#souris) est maintenu enfoncé.
    def mouse_hold(self, button = None):
        if any(self.mouseheld):
            if button is None: return True
            else: return self.mouseheld[button - 1]
        return False

    ## ~~~{.python .prototype}
    ## mouse_release(int button = None) -> bool
    ## ~~~
    ## Retourne si un [bouton de la souris](#souris) vient d'être relâché.
    def mouse_release(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return True
                elif e.button == button: return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_pose() -> 2-tuple
    ## ~~~
    ## Récupère la position de la souris.
    def mouse_pos(self):
        return pygame.mouse.get_pos()


class Group(list):
    def __init__(self, *args):
        list.__init__(self, args)
        for e in args: e.groups.append(self)

    def append(self, e):
        list.append(self, e)
        e.groups.append(self)

    def update(self, *args, **kwargs):
        for e in self: e.update(*args, **kwargs)

    def draw(self, surface):
        for e in self: e.draw(surface)

class Sprite:
    # Constructeur

    ## ~~~{.python .prototype}
    ## Sprite(Image image) -> Sprite
    ## ~~~
    ## Un `Sprite` possède une `image` qui peut être dessinée sur une surface et
    ## positionnée à l'aide d'un `rect`.
    def __init__(self, image):
        self.image = image
        self.rect = self.image.rect()
        self.groups = []

    # Attributs

    ## ~~~{.python .prototype}
    ## image -> Image
    ## ~~~

    ## ~~~{.python .prototype}
    ## rect -> Rect
    ## ~~~

    ## ~~~{.python .prototype}
    ## groups -> List<group>
    ## ~~~

    # Méthodes

    ## ~~~{.python .prototype}
    ## kill()
    ## ~~~
    ## Supprime le sprite de tous les groupes (`groups`) auxquels il appartient.
    def kill(self):
        for g in self.groups: g.remove(self)
        self.groups = []

    ## ~~~{.python .prototype}
    ## update()
    ## ~~~
    ## Met à jour le sprite. Ne fait rien par défaut, à redéfinir.<br>
    ## **Note**: Cette méthode est appelée par `Group.update()`.
    def update(self): pass

    ## ~~~{.python .prototype}
    ## draw(Image image)
    ## ~~~
    ## Dessine le sprite sur la surface spécifiée (`image`) à la position
    ## définie par le rectangle du sprite (`rect`).
    def draw(self, image): image.draw_img(self.image, self.rect)

class Counter:
    # Constructeur

    ## ~~~{.python .prototype}
    ## Counter(end: int = 0, period: int = 0) -> Counter
    ## ~~~
    ## Un `Counter` permet de compter de 0 jusqu'à `end` en incrémentant sa
    ## valeur périodiquement (`period`). Par défaut, le compteur n'a pas de
    ## valeur de fin (`end = 0`) et est incrémenté toutes les 1000 ms
    ## (`period = 1000`).
    def __init__(self, end = 0, period = 1000):
        self.end = end
        self.period = period
        self.restart()

    # Propriétés

    ## ~~~{.python .prototype}
    ## elapsed -> int
    ## ~~~
    ## Valeur du compteur.
    @property
    def elapsed(self):
        return (pygame.time.get_ticks() - self.t0) // self.period

    @property
    def remaining(self):
        return (self.end - self.elapsed)

    ## ~~~{.python .prototype}
    ## finished -> bool
    ## ~~~
    ## Vérifie si le compteur a fini.
    @property
    def finished(self):
        return (self.elapsed >= self.end)

    # Méthodes

    ## ~~~{.python .prototype}
    ## restart()
    ## ~~~
    ## Démarre ou redémarre le compteur.
    def restart(self):
        self.t0 = pygame.time.get_ticks()

class Animations:
    # Constructeur

    ## ~~~{.python .prototype}
    ## Animations(dict data, int period) -> Animations
    ## ~~~
    ##
    ## Les animations sont contenues dans le dictionnaire `data`. Chaque entrée
    ## fait correspondre le nom d'une animation (clé) à des frames (valeur).
    ## Les frames sont représentées par une liste d'indices, chaque indice
    ## faisant référence à une image.
    ##
    ## Le paramètre `period` correspond au temps (en ms) nécessaire pour passer
    ## d'une frame à la suivante.
    ##
    ## Par défaut, la première animation définie dans `data` est lancée.
    ##
    ## ~~~python
    ## # Exemple
    ## animations = retro.Animations(
    ##     data = {
    ##         "WALK_L":  range(0, 8),
    ##         "WALK_R":  range(0 + 133, 8 + 133),
    ##         "FALL_L":  range(8, 12),
    ##         "FALL_R":  range(8 + 133, 12 + 133),
    ##         ...
    ##     },
    ##     period  = 100,
    ## )
    ## ~~~
    def __init__(self, data, period):
        self.data   = data
        self.period = period
        if len(data) > 0: self.start(name = next(iter(self.data)))

    # Propriétés

    ## ~~~{.python .prototype}
    ## frame -> int
    ## ~~~
    ##
    ## Retourne l'indice de la frame de l'animation actuellement jouée.
    ## Les animations sont jouées en boucle.
    @property
    def frame(self):
        i = self.counter.elapsed % len(self.current)
        return self.current[i]

    ## ~~~{.python .prototype}
    ## finished -> bool
    ## ~~~
    ##
    ## Retourne si l'animation a été complétée au moins une fois.
    @property
    def finished(self): return self.counter.finished

    # Méthodes

    ## ~~~{.python .prototype}
    ## set(str name)
    ## ~~~
    ##
    ## Définit l'animation à jouer (`current`).
    def set(self, name):
        self.current = self.data[name]

    ## ~~~{.python .prototype}
    ## start(str name)
    ## ~~~
    ##
    ## Définit et démarre l'animation à jouer (`current`). L'attribut
    ## [`counter`](#classe-counter) permet de gérer le passage d'une frame à
    ## l'autre.
    def start(self, name):
        self.set(name)
        self.counter = Counter(
            end    = len(self.current),
            period = self.period,
        )

class AnimatedSprite(Sprite):
    # Constructeur

    ## ~~~{.python .prototype}
    ## AnimatedSprite(list images, Animations animations) -> AnimatedSprite
    ## ~~~
    ##
    ## Crée un sprite animé à partir d'une liste d'[`images`](#¢lasse-image)
    ## et d'[`animations`](#classe-animations).
    def __init__(self, images, animations):
        Sprite.__init__(self, images[0])
        self.images = images
        self.animations = animations

    # Méthodes

    ## ~~~{.python .prototype}
    ## update()
    ## ~~~
    ##
    ## Affiche la frame actuelle de l'animation en cours.
    def update(self): self.image = self.images[self.animations.frame]


class Vec:
    @classmethod
    def neg(cls, va): return [
        -a for a in va
    ]

    @classmethod
    def add(cls, a, b): return [
        c + d for c, d in cls.iterator(a, b)
    ]

    @classmethod
    def sub(cls, a, b): return [
        c - d for c, d in cls.iterator(a, b)
    ]

    @classmethod
    def mul(cls, a, b): return [
        c * d for c, d in cls.iterator(a, b)
    ]

    @classmethod
    def dot(cls, a, b): return sum(
        c * d for c, d in cls.iterator(a, b)
    )

    @classmethod
    def eq(cls, a, b): return (len(a) == len(b)) and all(
        c == d for c, d in cls.iterator(a, b)
    )

    @classmethod
    def ne(cls, a, b): return (len(a) != len(b)) or all(
        c != d for c, d in cls.iterator(a, b)
    )

    @classmethod
    def iterator(cls, a, b):
        if isinstance(a, Number):
            for i, _ in enumerate(b): yield a, b[i]
        elif isinstance(b, Number):
            for i, _ in enumerate(a): yield a[i], b
        else:
            for i, _ in enumerate(a): yield a[i], b[i]

