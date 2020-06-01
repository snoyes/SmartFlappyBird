import display
import pygame
from pygame.math import Vector2
from particle import Particle
import random


class Pipes:
    def __init__(self):
        self.pipes = []

    def addPipe(self):
        gapHeight = random.randrange(100, 300)
        gapPosition = random.randrange(1, display.height - gapHeight - 1)
        self.pipes.append(Pipe(0, gapPosition))
        self.pipes.append(Pipe(gapPosition + gapHeight, display.height - gapHeight))

    def update(self):
        for pipe in self.pipes:
            pipe.update()

        self.pipes = [pipe for pipe in self.pipes if not pipe.offScreen()]

        if not any(pipe.getRect().right > display.width * 0.6 for pipe in self.pipes):
            self.addPipe()

    def draw(self):
        for pipe in self.pipes:
            pipe.draw()

    def getRects(self):
        return [pipe.getRect() for pipe in self.pipes]

    def reset(self):
        self.pipes = []

    def getPipes(self):
        return self.pipes


class Pipe(Particle):
    def __init__(self, top, height, left=display.width, width=None):
        super().__init__()
        if width is None:
            width = display.width // 16
        self.width = width
        self.height = height
        self.moveTo(Vector2(left, top))
        self.applyForce(Vector2(-5, 0))

    def getRect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def update(self):
        self.doPhysics()

    def draw(self):
        display.drawRect(self.getRect())

    def offScreen(self):
        return self.pos.x < 0
