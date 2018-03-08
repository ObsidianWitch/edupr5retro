import os, inspect
import pygame
import retro

######################################################################
# Mise en place de la partie technique | ne pas toucher

scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))
scriptDIR  = os.path.dirname(scriptPATH)
assets = lambda filename: os.path.join(scriptDIR, "assets", filename)

window = retro.Window(
    title = "Mon Super Jeu",
    size  = (640, 480)
)
clock = pygame.time.Clock()
# clock = retro.Clock(30)

# Ressources
bandit1 = pygame.image.load(assets("bandit_rue.png"))
bandit1.set_colorkey((255, 255, 255))
bandit1_rect = bandit1.get_rect()
bandit1_rect.bottom = window.rect.bottom
bandit1_rect.left = 100

bandit2 = pygame.transform.scale(
    bandit1, (bandit1.get_width() // 2, bandit1.get_height() // 2)
)
bandit2_rect = bandit1.get_rect()
bandit2_rect.bottom = window.rect.bottom
bandit2_rect.left = 200

bandit3 = pygame.transform.rotate(bandit2, 180)
bandit3_rect = bandit2.get_rect()
bandit3_rect.bottom = window.rect.bottom
bandit3_rect.left = 200

decor = pygame.image.load(assets("map.png"))

zone_jaune = window.rect.copy()

def game():
    # Logiqe
    if window.keys[pygame.K_LEFT]:  zone_jaune.move_ip(-5, 0)
    if window.keys[pygame.K_RIGHT]: zone_jaune.move_ip( 5, 0)

    # Affichage
    window.screen.blit(
        source = decor,
        dest   = (0, 0),
        area   = zone_jaune,
    )

    window.screen.blit(bandit1, bandit1_rect)
    window.screen.blit(bandit2, bandit2_rect)
    window.screen.blit(bandit3, bandit3_rect)

    print(1000 / clock.tick(30))
    # print(1 / clock.tick())

window.loop(game)
