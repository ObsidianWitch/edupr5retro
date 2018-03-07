import pygame
import retro

def test_retroclock():
    retroclock = retro.Clock(framerate = 60)
    while 1: print(1 / retroclock.tick())

def test_pygameclock():
    pygameclock = pygame.time.Clock()
    while 1: print(1000 / pygameclock.tick(60))

test_retroclock()
# test_pygameclock()
