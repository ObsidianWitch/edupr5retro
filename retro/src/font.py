import typing as typ
import pygame
from retro.src.constants import *
from retro.src.image import Image

class Font:
    def __init__(self, size: int) -> None:
        self.pygfont = pygame.font.SysFont(None, size)

    def render(self,
        text: str,
        antialias: bool = True,
        color: pygame.Color = BLACK,
        bgcolor: pygame.Color = None
    ) -> Image:
        return Image(
            self.pygfont.render(text, antialias, color, bgcolor)
        )
