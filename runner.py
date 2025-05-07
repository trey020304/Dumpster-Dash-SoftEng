# runner.py
import pygame
from garbage import BioGarbage, NonBioGarbage, Obstacle

class Runner(pygame.sprite.Sprite):
    def __init__(self, x, y, run_animation_list, death_animation, game_instance):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.dead = False
        self.game = game_instance  # Reference to the Game instance
        self.run_animation = run_animation_list
        self.death_animation = death_animation
        self.current_animation = self.run_animation
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.current_animation[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.invincible = False
        self.invincible_timer = 0
        self.just_died = False

    def update(self, garbage_group):
        animation_cooldown = 30
        now = pygame.time.get_ticks()
        
        if self.just_died:
            self.just_died = False
            
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        if not self.dead and not self.invincible and not self.game.dead:
            collisions = pygame.sprite.spritecollide(self, garbage_group, False)
            for garbage in collisions:
                # Handle obstacle collision (new code)
                if isinstance(garbage, Obstacle):
                    self.game.resources['wrong_bin_sound'].play()
                    self.take_damage()
                    garbage.kill()
                    break
                    
                # Existing garbage collision handling
                wrong_collision = (
                    (isinstance(self, Bio) and isinstance(garbage, NonBioGarbage)) or 
                    (isinstance(self, NonBio) and isinstance(garbage, BioGarbage)))
                
                if wrong_collision:
                    self.game.resources['wrong_bin_sound'].play()
                    self.take_damage()
                    garbage.kill()
                    break

        if now - self.update_time > animation_cooldown:
            self.update_time = now
            self.frame_index += 1
            if self.frame_index >= len(self.current_animation):
                if self.dead:
                    self.frame_index = len(self.current_animation) - 1 
                else:
                    self.frame_index = 0

        self.image = self.current_animation[self.frame_index]

    def take_damage(self):
        self.game.health -= 1  # Modify the shared health
        self.invincible = True
        self.invincible_timer = 30
        if self.game.health <= 0:
            self.dead = True
            self.game.dead = True
            self.just_died = True
            self.current_animation = self.death_animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bio(Runner):
    def __init__(self, x, y, resources, game_instance):
        run_animation = resources['bio_animation']
        death_animation = resources['death_animation']
        super().__init__(x, y, run_animation, death_animation, game_instance)

class NonBio(Runner):
    def __init__(self, x, y, resources, game_instance):
        run_animation = resources['nonbio_animation']
        death_animation = resources['death_animation']
        super().__init__(x, y, run_animation, death_animation, game_instance)