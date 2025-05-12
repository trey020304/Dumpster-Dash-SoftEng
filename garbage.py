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

    @classmethod
    def load_images(cls, filenames):
        return [pygame.image.load('assets/obstacles/' + fn) for fn in filenames]

class BioGarbage(Garbage):
    filenames = ['banana.png', 'milk carton.png', 'box.png', 'leaf.png', 'poop.png', 
                'log.png', 'book.png', 'apple.png', 'meat.png', 'fish bone.png']
    
    @classmethod
    def get_images(cls):
        return cls.load_images(cls.filenames)

class NonBioGarbage(Garbage):
    filenames = ['plastic bag.png', 'coke.png', 'bottle.png', 'battery.png', 
                'light bulb.png', 'phone.png', 'laptop.png', 'can.png', 'soda.png', 'flask.png']
    
    @classmethod
    def get_images(cls):
        return cls.load_images(cls.filenames)
   
class Obstacle(Garbage):
    filenames = ['puddle.png', 'road barricade.png', 'traffic cone.png']
    
    @classmethod
    def get_images(cls):
        return cls.load_images(cls.filenames)