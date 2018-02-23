import os
import inspect
import pygame
import numpy

class Image:
    project_path = lambda filename: os.path.join(
        os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))),
        "..",
        filename,
    )

    @classmethod
    def from_path(cls, path):
        return pygame.image.load(cls.project_path(path))

    @classmethod
    def from_path_n(cls, paths):
        return [cls.from_path(p) for p in paths]

    @classmethod
    def from_ascii(cls, txt, dictionary):
        height = len(txt)
        width  = len(txt[0])

        rgb_sprite = numpy.zeros((width, height, 3))
        for y, x in numpy.ndindex(height, width):
            c = txt[y][x]
            rgb_sprite[x,y] = dictionary[c]

        return pygame.surfarray.make_surface(rgb_sprite)

    @classmethod
    def from_ascii_n(cls, txts, dictionary):
        return [cls.from_ascii(t, dictionary) for t in txts]

    @classmethod
    def from_spritesheet_n(cls, path, sprite_size, discard_color):
        spritesheet = cls.from_path(path)

        images = []
        for y in range(spritesheet.get_height() // sprite_size[1]):
            for x in range(spritesheet.get_width() // sprite_size[0]):
                img = spritesheet.subsurface(pygame.Rect(
                    x * sprite_size[0], # x
                    y * sprite_size[1], # y
                    sprite_size[0],     # width
                    sprite_size[1],     # height
                ))
                if img.get_at((0, 0)) == discard_color: break
                images.append(img)
        return images
