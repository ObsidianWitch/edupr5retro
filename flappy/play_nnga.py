import sys
from retro.src import retro
from flappy.nnga import NNGAPool
from flappy.game import Game

window = retro.Window(
    title = "Flappy Bird",
    size  = (288, 512),
    fps   = 0,
)
game = Game(window, nbirds = 10)
pool = NNGAPool(size = len(game.birds), arch = (2, 1))

def main():
    if not game.finished:
        for i, b in enumerate(game.birds):
            if b.fitness >= 10000:
                print(pool.generation, b.fitness)
                sys.exit()

            if b.alive and pool[i].predict(
                b.rect.y / window.rect().height,
                game.target.centery / window.rect().height,
            )[0] > 0.5: b.flap()
        game.run()
    else:
        best_fitness = pool.evolve(game.birds)

        print(pool.generation - 1, best_fitness)
        if pool.generation - 1 >= 50: sys.exit()

        game.reset()

window.loop(main)
