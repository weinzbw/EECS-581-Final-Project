import pygame



WHITE = (255,255,255)
BLACK = (0,0,0)
SALMON = (253,171,159)
HEIGHT = 100
WIDTH = 90

class arrow_white(pygame.sprite.Sprite):

    def __init__(self, pos, imagename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, (HEIGHT, WIDTH))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = pos

class arrow(pygame.sprite.Sprite):

    def __init__(self, pos, imagename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, (HEIGHT, WIDTH))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self): # THIS IS WHAT MAKES THE ARROWS MOVE
        self.rect.y += 1
        if (self.rect.top > (HEIGHT + 800)):
            self.rect.bottom = 0

