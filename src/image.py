import pygame
import numpy
from src.rect import Rect
class Image:
    # Image(size) -> Image
    # **size**: `tuple (int width, int height)`
    # Image(image) -> Image
    # **image**: `Image`
    def __init__(self, arg):
        if isinstance(arg, Image):
            self.pygsurface = arg.pygsurface.copy()
        elif isinstance(arg, pygame.Surface):
            self.pygsurface = arg
        else:
            self.__init__(pygame.Surface(arg))

    # Crée une image à partir d'un fichier.
    # **path**: `str`, chemin de l'image
    # **returns**: Image
    @classmethod
    def from_path(cls, path):
        return cls(pygame.image.load(path))

    # Crée une image à partir d'un tableau à 2 dimensions.
    # **array**: `2D array`
    # **returns**: Image
    @classmethod
    def from_array(cls, array):
        return cls(pygame.surfarray.make_surface(array))

    # Crée une image à partir d'un tableau à 2 dimensions de symboles. Chaque
    # symbole est remplacé par une couleur correspondant dans le dictionnaire
    # spécifié en paramètre.
    # **txt**: `2D array`
    # **dictionary**: `dict`
    # **returns**: Image
    @classmethod
    def from_ascii(cls, txt, dictionary):
        height = len(txt)
        width  = len(txt[0])

        rgb_sprite = numpy.zeros((width, height, 3))
        for y, x in numpy.ndindex(height, width):
            c = txt[y][x]
            rgb_sprite[x,y] = dictionary[c]

        return cls.from_array(rgb_sprite)

    # Crée une liste d'images en découpant une image (spritesheet) en
    # sous-images (sprite) d'une taille spécifée.
    # **path**: `str`, chemin de la spritesheet
    # **sprite_size**: `tuple (int width, int height)`, taille d'un prite
    # **discard_color**: `tuple (int r, int g, int b)`, passe à la ligne
    # suivante de la spritesheet lorsque cette couleur est rencontrée
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

    # Crée une copie complète de l'image actuelle.
    # **returns**: Image
    def copy(self):
        return self.__class__(self)

    # Crée une nouvelle image faisant référence à une zone plus petite de
    # l'image actuelle.
    # **area**: `Rect`, désigne la zone à extraire de l'image actuelle.
    # **returns**: `Image`
    def subimage(self, area):
        return self.__class__(self.pygsurface.subsurface(area))

    # Retourne un nouveau rectangle positionné en (0, 0) et de la taille de
    # l'image actuelle.
    # **returns**: `Rect`
    @property
    def rect(self): return Rect(self.pygsurface.get_rect())

    # Renvoie la couleur du pixel à la position spécifiée.
    # **pos**: `tuple (int x, int y)`, position
    # **returns**: `pygame.Color`
    def __getitem__(self, pos):
        return self.pygsurface.get_at(pos)

    # Définit la couleur du pixel à la position spécifiée.
    # **pos**: `tuple (int x, int y)`, position
    # **color**: `tuple (int r, int g, int b)`
    def __setitem__(self, pos, color):
        self.pygsurface.set_at(pos, color)

    # Définit la couleur de transparence de l'image.
    # **color**: `tuple (int r, int g, int b)`
    def colorkey(self, color):
        self.pygsurface.set_colorkey(color)
        return self

    # Remplit l'image d'une couleur.
    # **color**: `tuple (int r, int g, int b)`
    def fill(self, color):
        self.pygsurface.fill(color)
        return self

    # Dessine une image à la position spécifiée sur l'image actuelle.
    # **img**: `Image`
    # **pos**: `tuple (int x, int y)` ou `Rect`, position
    # **area**: `Rect`, désigne quelle zone (plus petite) de `img` doit être
    # dessinée.
    def draw_img(self, img, pos, area = None):
        self.pygsurface.blit(img.pygsurface, pos, area)
        return self

    # Dessine un rectangle.
    # **color**: `tuple (int r, int g, int b)`
    # **rect**: `Rect`
    # **width**: `int`, épaisseur du recrangle. Si 0 est spécifié, le rectangle
    # sera plein.
    def draw_rect(self, color, rect, width = 0):
        pygame.draw.rect(self.pygsurface, color, rect, width)
        return self

    # Dessine un cercle.
    # **color**: `tuple (int r, int g, int b)`
    # **center**: `tuple (int x, int y)`
    # **radius**: `int`, rayon
    # **width**:, `int`, épaisseur du cercle. Si 0 est spécifié, le cercle sera
    # plein.
    def draw_circle(self, color, center, radius, width = 0):
        pygame.draw.circle(self.pygsurface, color, center, radius, width)
        return self

    # Dessigne une ligne.
    # **color**: `tuple (int r, int g, int b)`
    # **start_pos**: `tuple (int x, int y)`, position de départ
    # **end_pos**: `tuple (int x, int y)`, possition d'arrivée
    # **width**: épaisseur
    def draw_line(self, color, start_pos, end_pos, width = 1):
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)
        return self

    # Inverse l'image.
    # **x**: `bool`: inverse l'image horizontalement.
    # **y**: `bool`: inverse l'image verticalement.
    def flip(self, x, y):
        self.pygsurface = pygame.transform.flip(self.pygsurface, x, y)
        return self

    # Redimensionne l'image.
    # **size**: `tuple (int width, int height)`, nouvelle taille de l'image
    def resize(self, size):
        self.pygsurface = pygame.transform.scale(self.pygsurface, size)
        return self

    # Mise à l'échelle de l'image.
    # **ratio**: `float`
    def scale(self, ratio):
        self.resize(size = (
                int(self.rect.w * ratio),
                int(self.rect.h * ratio),
        ))
        return self

    # Fait pivoter l'image.
    # **angle**: `int`, degrès
    def rotate(self, angle):
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)
        return self
