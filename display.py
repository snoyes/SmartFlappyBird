import pygame

width = 800
height = 600

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)


display = font = None
generation = 0
frame = 0


def setupDisplay():
    global display, font
    display = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont(None, 24)


def drawRect(r):
    pygame.draw.rect(display, WHITE, r)


path = "images/"
filename = "frame-%d.png"
birdFrames = [pygame.image.load(path + (filename % i)) for i in range(1, 9)]
birdRect = birdFrames[0].get_rect()


def drawBird(pos, vision, seed=None):
    global frame
    # pygame.draw.circle(display, WHITE, pos, width // 100)
    # for v in vision:
    # pygame.draw.line(display, (30, 30, 30), pos, v)
    sprite = birdFrames[(frame + seed) % 8]
    birdRect.center = pos
    display.blit(sprite, birdRect)


def drawScore():
    img = font.render(f"Generation {generation}", True, WHITE)
    display.blit(img, (20, 20))

    score = frame // 30
    img = font.render(f"Distance {score}", True, WHITE)
    display.blit(img, (20, 40))


def updateDisplay():
    global frame
    pygame.display.update()
    frame += 1


def reset():
    display.fill(BLACK)
