import pygame

class Arrow(pygame.sprite.Sprite):

    def __init__(self, pos, imagename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        self.rect.x += 5
        if (self.rect.left > (WIDTH + 50)):
            self.rect.right = 0