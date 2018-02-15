import pygame
import numpy

from shared.sprite import Sprite
from maze.palette import palette

class Player:
    char1_ascii = [
        '   RRR    ',
        '  RRWWR   ',
        '   RRR    ',
        '   YY     ',
        '   YYY    ',
        '   YY YG  ',
        '   GG     ',
        '   CC     ',
        '   CC     ',
        '  C  C    ',
        '  C  C    ',
    ]

    char2_ascii = [
        '   RRR    ',
        '  RRWWR   ',
        '   RRR    ',
        '   YY     ',
        '   YYY    ',
        '   YY YG  ',
        '   GG     ',
        '   CC     ',
        '   CC     ',
        '   CC     ',
        '   CC     ',
    ]

    def __init__(self, window):
        self.window = window

        self.sprite = Sprite.from_ascii(
            ascii_sprite = self.char1_ascii,
            dictionary   = palette,
            position     = (50, 50),
            colorkey     = palette[' '],
        )

    def move(self, keys):
        if keys[pygame.K_UP]:    self.sprite.rect.move_ip( 0, -1)
        if keys[pygame.K_DOWN]:  self.sprite.rect.move_ip( 0,  1)
        if keys[pygame.K_LEFT]:  self.sprite.rect.move_ip(-1,  0)
        if keys[pygame.K_RIGHT]: self.sprite.rect.move_ip( 1,  0)

    def draw(self):
        self.window.screen.blit(self.sprite.image, self.sprite.rect.topleft)
