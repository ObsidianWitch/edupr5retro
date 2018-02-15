import pygame
import numpy as np
import pygame.surfarray as surfarray
 
# crée une palette de couleurs
palette = {} # initialise un dictionnaire
palette['B'] =  [  0,   0, 255]   # BLUE
palette[' '] =  [  0,   0,   0]   # BLACK
palette['W'] =  [255, 255, 255]   # WHITE
palette['G'] =  [  0, 255,   0]   # GREEN
palette['R'] =  [255,   0,   0]   # RED
palette['Y'] =  [255, 255,   0]   # YELLOW
palette['C'] =  [  0, 225, 255]   # CYAN


# dimensions
WIDTH = 40  # largeur d'une case en pixels
NBcases = 10

# grille du jeu

plan = [ 'BBBBBBBBBB', 
         'B        B',
         'B BB BBBBB',
         'B B  B   B',
         'B BB BB  B',
         'B B   BB B',
         'B  B  B  B',
         'BB BB BB B',
         'B   B    B',
         'BBBBBBBBBB' ]

#verification du plan

if ( len(plan) != NBcases ): print("erreur, nombre de lignes dans le plan")
for ligne in plan:
    if ( len(ligne) != NBcases ): print("erreur, ligne pas à la bonne dimension")

# remplissage du tableau du labyrinthe
LABY  = np.zeros((NBcases,NBcases,3))
for y in range(NBcases):
    ligne = plan[y]
    for x in range(NBcases):
        c = ligne[x]
        LABY[x,y] = palette[c]
        
###################################################################################

def ToSprite(ascii):
   _larg = len(max(pers1, key=len)) # on prend la ligne la plus grande
   _haut = len(pers1)
   TBL = np.zeros((_larg,_haut,3)) # tableau 3 dimensions

   for y in range(_haut):
      ligne = ascii[y]
      for x in range(len(ligne)):
         c = ligne[x]  # on recupere la lettre
         TBL[x,y] = palette[c]  #on stocke le code couleur RVB
    
   # conversion du tableau de RVB en sprite pygame
   sprite = surfarray.make_surface(TBL)
   return sprite


pers1= [ '   RRR    ', 
         '  RRWWR   ',
         '   RRR    ',
         '   YY     ',
         '   YYY     ',
         '   YY YG   ',
         '   GG      ',
         '   CC      ',
         '   CC      ',
         '  C  C     ',
         '  C  C    ' ]
         
pers2 = [ '   RRR    ', 
         '  RRWWR   ',
         '   RRR    ',
         '   YY     ',
         '   YYY     ',
         '   YY YG   ',
         '   GG      ',
         '   CC      ',
         '   CC      ',
         '   CC     ',
         '   CC    ' ]


player_sprite = ToSprite(pers1)
player_x = 50
player_y = 50

###################################################################################
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("LABYRINTHE")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
    
    for event in pygame.event.get():  # User did something
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            
    KeysPressed = pygame.key.get_pressed()
   
    
    if KeysPressed[pygame.K_UP]:
        player_y -= 1
        
    if KeysPressed[pygame.K_DOWN]:
        player_y += 1
       
 
    # Draw background
    for ix in range(NBcases):
        for iy in range(NBcases):
            xpix = WIDTH * ix
            ypix = WIDTH * iy
            couleur = LABY[ix,iy]
            pygame.draw.rect(screen,couleur,[xpix,ypix,WIDTH,WIDTH])
             
    # draw player
    screen.blit(player_sprite,(player_x,player_y))
 
    print(player_sprite.get_width())
    
 
    # 30 fps
    clock.tick(30)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 

pygame.quit()