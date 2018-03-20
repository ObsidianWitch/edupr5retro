import random
import math
import sys
import retro
from game import Game

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

class NN(Sequential):
    def __init__(self):
        Sequential.__init__(self)
        self.add(Dense(input_dim = 2, units = 1))
        self.add(Activation("sigmoid"))

        sgd = SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True)
        self.compile(loss = "mse", optimizer = sgd, metrics = ["accuracy"])

    def predict(self, birdy, targety):
        birdy = birdy / window.rect().height
        targety = targety / window.rect().height

        neural_input = np.asarray([birdy, targety])
        neural_input = np.atleast_2d(neural_input)
        output_prob = Sequential.predict(self, neural_input, 1)[0]
        return (output_prob[0] >= 0.5)

class NNPool(list):
    def __init__(self, size):
        list.__init__(self, [NN() for i in range(size)])
        self.generation = 1

    @classmethod
    def crossover(cls, m1, m2):
        w1 = m1.get_weights()
        w2 = m2.get_weights()
        w1[0][0], w2[0][0] = np.copy(w2[0][0]), np.copy(w1[0][0])
        return np.asarray([w1, w2])

    @classmethod
    def mutate(cls, w):
        for i in range(len(w[0])):
            if random.uniform(0, 1) < 0.15:
                change = random.uniform(-0.5, 0.5)
                w[0][i] += change
        return w

    def evolve(self):
        # birds' indexes sorted by fitness
        isorted = sorted(
            range(len(game.birds)),
            key     = lambda i: game.birds[i].travelled,
            reverse = True,
        )

        # keep 4/10th of the pool with the best fitness
        nkeep = math.ceil(0.2 * len(game.birds))
        best = [self[i] for i in isorted[0:nkeep]]

        # evolve the rest of the pool
        # 1. crossover of two different random best
        # 2. mutate the new weights
        nevolve  = len(game.birds) - nkeep
        evolve = []
        for i in range(nevolve // 2):
            new_weights = self.crossover(*random.sample(best, 2))
            evolve.append(self.mutate(new_weights[0]))
            evolve.append(self.mutate(new_weights[1]))

        for i, m in enumerate(best): self[i].set_weights(m.get_weights())
        for i, w in enumerate(evolve): self[i + len(best)].set_weights(w)

        self.generation += 1
        return

window = retro.Window(
    title     = "Flappy Bird",
    size      = (288, 512),
    framerate = 100,
)
events = retro.Events()

game = Game(window, nbirds = 10)

pool = NNPool(size = len(game.birds))

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if not game.finished:
        for i, b in enumerate(game.birds):
            if b.alive and pool[i].predict(
                b.rect.y, game.target.centery
            ): b.flap()
        game.run()
    else:
        pool.evolve()
        game.reset()

    window.update()
