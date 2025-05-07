import pygame

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
    
    # Load images
    resources['menu_logo_img'] = pygame.image.load('assets/logos_and_icons/menu_logo.png').convert_alpha()
    resources['game_over_img'] = pygame.image.load('assets/logos_and_icons/game_over.png').convert_alpha()
    resources['play_button_img'] = pygame.image.load('assets/logos_and_icons/play.png').convert_alpha()
    resources['quit_button_img'] = pygame.image.load('assets/logos_and_icons/quit.png').convert_alpha()
    resources['restart_button_img'] = pygame.image.load('assets/logos_and_icons/restart.png').convert_alpha()
    resources['menu_button_img'] = pygame.image.load('assets/logos_and_icons/main_menu.png').convert_alpha()
    
    # Background
    resources['bg_image'] = pygame.image.load('assets/bg.png').convert()
    resources['overlap_bg_image'] = pygame.image.load('assets/bg.png').convert()
    resources['b_pos'] = 0
    resources['o_pos'] = 720
    resources['speed'] = 7
    
    # Lanes
    resources['left_lane'] = 150
    resources['center_lane'] = 166
    resources['right_lane'] = 275
    resources['lanes'] = [resources['left_lane'], resources['center_lane'], resources['right_lane']]
    
    resources['objectleft_lane'] = 130
    resources['objectcenter_lane'] = 245
    resources['objectright_lane'] = 360
    resources['objectlanes'] = [resources['objectleft_lane'], resources['objectcenter_lane'], resources['objectright_lane']]
    
    # Height
    resources['height'] = HEIGHT
    
    # Load animations
    resources['bio_animation'] = load_spritesheet('assets/wallyrunbio_spritesheet.png', 150, 150, 16)
    resources['nonbio_animation'] = load_spritesheet('assets/wallyrunnonbio_spritesheet.png', 150, 150, 16)
    resources['death_animation'] = load_spritesheet('assets/wally_death.png', 150, 150, 16)

    # Load garbage images
    bio_filenames = ['banana peel.png', 'milk carton.png', 'box.png', 'Leaves.png', 'Poop.png', 
                    'Log.png', 'Book.png', 'Apple.png', 'Meat.png', 'Fishbone.png']
    resources['biodegradable_images'] = [pygame.image.load('assets/' + fn) for fn in bio_filenames]
    
    nonbio_filenames = ['plastic bag.png', 'soda bottle.png', 'water bottle.png', 'Battery.png', 
                       'Lightbulb.png', 'Phone.png', 'Laptop.png', 'Can.png', 'Soda.png', 'Glass.png']
    resources['nonbiodegradable_images'] = [pygame.image.load('assets/' + fn) for fn in nonbio_filenames]
    
    # Load sounds
    pygame.mixer.init()
    resources['game_music'] = "assets/music/game_music.wav"
    resources['get_item_sound'] = pygame.mixer.Sound("assets/music/get_item.mp3")
    resources['game_over_sound'] = pygame.mixer.Sound("assets/music/game_over.mp3")
    
    # Play music
    pygame.mixer.music.load(resources['game_music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    
    return resources