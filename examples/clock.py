import pygame
from src.clock import Clock

pygame.init()
clock = Clock(framerate = 10)

while 1:
    print(f"t: {Clock.time()} ms")
    print(f"f: {1000 / clock.tick()} FPS")
