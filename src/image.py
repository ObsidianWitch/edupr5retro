import pygame
import numpy
from src.rect import Rect
class Image:
    # Constructeur

    ## Image(2-tuple size) -> Image
    ## Image(Image image) -> Image
    def __init__(self, arg):
        if isinstance(arg, Image):
            self.pygsurface = arg.pygsurface.copy()
        elif isinstance(arg, pygame.Surface):
            self.pygsurface = arg
        else:
            self.__init__(pygame.Surface(arg))

    # Méthodes de classe

    ## from_path(str path) -> Image
    ## Crée une image à partir d'un fichier dont le chemin est `path`.
    @classmethod
    def from_path(cls, path):
        return cls(pygame.image.load(path))

    ## from_array(2D-array array) -> Image
    ## Crée une image à partir du tableau à 2 dimensions `array`.
    @classmethod
    def from_array(cls, array):
        return cls(pygame.surfarray.make_surface(array))

    ## from_ascii(list txt, dict dictionary) -> Image
    ## Crée une image à partir de `txt`, une liste de chaînes de caractères.
    ## A chaque caractère possible dans `txt` est associé une couleur
    ## correspondante dans `dictionnary.
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

    ## from_spritesheet(str path, 2-tuple sprite_size, 3-tuple discard_color)
    ## Charge une image (spritesheet) à partie de son chemin `path`, et découpe
    ## celle-ci en sous-images de taille `sprite_size`. Les sous-images
    ## possédant la couleur `discard_color` au pixel (0, 0) sont éliminées.
    @classmethod
    def from_spritesheet(cls, path, sprite_size, discard_color):
        spritesheet = cls.from_path(path)

        images = []
        for y in range(spritesheet.rect.h // sprite_size[1]):
            for x in range(spritesheet.rect.w // sprite_size[0]):
                img = spritesheet.subimage(Rect(
                    x * sprite_size[0], # x
                    y * sprite_size[1], # y
                    sprite_size[0],     # width
                    sprite_size[1],     # height
                ))
                if img[0, 0] == discard_color: break
                images.append(img)

        return images

    # Méthodes

    ## copy() -> Image
    ## Crée une copie complète de l'image actuelle.
    def copy(self):
        return self.__class__(self)

    ## subimage(Rect area) -> Image
    ## Crée une nouvelle image faisant référence à une zone plus petite de
    ## l'image actuelle. `area` correspond à la zone à extraire de l'image
    ## actuelle.
    def subimage(self, area):
        return self.__class__(self.pygsurface.subsurface(area))

    ## [int x, int y] -> `pygame.Color`
    ## Renvoie la couleur du pixel à la position spécifiée.
    ## ```python
    ## i = Image((20, 20))
    ## print(i[0, 0]) # (0, 0, 0, 255)
    ## ```
    def __getitem__(self, pos):
        return self.pygsurface.get_at(pos)

    ## [int x, int y] = 3-tuple color
    ## Définit la couleur du pixel à la position spécifiée.
    ## ```python
    ## i = Image((20, 20))
    ## i[0, 0] = (0, 255, 0)
    ## print(i[0, 0]) # (0, 255, 0, 255)
    ## ```
    def __setitem__(self, pos, color):
        self.pygsurface.set_at(pos, color)

    ## colorkey(3-tuple color)
    ## Définit la couleur de transparence de l'image.
    def colorkey(self, color):
        self.pygsurface.set_colorkey(color)
        return self

    ## fill(3-tuple color)
    ## Remplit l'image d'une couleur.
    def fill(self, color):
        self.pygsurface.fill(color)
        return self

    ## draw_img(Image img, 2-tuple pos, Rect area = None):
    ## Dessine une image (`img`) à la position spécifiée (`pos`) sur l'image
    ## actuelle. Une zone spécifique de `img` peut être dessinée à l'aide de
    ## `area`.
    def draw_img(self, img, pos, area = None):
        self.pygsurface.blit(img.pygsurface, pos, area)
        return self

    ## draw_rect(3-tuple color, Rect rect, int width = 0):
    ## Dessine un rectangle `rect` de couleur `color` et d'épaisseur de bordure
    ## `width`. Si width est égal à 0, le rectangle sera plein.
    def draw_rect(self, color, rect, width = 0):
        pygame.draw.rect(self.pygsurface, color, rect, width)
        return self

    ## draw_circle(3-tuple color, 2-tuple center, int radius, int width = 0):
    ## Dessine un cercle de couleur `color`, de centre `center`, de rayon
    ## `radius` et d'épaisseur de bordure `width`. Si `width` est égal à 0, le
    ## cercle sera plein.
    def draw_circle(self, color, center, radius, width = 0):
        pygame.draw.circle(self.pygsurface, color, center, radius, width)
        return self

    ## draw_line(
    ##     3-tuple color, 2-tuple start_pos, 2-tuple end_pos, int width = 1
    ## )
    ## Dessine une ligne de couleur `color`, de position de départ `start_pos`,
    ## de position d'arrivée `end_pos` et d'épaisseur `width`.
    def draw_line(self, color, start_pos, end_pos, width = 1):
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)
        return self

    ## flip(bool x, bool y)
    ## Inverse l'image horizontalement (`x`) et/ou verticalement (`y`).
    def flip(self, x, y):
        self.pygsurface = pygame.transform.flip(self.pygsurface, x, y)
        return self

    ## resize(2-tuple size)
    ## Redimensionne l'image. Sa nouvelle taille sera `size`.
    def resize(self, size):
        self.pygsurface = pygame.transform.scale(self.pygsurface, size)
        return self

    ## scale(float ratio)
    ## Mise à l'échelle de l'image.
    def scale(self, ratio):
        self.resize(size = (
                int(self.rect.w * ratio),
                int(self.rect.h * ratio),
        ))
        return self

    ## rotate(int angle)
    ## Fait pivoter l'image d'un `angle` spécifié en degrés.
    def rotate(self, angle):
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)
        return self

    # Propriétés

    ## rect -> Rect
    ## Retourne un nouveau rectangle positionné en (0, 0) et de la taille de
    ## l'image actuelle.
    @property
    def rect(self): return Rect(self.pygsurface.get_rect())
