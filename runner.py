import pygame

class Runner(pygame.sprite.Sprite):
    def __init__(self, x, y, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, garbage_group):
        animation_cooldown = 20
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        if pygame.sprite.spritecollide(self, garbage_group, False):
            if (isinstance(self, Bio)) and any(isinstance(garbage, NonBio) for garbage in pygame.sprite.spritecollide(self, garbage_group, False)) or (
                    isinstance(self, NonBio)) and any(isinstance(garbage, Bio) for garbage in pygame.sprite.spritecollide(self, garbage_group, False)):
                return True

        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bio(Runner):
    def __init__(self, x, y, resources):
        animation_list = []
        for i in range(16):
            img = resources['bio_animation'][i]
            animation_list.append(img)
        super().__init__(x, y, animation_list)

class NonBio(Runner):
    def __init__(self, x, y, resources):
        animation_list = []
        for i in range(16):
            img = resources['nonbio_animation'][i]
            animation_list.append(img)
        super().__init__(x, y, animation_list)