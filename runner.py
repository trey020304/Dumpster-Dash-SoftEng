import pygame

class Runner(pygame.sprite.Sprite):
    def __init__(self, x, y, run_animation_list, death_animation):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.dead = False
        self.run_animation = run_animation_list
        self.death_animation = death_animation
        self.current_animation = self.run_animation
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.current_animation[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, garbage_group):
        animation_cooldown = 30
        now = pygame.time.get_ticks()
        
        #Check collision and switch to death animation
        if not self.dead and pygame.sprite.spritecollide(self, garbage_group, False):
            bad_collision = (
                isinstance(self, Bio) and any(isinstance(g, NonBio) for g in pygame.sprite.spritecollide(self, garbage_group, False))
            ) or (
                isinstance(self, NonBio) and any(isinstance(g, Bio) for g in pygame.sprite.spritecollide(self, garbage_group, False))
            )
            if bad_collision:
                self.dead = True
                self.current_animation = self.death_animation
                self.frame_index = 0
                self.update_time = now
        
        #Animate
        if now - self.update_time > animation_cooldown:
            self.update_time = now
            self.frame_index += 1
            if self.frame_index >= len(self.current_animation):
                if self.dead:
                    self.frame_index = len(self.current_animation) - 1 
                else:
                    self.frame_index = 0

        self.image = self.current_animation[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bio(Runner):
    def __init__(self, x, y, resources):
        run_animation = resources['bio_animation']
        death_animation = resources['death_animation']
        super().__init__(x, y, run_animation, death_animation)

class NonBio(Runner):
    def __init__(self, x, y, resources):
        run_animation = resources['nonbio_animation']
        death_animation = resources['death_animation']
        super().__init__(x, y, run_animation, death_animation)
