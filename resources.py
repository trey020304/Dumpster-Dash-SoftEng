import pygame
from garbage import BioGarbage, NonBioGarbage, Obstacle

# Constants
SCREEN_W = 500
SCREEN_H = 720
FPS = 60
HEIGHT = 1000

def load_spritesheet(path, frame_width, frame_height, num_frames):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame = sheet.subsurface(rect).copy()
        frames.append(frame)
    return frames

def load_resources():
    resources = {}
    
    # Load images and resize them
    def load_and_scale(image_path, scale_factor=None, new_size=None):
        img = pygame.image.load(image_path).convert_alpha()
        if scale_factor:
            new_width = int(img.get_width() * scale_factor)
            new_height = int(img.get_height() * scale_factor)
            img = pygame.transform.scale(img, (new_width, new_height))
        elif new_size:  # Alternatively, specify exact dimensions
            img = pygame.transform.scale(img, new_size)
        return img
    
    # Icons and buttons with scaling
    resources['menu_logo_img'] = load_and_scale('assets/icons/menu_logo.png', scale_factor=1)
    resources['game_over_img'] = load_and_scale('assets/icons/game_over.png', scale_factor=1)
    resources['play_button_img'] = load_and_scale('assets/icons/play.png', scale_factor=.85)
    resources['leaderboard_button_img'] = load_and_scale('assets/icons/Leaderboard.png', scale_factor=.6)
    resources['leaderboard_img'] = load_and_scale('assets/leaderboard panel.png', scale_factor=.4)
    resources['back_button_img'] = load_and_scale('assets/icons/X.png', scale_factor=0.25)
    resources['logout_button_img'] = load_and_scale('assets/icons/Log out.png', scale_factor=0.4)
    resources['quit_button_img'] = load_and_scale('assets/icons/quit.png', scale_factor=0.4)
    resources['restart_button_img'] = load_and_scale('assets/icons/restart.png', scale_factor=1)
    resources['menu_button_img'] = load_and_scale('assets/icons/main_menu.png', scale_factor=1)
    resources['login_button_img'] = load_and_scale('assets/icons/Log In.png', scale_factor=.6)
    resources['create_button_img'] = load_and_scale('assets/icons/Create Account.png', scale_factor=.6)

    # Load background
    resources['bg_image'] = pygame.image.load('assets/bg.png').convert()
    # You can resize the background if needed
    # resources['bg_image'] = pygame.transform.scale(resources['bg_image'], (SCREEN_W, SCREEN_H))
    resources['bg_height'] = resources['bg_image'].get_height()
    resources['scroll_pos'] = 0
    resources['menu_speed'] = 3
    resources['game_speed'] = 7

    # Load instructions
    resources['instruction_img'] = load_and_scale('assets/instruction.png', scale_factor=.35)

    # Lanes (unchanged)
    resources['left_lane'] = 150
    resources['center_lane'] = 166
    resources['right_lane'] = 275
    resources['lanes'] = [resources['left_lane'], resources['center_lane'], resources['right_lane']]
    
    resources['objectleft_lane'] = 130
    resources['objectcenter_lane'] = 245
    resources['objectright_lane'] = 360
    resources['objectlanes'] = [resources['objectleft_lane'], resources['objectcenter_lane'], resources['objectright_lane']]
    
    resources['height'] = HEIGHT
    
    # Load animations - you can resize frames here
    def load_scaled_spritesheet(path, frame_width, frame_height, num_frames, scale_factor=None, new_size=None):
        frames = load_spritesheet(path, frame_width, frame_height, num_frames)
        if scale_factor or new_size:
            scaled_frames = []
            for frame in frames:
                if scale_factor:
                    new_width = int(frame.get_width() * scale_factor)
                    new_height = int(frame.get_height() * scale_factor)
                    scaled_frame = pygame.transform.scale(frame, (new_width, new_height))
                elif new_size:
                    scaled_frame = pygame.transform.scale(frame, new_size)
                scaled_frames.append(scaled_frame)
            return scaled_frames
        return frames
    
    # Example with scaled animations:
    resources['bio_animation'] = load_scaled_spritesheet('assets/animations/wallyrunbio_spritesheet.png', 150, 150, 16, scale_factor=1)
    resources['nonbio_animation'] = load_scaled_spritesheet('assets/animations/wallyrunnonbio_spritesheet.png', 150, 150, 16, scale_factor=1)
    resources['death_animation'] = load_scaled_spritesheet('assets/animations/wally_death.png', 150, 150, 16, scale_factor=1)

    # Load garbage images - you'll need to modify the get_images() methods to accept size parameters
    resources['biodegradable_images'] = BioGarbage.get_images()  # Modify this class to handle scaling
    resources['nonbiodegradable_images'] = NonBioGarbage.get_images()  # Modify this class to handle scaling
    resources['obstacle_images'] = Obstacle.get_images()  # Modify this class to handle scaling

    # Load health system images - make sure the file paths are correct
    resources['heart_3_img'] = load_and_scale('assets/icons/heart 3.png', scale_factor=2)
    resources['heart_2_img'] = load_and_scale('assets/icons/heart 2.png', scale_factor=2)
    resources['heart_1_img'] = load_and_scale('assets/icons/heart 1.png', scale_factor=2)
    resources['heart_0_img'] = load_and_scale('assets/icons/heart 0.png', scale_factor=2)
    
    # Sounds (unchanged)
    pygame.mixer.init()
    resources['game_music'] = "assets/audio/game_music.wav"
    resources['get_item_sound'] = pygame.mixer.Sound("assets/audio/get_item.mp3")
    resources['game_over_sound'] = pygame.mixer.Sound("assets/audio/game_over.mp3")
    resources['wrong_bin_sound'] = pygame.mixer.Sound("assets/audio/wrong_bin.mp3")
    
    pygame.mixer.music.load(resources['game_music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    
    return resources