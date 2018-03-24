import random
import math
import sys
import copy
import retro
from game import Game

ANALYSIS = sys.argv[1] if len(sys.argv) > 1 else False

class NN(list):
    def __init__(self, *args):
        def genw(): return [
            genw_neurons(i) for i,_ in enumerate(args[0:-1])
        ]
        def genw_neurons(i): return [
            genw_values(i) for _ in range(args[i + 1])
        ]
        def genw_values(i): return [
            random.uniform(-1.0, 1.0) for _ in range(args[i])
        ]
        list.__init__(self, genw())

    def predict(self, *inputs):
        def sigmoid(x): return 1 / (1 + math.exp(-x))
        def dot(v1, v2): return sum(v1[i] * v2[i] for i, _ in enumerate(v1))

        values = inputs
        for w in self: values = [
            sigmoid(dot(values, n)) for n in w
        ]

        return values

class NNPool(list):
    def __init__(self, size, arch):
        list.__init__(self, [NN(*arch) for i in range(size)])
        self.arch = arch
        self.generation = 1

    @classmethod
    def crossover(cls, nn1, nn2):
        nn3 = copy.deepcopy(nn1)
        nn4 = copy.deepcopy(nn2)

        if len(nn3[0][0]) == 1:
            pass
        elif len(nn3[0]) == 1:
            nn3[0][0][0], nn4[0][0][0] = nn4[0][0][0], nn3[0][0][0]
        elif len(nn3) == 1:
            nn3[0][0], nn4[0][0] = nn4[0][0], nn3[0][0]
        else:
            nn3[0], nn4[0] = nn4[0], nn3[0]

        return (nn3, nn4)

    @classmethod
    def mutate(cls, nn):
        for i, _ in enumerate(nn):
            for j, _ in enumerate(nn[i]):
                for k, _ in enumerate(nn[i][j]):
                    if random.uniform(0, 1) < 0.15:
                        nn[i][j][k] += random.uniform(-0.5, 0.5)
        return nn

    def evolve(self, units):
        # birds' indexes sorted by fitness
        isorted = sorted(
            range(len(units)),
            key     = lambda i: units[i].fitness,
            reverse = True,
        )

        # 2/10th of the new pool will contain the best NNs from the previous
        # generation
        nbest = math.ceil(0.2 * len(self))
        best = [self[i] for i in isorted[0 : nbest]]

        # 6/10th of the new pool will contain evolved NNs
        # 1. crossover of two different random best
        # 2. mutate the new weights
        nevolve = math.ceil(0.8 * len(self))
        evolve = []
        for i in range(nevolve // 2):
            new_nns = self.crossover(*random.sample(best, 2))
            evolve.append(self.mutate(new_nns[0]))
            evolve.append(self.mutate(new_nns[1]))

        list.__init__(self, best + evolve)

        self.generation += 1

        return units[isorted[0]].fitness

window = retro.Window(
    title     = "Flappy Bird",
    size      = (288, 512),
    framerate = 0,
)
events = retro.Events()
game = Game(window, nbirds = 10)
pool = NNPool(size = len(game.birds), arch = (2, 1))

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if not game.finished:
        for i, b in enumerate(game.birds):
            if ANALYSIS and b.fitness >= 1000:
                print(b.fitness)
                sys.exit()

            if b.alive and pool[i].predict(
                b.rect.y / window.rect().height,
                game.target.centery / window.rect().height,
            )[0] > 0.5: b.flap()
        game.run()
    else:
        best_fitness = pool.evolve(game.birds)

        if ANALYSIS:
            print(best_fitness)
            if pool.generation >= 50: sys.exit()

        game.reset()

    window.update()
