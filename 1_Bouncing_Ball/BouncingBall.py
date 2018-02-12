import pygame

# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]

# Initialization
pygame.init()

screen_size = [800, 600]
screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Bouncing Ball !!!")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Starting position
box_x = 50
box_y = screen_size[1] // 2

# Speed and direction
box_change_x = 3
box_change_y = 3

box_rayon = 10

box_state = 0

# Loop until the user clicks the close button.
done = False

# -------- Main Program Loop -----------
while not done:
    event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event

    # EVENEMENTS
    # détecte le clic sur le bouton close de la fenêtre
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
          done = True

    # LOGIQUE
    # Move the rectangle
    box_x += box_change_x
    box_y += box_change_y

    # Rebond
    if box_y > screen_size[1] or box_y < 0:
        box_change_y = box_change_y * -1
        box_state = 1 - box_state
    if box_x > screen_size[0] or box_x < 0:
        box_change_x = box_change_x * -1
        box_state = 1 - box_state

    #DESSIN
    # Set the screen background
    screen.fill(WHITE)

    # Draw screen border
    pygame.draw.rect(screen,GREEN,[0, 0, screen_size[0], screen_size[1]], 5)

    #dessine le palet
    pygame.draw.circle(screen, BLUE, [box_x, box_y], box_rayon *2)
    pygame.draw.circle(screen, RED if box_state == 0 else GREEN, [box_x, box_y], box_rayon )

    # Limit to 30 frames per second
    clock.tick(30)

    # bascule l'affichage à l'écran
    pygame.display.flip()

    #debug
    print('position ({0:3d},{1:3d}) and (dx,dy): ({2},{3})'.format(box_x,box_y,box_change_x,box_change_y))

# Close everything down
pygame.quit()
