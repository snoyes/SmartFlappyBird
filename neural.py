import random


def rangeMap(x, sourceMin, sourceMax, targetMin, targetMax):
    return (x - sourceMin) / (sourceMax - sourceMin) * (
        targetMax - targetMin
    ) + targetMin


class NeuralNetwork:
    def __init__(self, *args, weights=None):
        self.network = []
        if weights is None:
            numInputs = 1
            for size in args:
                self.network.append(
                    [Perceptron(numInputs=numInputs) for _ in range(size)]
                )
                numInputs = size
        else:
            numInputs = 1
            for layer in weights:
                self.network.append([Perceptron(weights=weights) for weights in layer])

    def predict(self, inputs):
        # First layer gets one input each
        assert len(inputs) == len(self.network[0])
        outputs = [p.guess([i]) for p, i in zip(self.network[0], inputs)]

        # Remaining layers each get all outputs from previous layers
        for layer in self.network[1:]:
            outputs = [p.guess(outputs) for p in layer]

        return outputs

    def copyNetwork(self):
        weights = []
        for layer in self.network:
            weights.append([p.getWeights() for p in layer])

        return weights

    def mutate(self):
        for layer in self.network:
            for p in layer:
                for i, w in enumerate(p.weights):
                    if random.random() < 0.01:
                        #                        offset = random.uniform(-0.01, 0.01)
                        #                        p.weights[i] += offset
                        #                        p.weights[i] = min(p.weights[i], 1)
                        #                        p.weights[i] = max(p.weights[i], -1)
                        p.weights[i] = random.uniform(-1, 1)


class Perceptron:
    def __init__(self, numInputs=0, weights=None):
        if weights is None:
            self.weights = [random.uniform(-1, 1) for _ in range(numInputs + 1)]
        else:
            self.weights = weights
        self.bias = self.weights.pop()

    def guess(self, inputs):
        assert len(inputs) == len(self.weights)
        agg = sum(x * y for x, y in zip(inputs, self.weights)) + self.bias
        return self.activation(agg)

    def activation(self, x):
        return rangeMap(x, -len(self.weights) - 1, len(self.weights) + 1, 0, 1)

    def getWeights(self):
        return self.weights + [
            self.bias,
        ]
