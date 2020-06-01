import pygame
import display
from bird import Flock
from pipe import Pipes


def handleInput():
    global running, flock, goFast
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            flock.jump()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            flock.saveBest()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            flock.loadBest()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
            flock.reset()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            goFast = not goFast


pygame.init()

pipes = Pipes()
flock = Flock()

display.setupDisplay()

clock = pygame.time.Clock()
goFast = False
running = True
while running:
    if not goFast:
        clock.tick(30)

    handleInput()
    display.reset()
    pipes.update()
    pipes.draw()
    flock.update(pipes)
    flock.draw()
    display.drawScore()
    display.updateDisplay()
