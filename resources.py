import pygame
import os

# Constants
SCREEN_W = 500
SCREEN_H = 720
FPS = 60
HEIGHT = 1000

def load_image(path, alpha=True):
    """Helper function to load images with optional alpha channel"""
    img = pygame.image.load(path)
    return img.convert_alpha() if alpha else img.convert()

def load_sound(path, volume=1.0):
    """Helper function to load and configure sounds"""
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

def load_animation_frames(folder_path, frame_count, file_pattern="{}.png"):
    """Load a sequence of animation frames from a folder"""
    frames = []
    for i in range(frame_count):
        frame_path = os.path.join(folder_path, file_pattern.format(i))
        frames.append(load_image(frame_path))
    return frames

def load_garbage_images(file_names, assets_folder="assets"):
    """Load multiple garbage images from file names"""
    return [load_image(os.path.join(assets_folder, fn)) for fn in file_names]

def load_resources():
    resources = {
        'speed': 7,
        'b_pos': 0,
        'o_pos': SCREEN_H,
        'height': HEIGHT
    }
    
    # Load UI images
    ui_images = {
        'menu_logo_img': 'assets/logos_and_icons/menu_logo.png',
        'game_over_img': 'assets/logos_and_icons/game_over.png',
        'play_button_img': 'assets/logos_and_icons/play.png',
        'quit_button_img': 'assets/logos_and_icons/quit.png',
        'restart_button_img': 'assets/logos_and_icons/restart.png',
        'menu_button_img': 'assets/logos_and_icons/main_menu.png'
    }
    for key, path in ui_images.items():
        resources[key] = load_image(path)
    
    # Load backgrounds
    resources['bg_image'] = load_image('assets/bg.png', alpha=False)
    resources['overlap_bg_image'] = resources['bg_image'].copy()
    
    # Configure lanes
    resources.update({
        'left_lane': 150,
        'center_lane': 166,
        'right_lane': 275,
        'objectleft_lane': 130,
        'objectcenter_lane': 245,
        'objectright_lane': 360
    })
    resources['lanes'] = resources['left_lane'], resources['center_lane'], resources['right_lane']
    resources['objectlanes'] = [resources['objectleft_lane'], resources['objectcenter_lane'], resources['objectright_lane']]
    
    # Load animations using helper function
    resources['bio_animation'] = load_animation_frames('assets/wallyrunbio', 16)
    resources['nonbio_animation'] = load_animation_frames('assets/wallyrunnonbio', 16)
    
    # Load garbage images using helper functions
    bio_filenames = ['banana peel.png', 'milk carton.png', 'box.png', 'Leaves.png', 'Poop.png', 
                    'Log.png', 'Book.png', 'Apple.png', 'Meat.png', 'Fishbone.png']
    nonbio_filenames = ['plastic bag.png', 'soda bottle.png', 'water bottle.png', 'Battery.png', 
                       'Lightbulb.png', 'Phone.png', 'Laptop.png', 'Can.png', 'Soda.png', 'Glass.png']
    
    resources['biodegradable_images'] = load_garbage_images(bio_filenames)
    resources['nonbiodegradable_images'] = load_garbage_images(nonbio_filenames)
    
    # Initialize and load sounds
    pygame.mixer.init()
    resources['game_music'] = "assets/music/game_music.wav"
    resources['get_item_sound'] = load_sound("assets/music/get_item.mp3", 0.5)
    resources['game_over_sound'] = load_sound("assets/music/game_over.mp3", 0.5)
    
    # Configure and play music
    pygame.mixer.music.load(resources['game_music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    
    return resources