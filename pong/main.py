import pygame
# Setup
pygame.init()

# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]

police = pygame.font.SysFont("arial", 15)


#fonction dessinant le personnage
def DrawStriker(x, y):
   pygame.draw.rect(screen, WHITE, (x,y,stricker_width,stricker_height), 0)
    
def DrawBall(x,y):
   pygame.draw.circle(screen, WHITE, (x,y),10, 0)

 
    

 
# Set the width and height of the screen [width,height]
screeenWidth = 600
screenHeight = 400
screen = pygame.display.set_mode((screeenWidth,screenHeight))
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0) 
 
# Speed in pixels per frame

 
# Current position

stricker_height = 50
stricker_dist   = 20  # distance au bord de la raquette
stricker_width  = 10  # epaisseur de la raquette

striker_1_x = stricker_dist
striker_1_y = 50

striker_2_x = screeenWidth - stricker_dist
striker_2_y = 30

ball_x = int(screeenWidth / 2)
ball_y = int(screenHeight / 2)
ball_speed_x = -2
ball_speed_y = -2
ball_radius  = 10

score_player1 = 0
score_player2 = 0
 
# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)   # Remise à zero de la variable event
   
   # récupère la liste des touches claviers appuyeées sous la forme liste bool
   pygame.event.pump()
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
            
   KeysPressed = pygame.key.get_pressed()
   
   if KeysPressed[pygame.K_UP]:
       striker_1_y -= 2
      
   if KeysPressed[pygame.K_DOWN]:
       striker_1_y += 2 
       
      
   
    # LOGIQUE
    # Move the object according to the speed vector.
   ball_x += ball_speed_x
   ball_y += ball_speed_y
   
   if ( ball_y < ball_radius ):
       ball_y = ball_radius
       ball_speed_y *= -1
       
   # collision avec le palet de gauche
   if ( ball_x - ball_radius  <  stricker_dist + stricker_width ):
       if ( ( ball_y > striker_1_y  ) and (ball_y  <  striker_1_y + stricker_height) ):
          ball_x = stricker_dist + stricker_width + ball_radius
          ball_speed_x *= -1
           
      

 
    # DESSIN
 
    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
   screen.fill(BLACK)
 
   DrawStriker(striker_1_x, striker_1_y)
   DrawStriker(striker_2_x, striker_2_y)
   DrawBall(ball_x,ball_y)
    
   #  dessine le texte dans une zone de rendu à part 
   zone = police.render( str(score_player1)+" : " + str(score_player2), True, GREEN)
   # affiche la zone de rendu aus dessus de fenetre de jeu
   screen.blit(zone,(300,10))
   
 
 
    # Go ahead and update the screen with what we've drawn.
   pygame.display.flip()
 
    # Limit frames per second
   clock.tick(30)
 
# Close the window and quit.
pygame.quit()