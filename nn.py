import random
import math
import copy

class NN(list):
    def __init__(self, arch):
        def genw_layers(): return [
            genw_neurons(i) for i,_ in enumerate(arch[0:-1])
        ]
        def genw_neurons(i): return [
            genw_weights(i) for _ in range(arch[i + 1])
        ]
        def genw_weights(i): return [
            random.uniform(-5.0, 5.0) for _ in range(arch[i])
        ]

        list.__init__(self, genw_layers())

    def predict(self, *inputs):
        def dot(v1, v2): return sum(v1[i] * v2[i] for i, _ in enumerate(v1))

        values = inputs
        for w in self: values = [
            math.tanh(dot(values, n)) for n in w
        ]

        return values

class NNGAPool(list):
    def __init__(self, size, arch):
        list.__init__(self, [NN(arch) for i in range(size)])
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
                        nn[i][j][k] += random.uniform(-1.0, 1.0)
        return nn

    # Evolve a population of NNs based on the fitness retrieved from associated
    # `units`. Returns the best fitness from the generation before the
    # evolution.
    def evolve(self, units):
        # units' indexes sorted by fitness
        isorted = sorted(
            range(len(units)),
            key     = lambda i: units[i].fitness,
            reverse = True,
        )

        # 2/10th of the new pool will contain the best NNs from the previous
        # generation
        nbest = math.ceil(0.2 * len(self))
        best = [self[i] for i in isorted[0 : nbest]]

        # 8/10th of the new pool will contain evolved NNs
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
