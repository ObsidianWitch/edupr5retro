import pygame

class Surface:
    def __init__(self, pygsurface):
        self.pygsurface = pygsurface

    def draw_surface(self, source, position, area = None):
        self.pygsurface(source, position, area)
