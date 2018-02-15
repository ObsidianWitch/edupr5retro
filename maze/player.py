import pygame
import numpy

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

        self.sprite = self.to_sprite(self.char1_ascii)
        self.x = 50
        self.y = 50

    def to_sprite(self, ascii):
       _larg = len(max(ascii, key=len)) # on prend la ligne la plus grande
       _haut = len(ascii)
       TBL = numpy.zeros((_larg,_haut,3)) # tableau 3 dimensions

       for y in range(_haut):
          ligne = ascii[y]
          for x in range(len(ligne)):
             c = ligne[x]  # on recupere la lettre
             TBL[x,y] = palette[c]  #on stocke le code couleur RVB

       return pygame.surfarray.make_surface(TBL)

    def move(self, keys):
        if keys[pygame.K_UP]:    self.y -= 1
        if keys[pygame.K_DOWN]:  self.y +=1
        if keys[pygame.K_LEFT]:  self.x -= 1
        if keys[pygame.K_RIGHT]: self.x +=1

    def draw(self):
        self.window.screen.blit(self.sprite, (self.x, self.y))
