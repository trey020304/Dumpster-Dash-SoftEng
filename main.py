import pygame
from pygame.locals import *
import sys
import random

# Initialize pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Window dimensions
screen_w = 500
screen_h = 720

# Create window
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Dumpster Dash')

#button initialize
menu_logo_img = pygame.image.load('assets/logos_and_icons/menu_logo.png').convert_alpha()
game_over_img = pygame.image.load('assets/logos_and_icons/game_over.png').convert_alpha()
play_button_img = pygame.image.load('assets/logos_and_icons/play.png').convert_alpha()
quit_button_img = pygame.image.load('assets/logos_and_icons/quit.png').convert_alpha()
restart_button_img = pygame.image.load('assets/logos_and_icons/restart.png').convert_alpha()
menu_button_img = pygame.image.load('assets/logos_and_icons/main_menu.png').convert_alpha()

#logo
class Logo():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw (self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

menu_logo = Logo(250, 200, menu_logo_img)
game_over = Logo(250, 200, game_over_img)

# Scrolling background
bg_image = pygame.image.load('assets/bg.png').convert()
overlap_bg_image = pygame.image.load('assets/bg.png').convert()
b_pos = 0
o_pos = 720
speed = 7

# Lane coordinates
left_lane = 150
center_lane = 166
right_lane = 275  
lanes = [left_lane, center_lane, right_lane]

objectleft_lane = 130
objectcenter_lane = 245
objectright_lane = 360
objectlanes = [objectleft_lane, objectcenter_lane, objectright_lane]

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Game settings
score = 0
highest_score = 0

# Height
height = 1000

# Music
# Music
game_music = "assets/music/game_music.wav"

# Load audio effects
get_item_sound = pygame.mixer.Sound("assets/music/get_item.mp3")
game_over_sound = pygame.mixer.Sound("assets/music/game_over.mp3")


# Load music
pygame.mixer.music.load(game_music)

# Play music
pygame.mixer.music.play(-1)  # -1 plays the music indefinitely

# Set music volume
pygame.mixer.music.set_volume(0.2)

# Wally
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
        # Handle animation
        # Update image
        self.image = self.animation_list[self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # If the animation surpasses the last frame, reset
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        # Check for collision between runner and garbage objects
        if pygame.sprite.spritecollide(self, garbage_group, False):
            # Check if the runner is colliding with the corresponding type of garbage
            if (
                (isinstance(self, Bio) and any(isinstance(garbage, NonBioGarbage) for garbage in pygame.sprite.spritecollide(self, garbage_group, False))) 
                or (isinstance(self, NonBio) and any(isinstance(garbage, BioGarbage) for garbage in pygame.sprite.spritecollide(self, garbage_group, False)))
            ):
                # Game over
                switch_state("Game Over")
                print("Game over")

        self.draw()

    def draw(self):
        screen.blit(self.image, self.rect)


class Bio(Runner):
    def __init__(self, x, y):
        animation_list = []
        for i in range(16):
            img = pygame.image.load(f'assets/wallyrunbio/{i}.png')
            animation_list.append(img)
        super().__init__(x, y, animation_list)


class NonBio(Runner):
    def __init__(self, x, y):
        animation_list = []
        for i in range(16):
            img = pygame.image.load(f'assets/wallyrunnonbio/{i}.png')
            animation_list.append(img)
        super().__init__(x, y, animation_list)


wally1 = Bio(250, 575)
wally2 = NonBio(250, 575)

active_wally = wally1
prev_wally_position = active_wally.rect.center

class Garbage(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Scale the image down so it's not wider than the lane
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


# Sprite groups
garbage_group = pygame.sprite.Group()

# Load the garbage images
gar1 = BioGarbage
bio_filenames = ['banana peel.png', 'milk carton.png', 'box.png', 'Leaves.png', 'Poop.png', 'Log.png', 'Book.png', 'Apple.png', 'Meat.png', 'Fishbone.png']
biodegradable_images = []
for bio_filename in bio_filenames:
    image = pygame.image.load('assets/' + bio_filename)
    biodegradable_images.append(image)

gar2 = NonBioGarbage
nonbio_filenames = ['plastic bag.png', 'soda bottle.png', 'water bottle.png', 'Battery.png', 'Lightbulb.png', 'Phone.png', 'Laptop.png', 'Can.png', 'Soda.png', 'Glass.png']
nonbiodegradable_images = []
for nonbio_filename in nonbio_filenames:
    image = pygame.image.load('assets/' + nonbio_filename)
    nonbiodegradable_images.append(image)


def create_garbage():
    # Select a random lane
    lane = random.choice(objectlanes)

    garbage_list = [gar1, gar2]

    # Select a random garbage object
    garbage_object = random.choice(garbage_list)

    # Select a random garbage image
    if garbage_object == gar1:
        image = random.choice(biodegradable_images)
    else:
        image = random.choice(nonbiodegradable_images)

    # Create a new garbage object with the selected image
    garbage = garbage_object(image, lane, -height / 2)
    garbage.rect.center = (lane, -height / 2)
    garbage_group.add(garbage)
    

def switch_state(state):
    global current_state
    current_state = state

# Game states
class MainMenu:
    def __init__(self):
        self.play_button = play_button_img.get_rect(center=(250, 500))
        self.exit_button = quit_button_img.get_rect(center=(250, 600))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                switch_state("Game")
            elif self.exit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def draw(self):
        screen.blit(menu_logo_img, (menu_logo.rect.x, menu_logo.rect.y))  # Draw the menu logo
        screen.blit(play_button_img, self.play_button)
        screen.blit(quit_button_img, self.exit_button)

class Game:
    def __init__(self):
        self.score = 0
        self.highest_score = highest_score  # Assign the initial highest score
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.increment_timer = 0  # New attribute to track the increment timer
        self.speed = 7  # Initial speed

    def handle_events(self, event):
        global active_wally  # Add this line
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and active_wally.rect.center[0] > left_lane:
                active_wally.rect.left -= 115
            elif event.key == pygame.K_RIGHT and active_wally.rect.center[0] < right_lane:
                active_wally.rect.left += 115
            elif event.key == pygame.K_q:
                prev_wally_position = active_wally.rect.center  # Store the current position
                active_wally = wally1
                active_wally.rect.center = prev_wally_position  # Set the position to the stored position
            elif event.key == pygame.K_e:
                prev_wally_position = active_wally.rect.center  # Store the current position
                active_wally = wally2
                active_wally.rect.center = prev_wally_position  # Set the position to the stored position
            # Quitting the Game
            elif event.key == pygame.K_ESCAPE:
                switch_state("MainMenu")
                return
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    def update(self):
        active_wally.update(garbage_group)
        if self.score > self.highest_score:
            self.highest_score = self.score  # Update the highest score

        # Add garbage
        if len(garbage_group) < 3: #Length of the garbage group in relation to other garbage
            add_garbage = True
            for garbage in garbage_group:
                if garbage.rect.top < garbage.rect.height * 1:  # Closeness of spawning with one another
                    add_garbage = False

            if add_garbage:
                create_garbage()

        # Move and remove garbage
        for garbage in garbage_group:
            garbage.rect.y += self.speed

            # Remove garbage once it goes off screen
            if garbage.rect.top >= height:
                garbage.kill()

        # Check for collision between Wally and garbage objects
        collisions = pygame.sprite.spritecollide(active_wally, garbage_group, True)
        for garbage in collisions:
            # Check if the active Wally is colliding with the corresponding type of garbage
            if (isinstance(active_wally, Bio) and isinstance(garbage, NonBioGarbage)) or (
                    isinstance(active_wally, NonBio) and isinstance(garbage, BioGarbage)):
                # Play game over sound
                self.speed = 7
                game_over_sound.play()
                pygame.time.wait(1500)  # Wait for 2000 milliseconds (2 seconds)
                switch_state("GameOver")
                
            elif (active_wally == wally1 and isinstance(garbage, BioGarbage)) or (active_wally == wally2 and isinstance(garbage, NonBioGarbage)):
                # Play get item sound
                get_item_sound.play()
                
                # Increment score
                self.score += 1
                self.increment_timer += 1
                
        if self.increment_timer >= 5:
            self.speed += .75  # Increase the speed
            self.increment_timer = 0  # Reset the increment timer
            


    def draw(self):

        active_wally.draw()

        # Display the score 
        font = pygame.font.Font(pygame.font.get_default_font(), 25)
        score_text = font.render('Score: ' + str(self.score), True, black)
        score_rect = score_text.get_rect()
        score_rect.center = (246, 63)
        screen.blit(score_text, score_rect)
        garbage_group.draw(screen)
        
        font = pygame.font.Font(pygame.font.get_default_font(), 25)
        score_text = font.render('Score: ' + str(self.score), True, white)
        score_rect = score_text.get_rect()
        score_rect.center = (243, 60)
        screen.blit(score_text, score_rect)
        garbage_group.draw(screen)
        
        if self.score > self.highest_score:
            self.highest_score = self.score
        
        

class GameOver:
    def __init__(self, score, highest_score):
        self.restart_button = restart_button_img.get_rect(center=(250, 500))
        self.menu_button = menu_button_img.get_rect(center=(250, 600))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.rect = game_over_img.get_rect(center=(250, 200))
        self.score = score
        self.highest_score = highest_score
        
        def switch_state(state):
            global current_state
            if state == "GameOver":
                current_state = "GameOver"
                game_over = GameOver(game.score, game.highest_score)  # Pass the highest score
            else:
                current_state = state

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                switch_state("Game")
                game.score = self.score
                game.highest_score = self.highest_score
            elif self.menu_button.collidepoint(event.pos):
                game.score = 0
                switch_state("MainMenu")

    def update(self):
        pass

    def draw(self):
        screen.blit(game_over_img, (self.rect.x, self.rect.y))
        screen.blit(restart_button_img, self.restart_button)
        screen.blit(menu_button_img, self.menu_button)

        score_text = self.font.render('Score: ' + str(game.score), True, black)
        score_rect = score_text.get_rect()
        score_rect.center = (250, 400)
        screen.blit(score_text, score_rect)
        
        score_text = self.font.render('Score: ' + str(game.score), True, white)
        score_rect = score_text.get_rect()
        score_rect.center = (247, 397)
        screen.blit(score_text, score_rect)
        
        
        highest_score_text = self.font.render('Highest Score: ' + str(self.highest_score), True, black)
        highest_score_rect = highest_score_text.get_rect()
        highest_score_rect.center = (250, 425)
        screen.blit(highest_score_text, highest_score_rect)
        
        highest_score_text = self.font.render('Highest Score: ' + str(self.highest_score), True, white)
        highest_score_rect = highest_score_text.get_rect()
        highest_score_rect.center = (247, 422)
        screen.blit(highest_score_text, highest_score_rect)

# Create game states
main_menu = MainMenu()
game = Game()
game_over = GameOver(game.score, game.highest_score)

# Set starting game state
current_state = "MainMenu"

while True:
    
    # Draw scrolling background
    if b_pos >= screen_h:
        b_pos = -screen_h
    if o_pos >= screen_h:
        o_pos = -screen_h

    b_pos += speed
    o_pos += speed

    screen.blit(bg_image, (0, b_pos))
    screen.blit(overlap_bg_image, (0, o_pos))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_state == "MainMenu":
            main_menu.handle_events(event)
        elif current_state == "Game":
            game.handle_events(event)
        elif current_state == "GameOver":
            game_over.handle_events(event)

    if current_state == "MainMenu":
        main_menu.update()
        main_menu.draw()
    elif current_state == "Game":
        game.update()
        game.draw()
    elif current_state == "GameOver":
        game_over.update()
        game_over.draw()
        game_over.highest_score = game.highest_score  # Update the highest score in the Game instance

    pygame.display.update()
    clock.tick(FPS)