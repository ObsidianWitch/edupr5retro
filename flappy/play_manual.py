from retro.src import retro
from flappy.game import Game

window = retro.Window(title='Flappy Bird', size=(288, 512), ups=30, fps=30)

game = Game(window, nbirds = 1)

def update():
    if not game.finished:
        b = game.birds[0]
        if window.events.key_press(retro.K_SPACE): b.flap()
        game.update()
    else:
        game.reset()

window.loop(update, game.render)
