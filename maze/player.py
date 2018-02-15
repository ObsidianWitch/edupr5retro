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

        self.dx = 1
        self.dy = 1

        self.sprite = Sprite.from_ascii(
            ascii_sprite = self.char1_ascii,
            dictionary   = palette,
            position     = (50, 50),
            colorkey     = palette[' '],
        )

    def flip(self, xflip = False, yflip = False):
        if xflip: self.dx *= -1
        if yflip: self.dy *= -1
        self.sprite.image = pygame.transform.flip(
            self.sprite.image, xflip, False
        )

    def move(self, keys):
        if keys[pygame.K_UP]:
            if self.dy > 0: self.flip(yflip = True)
            self.sprite.rect.move_ip(0, self.dy)
        if keys[pygame.K_DOWN]:
            if self.dy < 0: self.flip(yflip = True)
            self.sprite.rect.move_ip(0, self.dy)
        if keys[pygame.K_LEFT]:
            if self.dx > 0: self.flip(xflip = True)
            self.sprite.rect.move_ip(self.dx,  0)
        if keys[pygame.K_RIGHT]:
            if self.dx < 0: self.flip(xflip = True)
            self.sprite.rect.move_ip( 1,  0)

    def draw(self):
        self.window.screen.blit(self.sprite.image, self.sprite.rect.topleft)
