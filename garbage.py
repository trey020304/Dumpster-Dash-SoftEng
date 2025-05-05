import pygame

class Garbage(pygame.sprite.Sprite):
    def __init__(self, image, x, y, resources):
        pygame.sprite.Sprite.__init__(self)
        image_scale = 60 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class BioGarbage(Garbage):
    pass

class NonBioGarbage(Garbage):
    pass