import sys, pygame

# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]

class Window:
    def __init__(self):
        pygame.init()

        self.width  = 800
        self.height = 600
        self.screen = pygame.display.set_mode([self.width, self.height])

        pygame.display.set_caption("Bouncing Ball !!!")

        self.clock = pygame.time.Clock()

    def loop(self, instructions):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            instructions()

            self.clock.tick(30) # 30 FPS

            pygame.display.flip() # update display Surface

# Initialization
window = Window()

# Starting position
box_x = 50
box_y = window.height // 2

# Speed and direction
box_change_x = 3
box_change_y = 3

box_rayon = 10

box_state = 0

def game_logic():
    # TEMP The global statement is a declaration which holds for the entire current
    # code block. It means that the listed identifiers are to be interpreted as
    # globals.
    global box_x
    global box_y
    global box_change_y
    global box_change_x
    global box_state

    # LOGIQUE
    # Move the rectangle
    box_x += box_change_x
    box_y += box_change_y

    # Rebond
    if box_y > window.height or box_y < 0:
        box_change_y = box_change_y * -1
        box_state = 1 - box_state
    if box_x > window.width or box_x < 0:
        box_change_x = box_change_x * -1
        box_state = 1 - box_state

    #DESSIN
    # Set the screen background
    window.screen.fill(WHITE)

    # Draw screen border
    pygame.draw.rect(window.screen,GREEN,[0, 0, window.width, window.height], 5)

    #dessine le palet
    pygame.draw.circle(window.screen, BLUE, [box_x, box_y], box_rayon *2)
    pygame.draw.circle(window.screen, RED if box_state == 0 else GREEN, [box_x, box_y], box_rayon )

    #debug
    print('position ({0:3d},{1:3d}) and (dx,dy): ({2},{3})'.format(box_x,box_y,box_change_x,box_change_y))

window.loop(game_logic)


# Close everything down
pygame.quit()
