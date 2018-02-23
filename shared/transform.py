import pygame

def scale(surface, ratio):
    rect = surface.get_rect()
    rect.size = (
        int(rect.width * ratio),
        int(rect.height * ratio),
    )
    return pygame.transform.scale(surface, rect.size)

def scale_n(surfaces, ratio): return [
    scale(s, ratio) for s in surfaces
]

def flip_n(surfaces, xflip, yflip): return [
    pygame.transform.flip(s, xflip, yflip) for s in surfaces
]
