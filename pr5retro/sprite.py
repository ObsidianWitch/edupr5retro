import pygame
from pr5retro.image import Image

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

class Timer:
    def __init__(self, end = 0, period = 1000):
        self.end = end
        self.period = period
        self.restart()

    @property
    def time(self): return (pygame.time.get_ticks() // self.period)

    @property
    def elapsed(self): return (self.time - self.t0)

    @property
    def remaining(self): return (self.end - self.elapsed)

    @property
    def finished(self): return (self.elapsed >= self.end)

    def restart(self): self.t0 = self.time

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
        i = self.timer.elapsed % len(self.current)
        return self.current[i]

    ## ~~~{.python .prototype}
    ## finished -> bool
    ## ~~~
    ##
    ## Retourne si l'animation a été complétée au moins une fois.
    @property
    def finished(self): return self.timer.finished

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
    ## [`timer`](#classe-timer) permet de gérer le passage d'une frame à
    ## l'autre.
    def start(self, name):
        self.set(name)
        self.timer = Timer(
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
