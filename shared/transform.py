import pygame

def scale_n(surfaces, ratio): return [
    scale(s, ratio) for s in surfaces
]

def flip_n(surfaces, xflip, yflip): return [
    pygame.transform.flip(s, xflip, yflip) for s in surfaces
]
