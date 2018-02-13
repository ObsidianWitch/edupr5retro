import sys, pygame

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

class Ball:
    def __init__(self, window):
        self.window = window

        self.x = 50
        self.y = self.window.height // 2

        self.dx = 3
        self.dy = 3

        self.radius = 10

        self.outer_circle_color = pygame.Color("blue")
        self.inner_circle_color = pygame.Color("red")

        self.bounce_state = 0

    def bounce(self, dx_mul = 1, dy_mul = 1):
        y_collision = (self.y > self.window.height or self.y < 0)
        x_collision = (self.x > self.window.width or self.x < 0)

        if not y_collision and not x_collision: return

        if y_collision: self.dy *= -1
        if x_collision: self.dx *= -1

        if self.inner_circle_color == pygame.Color("red"):
            self.inner_circle_color = pygame.Color("green")
        else:
            self.inner_circle_color = pygame.Color("red")

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.bounce()

    def draw(self):
        pygame.draw.circle(
            self.window.screen,      # surface
            self.outer_circle_color, # color
            [self.x, self.y],        # position
            self.radius * 2          # radius
        )
        pygame.draw.circle(
            self.window.screen,      # surface
            self.inner_circle_color, # color
            [self.x, self.y],        # position
            self.radius              # radius
        )

# main function to avoid namespace pollution (global variables)
def main():
    window = Window()

    ball = Ball(window)

    def game_update():
        # Update
        ball.update()

        # Draw
        window.screen.fill(pygame.Color("white"))
        pygame.draw.rect(
            window.screen,                       # surface
            pygame.Color("green"),               # color
            [0, 0, window.width, window.height], # rect
            5                                    # width
        )
        ball.draw()

        # Debug
        print(f"position: ({ball.x}, {ball.y})\tspeed: ({ball.dx}, {ball.dy})")

    window.loop(game_update)

main()
