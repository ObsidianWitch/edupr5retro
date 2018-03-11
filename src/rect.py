import pygame
class Rect(pygame.Rect):
    # Renvoie un nouveau rectangle possédant la même position et la même taille
    # que l'original.
    def copy(self): return pygame.Rect.copy(self)

    # Déplace le rectangle de `x` et `y`.
    def move(self, *vec): pygame.Rect.move_ip(self, vec) ; return self

    # Déplace le rectangle actuel dans `rect`. Si le rectangle actuel est trop
    # grand pour rentrer dans `rect`, il sera centré à l'intérieur et sa taille
    # ne changera pas.
    def clamp(self, rect): pygame.Rect.clamp_ip(self, rect) ; return self

    # Renvoie un nouveau rectangle étant l'union du rectangle actuel et de
    # `rect`.
    def union(self, rect): return pygame.Rect.union(self, rect)

    # Renvoie un nouveau rectangle étant l'intersection du rectangle actuel et
    # de `rect`.
    def intersection(self, rect): return pygame.Rect.clip(self, rect)

    # Teste si `rect` est complétement à l'intérieur du rectangle actuel.
    def contains(self, rect): return pygame.Rect.contains(self, rect)

    # Teste si `p` est à l'intérieur du rectangle actuel.
    def collidepoint(self, *p): return pygame.Rect.collidepoint(self, p)

    # Teste s'il y intersection entre `rect` et le rectangle actuel.
    def colliderect(self, rect): return pygame.Rect.colliderect(self, rect)

    # Disable some methods inherited from pygame.Rect.
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
