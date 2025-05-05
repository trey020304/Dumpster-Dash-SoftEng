import pygame
import random
import sys
from runner import Bio, NonBio
from garbage import BioGarbage, NonBioGarbage

class Logo:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class MainMenu:
    def __init__(self, resources, game_instance):
        self.resources = resources
        self.game = game_instance  # Reference to the Game instance
        self.play_button = resources['play_button_img'].get_rect(center=(250, 500))
        self.exit_button = resources['quit_button_img'].get_rect(center=(250, 600))
        self.menu_logo = Logo(250, 200, resources['menu_logo_img'])

    def handle_events(self, event, switch_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                self.game.reset_game()  # Reset game state before starting
                switch_state("Game")
            elif self.exit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def draw(self, screen):
        self.menu_logo.draw(screen)
        screen.blit(self.resources['play_button_img'], self.play_button)
        screen.blit(self.resources['quit_button_img'], self.exit_button)

class Game:
    def __init__(self, resources):
        self.resources = resources
        self.highest_score = 0  # Persistent across games
        self.reset_game()

    def reset_game(self):
        """Reset all game state variables for a new game"""
        self.score = 0
        self.last_score = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.increment_timer = 0
        self.speed = 7
        self.active_wally = Bio(250, 575, self.resources)
        self.prev_wally_position = self.active_wally.rect.center
        self.wally1 = self.active_wally
        self.wally2 = NonBio(250, 575, self.resources)
        self.garbage_group = pygame.sprite.Group()

    def handle_events(self, event, switch_state):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.active_wally.rect.center[0] > self.resources['left_lane']:
                self.active_wally.rect.left -= 115
            elif event.key == pygame.K_RIGHT and self.active_wally.rect.center[0] < self.resources['right_lane']:
                self.active_wally.rect.left += 115
            elif event.key == pygame.K_q:
                self.prev_wally_position = self.active_wally.rect.center
                self.active_wally = self.wally1
                self.active_wally.rect.center = self.prev_wally_position
            elif event.key == pygame.K_e:
                self.prev_wally_position = self.active_wally.rect.center
                self.active_wally = self.wally2
                self.active_wally.rect.center = self.prev_wally_position
            elif event.key == pygame.K_ESCAPE:
                switch_state("MainMenu")

    def update(self, switch_state):
        self.active_wally.update(self.garbage_group)

        # Add new garbage if needed
        if len(self.garbage_group) < 3:
            add_garbage = True
            for garbage in self.garbage_group:
                if garbage.rect.top < garbage.rect.height * 1:
                    add_garbage = False
            if add_garbage:
                self.create_garbage()

        # Move garbage
        for garbage in self.garbage_group:
            garbage.rect.y += self.speed
            if garbage.rect.top >= self.resources['height']:
                garbage.kill()

        # Check collisions
        collisions = pygame.sprite.spritecollide(self.active_wally, self.garbage_group, True)
        for garbage in collisions:
            if ((isinstance(self.active_wally, Bio)) and (isinstance(garbage, NonBioGarbage)) or 
                (isinstance(self.active_wally, NonBio)) and isinstance(garbage, BioGarbage)):
                self.last_score = self.score
                if self.score > self.highest_score:
                    self.highest_score = self.score
                self.resources['game_over_sound'].play()
                pygame.time.wait(1500)
                switch_state("GameOver")
            else:
                self.resources['get_item_sound'].play()
                self.score += 1
                self.increment_timer += 1

        # Increase speed periodically
        if self.increment_timer >= 5:
            self.speed += 0.75
            self.increment_timer = 0

    def create_garbage(self):
        lane = random.choice(self.resources['objectlanes'])
        garbage_type = random.choice([BioGarbage, NonBioGarbage])
        image = random.choice(
            self.resources['biodegradable_images'] if garbage_type == BioGarbage 
            else self.resources['nonbiodegradable_images']
        )
        garbage = garbage_type(image, lane, -self.resources['height'] / 2, self.resources)
        garbage.rect.center = (lane, -self.resources['height'] / 2)
        self.garbage_group.add(garbage)

    def draw(self, screen):
        self.active_wally.draw(screen)
        font = self.font
        
        # Score display with outline
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_text, (200, 63))
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (200, 60))
        
        self.garbage_group.draw(screen)

class GameOver:
    def __init__(self, resources, game_instance):
        self.resources = resources
        self.game = game_instance
        self.restart_button = resources['restart_button_img'].get_rect(center=(250, 500))
        self.menu_button = resources['menu_button_img'].get_rect(center=(250, 600))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.rect = resources['game_over_img'].get_rect(center=(250, 200))

    def handle_events(self, event, switch_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                self.game.reset_game()
                switch_state("Game")
            elif self.menu_button.collidepoint(event.pos):
                switch_state("MainMenu")

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.resources['game_over_img'], (self.rect.x, self.rect.y))
        screen.blit(self.resources['restart_button_img'], self.restart_button)
        screen.blit(self.resources['menu_button_img'], self.menu_button)

        # Final score displays
        score_text = self.font.render(f'Score: {self.game.last_score}', True, (0, 0, 0))
        screen.blit(score_text, (200, 400))
        score_text = self.font.render(f'Score: {self.game.last_score}', True, (255, 255, 255))
        screen.blit(score_text, (200, 397))
        
        high_text = self.font.render(f'High Score: {self.game.highest_score}', True, (0, 0, 0))
        screen.blit(high_text, (166, 425))
        high_text = self.font.render(f'High Score: {self.game.highest_score}', True, (255, 255, 255))
        screen.blit(high_text, (166, 422))