import pygame
import numpy as np
import os, inspect
import pygame.surfarray as surfarray
 
#recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"data")
  
fond = pygame.image.load(os.path.join(assets, "map.png"))
planche_sprites = pygame.image.load(os.path.join(assets, "planche.png"))
planche_sprites.set_colorkey((0,0,0))

LARG = 30
def ChargeSerieSprites(id):
   sprite = []
   for i in range(18):
      spr = planche_sprites.subsurface((LARG * i, LARG * id, LARG,LARG))
      test = spr.get_at((10,10))
      if ( test != (255,0,0,255) ):
         sprite.append( spr )
   return sprite



###################################################################################
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("LEMMINGS")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# liste des etats
EtatMarche = 100
EtatChute  = 200
EtatStop   = 300
EtatDead   = 400
   
# liste des lemmins en cours de jeu

lemmingsLIST = []
compteur_creation = 0

 
 
# -------- Main Program Loop -----------

marche = ChargeSerieSprites(0)
tombe  = ChargeSerieSprites(1)

pygame.mouse.set_visible(1)

while not done:
    event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
   
    time = int( pygame.time.get_ticks() / 100 )
    
    # draw background
    screen.blit(fond,(0,0))
    
    # creation des lemmings : 1 lemming toutes les 1,5 secondes
    if (  (compteur_creation < 5 ) and ( (time+compteur_creation) % 15 == 0) ):
      compteur_creation += 1
      new_lemming = {}
      new_lemming['x']  = 250
      new_lemming['y']  = 100
      new_lemming['vx'] = -1
      new_lemming['etat'] = EtatChute  
      new_lemming['fallcount'] = 0
      lemmingsLIST.append(new_lemming)

   # gestion des évènements
   
   
    for event in pygame.event.get():  # User did something
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            
    if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            pygame.draw.line(screen, (255,255,255),(x-5,y),(x+5,y))
            pygame.draw.line(screen, (255,255,255),(x,y-5),(x,y+5))
            print("Click - Grid coordinates: ", x, y)
            
   # ETAPE 1 : gestion des transitions
   
   # ETAPE 2 : gestion des actions
   
             
    for onelemming in lemmingsLIST:
      if ( onelemming['etat'] == EtatChute ):
         onelemming['y'] += 3
         onelemming['fallcount'] += 3
    
    # ETAPE 3 : affichage des lemmings
    
    for onelemming in lemmingsLIST:
      xx = onelemming['x']
      yy = onelemming['y']
      state = onelemming['etat']      
      
      if ( state == EtatChute ):
         screen.blit(tombe[time%len(tombe)],(xx,yy))

 
    clock.tick(20)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 

pygame.quit()