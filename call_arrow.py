import pygame
from arrows import arrow, arrow_white

WHITE = (255,255,255)
BLACK = (0,0,0)
SALMON = (253,171,159)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape Room")

exit = False
running = True

a1w = arrow_white((250, 500), "right arrow white.png")
a2w = arrow_white((350, 500), "left arrow white.png")
a3w = arrow_white((450, 500), "up arrow white.png")
a4w = arrow_white((550, 500), "down arrow white.png")

a1 = arrow((250, 25), "right arrow pink.png")
a2 = arrow((350, 25), "left arrow pink.png")
a3 = arrow((450, 25), "up arrow blue.png")
a4 = arrow((550, 25), "down arrow blue.png")

arrowGrayList = [a1w, a2w, a3w, a4w]
arrowList = [a1, a2, a3, a4]
allArrows = pygame.sprite.Group()

millisecondsDelay = 1000 # 1 sec- this is the starting delay!!!
arrowTimerEvent = pygame.USEREVENT + 1
pygame.time.set_timer(arrowTimerEvent, millisecondsDelay)
spawned = 0

clock = pygame.time.Clock()

while running:
    clock.tick()

    #Update
    allArrows.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == arrowTimerEvent:
            if spawned < len(arrowList):
                allArrows.add(arrowGrayList[spawned])
                allArrows.add(arrowList[spawned])
                spawned += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if pygame.sprite.collide_rect(a1, a1w):
            a1.rect.center = (900, 600)
    if keys[pygame.K_LEFT]:
        if pygame.sprite.collide_rect(a2, a2w):
            a2.rect.center = (900, 600)
    if keys[pygame.K_UP]:
        if pygame.sprite.collide_rect(a3, a3w):
            a3.rect.center = (900, 600)
    if keys[pygame.K_DOWN]:
        if pygame.sprite.collide_rect(a4, a4w):
            a4.rect.center = (900, 600)
    #draw
    screen.fill(SALMON)
    allArrows.draw(screen)

    pygame.display.flip()

pygame.quit()