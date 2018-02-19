import os, inspect
import pygame
import pygame.surfarray as surfarray
import numpy as np

from lemmings.common import asset_path

class StateRun:
    def __init__(self, window):
        self.window = window

        # liste des etats
        self.EtatMarche = 100
        self.EtatChute  = 200
        self.EtatStop   = 300
        self.EtatDead   = 400

        self.bg = pygame.image.load(asset_path("map.png"))
        self.spritesheet = pygame.image.load(asset_path("planche.png"))
        self.spritesheet.set_colorkey((0,0,0))

        self.lemmings = []
        self.compteur_creation = 0

        self.marche = self.chargeSerieSprites(0)
        self.tombe  = self.chargeSerieSprites(1)

    def chargeSerieSprites(self, id):
        sprite_width = 30
        sprite = []
        for i in range(18):
            spr = self.spritesheet.subsurface(
                (sprite_width * i, sprite_width * id, sprite_width, sprite_width)
            )
            test = spr.get_at((10,10))
            if (test != (255,0,0,255)): sprite.append(spr)
        return sprite

    def new_lemming(self): return {
        "x": 250,
        "y": 100,
        "vx": -1,
        "etat": self.EtatChute,
        "fallcount": 0,
    }

    def run(self):
        time = int(pygame.time.get_ticks() / 100)

        # draw background
        self.window.screen.blit(self.bg, (0,0))

        # creation des lemmings : 1 lemming toutes les 1,5 secondes
        if (
            (self.compteur_creation < 5 )
            and ((time + self.compteur_creation) % 15 == 0)
        ):
            self.compteur_creation += 1
            self.lemmings.append(self.new_lemming())

       # gestion des évènements
        for e in self.window.events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                pygame.draw.line(self.window.screen, (255,255,255),(x-5,y),(x+5,y))
                pygame.draw.line(self.window.screen, (255,255,255),(x,y-5),(x,y+5))
                print("Click - Grid coordinates: ", x, y)

       # ETAPE 1 : gestion des transitions

       # ETAPE 2 : gestion des actions
        for onelemming in self.lemmings:
            if ( onelemming['etat'] == self.EtatChute ):
                onelemming['y'] += 3
                onelemming['fallcount'] += 3

        # ETAPE 3 : affichage des lemmings
        for onelemming in self.lemmings:
            xx = onelemming['x']
            yy = onelemming['y']

            if (onelemming['etat'] == self.EtatChute):
                self.window.screen.blit(self.tombe[time%len(self.tombe)], (xx, yy))
