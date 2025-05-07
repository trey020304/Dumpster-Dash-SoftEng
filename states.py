import pygame
import random
import sys
from runner import Bio, NonBio
from garbage import BioGarbage, NonBioGarbage, Obstacle
from firebase import HighScoreDB, LeaderBoardDB

current_player_HS = HighScoreDB
leaderboard_db = LeaderBoardDB
uid = 'lyBQ8JNZn3UXdAXQYto6GhczkbJ2'

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
        self.game = game_instance
        # Reset background position when menu loads
        resources['b_pos'] = 0
        resources['o_pos'] = 720
        self.play_button = resources['play_button_img'].get_rect(center=(250, 466))
        self.exit_button = resources['quit_button_img'].get_rect(center=(416, 625))
        self.logout_button = resources['logout_button_img'].get_rect(center=(84, 625))
        self.leaderboard_button = resources['leaderboard_button_img'].get_rect(center=(250, 625))
        self.menu_logo = Logo(250, 200, resources['menu_logo_img'])
        

    def handle_events(self, event, switch_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            print(f"Mouse click at: {mouse_pos}")  # Debug print
            
            if self.play_button.collidepoint(mouse_pos):
                print("Play button clicked")
                self.game.reset_game()
                switch_state("Game")
            elif self.leaderboard_button.collidepoint(mouse_pos):
                print("Leaderboard button clicked")
                switch_state("Leaderboard")
            elif self.exit_button.collidepoint(mouse_pos):
                print("Exit button clicked")
                pygame.quit()
                sys.exit()
            else:
                print("Clicked somewhere else")

    def update(self):
        pass

    def draw(self, screen):
        self.menu_logo.draw(screen)
        screen.blit(self.resources['play_button_img'], self.play_button)
        screen.blit(self.resources['quit_button_img'], self.exit_button)
        screen.blit(self.resources['logout_button_img'], self.logout_button)
        screen.blit(self.resources['leaderboard_button_img'], self.leaderboard_button)

class Leaderboard:
    def __init__(self, resources, game_instance):
        self.resources = resources
        self.game = game_instance
        self.back_button = resources['back_button_img'].get_rect(center=(440, 60))
        self.font_large = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.font_medium = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.font_small = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.leaderboard_data = self.fetch_leaderboard_data()
        
    def fetch_leaderboard_data(self):
        firebase_data = LeaderBoardDB.get_leaderboard_from_DB()
        
        firebase_data.sort(key=lambda x: x["highscore"], reverse=True)
        trimmed = firebase_data[:10]

        return [{"name": entry.get("username", "-"), "score": entry.get("highscore", 0)} for entry in trimmed]

    def handle_events(self, event, switch_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                switch_state("MainMenu")

    def update(self):
        pass

    def draw(self, screen):
        # Draw leaderboard background
        screen.blit(self.resources['leaderboard_img'], (47, -37))
        
        # Draw column headers
        rank_header = self.font_small.render("RANK", True, (255, 255, 255))
        name_header = self.font_small.render("NAME", True, (255, 255, 255))
        score_header = self.font_small.render("SCORE", True, (255, 255, 255))
        
        screen.blit(rank_header, (92.5, 142.5))
        screen.blit(name_header, (167.5, 142.5))
        screen.blit(score_header, (340, 142.5))
        
        # Draw leaderboard entries
        for i in range(10):  # Always show 10 ranks
            entry = self.leaderboard_data[i] if i < len(self.leaderboard_data) else {"name": "-", "score": '-'}
            y_pos = 172 + i * 48.5
            
            # Rank
            rank = self.font_small.render(f"{i+1}.", True, (255, 255, 255))
            screen.blit(rank, (95, y_pos))
            
            # Name
            name = self.font_small.render(entry['name'], True, (255, 255, 255))
            screen.blit(name, (167.5, y_pos))
            
            # Score
            score = self.font_small.render(str(entry['score']), True, (255, 255, 255))
            screen.blit(score, (340, y_pos))
        
        # Draw back button
        screen.blit(self.resources['back_button_img'], self.back_button)

class Game:
    def __init__(self, resources):
        self.resources = resources
        self.highest_score = current_player_HS.getCurrentPlayerHighScore(uid)
        self.reset_game()

    def reset_game(self):
        """Reset all game state variables for a new game"""
        self.score = 0
        self.last_score = 0
        self.health = 3  # Moved health here to be shared
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.increment_timer = 0
        self.speed = self.resources['game_speed']
        self.resources['scroll_pos'] = 0
        self.resources['b_pos'] = 0
        self.resources['o_pos'] = 720
        self.active_wally = Bio(250, 575, self.resources, self)
        self.prev_wally_position = self.active_wally.rect.center
        self.wally1 = self.active_wally
        self.wally2 = NonBio(250, 575, self.resources, self)
        self.garbage_group = pygame.sprite.Group()
        self.dead = False
        self.death_timer = None
        self.death_delay = 1500

    def handle_events(self, event, switch_state):
        if self.dead:  # Don't process any movement or switching controls if dead
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                switch_state("MainMenu")
            return
            
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

    # states.py (Game class update method)
    def update(self, switch_state):
        # Check if runner just died
        if self.active_wally.just_died:
            self.dead = True
            self.death_timer = pygame.time.get_ticks()
            self.last_score = self.score
            if self.score > self.highest_score:
                self.highest_score = self.score
                current_player_HS.updateCurrentPlayerHighScore(uid ,self.score)
            self.resources['game_over_sound'].play()
        
        # If dead, wait for death animation to finish
        if self.dead:
            self.active_wally.update(self.garbage_group)
            if pygame.time.get_ticks() - self.death_timer >= self.death_delay:
                switch_state("GameOver")
            return
        
        # Normal game update
        self.active_wally.update(self.garbage_group)

        # Add new garbage if needed
        if len(self.garbage_group) < 3:
            add_garbage = True
            for garbage in self.garbage_group:
                if garbage.rect.top < garbage.rect.height * 1:
                    add_garbage = False
            if add_garbage:
                self.create_garbage()

        # Move garbage and remove if off-screen
        for garbage in list(self.garbage_group):
            garbage.rect.y += self.speed
            if garbage.rect.top >= self.resources['height']:
                garbage.kill()

        # Check for correct matches (only for scoring)
        for garbage in list(self.garbage_group):
            if self.active_wally.rect.colliderect(garbage.rect):
                if ((isinstance(self.active_wally, Bio) and isinstance(garbage, BioGarbage)) or 
                    (isinstance(self.active_wally, NonBio) and isinstance(garbage, NonBioGarbage))):
                    self.score += 1
                    self.increment_timer += 1
                    self.resources['get_item_sound'].play()
                    garbage.kill()
                    break

        # Increase speed periodically
        if self.increment_timer >= 5:
            self.speed += 0.75
            self.increment_timer = 0

    # In states.py, modify the create_garbage method in the Game class:
    def create_garbage(self):
        lane = random.choice(self.resources['objectlanes'])
        # 20% chance to spawn an obstacle, 80% chance to spawn regular garbage
        garbage_type = random.choices(
            [Obstacle, BioGarbage, NonBioGarbage],
            weights=[0.2, 0.4, 0.4]
        )[0]
        
        if garbage_type == Obstacle:
            image = random.choice(self.resources['obstacle_images'])
        else:
            image = random.choice(
                self.resources['biodegradable_images'] if garbage_type == BioGarbage 
                else self.resources['nonbiodegradable_images']
            )
        
        garbage = garbage_type(image, lane, -self.resources['height'] / 2, self.resources)
        garbage.rect.center = (lane, -self.resources['height'] / 2)
        self.garbage_group.add(garbage)

    # states.py (Game class draw method)
    def draw(self, screen):
        self.active_wally.draw(screen)
        font = self.font
            
        # Score display
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_text, (200, 63))
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (200, 60))
        
        # Health display using shared health
        health_text = font.render(f'Health: {self.health}', True, (0, 0, 0))
        screen.blit(health_text, (30, 63))
        health_text = font.render(f'Health: {self.health}', True, (255, 255, 255))
        screen.blit(health_text, (30, 60))
        
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