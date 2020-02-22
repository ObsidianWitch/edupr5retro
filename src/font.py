import pygame
from src.constants import *
from src.image import Image
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
