import display
import pygame
from pygame.math import Vector2
from particle import Particle
from neural import NeuralNetwork
import random
import copy
import pickle

gravity = Vector2(0, 1)


class Flock:
    def __init__(self):
        self.livingBirds = []
        self.deadBirds = []

    def update(self, pipes):
        for bird in self.livingBirds:
            bird.update(pipes)

        self.checkCollisions(pipes)

        self.deadBirds.extend([bird for bird in self.livingBirds if bird.isDead()])
        self.livingBirds = [bird for bird in self.livingBirds if not bird.isDead()]
        if len(self.livingBirds) == 0:
            self.hatchBirds()
            pipes.reset()

    def reset(self):
        for bird in self.livingBirds:
            bird.kill()

    def hatchBirds(self):
        display.generation += 1
        display.frame = 0
        for _ in range(500):
            if len(self.deadBirds) == 0:
                chick = Bird()
            else:
                parent = random.choices(
                    self.deadBirds, weights=[b.fitness for b in self.deadBirds]
                ).pop()
                parentBrain = parent.getBrain()
                chickBrain = NeuralNetwork(weights=parentBrain)
                chickBrain.mutate()
                chick = Bird(brain=chickBrain)

            self.livingBirds.append(chick)

        self.deadBirds = []

    def draw(self):
        for bird in self.livingBirds:
            bird.draw()

    def jump(self):
        for bird in self.livingBirds:
            bird.jump()

    def checkCollisions(self, pipes):

        for bird in self.livingBirds:
            birdPos = bird.getPosition()
            if bird.offScreen():
                bird.kill()
            if bird.collide(pipes.getRects()):
                bird.kill()

    def saveBest(self):
        self.livingBirds.sort(reverse=True, key=lambda bird: bird.fitness)
        if len(self.livingBirds) > 0:
            for bird in self.livingBirds:
                with open("birdbrain.pickle", "wb") as f:
                    pickle.dump(bird.getBrain(), f, pickle.HIGHEST_PROTOCOL)

    def loadBest(self):
        self.livingBirds = []
        with open("birdbrain.pickle", "rb") as f:
            trainedNet = pickle.load(f)
            chickBrain = NeuralNetwork(weights=trainedNet)
            chick = Bird(brain=chickBrain)
            self.livingBirds.append(chick)


class Bird(Particle):
    def __init__(self, brain=None):
        super().__init__()
        xRandom = random.uniform(0.09, 0.14)
        self.moveTo(Vector2(display.width * xRandom, display.height // 2))
        if brain is None:
            self.brain = NeuralNetwork(6, 10, 1)
        else:
            self.brain = brain
        self.alive = True
        self.vision = []
        self.fitness = 0
        self.seed = random.randint(0, 7)

    def getBrain(self):
        return self.brain.copyNetwork()

    def getPosition(self):
        return self.pos

    def update(self, pipes):
        self.applyForce(gravity)
        self.think(pipes)
        self.doPhysics()
        if self.alive:
            self.fitness += 1

    def think(self, pipes):
        inputs = [self.pos.y / display.height, self.vel.y / self.maxVelocity]

        self.vision = self.perceive(pipes)
        for v in self.vision:
            inputs.append(v.x / display.width)
            inputs.append(v.y / display.height)
            # inputs.append(self.pos.angle_to(v) / 360)

        while len(inputs) < 4:
            inputs.append(0)

        predictions = self.brain.predict(inputs)
        prediction = predictions.pop()
        if prediction > 0.50:
            self.jump()

    def perceive(self, pipescollection):
        # for now, I'll just look at the bottom left of pipe[0] and top left of pipe[1]
        # TODO: look at the next pipe in the future
        seen = []
        pipes = pipescollection.getPipes()
        if len(pipes) > 0:
            seen.append(Vector2(pipes[0].getRect().bottomleft))
        if len(pipes) > 1:
            seen.append(Vector2(pipes[1].getRect().topleft))
        return seen

    def draw(self):
        display.drawBird(self.pos, self.vision, seed=self.seed)

    def kill(self):
        self.alive = False

    def isDead(self):
        return not self.alive

    def offScreen(self):
        return self.pos.y < 0 or self.pos.y > display.height

    def collide(self, pipeRects):
        birdRect = display.birdRect
        birdRect.center = self.pos
        return birdRect.collidelist(pipeRects) > -1

    def jump(self):
        self.applyForce(Vector2(0, -30))
