import os
import retro

def assets(filename): return os.path.join("assets", filename)

class Sprite:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.rect()

    def collide(self, *args):
        for elem in args:
            if self.rect.colliderect(elem): return True
        return False

    def update(self): pass
    def draw(self, image): image.draw_img(self.image, self.rect)

class Game:
    MAZE_IMG = retro.Image.from_path(assets("maze.png"))

    def __init__(self, window):
        self.window = window
        self.maze = Sprite(self.MAZE_IMG.copy())
        self.maze.rect.bottom = self.window.rect().bottom

    def run(self):
        # Update
        # TODO

        # Draw
        self.window.fill(retro.BLACK)
        self.maze.draw(self.window)
