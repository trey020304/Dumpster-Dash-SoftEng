import pygame
from pygame.locals import *
import sys
from states import MainMenu, Game, GameOver, Leaderboard, Login
from resources import load_resources, SCREEN_W, SCREEN_H, FPS
import firebase

# Initialize pygame
pygame.init()

# Create window
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Dumpster Dash')

# Load all resources
resources = load_resources()

game = Game(resources)

# Create all game states
login = Login(resources, game)
main_menu = MainMenu(resources, game)
game_over = GameOver(resources, game)
leaderboard = Leaderboard(resources, game)


# Dictionary to manage all states
states = {
    "Login": login, 
    "MainMenu": main_menu,
    "Game": game,
    "GameOver": game_over,
    "Leaderboard": leaderboard
}

# Set starting game state
uid = firebase.load_session()
if not uid:
    current_state = "Login"
else:
    current_state = "MainMenu"

def switch_state(state, reset_login=False):
    global current_state
    print(f"Switching state from {current_state} to {state}")
    
    if reset_login and state == "Login":
        # Access the login state through the states dictionary
        states["Login"].reset_state()
    
    current_state = state

clock = pygame.time.Clock()

# Main game loop
while True:
    scroll_speed = 0
    
    if current_state == "MainMenu" or current_state == "Leaderboard" or current_state == "Login":
        scroll_speed = resources['menu_speed']
    elif current_state == "Game" and not game.dead:
        scroll_speed = game.speed
    
    # Update scroll position (using modulo for seamless wrapping)
    resources['scroll_pos'] = (resources['scroll_pos'] + scroll_speed) % resources['bg_height']
    
    # Draw the background - two copies for seamless scrolling
    screen.blit(resources['bg_image'], (0, resources['scroll_pos'] - resources['bg_height']))
    screen.blit(resources['bg_image'], (0, resources['scroll_pos']))
    
    # If your background is smaller than screen height, draw a third copy
    if resources['bg_height'] < SCREEN_H:
        screen.blit(resources['bg_image'], (0, resources['scroll_pos'] + resources['bg_height']))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Pass events to the current state
        if current_state in states:
            states[current_state].handle_events(event, switch_state)
    
    # Update and draw current state
    if current_state in states:
        if current_state == "Game":
            states[current_state].update(switch_state)  # Pass switch_state for Game
        else:
            states[current_state].update()  # Other states don't need it
        states[current_state].draw(screen)
    
    pygame.display.update()
    clock.tick(FPS)