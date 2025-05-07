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
    filenames = ['banana peel.png', 'milk carton.png', 'box.png', 'Leaves.png', 'Poop.png', 
                'Log.png', 'Book.png', 'Apple.png', 'Meat.png', 'Fishbone.png']
    
    @classmethod
    def get_images(cls):
        return cls.load_images(cls.filenames)

class NonBioGarbage(Garbage):
    filenames = ['plastic bag.png', 'soda bottle.png', 'water bottle.png', 'Battery.png', 
                'Lightbulb.png', 'Phone.png', 'Laptop.png', 'Can.png', 'Soda.png', 'Glass.png']
    
    @classmethod
    def get_images(cls):
        return cls.load_images(cls.filenames)
   
class Obstacle(Garbage):
    filenames = ['puddle.png', 'road barricade.png', 'traffic cone.png']
    
    @classmethod
    def get_images(cls):
        return cls.load_images(cls.filenames)