import include.retro as retro
from bouncing_ball.ball import Ball
from shared.window import Window

window = Window(
    size  = (800, 600),
    title = "Bouncing Ball !!!",
)
window.cursor(False)

ball = Ball(window)

def game():
    # Update
    ball.update()

    # Draw
    window.fill(retro.WHITE) \
          .draw_rect(
              color = retro.GREEN,
              rect  = window.rect(),
              width = 5,
          )
    ball.draw()

    # Debug
    print(f"position: {ball.circle.center}\tspeed: {ball.speed}")

window.loop(game)
