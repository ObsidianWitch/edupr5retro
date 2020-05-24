import random
import math
import numpy

# A neural networks possesses multiple layers. Each layer contains multiple
# neurons. All the neurons from one layer are connected to the neurons of the
# previous layer. These connections are weighted. The first layer is the inputs
# layer. The last layer is the outputs layer.
#
# n_ij: neuron j from layer i
# w_klm: weight connecting neuron m from layer k to neuron l from layer k+1
#        e.g. w131 connects n11 and n23
#         n20
#     n10     n30
# n00     n21
#     n11     n31
# n01     n22
#     n12     n32
#         n23
#
# Outputs and intermediate neurons are computed as follows:
# n_ij (i > 0) = activation(n_(i-1)0 * w_(i-1)j0 + n_(i-1)1 * w_(i-1)j1 + ...)
#              = activation(n_(i-1) · w_(i-1)j)
# e.g. n32 = activation(n20 * w220 + n21 * w221 + n22 * w222 + n23 * w223)
#          = activation(n2 · w22)
#
# The architecture (`arch`) of a neural network refers to the number of layers
# The `arch` describes the number of layers and the number of neurons per layer
# of this neural network. E.g. arch = (3, 5, 4, 2) describes a NN w/ 4 layers
# containing 3, 5, 4 and 2 neurons.
#
# Weights are populated with the `finit` function.
# A Neuron's value is computed with the help of an activation function
# `factivate`.
class NN(list):
    def __init__(self, arch, finit, factivate):
        def genw_column():
            return [ genw_next(k) for k in range(len(arch) - 1) ]
        def genw_next(k):
            return [ genw_prev(k) for _ in range(arch[k + 1]) ]
        def genw_prev(k):
            return [ finit() for _ in range(arch[k]) ]

        list.__init__(self, genw_column())
        self.factivate = factivate

    def predict(self, *inputs):
        outputs = inputs
        for wcol in self:
            outputs = [ self.factivate(numpy.dot(values, wnext))
                       for wnext in wcol ]
        return outputs
