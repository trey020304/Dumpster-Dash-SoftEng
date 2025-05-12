import pygame
from pygame.locals import *
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
        self.resources = resources
        self.game = game_instance
        self.menu_logo = Logo(250, 250, resources['menu_logo_img'])
        
        # Notification system
        self.notification_text = ""
        self.notification_timer = 0
        self.notification_duration = 3000
        self.notification_color = (0, 255, 0)
        self.show_notification = False
        self.notification_rect = pygame.Rect(50, 30, 400, 30)
        
        # Form state management
        self.show_login_form = False
        self.show_create_account = False
        self.show_forgot_password = False
        self.email_text = ""
        self.username_text = ""
        self.password_text = ""
        self.confirm_password_text = ""
        self.active_field = None
        
        # UI positioning - ADDED ALL NECESSARY POSITIONING ATTRIBUTES
        self.title_y = 150
        self.label_x = 50
        self.field_x = 150
        self.field_width = 200
        self.field_height = 32
        self.login_email_label_y = 200  # Added this
        self.login_password_label_y = 250  # Added this
        
        # UI styling
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.overlay = pygame.Surface((500, 720), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        
        # Initialize UI components
        self._init_buttons()
        self._init_field_rects()

    def _init_buttons(self):
        """Initialize all button rectangles"""
        self.submit_button = pygame.Rect(150, 450, 200, 40)
        self.back_button = self.resources['back_button_img'].get_rect(center=(450, 100))
        self.login_button = self.resources['login_button_img'].get_rect(center=(380, 525))
        self.create_button = self.resources['create_button_img'].get_rect(center=(130, 525))
        self.exit_button = self.resources['quit_button_img'].get_rect(center=(250, 625))

    def _init_field_rects(self):
        """Initialize field rectangles with positions"""
        # Login form fields
        self.login_email_rect = pygame.Rect(self.field_x, self.login_email_label_y, self.field_width, self.field_height)
        self.login_password_rect = pygame.Rect(self.field_x, self.login_password_label_y, self.field_width, self.field_height)
        
        # Create account fields
        self.email_rect = pygame.Rect(self.field_x, 200, self.field_width, self.field_height)
        self.username_rect = pygame.Rect(self.field_x, 250, self.field_width, self.field_height)
        self.password_rect = pygame.Rect(self.field_x, 300, self.field_width, self.field_height)
        self.confirm_password_rect = pygame.Rect(self.field_x, 350, self.field_width, self.field_height)

        # Forgot password field and link position
        self.forgot_email_label_y = 250  # You can adjust this as needed
        self.forgot_email_rect = pygame.Rect(self.field_x, self.forgot_email_label_y, self.field_width, self.field_height)
        # Center "Forgot Password?" link under password field
        forgot_text_width = self.small_font.size("Forgot Password?")[0]
        self.forgot_password_pos = (250 - forgot_text_width // 2, self.login_password_label_y + 40)

    def _draw_login_form(self, screen):
        """Draw the login form with email and password fields"""
        # Title
        title = self.font.render("Login to Your Account", True, (255, 255, 255))
        screen.blit(title, (250 - title.get_width()//2, self.title_y))
        
        # Email field - USING THE DEFINED ATTRIBUTES
        screen.blit(self.font.render("Email:", True, (255, 255, 255)), 
                   (self.label_x, self.login_email_label_y))
        pygame.draw.rect(screen, 
                        (255, 255, 255) if self.active_field == "login_email" else (200, 200, 200), 
                        self.login_email_rect, 2)
        email_text = self.font.render(self.email_text, True, (255, 255, 255))
        screen.blit(email_text, (self.login_email_rect.x + 5, self.login_email_rect.y + 5))
        
        # Password field - USING THE DEFINED ATTRIBUTES
        screen.blit(self.font.render("Password:", True, (255, 255, 255)), 
                   (self.label_x, self.login_password_label_y))
        pygame.draw.rect(screen, 
                        (255, 255, 255) if self.active_field == "login_password" else (200, 200, 200), 
                        self.login_password_rect, 2)
        password_text = self.font.render("*" * len(self.password_text), True, (255, 255, 255))
        screen.blit(password_text, (self.login_password_rect.x + 5, self.login_password_rect.y + 5))
        
        # Submit button
        pygame.draw.rect(screen, (0, 100, 200), self.submit_button, border_radius=5)
        submit_text = self.font.render("LOGIN", True, (255, 255, 255))
        screen.blit(submit_text, (250 - submit_text.get_width()//2, 410))

    def handle_events(self, event, switch_state):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not (self.show_login_form or self.show_create_account or self.show_forgot_password):
                if self.login_button.collidepoint(mouse_pos):
                    self.show_login_form = True
                    self.email_text = ""
                    self.password_text = ""
                    self.active_field = None
                elif self.create_button.collidepoint(mouse_pos):
                    self.show_create_account = True
                    self.email_text = ""
                    self.username_text = ""
                    self.password_text = ""
                    self.confirm_password_text = ""
                    self.active_field = None
                elif self.exit_button.collidepoint(mouse_pos):  # Add this condition
                    print("Exit button clicked")
                    pygame.quit()
                    sys.exit()
            else:
                if self.back_button.collidepoint(mouse_pos):
                    self.reset_state()
                elif self.submit_button.collidepoint(mouse_pos):
                    if self.show_login_form:
                        # Login logic
                        if "@" not in self.email_text or len(self.password_text) < 6:
                            self.show_notification_message("Invalid email or password", False)
                        else:
                            try:
                                result = auth.login(self.email_text, self.password_text)
                                if result and result != 'invalid_credentials' and result != 'unknown_error':
                                    switch_state("MainMenu")
                                else:
                                    self.show_notification_message("Login failed", False)
                            except Exception as e:
                                print("Login error:", e)
                                self.show_notification_message("Login error", False)
                    elif self.show_create_account:
                        # Create account logic
                        if not self._validate_create_account():
                            return
                        try:
                            result = auth.register(
                                self.email_text,
                                self.password_text,
                                self.confirm_password_text,
                                self.username_text
                            )
                            if result == 'success':
                                self.show_notification_message("Account created! Please login.", True)
                                self.show_create_account = False
                                self.show_login_form = True
                            elif result == 'already_registered':
                                self.show_notification_message("Email already registered", False)
                            else:
                                self.show_notification_message("Account creation failed", False)
                        except Exception as e:
                            print("Create account error:", e)
                            self.show_notification_message("Account creation error", False)
                    elif self.show_forgot_password:
                        # Forgot password logic
                        if not self.email_text or '@' not in self.email_text:
                            self.show_notification_message("Enter a valid email", False)
                            return
                        try:
                            result = auth.reset_password(self.email_text)
                            if result == 'reset_email_sent':
                                self.show_notification_message("Reset email sent!", True)
                            else:
                                self.show_notification_message("Reset failed", False)
                        except Exception as e:
                            print("Reset password error:", e)
                            self.show_notification_message("Reset error", False)
                # Field selection for create account
                if self.show_create_account:
                    if self.email_rect.collidepoint(mouse_pos):
                        self.active_field = "email"
                    elif self.username_rect.collidepoint(mouse_pos):
                        self.active_field = "username"
                    elif self.password_rect.collidepoint(mouse_pos):
                        self.active_field = "password"
                    elif self.confirm_password_rect.collidepoint(mouse_pos):
                        self.active_field = "confirm_password"
                    else:
                        self.active_field = None
                # Field selection for login
                elif self.show_login_form:
                    if self.login_email_rect.collidepoint(mouse_pos):
                        self.active_field = "login_email"
                    elif self.login_password_rect.collidepoint(mouse_pos):
                        self.active_field = "login_password"
                    # Forgot password link
                    elif pygame.Rect(self.forgot_password_pos, (self.small_font.size("Forgot Password?")[0], self.small_font.get_height())).collidepoint(mouse_pos):
                        self.show_login_form = False
                        self.show_create_account = False
                        self.show_forgot_password = True
                        self.active_field = "forgot_email"
                    else:
                        self.active_field = None
                # Field selection for forgot password
                elif self.show_forgot_password:
                    if self.forgot_email_rect.collidepoint(mouse_pos):
                        self.active_field = "forgot_email"
                    else:
                        self.active_field = None

        elif event.type == pygame.KEYDOWN:
            if self.active_field == "login_email" or self.active_field == "email" or self.active_field == "forgot_email":
                if event.key == pygame.K_BACKSPACE:
                    self.email_text = self.email_text[:-1]
                else:
                    self.email_text += event.unicode
            elif self.active_field == "login_password" or self.active_field == "password":
                if event.key == pygame.K_BACKSPACE:
                    self.password_text = self.password_text[:-1]
                else:
                    self.password_text += event.unicode
            elif self.active_field == "username":
                if event.key == pygame.K_BACKSPACE:
                    self.username_text = self.username_text[:-1]
                else:
                    self.username_text += event.unicode
            elif self.active_field == "confirm_password":
                if event.key == pygame.K_BACKSPACE:
                    self.confirm_password_text = self.confirm_password_text[:-1]
                else:
                    self.confirm_password_text += event.unicode

    def reset_state(self):
        """Reset all form states"""
        self.show_login_form = False
        self.show_create_account = False
        self.show_forgot_password = False
        self.email_text = ""
        self.password_text = ""
        self.active_field = None
        self.show_notification = False

    def show_notification_message(self, message, is_success):
        """Show a notification message"""
        self.notification_text = message
        self.notification_color = (0, 200, 0) if is_success else (200, 0, 0)
        self.show_notification = True
        self.notification_timer = pygame.time.get_ticks()

    def draw(self, screen):
        """Main draw method"""
        self.menu_logo.draw(screen)

        if not (self.show_login_form or self.show_create_account):
            # Main menu buttons
            screen.blit(self.resources['login_button_img'], self.login_button)
            screen.blit(self.resources['create_button_img'], self.create_button)
        else:
            # Form overlay and back button
            screen.blit(self.overlay, (0, 0))
            screen.blit(self.resources['back_button_img'], self.back_button)
            
            # Notification
            if self.show_notification:
                self._draw_notification(screen)
            
            # Current form
            if self.show_login_form:
                self._draw_login_form(screen)
            elif self.show_create_account:
                self._draw_create_account_form(screen)

    def update(self):
        """Update animations/timers"""
        pass

    def draw(self, screen):
        self.menu_logo.draw(screen)

        if not (self.show_login_form or self.show_create_account or self.show_forgot_password):
            # Main menu buttons
            screen.blit(self.resources['login_button_img'], self.login_button)
            screen.blit(self.resources['create_button_img'], self.create_button)
            screen.blit(self.resources['quit_button_img'], self.exit_button)
        else:
            # Form overlay and back button
            screen.blit(self.overlay, (0, 0))
            screen.blit(self.resources['back_button_img'], self.back_button)
            
            # Notification (drawn first so it appears behind form title)
            if self.show_notification:
                self._draw_notification(screen)
                
            # Draw the appropriate form
            if self.show_login_form:
                self._draw_login_form(screen)
            elif self.show_create_account:
                self._draw_create_account_form(screen)
            elif self.show_forgot_password:
                self._draw_forgot_password_form(screen)

    def _draw_login_form(self, screen):
        """Draw login form with perfectly aligned elements"""
        # Title (centered)
        title = self.font.render("Login to Your Account", True, (255, 255, 255))
        screen.blit(title, (250 - title.get_width()//2, self.title_y))
        
        # Email field
        screen.blit(self.font.render("Email:", True, (255, 255, 255)), 
                   (self.label_x, self.login_email_label_y))
        pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "login_email" else (200, 200, 200), 
                        self.login_email_rect, 2)
        email_surface = self._render_text_with_clipping(self.email_text, self.login_email_rect)
        screen.blit(email_surface, (self.login_email_rect.x + 5, self.login_email_rect.y + 5))
        
        # Password field
        screen.blit(self.font.render("Password:", True, (255, 255, 255)), 
                   (self.label_x, self.login_password_label_y))
        pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "login_password" else (200, 200, 200), 
                        self.login_password_rect, 2)
        password_surface = self._render_text_with_clipping("*" * len(self.password_text), self.login_password_rect)
        screen.blit(password_surface, (self.login_password_rect.x + 5, self.login_password_rect.y + 5))
        
        # Forgot password link (centered)
        forgot_text = self.small_font.render("Forgot Password?", True, (100, 150, 255))
        screen.blit(forgot_text, self.forgot_password_pos)
        
        # Submit button
        screen.blit(self.resources['login_button_img'], self.submit_button)

    def _draw_create_account_form(self, screen):
        """Draw the create account form with perfectly aligned elements and invisible button text"""
        # Positioning constants
        TITLE_Y = 180
        FIRST_FIELD_Y = 230
        LABEL_X = 50
        LABEL_FIELD_SPACING = 35  # New: Space between label and field
        FIELD_X = LABEL_X + 150 + LABEL_FIELD_SPACING  # Adjusted field position
        FIELD_WIDTH = 200
        FIELD_HEIGHT = 32
        VERTICAL_SPACING = 50
    
        
        # Draw title (centered)
        title = self.font.render("Create New Account", True, (255, 255, 255))
        screen.blit(title, (250 - title.get_width()//2, TITLE_Y))

        # Field definitions
        fields = [
            ("Email:", self.email_rect, "email", self.email_text),
            ("Username:", self.username_rect, "username", self.username_text),
            ("Password:", self.password_rect, "password", "*" * len(self.password_text)),
            ("Confirm Password:", self.confirm_password_rect, "confirm_password", "*" * len(self.confirm_password_text))
        ]

        # Draw all fields and labels
        for i, (label_text, rect, field_name, field_text) in enumerate(fields):
            # Calculate y-position
            field_y = FIRST_FIELD_Y + (i * VERTICAL_SPACING)
            
            # Update field rectangle
            rect.x = FIELD_X
            rect.y = field_y
            rect.width = FIELD_WIDTH
            rect.height = FIELD_HEIGHT

            # Draw label (vertically centered with field text)
            label = self.font.render(label_text, True, (255, 255, 255))
            label_y = field_y + (FIELD_HEIGHT - label.get_height()) // 2 + 2  # +2 for visual perfection
            screen.blit(label, (LABEL_X, label_y))

            # Draw field background
            pygame.draw.rect(screen, 
            (255, 255, 255) if self.active_field == field_name else (200, 200, 200), rect, 2)

            # Draw field text with perfect alignment
            text_surface = self._render_text_with_clipping(field_text, rect)
            text_y = field_y + (FIELD_HEIGHT - text_surface.get_height()) // 2
            screen.blit(text_surface, (rect.x + 5, text_y))

        # Draw button WITHOUT any text (completely invisible text)
        screen.blit(self.resources['create_button_img'], self.submit_button)
        
        # Alternative: If you need to keep text coordinates for click detection
        # but want it invisible, use this instead:
        """
        button_text = self.font.render("", True, (0, 0, 0, 0))  # Fully transparent
        text_x = self.submit_button.x + (self.submit_button.width - button_text.get_width()) // 2
        text_y = self.submit_button.y + (self.submit_button.height - button_text.get_height()) // 2
        screen.blit(button_text, (text_x, text_y))
        """
    
    def _draw_forgot_password_form(self, screen):
        """Draw forgot password form with perfectly aligned elements"""
        # Title (centered)
        title = self.font.render("Reset Password", True, (255, 255, 255))
        screen.blit(title, (250 - title.get_width()//2, self.title_y))
        
        # Instructions (centered)
        instructions = self.small_font.render("Enter your email to receive a reset link", True, (255, 255, 255))
        screen.blit(instructions, (250 - instructions.get_width()//2, self.title_y + 50))
        
        # Email field
        screen.blit(self.font.render("Email:", True, (255, 255, 255)), 
                   (self.label_x, self.forgot_email_label_y))
        pygame.draw.rect(screen, (255, 255, 255) if self.active_field == "forgot_email" else (200, 200, 200), 
                        self.forgot_email_rect, 2)
        email_surface = self._render_text_with_clipping(self.email_text, self.forgot_email_rect)
        screen.blit(email_surface, (self.forgot_email_rect.x + 5, self.forgot_email_rect.y + 5))
        
        # Submit button with centered text
        submit_text = self.font.render("Send Reset Link", True, (255, 255, 255))
        text_x = self.submit_button.x + (self.submit_button.width - submit_text.get_width()) // 2
        text_y = self.submit_button.y + (self.submit_button.height - submit_text.get_height()) // 2
        screen.blit(submit_text, (text_x, text_y))

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

    def _validate_create_account(self):
        """Validate form inputs with specific error messages"""
        if not self.email_text or '@' not in self.email_text:
            self.show_notification_message("Invalid email format", False)
            return False
            
        if len(self.password_text) < 6:
            self.show_notification_message("Password too weak (min 6 chars)", False)
            return False
            
        if self.password_text != self.confirm_password_text:
            self.show_notification_message("Passwords don't match", False)
            return False
            
        return True

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
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        

    def handle_events(self, event, switch_state):
        if event.type == pygame.MOUSEBUTTONDOWN:
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
        if event.type == pygame.MOUSEBUTTONDOWN:
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
        self.highest_score = current_player_HS.getCurrentPlayerHighScore(uid) or 0  # Default to 0 if None
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