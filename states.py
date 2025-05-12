import pygame
import random
import sys
from runner import Bio, NonBio
from garbage import BioGarbage, NonBioGarbage, Obstacle
from firebase import HighScoreDB, LeaderBoardDB, Authorization
import firebase

current_player_HS = HighScoreDB
leaderboard_db = LeaderBoardDB
auth = Authorization
uid = firebase.load_session()

class Logo:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Login:
    def __init__(self, resources, game_instance):
        self.resources = resources  # Store resources as instance variable
        self.game = game_instance
        self.menu_logo = Logo(250, 250, resources['menu_logo_img'])
        self.activate_submit_button = ''
        self.reset_password_status = ''
        
        # Initialize all state variables
        self.show_login_form = False
        self.show_create_account = False
        self.show_forgot_password = False
        
        # Initialize fonts
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), 16)
        
        # Initialize text fields
        self.email_text = ""
        self.username_text = ""
        self.password_text = ""
        self.confirm_password_text = ""
        self.active_field = None
        
        # Notification system
        self.notification_text = ""
        self.notification_timer = 0
        self.notification_duration = 3000
        self.notification_color = (0, 255, 0)
        self.show_notification = False
        self.notification_rect = pygame.Rect(50, 30, 400, 30)
        
        # Create overlay
        self.overlay = pygame.Surface((500, 720), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        
        # Initialize all buttons here (only once)
        self._init_buttons()

    def _init_buttons(self):
        """Initialize all button rects once"""
        self.submit_button = self.resources['create_button_img'].get_rect(center=(250, 600))
        self.back_button_x = self.resources['back_button_img'].get_rect(center=(450, 100))
        self.login_button = self.resources['login_button_img'].get_rect(center=(380, 575))
        self.create_button = self.resources['create_button_img'].get_rect(center=(130, 575))

    def reset_state(self):
        """Reset only the form states, not the buttons"""
        self.show_login_form = False
        self.show_create_account = False
        self.show_forgot_password = False
        self.email_text = ""
        self.username_text = ""
        self.password_text = ""
        self.confirm_password_text = ""
        self.active_field = None
        
        # Create semi-transparent background surface
        self.overlay = pygame.Surface((500, 720), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  # Black with 180/255 opacity
        
        # Reuse existing buttons for forms
        self.submit_button = self.resources['create_button_img'].get_rect(center=(250, 600))  # Moved up for forgot password
        self.back_button_x = self.resources['back_button_img'].get_rect(center=(450, 100))

    def handle_events(self, event, switch_state):
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            mouse_pos = event.pos
            
            if not (self.show_login_form or self.show_create_account or self.show_forgot_password):
                # Main screen buttons
                if self.login_button.collidepoint(mouse_pos):
                    self.show_login_form = True
                elif self.create_button.collidepoint(mouse_pos):
                    self.show_create_account = True
            else:
                # Form screen buttons
                if self.back_button_x.collidepoint(mouse_pos):
                    self.show_login_form = False
                    self.show_create_account = False
                    self.show_forgot_password = False
                    self.reset_state()
                elif self.submit_button.collidepoint(mouse_pos):
                    if self.show_login_form:
                        # Add validation for empty fields
                        if not self.email_text or not self.password_text:
                            print("Please fill in all fields!")
                            self.show_notification_message('Please fill in all fields!', False)
                            switch_state("Login")
                            return
                        
                        global uid
                        uid = auth.login(self.email_text, self.password_text)
                        if uid in ('invalid_credentials', 'unknown_error'):
                            print("Invalid credentials!")
                            switch_state("Login")
                            self.show_notification_message('Invalid Credentials', False)
                        else:
                            switch_state("MainMenu")
                            print('Logging in...')
                            self.show_notification_message('Successful Login', False)

                    elif self.show_create_account:
                        self.activate_submit_button = auth.register(self.email_text, self.password_text, self.confirm_password_text, self.username_text)
                        if not self.email_text or not self.password_text or not self.confirm_password_text or not self.username_text:
                            print('Please fill in all fields.')
                            self.show_notification_message('Please fill in all fields.', False)
                        elif (self.activate_submit_button == ''):
                            print('Either invalid e-mail or not matching passwords')
                            self.show_notification_message('Invalid e-mail or unmatching passwords', False)
                        elif (self.activate_submit_button == 'already_registered'):
                            print('Email already associated with an account. Try again.')
                            self.show_notification_message('Email already registered.', False)
                        elif (self.activate_submit_button == 'success'):
                            switch_state("Login")
                            print('You have successfully registered. Please log in.')
                            self.show_notification_message('Successfully registered. Log in.', True)
                        else:
                            print('Registration failed for unknown reasons.')
                            self.show_notification_message('Registration failed. Try again.', False)
                    elif self.show_forgot_password:
                        self.reset_password_status = auth.reset_password(self.email_text)
                        if (self.reset_password_status == 'reset_email_sent'):
                            print('Reset email sent.')
                            self.show_forgot_password = False
                            self.show_login_form = True
                            switch_state("Login")
                        else:
                            print('That address is either invalid, not a verified primary email or is not associated with a personal user account.')
                
                # Field selection
                if self.show_login_form:
                    self.active_field = "login_email" if self.login_email_rect.collidepoint(mouse_pos) else \
                                      "login_password" if self.login_password_rect.collidepoint(mouse_pos) else None
                    # Check if forgot password was clicked
                    if self.forgot_password_rect.collidepoint(mouse_pos):
                        self.show_login_form = False
                        self.show_forgot_password = True
                elif self.show_create_account:
                    self.active_field = "email" if self.email_rect.collidepoint(mouse_pos) else \
                                      "username" if self.username_rect.collidepoint(mouse_pos) else \
                                      "password" if self.password_rect.collidepoint(mouse_pos) else \
                                      "confirm_password" if self.confirm_password_rect.collidepoint(mouse_pos) else None
                elif self.show_forgot_password:
                    self.active_field = "forgot_email" if self.forgot_email_rect.collidepoint(mouse_pos) else None
        
        # Handle text input
        if event.type == pygame.KEYDOWN and (self.show_login_form or self.show_create_account or self.show_forgot_password):
            if self.active_field == "login_email":
                if event.key == pygame.K_BACKSPACE:
                    self.email_text = self.email_text[:-1]
                else:
                    self.email_text += event.unicode
            elif self.active_field == "login_password":
                if event.key == pygame.K_BACKSPACE:
                    self.password_text = self.password_text[:-1]
                else:
                    self.password_text += event.unicode
            elif self.active_field == "email":
                if event.key == pygame.K_BACKSPACE:
                    self.email_text = self.email_text[:-1]
                else:
                    self.email_text += event.unicode
            elif self.active_field == "username":
                if event.key == pygame.K_BACKSPACE:
                    self.username_text = self.username_text[:-1]
                else:
                    self.username_text += event.unicode
            elif self.active_field == "password":
                if event.key == pygame.K_BACKSPACE:
                    self.password_text = self.password_text[:-1]
                else:
                    self.password_text += event.unicode
            elif self.active_field == "confirm_password":
                if event.key == pygame.K_BACKSPACE:
                    self.confirm_password_text = self.confirm_password_text[:-1]
                else:
                    self.confirm_password_text += event.unicode
            elif self.active_field == "forgot_email":
                if event.key == pygame.K_BACKSPACE:
                    self.email_text = self.email_text[:-1]
                else:
                    self.email_text += event.unicode

    def update(self):
        # Define rectangles for text fields
        field_width = 200
        field_x = 250
        
        # Login form fields
        self.login_email_rect = pygame.Rect(field_x, 242.5, field_width, 32)
        self.login_password_rect = pygame.Rect(field_x, 292.5, field_width, 32)
        
        # Create account form fields
        self.email_rect = pygame.Rect(field_x, 242.5, field_width, 32)
        self.username_rect = pygame.Rect(field_x, 292.5, field_width, 32)
        self.password_rect = pygame.Rect(field_x, 342.5, field_width, 32)
        self.confirm_password_rect = pygame.Rect(field_x, 392.5, field_width, 32)
        
        # Forgot password field
        self.forgot_email_rect = pygame.Rect(field_x, 292.5, field_width, 32)
        
        # Forgot password text rect
        forgot_text = self.font.render("Forgot Password?", True, (100, 150, 255))
        self.forgot_password_rect = forgot_text.get_rect(center=(250, 350))

    def draw(self, screen):
        self.menu_logo.draw(screen)
        
        if not (self.show_login_form or self.show_create_account or self.show_forgot_password):
            # Draw main login screen
            screen.blit(self.resources['login_button_img'], self.login_button)
            screen.blit(self.resources['create_button_img'], self.create_button)
        else:
            # Draw semi-transparent overlay
            screen.blit(self.overlay, (0, 0))
            
            # Draw back button
            screen.blit(self.resources['back_button_img'], self.back_button_x)
            
            if self.show_notification:
                self._draw_notification(screen)

            if self.show_login_form:
                # Draw login form
                title = self.font.render("Login to Your Account", True, (255, 255, 255))
                screen.blit(title, (250 - title.get_width()//2, 180))
                
                # Labels
                email_label = self.font.render("Email:", True, (255, 255, 255))
                password_label = self.font.render("Password:", True, (255, 255, 255))
                screen.blit(email_label, (50, 250))
                screen.blit(password_label, (50, 300))
                
                # Input fields
                pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "login_email" else (200, 200, 200), 
                                self.login_email_rect, 2)
                pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "login_password" else (200, 200, 200), 
                                self.login_password_rect, 2)
                
                # Text
                email_surface = self._render_text_with_clipping(self.email_text, self.email_rect)
                password_surface = self._render_text_with_clipping("*" * len(self.password_text), self.password_rect)
                screen.blit(email_surface, (self.login_email_rect.x + 5, self.login_email_rect.y + 5))
                screen.blit(password_surface, (self.login_password_rect.x + 5, self.login_password_rect.y + 5))
                
                # Forgot password text
                forgot_text = self.small_font.render("Forgot Password?", True, (100, 150, 255))
                screen.blit(forgot_text, (250 - forgot_text.get_width()//2, 350))
                # Underline
                pygame.draw.line(screen, (100, 150, 255), 
                               (self.forgot_password_rect.left, self.forgot_password_rect.bottom),
                               (self.forgot_password_rect.right, self.forgot_password_rect.bottom), 1)
                
                # Submit button
                screen.blit(self.resources['login_button_img'], self.submit_button)
                
            elif self.show_create_account:
                # Draw create account form
                title = self.font.render("Create New Account", True, (255, 255, 255))
                screen.blit(title, (250 - title.get_width()//2, 180))
                
                # Labels
                email_label = self.font.render("Email:", True, (255, 255, 255))
                username_label = self.font.render("Username:", True, (255, 255, 255))
                password_label = self.font.render("Password:", True, (255, 255, 255))
                confirm_label = self.font.render("Confirm Password:", True, (255, 255, 255))
                
                screen.blit(email_label, (50, 250))
                screen.blit(username_label, (50, 300))
                screen.blit(password_label, (50, 350))
                screen.blit(confirm_label, (50, 400))
                
                # Input fields
                pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "email" else (200, 200, 200), 
                                self.email_rect, 2)
                pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "username" else (200, 200, 200), 
                                self.username_rect, 2)
                pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "password" else (200, 200, 200), 
                                self.password_rect, 2)
                pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "confirm_password" else (200, 200, 200), 
                                self.confirm_password_rect, 2)
                
                # Text
                email_surface = self._render_text_with_clipping(self.email_text, self.email_rect)
                username_surface = self._render_text_with_clipping(self.username_text, self.username_rect)
                password_surface = self._render_text_with_clipping("*" * len(self.password_text), self.password_rect)
                confirm_surface = self._render_text_with_clipping("*" * len(self.confirm_password_text), self.confirm_password_rect)
                
                screen.blit(email_surface, (self.email_rect.x + 5, self.email_rect.y + 5))
                screen.blit(username_surface, (self.username_rect.x + 5, self.username_rect.y + 5))
                screen.blit(password_surface, (self.password_rect.x + 5, self.password_rect.y + 5))
                screen.blit(confirm_surface, (self.confirm_password_rect.x + 5, self.confirm_password_rect.y + 5))
                
                # Submit button
                screen.blit(self.resources['create_button_img'], self.submit_button)
                
            elif self.show_forgot_password:
                # Draw forgot password form
                title = self.font.render("Reset Password", True, (255, 255, 255))
                screen.blit(title, (250 - title.get_width()//2, 180))
                
                instructions = self.small_font.render("Enter your email to receive a reset link", True, (255, 255, 255))
                screen.blit(instructions, (250 - instructions.get_width()//2, 230))
                
                # Label
                email_label = self.font.render("Email:", True, (255, 255, 255))
                screen.blit(email_label, (50, 300))
                
                # Input field
                pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "forgot_email" else (200, 200, 200), 
                                self.forgot_email_rect, 2)
                
                # Text
                email_surface = self._render_text_with_clipping(self.email_text, self.email_rect)
                screen.blit(email_surface, (self.forgot_email_rect.x + 5, self.forgot_email_rect.y + 5))
                
                # Only show the submit button (no login button)
                submit_text = self.font.render("Send Reset Link", True, (255, 255, 255))
                screen.blit(submit_text, (self.submit_button.x + 20, self.submit_button.y + 10))
    
    def show_notification_message(self, message, is_success):
        """Show a notification message"""
        self.notification_text = message
        self.notification_color = (0, 200, 0) if is_success else (200, 0, 0)
        self.show_notification = True
        self.notification_timer = pygame.time.get_ticks()

    def _draw_notification(self, screen):
        """Draw notification popup with perfect positioning"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.notification_timer

        if elapsed >= self.notification_duration:
            self.show_notification = False
            return
            

    # Calculate fade effect (last 500ms)
        alpha = min(255, 255 * (1 - max(0, elapsed - (self.notification_duration - 500)) / 500))

    # Create notification surface
        notification = pygame.Surface((self.notification_rect.width, self.notification_rect.height), pygame.SRCALPHA)

    # Background with rounded corners
        pygame.draw.rect(notification, (*self.notification_color, alpha), 
                        (0, 0, self.notification_rect.width, self.notification_rect.height),
                        border_radius=8)
        pygame.draw.rect(notification, (255, 255, 255, alpha),
                        (0, 0, self.notification_rect.width, self.notification_rect.height),
                        2, border_radius=8)

    # Text (centered)
        text = self.font.render(self.notification_text, True, (255, 255, 255, alpha))
        text_rect = text.get_rect(center=(self.notification_rect.width//2, self.notification_rect.height//2))
        notification.blit(text, text_rect)

        screen.blit(notification, self.notification_rect)

    def _render_text_with_clipping(self, text, rect):
        """Render text with perfect alignment and right-side clipping"""
        text_surface = self.font.render(text, True, (255, 255, 255))
        if text_surface.get_width() <= rect.width - 10:
            return text_surface
        
        # Create clipped surface showing rightmost portion of text
        clipped = pygame.Surface((rect.width - 10, rect.height - 5), pygame.SRCALPHA)
        clipped.blit(text_surface, (rect.width - 10 - text_surface.get_width(), 0))
        return clipped


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
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            mouse_pos = event.pos
            
            if self.play_button.collidepoint(mouse_pos):
                print("Play button clicked")
                self.game.reset_game()
                switch_state("Game")
            elif self.leaderboard_button.collidepoint(mouse_pos):
                print("Leaderboard button clicked")
                lb = Leaderboard(self.resources, self.game)
                lb.refresh()
                switch_state("Leaderboard")
            elif self.logout_button.collidepoint(mouse_pos):
                auth.logout()
                print("Logout button clicked")
                switch_state("Login", reset_login=True)
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
        self.leaderboard_data = []  # Initialize empty, to be filled on refresh

    def refresh(self):
        self.leaderboard_data = self.fetch_leaderboard_data()

    def fetch_leaderboard_data(self):
        firebase_data = LeaderBoardDB.get_leaderboard_from_DB()
        firebase_data.sort(key=lambda x: x["highscore"], reverse=True)
        trimmed = firebase_data[:10]
        return [{"name": entry.get("username", "-"), "score": entry.get("highscore", 0)} for entry in trimmed]


    def handle_events(self, event, switch_state):
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if self.back_button.collidepoint(event.pos):
                switch_state("MainMenu")

    def update(self):
        pass

    def draw(self, screen):
        self.refresh()
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

    def draw(self, screen):
        self.active_wally.draw(screen)
        font = self.font
            
        # Score display (unchanged)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_text, (200, 63))
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (200, 60))
        
        # Health display using heart images
        heart_x = 30
        heart_y = 60
        heart_spacing = 40  # Space between hearts
        
        # Determine which heart image to show based on health
        if self.health == 3:
            heart_img = self.resources['heart_3_img']
        elif self.health == 2:
            heart_img = self.resources['heart_2_img']
        elif self.health == 1:
            heart_img = self.resources['heart_1_img']
        else:  # health <= 0
            heart_img = self.resources['heart_0_img']
        
        # Draw the heart image
        screen.blit(heart_img, (heart_x, heart_y))
        
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
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
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