import os
import pygame

asset_path = lambda filename: os.path.join("empire_city/data", filename)
get_time = lambda: pygame.time.get_ticks() // 1000
