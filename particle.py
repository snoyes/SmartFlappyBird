import pygame


class Particle:
    def __init__(self):
        self.pos = pygame.math.Vector2()
        self.vel = pygame.math.Vector2()
        self.acc = pygame.math.Vector2()

        self.maxVelocity = 10

    def applyForce(self, v):
        self.acc += v

    def doPhysics(self):
        self.vel += self.acc
        if self.vel.length() != 0:
            self.vel.scale_to_length(min(self.vel.length(), self.maxVelocity))
        self.pos += self.vel

        self.acc *= 0

    def moveTo(self, pos):
        self.pos = pos
